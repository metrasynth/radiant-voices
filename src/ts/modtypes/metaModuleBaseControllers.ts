/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { Controllers, ModuleType } from "./moduleType"
import { MetaModuleControllerValues } from "./metaModuleControllerValues"
// @ts-ignore
// noinspection ES6UnusedImports
import { PlayPatterns } from "./metaModuleEnums"
export class MetaModuleBaseControllers implements Controllers {
  constructor(
    readonly module: ModuleType,
    readonly controllerValues: MetaModuleControllerValues
  ) {}
  // noinspection JSUnusedGlobalSymbols
  get volume(): number {
    return this.controllerValues.volume
  }
  // noinspection JSUnusedGlobalSymbols
  set volume(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 1024)
    controllerValues.volume = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get inputModule(): number {
    return this.controllerValues.inputModule
  }
  // noinspection JSUnusedGlobalSymbols
  set inputModule(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 1), 256)
    controllerValues.inputModule = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get playPatterns(): PlayPatterns {
    return this.controllerValues.playPatterns
  }
  // noinspection JSUnusedGlobalSymbols
  set playPatterns(newValue: PlayPatterns) {
    const { controllerValues } = this
    controllerValues.playPatterns = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get bpm(): number {
    return this.controllerValues.bpm
  }
  // noinspection JSUnusedGlobalSymbols
  set bpm(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 1), 800)
    controllerValues.bpm = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get tpl(): number {
    return this.controllerValues.tpl
  }
  // noinspection JSUnusedGlobalSymbols
  set tpl(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 1), 31)
    controllerValues.tpl = newValue
  }
}
