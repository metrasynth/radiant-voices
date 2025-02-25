/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { Controllers, ModuleType } from "./moduleType"
import { SmoothControllerValues } from "./smoothControllerValues"
// @ts-ignore
// noinspection ES6UnusedImports
import { Mode } from "./smoothEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { Channels } from "./smoothEnums"
export class SmoothBaseControllers implements Controllers {
  constructor(
    readonly module: ModuleType,
    readonly controllerValues: SmoothControllerValues
  ) {}
  // noinspection JSUnusedGlobalSymbols
  get rise(): number {
    return this.controllerValues.rise
  }
  // noinspection JSUnusedGlobalSymbols
  set rise(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 32768)
    controllerValues.rise = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get fall(): number {
    return this.controllerValues.fall
  }
  // noinspection JSUnusedGlobalSymbols
  set fall(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 32768)
    controllerValues.fall = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get fallEqRise(): boolean {
    return this.controllerValues.fallEqRise
  }
  // noinspection JSUnusedGlobalSymbols
  set fallEqRise(newValue: boolean) {
    const { controllerValues } = this
    controllerValues.fallEqRise = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get scale(): number {
    return this.controllerValues.scale
  }
  // noinspection JSUnusedGlobalSymbols
  set scale(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 400)
    controllerValues.scale = newValue
  }
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
  get channels(): Channels {
    return this.controllerValues.channels
  }
  // noinspection JSUnusedGlobalSymbols
  set channels(newValue: Channels) {
    const { controllerValues } = this
    controllerValues.channels = newValue
  }
}
