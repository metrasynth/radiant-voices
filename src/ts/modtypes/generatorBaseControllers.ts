/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { Controllers, ModuleType } from "./moduleType"
import { GeneratorControllerValues } from "./generatorControllerValues"
// @ts-ignore
// noinspection ES6UnusedImports
import { Waveform } from "./generatorEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { Mode } from "./generatorEnums"
export class GeneratorBaseControllers implements Controllers {
  constructor(
    readonly module: ModuleType,
    readonly controllerValues: GeneratorControllerValues
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
  get waveform(): Waveform {
    return this.controllerValues.waveform
  }
  // noinspection JSUnusedGlobalSymbols
  set waveform(newValue: Waveform) {
    const { controllerValues } = this
    controllerValues.waveform = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get panning(): number {
    return this.controllerValues.panning + -128
  }
  // noinspection JSUnusedGlobalSymbols
  set panning(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, -128), 128)
    controllerValues.panning = newValue - -128
  }
  // noinspection JSUnusedGlobalSymbols
  get attack(): number {
    return this.controllerValues.attack
  }
  // noinspection JSUnusedGlobalSymbols
  set attack(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 512)
    controllerValues.attack = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get release(): number {
    return this.controllerValues.release
  }
  // noinspection JSUnusedGlobalSymbols
  set release(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 512)
    controllerValues.release = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get polyphonyCh(): number {
    return this.controllerValues.polyphonyCh
  }
  // noinspection JSUnusedGlobalSymbols
  set polyphonyCh(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 1), 16)
    controllerValues.polyphonyCh = newValue
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
  get sustain(): boolean {
    return this.controllerValues.sustain
  }
  // noinspection JSUnusedGlobalSymbols
  set sustain(newValue: boolean) {
    const { controllerValues } = this
    controllerValues.sustain = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get freqModulationByInput(): number {
    return this.controllerValues.freqModulationByInput
  }
  // noinspection JSUnusedGlobalSymbols
  set freqModulationByInput(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 256)
    controllerValues.freqModulationByInput = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get dutyCycle(): number {
    return this.controllerValues.dutyCycle
  }
  // noinspection JSUnusedGlobalSymbols
  set dutyCycle(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 1022)
    controllerValues.dutyCycle = newValue
  }
}
