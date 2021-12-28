/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { Controllers, ModuleType } from "./moduleType"
import { DistortionControllerValues } from "./distortionControllerValues"
// @ts-ignore
// noinspection ES6UnusedImports
import { Type } from "./distortionEnums"
export class DistortionBaseControllers implements Controllers {
  constructor(
    readonly module: ModuleType,
    readonly controllerValues: DistortionControllerValues
  ) {}
  // noinspection JSUnusedGlobalSymbols
  get volume(): number {
    return this.controllerValues.volume
  }
  // noinspection JSUnusedGlobalSymbols
  set volume(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 256)
    controllerValues.volume = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get type(): Type {
    return this.controllerValues.type
  }
  // noinspection JSUnusedGlobalSymbols
  set type(newValue: Type) {
    const { controllerValues } = this
    controllerValues.type = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get power(): number {
    return this.controllerValues.power
  }
  // noinspection JSUnusedGlobalSymbols
  set power(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 256)
    controllerValues.power = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get bitDepth(): number {
    return this.controllerValues.bitDepth
  }
  // noinspection JSUnusedGlobalSymbols
  set bitDepth(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 1), 16)
    controllerValues.bitDepth = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get freq(): number {
    return this.controllerValues.freq
  }
  // noinspection JSUnusedGlobalSymbols
  set freq(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 44100)
    controllerValues.freq = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get noise(): number {
    return this.controllerValues.noise
  }
  // noinspection JSUnusedGlobalSymbols
  set noise(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 256)
    controllerValues.noise = newValue
  }
}
