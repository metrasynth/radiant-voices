/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { Controllers, ModuleType } from "./moduleType"
import { AdsrControllerValues } from "./adsrControllerValues"
// @ts-ignore
// noinspection ES6UnusedImports
import { Curve } from "./adsrEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { Sustain } from "./adsrEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { State } from "./adsrEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { OnNoteOn } from "./adsrEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { OnNoteOff } from "./adsrEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { Mode } from "./adsrEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { SmoothTransitions } from "./adsrEnums"
export class AdsrBaseControllers implements Controllers {
  constructor(
    readonly module: ModuleType,
    readonly controllerValues: AdsrControllerValues
  ) {}
  // noinspection JSUnusedGlobalSymbols
  get volume(): number {
    return this.controllerValues.volume
  }
  // noinspection JSUnusedGlobalSymbols
  set volume(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 32768)
    controllerValues.volume = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get attack(): number {
    return this.controllerValues.attack
  }
  // noinspection JSUnusedGlobalSymbols
  set attack(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 10000)
    controllerValues.attack = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get decay(): number {
    return this.controllerValues.decay
  }
  // noinspection JSUnusedGlobalSymbols
  set decay(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 10000)
    controllerValues.decay = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get sustainLevel(): number {
    return this.controllerValues.sustainLevel
  }
  // noinspection JSUnusedGlobalSymbols
  set sustainLevel(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 32768)
    controllerValues.sustainLevel = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get release(): number {
    return this.controllerValues.release
  }
  // noinspection JSUnusedGlobalSymbols
  set release(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 10000)
    controllerValues.release = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get attackCurve(): Curve {
    return this.controllerValues.attackCurve
  }
  // noinspection JSUnusedGlobalSymbols
  set attackCurve(newValue: Curve) {
    const { controllerValues } = this
    controllerValues.attackCurve = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get decayCurve(): Curve {
    return this.controllerValues.decayCurve
  }
  // noinspection JSUnusedGlobalSymbols
  set decayCurve(newValue: Curve) {
    const { controllerValues } = this
    controllerValues.decayCurve = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get releaseCurve(): Curve {
    return this.controllerValues.releaseCurve
  }
  // noinspection JSUnusedGlobalSymbols
  set releaseCurve(newValue: Curve) {
    const { controllerValues } = this
    controllerValues.releaseCurve = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get sustain(): Sustain {
    return this.controllerValues.sustain
  }
  // noinspection JSUnusedGlobalSymbols
  set sustain(newValue: Sustain) {
    const { controllerValues } = this
    controllerValues.sustain = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get sustainPedal(): boolean {
    return this.controllerValues.sustainPedal
  }
  // noinspection JSUnusedGlobalSymbols
  set sustainPedal(newValue: boolean) {
    const { controllerValues } = this
    controllerValues.sustainPedal = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get state(): State {
    return this.controllerValues.state
  }
  // noinspection JSUnusedGlobalSymbols
  set state(newValue: State) {
    const { controllerValues } = this
    controllerValues.state = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get onNoteOn(): OnNoteOn {
    return this.controllerValues.onNoteOn
  }
  // noinspection JSUnusedGlobalSymbols
  set onNoteOn(newValue: OnNoteOn) {
    const { controllerValues } = this
    controllerValues.onNoteOn = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get onNoteOff(): OnNoteOff {
    return this.controllerValues.onNoteOff
  }
  // noinspection JSUnusedGlobalSymbols
  set onNoteOff(newValue: OnNoteOff) {
    const { controllerValues } = this
    controllerValues.onNoteOff = newValue
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
  get smoothTransitions(): SmoothTransitions {
    return this.controllerValues.smoothTransitions
  }
  // noinspection JSUnusedGlobalSymbols
  set smoothTransitions(newValue: SmoothTransitions) {
    const { controllerValues } = this
    controllerValues.smoothTransitions = newValue
  }
}
