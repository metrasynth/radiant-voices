/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { Controllers, ModuleType } from "./moduleType"
import { DelayControllerValues } from "./delayControllerValues"
// @ts-ignore
// noinspection ES6UnusedImports
import { Channels } from "./delayEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { DelayUnit } from "./delayEnums"
export class DelayBaseControllers implements Controllers {
  constructor(
    readonly module: ModuleType,
    readonly controllerValues: DelayControllerValues
  ) {}
  // noinspection JSUnusedGlobalSymbols
  get dry(): number {
    return this.controllerValues.dry
  }
  // noinspection JSUnusedGlobalSymbols
  set dry(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 512)
    controllerValues.dry = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get wet(): number {
    return this.controllerValues.wet
  }
  // noinspection JSUnusedGlobalSymbols
  set wet(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 512)
    controllerValues.wet = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get delayL(): number {
    return this.controllerValues.delayL
  }
  // noinspection JSUnusedGlobalSymbols
  set delayL(newValue: number) {
    const { controllerValues } = this
    switch (this.controllerValues.delayUnit) {
      case DelayUnit.SecDiv_16384:
        newValue = Math.min(Math.max(newValue, 0), 256)
        break
      case DelayUnit.Ms:
        newValue = Math.min(Math.max(newValue, 0), 4000)
        break
      case DelayUnit.Hz:
        newValue = Math.min(Math.max(newValue, 0), 8192)
        break
      case DelayUnit.Tick:
        newValue = Math.min(Math.max(newValue, 0), 256)
        break
      case DelayUnit.Line:
        newValue = Math.min(Math.max(newValue, 0), 256)
        break
      case DelayUnit.LineDiv_2:
        newValue = Math.min(Math.max(newValue, 0), 256)
        break
      case DelayUnit.LineDiv_3:
        newValue = Math.min(Math.max(newValue, 0), 256)
        break
      case DelayUnit.SecDiv_44100:
        newValue = Math.min(Math.max(newValue, 0), 32768)
        break
      case DelayUnit.SecDiv_48000:
        newValue = Math.min(Math.max(newValue, 0), 32768)
        break
      case DelayUnit.Sample:
        newValue = Math.min(Math.max(newValue, 0), 32768)
        break
    }
    controllerValues.delayL = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get delayR(): number {
    return this.controllerValues.delayR
  }
  // noinspection JSUnusedGlobalSymbols
  set delayR(newValue: number) {
    const { controllerValues } = this
    switch (this.controllerValues.delayUnit) {
      case DelayUnit.SecDiv_16384:
        newValue = Math.min(Math.max(newValue, 0), 256)
        break
      case DelayUnit.Ms:
        newValue = Math.min(Math.max(newValue, 0), 4000)
        break
      case DelayUnit.Hz:
        newValue = Math.min(Math.max(newValue, 0), 8192)
        break
      case DelayUnit.Tick:
        newValue = Math.min(Math.max(newValue, 0), 256)
        break
      case DelayUnit.Line:
        newValue = Math.min(Math.max(newValue, 0), 256)
        break
      case DelayUnit.LineDiv_2:
        newValue = Math.min(Math.max(newValue, 0), 256)
        break
      case DelayUnit.LineDiv_3:
        newValue = Math.min(Math.max(newValue, 0), 256)
        break
      case DelayUnit.SecDiv_44100:
        newValue = Math.min(Math.max(newValue, 0), 32768)
        break
      case DelayUnit.SecDiv_48000:
        newValue = Math.min(Math.max(newValue, 0), 32768)
        break
      case DelayUnit.Sample:
        newValue = Math.min(Math.max(newValue, 0), 32768)
        break
    }
    controllerValues.delayR = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get volumeL(): number {
    return this.controllerValues.volumeL
  }
  // noinspection JSUnusedGlobalSymbols
  set volumeL(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 256)
    controllerValues.volumeL = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get volumeR(): number {
    return this.controllerValues.volumeR
  }
  // noinspection JSUnusedGlobalSymbols
  set volumeR(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 256)
    controllerValues.volumeR = newValue
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
  // noinspection JSUnusedGlobalSymbols
  get inverse(): boolean {
    return this.controllerValues.inverse
  }
  // noinspection JSUnusedGlobalSymbols
  set inverse(newValue: boolean) {
    const { controllerValues } = this
    controllerValues.inverse = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get delayUnit(): DelayUnit {
    return this.controllerValues.delayUnit
  }
  // noinspection JSUnusedGlobalSymbols
  set delayUnit(newValue: DelayUnit) {
    const { controllerValues } = this
    controllerValues.delayUnit = newValue
    this.delayL = this.delayL
    this.delayR = this.delayR
  }
  // noinspection JSUnusedGlobalSymbols
  get delayMultiplier(): number {
    return this.controllerValues.delayMultiplier
  }
  // noinspection JSUnusedGlobalSymbols
  set delayMultiplier(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 1), 15)
    controllerValues.delayMultiplier = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get feedback(): number {
    return this.controllerValues.feedback
  }
  // noinspection JSUnusedGlobalSymbols
  set feedback(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 32768)
    controllerValues.feedback = newValue
  }
}
