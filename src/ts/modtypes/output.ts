/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { Project } from "../project"
import { ModuleBase } from "./moduleBase"
import {
  ControllerValues,
  Controllers,
  ModuleType,
  OptionValues,
  Options,
} from "./moduleType"
import { OutputBehavior } from "./outputBehavior"
export namespace Output {
  interface OutputControllerValues extends ControllerValues {}
  class OutputControllers implements Controllers {
    constructor(readonly controllerValues: OutputControllerValues) {}
  }
  interface OutputOptionValues extends OptionValues {}
  class OutputOptions implements Options {
    constructor(readonly optionValues: OutputOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "Output"
    flags = 67
    readonly typeName = "Output"
    readonly controllerSetters = []
    readonly controllerValues: OutputControllerValues = {}
    readonly controllers: OutputControllers = new OutputControllers(
      this.controllerValues
    )
    readonly c = this.controllers
    readonly optionValues: OutputOptionValues = {}
    readonly options: OutputOptions = new OutputOptions(this.optionValues)
    readonly o = this.options
    behavior?: OutputBehavior
    constructor() {
      super()
      this.behavior = new OutputBehavior(this)
    }
    attachTo(project: Project): AttachedModule {
      return super.attachTo(project) as AttachedModule
    }
  }
  export class AttachedModule extends Module {
    get index(): number {
      if (this._index === undefined) {
        throw new Error("Attached module has empty index")
      }
      return this._index
    }
    set index(_: number) {
      throw new Error("Module index can only be assigned once")
    }
  }
}
