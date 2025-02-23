/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { Controllers, ModuleType } from "./moduleType"
import { Pitch2CtlControllerValues } from "./pitch2CtlControllerValues"
// @ts-ignore
// noinspection ES6UnusedImports
import { Mode } from "./pitch2CtlEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { NoteOffAction } from "./pitch2CtlEnums"
export class Pitch2CtlBaseControllers implements Controllers {
  constructor(
    readonly module: ModuleType,
    readonly controllerValues: Pitch2CtlControllerValues
  ) {}
  // noinspection JSUnusedGlobalSymbols
  get mode(): Mode {
    return this.controllerValues.mode
  }
  // noinspection JSUnusedGlobalSymbols
  set mode(newValue: Mode) {
    const { controllerValues } = this
    controllerValues.mode = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get noteOffAction(): NoteOffAction {
    return this.controllerValues.noteOffAction
  }
  // noinspection JSUnusedGlobalSymbols
  set noteOffAction(newValue: NoteOffAction) {
    const { controllerValues } = this
    controllerValues.noteOffAction = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get firstNote(): number {
    return this.controllerValues.firstNote
  }
  // noinspection JSUnusedGlobalSymbols
  set firstNote(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 256)
    controllerValues.firstNote = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get range(): number {
    return this.controllerValues.range
  }
  // noinspection JSUnusedGlobalSymbols
  set range(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 256)
    controllerValues.range = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get outMin(): number {
    return this.controllerValues.outMin
  }
  // noinspection JSUnusedGlobalSymbols
  set outMin(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 32768)
    controllerValues.outMin = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get outMax(): number {
    return this.controllerValues.outMax
  }
  // noinspection JSUnusedGlobalSymbols
  set outMax(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 32768)
    controllerValues.outMax = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get outController(): number {
    return this.controllerValues.outController
  }
  // noinspection JSUnusedGlobalSymbols
  set outController(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 255)
    controllerValues.outController = newValue
  }
}
