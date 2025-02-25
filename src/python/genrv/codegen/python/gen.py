import black
from genrv.codegen.base import CodeGenerator
from isort import Config
from isort.main import sort_imports


class PythonGenerator(CodeGenerator):
    def run(self, env):
        filemode = black.FileMode()
        for modtype_name, modtype in self.fileformat["module_types"].items():
            ctlmap = {}
            for ctls in modtype.get("controllers", []):
                for ctlname, ctl in ctls.items():
                    ctlmap[ctlname] = ctl
            outfile = f"{modtype_name.lower()}.py"
            outpath = self.dest_base / "modules" / "base" / outfile
            ctx = dict(modtype=modtype, modtype_name=modtype_name, ctlmap=ctlmap)
            template = env.get_template("python/base_module.py.jinja2")
            content = template.render(ctx)
            try:
                content = black.format_str(content, mode=filemode)
            except Exception as e:
                print(content)
                raise e
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
            content = black.format_str(content, mode=filemode)
            self.write_file(outpath, content)
            isort_config = Config()
            sort_imports(outpath, isort_config)
