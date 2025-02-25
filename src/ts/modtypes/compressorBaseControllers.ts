/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { Controllers, ModuleType } from "./moduleType"
import { CompressorControllerValues } from "./compressorControllerValues"
// @ts-ignore
// noinspection ES6UnusedImports
import { Mode } from "./compressorEnums"
export class CompressorBaseControllers implements Controllers {
  constructor(
    readonly module: ModuleType,
    readonly controllerValues: CompressorControllerValues
  ) {}
  // noinspection JSUnusedGlobalSymbols
  get volume(): number {
    return this.controllerValues.volume
  }
  // noinspection JSUnusedGlobalSymbols
  set volume(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 512)
    controllerValues.volume = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get threshold(): number {
    return this.controllerValues.threshold
  }
  // noinspection JSUnusedGlobalSymbols
  set threshold(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 512)
    controllerValues.threshold = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get slope(): number {
    return this.controllerValues.slope
  }
  // noinspection JSUnusedGlobalSymbols
  set slope(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 200)
    controllerValues.slope = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get attack(): number {
    return this.controllerValues.attack
  }
  // noinspection JSUnusedGlobalSymbols
  set attack(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 500)
    controllerValues.attack = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get release(): number {
    return this.controllerValues.release
  }
  // noinspection JSUnusedGlobalSymbols
  set release(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 1), 1000)
    controllerValues.release = newValue
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
  get sidechainInput(): number {
    return this.controllerValues.sidechainInput
  }
  // noinspection JSUnusedGlobalSymbols
  set sidechainInput(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 32)
    controllerValues.sidechainInput = newValue
  }
}
