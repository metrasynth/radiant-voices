import black
from jinja2 import Environment

from ..codegen import CodeGenerator


class PythonMutableGenerator(CodeGenerator):
    def run(self, env: Environment):
        filemode = black.FileMode()
        for modtype_name, modtype in self.fileformat["module_types"].items():
            outfile = f"{modtype_name.lower()}.py"
            outpath = self.dest_base / "modules" / "base" / outfile
            ctx = dict(modtype=modtype, modtype_name=modtype_name, repr=repr)
            template = env.get_template("pymutable/base_module.py.jinja2")
            content = template.render(ctx)
            content = black.format_str(content, mode=filemode)
            self.write_file(outpath, content)
