import json

ModSuffixes=['blocker',
             'ctl',
             'filter',
             'generator',
             'player',
             'pro',
             'shifter',
             'synth',
             'voice']

def dumps(struct):
    import re
    def mod_name(obj):
        return obj.__module__
    def class_name(obj):
        tokens=obj.__module__.split(".")
        classname=tokens[-1]        
        for suffix in ModSuffixes:
            if classname.endswith(suffix):
                return "%s%s" % (classname[:-(len(suffix))].capitalize(),
                                 suffix.capitalize())
        return classname.capitalize()
    def enum_name(obj):
        tokens=[tok for tok in re.split("\'|\\<|\\>|\\s|\\.",
                                        str(obj.__class__))
                if tok!='']
        return tokens[-1]
    class SVEncoder(json.JSONEncoder):
        def default(self, obj):
            if not (isinstance(obj, str) or
                    isinstance(obj, float) or
                    isinstance(obj, int)):
                typerepr=str(type(obj))
                if "class" in typerepr:
                    return "class: %s.%s" % (mod_name(obj),
                                             class_name(obj))
                elif "enum" in typerepr:
                    return "enum: %s.%s.%s.%s" % (mod_name(obj),
                                                  class_name(obj),
                                                  enum_name(obj),
                                                  obj.name)
                else:
                    raise RuntimeError("Couldn't encode %s" % obj)
            return json.JSONEncoder.default(self, obj)
    return json.dumps(struct, cls=SVEncoder)

def loads(text):
    import importlib, re
    def is_class(value):
        return value.startswith("class:")
    def load_class(value):
        path=re.split("\\:\\s*", value)[-1]
        tokens=path.split(".")
        modname, classname = ".".join(tokens[:-1]), tokens[-1]
        mod=importlib.import_module(modname)
        return getattr(mod, classname)
    def is_enum(value):
        return value.startswith("enum:")
    def load_enum(value):
        path=re.split("\\:\\s*", value)[-1]
        tokens=path.split(".")
        modname, classname, enumname, name = (".".join(tokens[:-3]),
                                              tokens[-3],
                                              tokens[-2],
                                              tokens[-1])
        mod=importlib.import_module(modname)
        klass=getattr(mod, classname)
        enum=getattr(klass, enumname)
        return getattr(enum, name)
    def sv_hook(obj):
        for key, value in obj.items():
            if isinstance(value, str):
                if is_class(value):
                    obj[key]=load_class(value)
                elif is_enum(value):
                    obj[key]=load_enum(value)
                else:
                    raise RuntimeError("Couldn't parse %s" % value)
        return obj
    return json.loads(text, object_hook=sv_hook)

if __name__=="__main__":
    try:
        import sys, os
        if len(sys.argv) < 2:
            raise RuntimeError("Please enter filename")
        filename=sys.argv[1]
        if not os.path.exists(filename):
            raise RuntimeError("File does not exist")
        if not filename.endswith(".sunvox"):
            raise RuntimeError("File must be a .sunvox file")
        from rv.readers.reader import read_sunvox_file
        proj=read_sunvox_file(filename)
        def expand_chains(proj):
            mods={mod.index:mod
                  for mod in proj.modules}
            connections=dict(proj.module_connections)
            chains=[]
            def expand(i, state=[]):
                state.append(i)
                if connections[i]==[]:
                    chains.append(state)
                for j in connections[i]:
                    if j in connections:
                        expand(j, list(state))
            expand(0)
            chains=[[mods[i] for i in reversed(chain)]
                    for chain in chains]
            def keyfn(chain):
                return "/".join([str(mod.index)
                                 for mod in chain])
            return {keyfn(chain):chain
                    for chain in chains}
        chains=expand_chains(proj)
        for _, chain in chains.items():
            struct=[{"type": mod.__class__,
                     "values": dict(mod.controller_values)}
                    for mod in chain]
            print (loads(dumps(struct)))
    except RuntimeError as error:
        print ("Error: %s" % str(error))
