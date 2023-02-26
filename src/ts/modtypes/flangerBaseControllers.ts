/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { Controllers, ModuleType } from "./moduleType"
import { FlangerControllerValues } from "./flangerControllerValues"
// @ts-ignore
// noinspection ES6UnusedImports
import { LfoWaveform } from "./flangerEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { LfoFreqUnit } from "./flangerEnums"
export class FlangerBaseControllers implements Controllers {
  constructor(
    readonly module: ModuleType,
    readonly controllerValues: FlangerControllerValues
  ) {}
  // noinspection JSUnusedGlobalSymbols
  get dry(): number {
    return this.controllerValues.dry
  }
  // noinspection JSUnusedGlobalSymbols
  set dry(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 256)
    controllerValues.dry = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get wet(): number {
    return this.controllerValues.wet
  }
  // noinspection JSUnusedGlobalSymbols
  set wet(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 256)
    controllerValues.wet = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get feedback(): number {
    return this.controllerValues.feedback
  }
  // noinspection JSUnusedGlobalSymbols
  set feedback(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 256)
    controllerValues.feedback = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get delay(): number {
    return this.controllerValues.delay
  }
  // noinspection JSUnusedGlobalSymbols
  set delay(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 8), 1000)
    controllerValues.delay = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get response(): number {
    return this.controllerValues.response
  }
  // noinspection JSUnusedGlobalSymbols
  set response(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 256)
    controllerValues.response = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get lfoFreq(): number {
    return this.controllerValues.lfoFreq
  }
  // noinspection JSUnusedGlobalSymbols
  set lfoFreq(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 512)
    controllerValues.lfoFreq = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get lfoAmp(): number {
    return this.controllerValues.lfoAmp
  }
  // noinspection JSUnusedGlobalSymbols
  set lfoAmp(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 256)
    controllerValues.lfoAmp = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get lfoWaveform(): LfoWaveform {
    return this.controllerValues.lfoWaveform
  }
  // noinspection JSUnusedGlobalSymbols
  set lfoWaveform(newValue: LfoWaveform) {
    const { controllerValues } = this
    controllerValues.lfoWaveform = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get setLfoPhase(): number {
    return this.controllerValues.setLfoPhase
  }
  // noinspection JSUnusedGlobalSymbols
  set setLfoPhase(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 256)
    controllerValues.setLfoPhase = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get lfoFreqUnit(): LfoFreqUnit {
    return this.controllerValues.lfoFreqUnit
  }
  // noinspection JSUnusedGlobalSymbols
  set lfoFreqUnit(newValue: LfoFreqUnit) {
    const { controllerValues } = this
    controllerValues.lfoFreqUnit = newValue
  }
}
