from subprocess import call

from genrv.codegen.base import CodeGenerator
from stringcase import camelcase


def normalize_whitespace(s):
    s = "\n".join(line.rstrip() for line in s.splitlines())
    while "\n\n" in s:
        s = s.replace("\n\n", "\n")
    return s


class TypescriptGenerator(CodeGenerator):
    def run(self, env):
        # Generate modtypes/allModTypes.ts
        ctx = {"module_types": self.fileformat["module_types"]}
        template = env.get_template("ts/m.ts.jinja2")
        content = template.render(ctx)
        allmodtypes_path = self.dest_base / "modtypes" / "m.ts"
        content = normalize_whitespace(content)
        self.write_file(allmodtypes_path, content)
        # Generate modtypes/{{ mod_type }}.ts and {{ mod_type }}Behavior.ts
        for modtype_name, modtype in self.fileformat["module_types"].items():
            ctx = dict(
                modtype=modtype, modtype_name=modtype_name, enumerate=enumerate, len=len
            )

            outfile = f"{camelcase(modtype_name)}.ts"
            outpath = self.dest_base / "modtypes" / outfile
            template = env.get_template("ts/modtype.ts.jinja2")
            content = template.render(ctx)
            content = normalize_whitespace(content)
            self.write_file(outpath, content)

            outfile = f"{camelcase(modtype_name)}BaseControllers.ts"
            outpath = self.dest_base / "modtypes" / outfile
            template = env.get_template("ts/moduleBaseControllers.ts.jinja2")
            content = template.render(ctx)
            content = normalize_whitespace(content)
            self.write_file(outpath, content)

            outfile = f"{camelcase(modtype_name)}ControllerValues.ts"
            outpath = self.dest_base / "modtypes" / outfile
            template = env.get_template("ts/moduleControllerValues.ts.jinja2")
            content = template.render(ctx)
            content = normalize_whitespace(content)
            self.write_file(outpath, content)

            outfile = f"{camelcase(modtype_name)}Enums.ts"
            outpath = self.dest_base / "modtypes" / outfile
            if "enums" in modtype:
                template = env.get_template("ts/moduleEnums.ts.jinja2")
                content = template.render(ctx)
                content = normalize_whitespace(content)
                self.write_file(outpath, content)
            else:
                outpath.unlink(missing_ok=True)

            outfile = f"{camelcase(modtype_name)}Behavior.ts"
            outpath = self.dest_base / "modtypes" / outfile
            template = env.get_template("ts/moduleBehavior.ts.jinja2")
            content = template.render(ctx)
            content = normalize_whitespace(content)
            if not outpath.exists() or outpath.read_text().startswith("/* (unchanged"):
                self.write_file(outpath, content)

            outfile = f"{camelcase(modtype_name)}Controllers.ts"
            outpath = self.dest_base / "modtypes" / outfile
            template = env.get_template("ts/moduleControllers.ts.jinja2")
            content = template.render(ctx)
            content = normalize_whitespace(content)
            if not outpath.exists() or outpath.read_text().startswith("/* (unchanged"):
                self.write_file(outpath, content)

        # Autoformat
        call(["npx", "prettier", "--write", str(self.dest_base.absolute())])
