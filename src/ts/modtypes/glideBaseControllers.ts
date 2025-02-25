/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { Controllers, ModuleType } from "./moduleType"
import { GlideControllerValues } from "./glideControllerValues"
export class GlideBaseControllers implements Controllers {
  constructor(
    readonly module: ModuleType,
    readonly controllerValues: GlideControllerValues
  ) {}
  // noinspection JSUnusedGlobalSymbols
  get response(): number {
    return this.controllerValues.response
  }
  // noinspection JSUnusedGlobalSymbols
  set response(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 1000)
    controllerValues.response = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get sampleRate(): number {
    return this.controllerValues.sampleRate
  }
  // noinspection JSUnusedGlobalSymbols
  set sampleRate(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 1), 32768)
    controllerValues.sampleRate = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get resetOnFirstNote(): boolean {
    return this.controllerValues.resetOnFirstNote
  }
  // noinspection JSUnusedGlobalSymbols
  set resetOnFirstNote(newValue: boolean) {
    const { controllerValues } = this
    controllerValues.resetOnFirstNote = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get polyphony(): boolean {
    return this.controllerValues.polyphony
  }
  // noinspection JSUnusedGlobalSymbols
  set polyphony(newValue: boolean) {
    const { controllerValues } = this
    controllerValues.polyphony = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get pitch(): number {
    return this.controllerValues.pitch + -600
  }
  // noinspection JSUnusedGlobalSymbols
  set pitch(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, -600), 600)
    controllerValues.pitch = newValue - -600
  }
  // noinspection JSUnusedGlobalSymbols
  get pitchScale(): number {
    return this.controllerValues.pitchScale
  }
  // noinspection JSUnusedGlobalSymbols
  set pitchScale(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 200)
    controllerValues.pitchScale = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get reset(): boolean {
    return this.controllerValues.reset
  }
  // noinspection JSUnusedGlobalSymbols
  set reset(newValue: boolean) {
    const { controllerValues } = this
    controllerValues.reset = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get octave(): number {
    return this.controllerValues.octave + -10
  }
  // noinspection JSUnusedGlobalSymbols
  set octave(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, -10), 10)
    controllerValues.octave = newValue - -10
  }
  // noinspection JSUnusedGlobalSymbols
  get freqMultiply(): number {
    return this.controllerValues.freqMultiply
  }
  // noinspection JSUnusedGlobalSymbols
  set freqMultiply(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 1), 256)
    controllerValues.freqMultiply = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get freqDivide(): number {
    return this.controllerValues.freqDivide
  }
  // noinspection JSUnusedGlobalSymbols
  set freqDivide(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 1), 256)
    controllerValues.freqDivide = newValue
  }
}
