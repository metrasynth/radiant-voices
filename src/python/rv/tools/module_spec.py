from enum import IntEnum
from typing import Type

from rich import get_console, print
from rich.table import Table
from rv.api import m
from rv.controller import DependentRange, Range
from slugify import slugify
from sunvox.api import INIT_FLAG, Slot, deinit, init


class CtlType(IntEnum):
    SCALED = 0
    ENUM = 1


def report_module(slot: Slot, name: str, modcls: Type[m.Module]):
    mod_num = slot.new_module(name, name, 0, 0, 0)
    table = Table(show_header=True, title=name)
    table.add_column("#")
    table.add_column("Name")
    table.add_column("Slug")
    table.add_column("Type")
    table.add_column("Default")
    table.add_column("Group")
    table.add_column("Range (Real)")
    table.add_column("Range (Scaled)")
    table.add_column("Range (Display)")
    table.add_column("Offset")
    table.add_column("Errors")
    any_errors = False
    for x in range(256):
        if not (name := slot.get_module_ctl_name(mod_num, x)):
            break
        if name == "...":
            break
        slug = slugify(name)
        number = str(x)
        ctl_type = CtlType(slot.get_module_ctl_type(mod_num, x))
        type_name = ctl_type.name
        default = slot.get_module_ctl_value(mod_num, x, 2)
        group = slot.get_module_ctl_group(mod_num, x)
        real_min = slot.get_module_ctl_min(mod_num, x, 0)
        real_max = slot.get_module_ctl_max(mod_num, x, 0)
        real_range = f"[{real_min}, {real_max}]"
        scaled_min = slot.get_module_ctl_min(mod_num, x, 1)
        scaled_max = slot.get_module_ctl_max(mod_num, x, 1) or 32768
        scaled_range = f"[{scaled_min}, {scaled_max}]"
        display_min = slot.get_module_ctl_min(mod_num, x, 2)
        display_max = slot.get_module_ctl_max(mod_num, x, 2)
        display_range = f"[{display_min}, {display_max}]"
        offset = slot.get_module_ctl_offset(mod_num, x)
        try:
            c = list(modcls.controllers.values())[x]
            errors = []
        except IndexError:
            c = None
            errors = ["Missing RV controller"]
        if c:
            if c.default != default:
                errors += [f"Default mismatch: {c.default=}"]
            if isinstance(c.value_type, DependentRange):
                errors += ["Unverified DependentRange"]
            elif isinstance(c.value_type, Range):
                if c.value_type.min != display_min:
                    errors += [f"Min mismatch: {c.value_type.min=}"]
                if c.value_type.max != display_max:
                    errors += [f"max mismatch: {c.value_type.max=}"]
            elif isinstance(c.value_type, type) and issubclass(c.value_type, IntEnum):
                max_enum = max(*list(c.value_type))
                if max_enum < real_max:
                    errors += [f"IntEnum missing: {max_enum.value=}"]
            elif c.value_type is bool:
                if real_max != 1:
                    errors += ["Bool should be IntEnum"]
            else:
                errors += [f"⛔️ {c.value_type=}"]
        any_errors = any_errors or bool(errors)
        table.add_row(
            number,
            name,
            slug,
            type_name,
            str(default),
            str(group),
            real_range,
            scaled_range,
            display_range,
            str(offset),
            "\n".join(errors),
        )
    get_console().width = 200
    print(table)


def main():
    init(None, 44100, 2, INIT_FLAG.ONE_THREAD | INIT_FLAG.USER_AUDIO_CALLBACK)
    slot = Slot()
    for modcls in m.MODULE_CLASSES.values():
        report_module(slot, modcls.mtype, modcls)
    deinit()


if __name__ == "__main__":
    main()
