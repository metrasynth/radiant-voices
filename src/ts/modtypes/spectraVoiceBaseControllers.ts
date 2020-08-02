/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { Controllers, ModuleType } from "./moduleType"
import { SpectraVoiceControllerValues } from "./spectraVoiceControllerValues"
// @ts-ignore
// noinspection ES6UnusedImports
import { Mode } from "./spectraVoiceEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { HarmonicType } from "./spectraVoiceEnums"
export class SpectraVoiceBaseControllers implements Controllers {
  constructor(
    readonly module: ModuleType,
    readonly controllerValues: SpectraVoiceControllerValues
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
    newValue = Math.min(Math.max(newValue, 1), 32)
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
  get spectrumResolution(): number {
    return this.controllerValues.spectrumResolution
  }
  // noinspection JSUnusedGlobalSymbols
  set spectrumResolution(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 5)
    controllerValues.spectrumResolution = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get harmonic(): number {
    return this.controllerValues.harmonic
  }
  // noinspection JSUnusedGlobalSymbols
  set harmonic(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 15)
    controllerValues.harmonic = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get hFreqHz(): number {
    return this.controllerValues.hFreqHz
  }
  // noinspection JSUnusedGlobalSymbols
  set hFreqHz(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 22050)
    controllerValues.hFreqHz = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get hVolume(): number {
    return this.controllerValues.hVolume
  }
  // noinspection JSUnusedGlobalSymbols
  set hVolume(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 255)
    controllerValues.hVolume = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get hWidth(): number {
    return this.controllerValues.hWidth
  }
  // noinspection JSUnusedGlobalSymbols
  set hWidth(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 255)
    controllerValues.hWidth = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get hType(): HarmonicType {
    return this.controllerValues.hType
  }
  // noinspection JSUnusedGlobalSymbols
  set hType(newValue: HarmonicType) {
    const { controllerValues } = this
    controllerValues.hType = newValue
  }
}
