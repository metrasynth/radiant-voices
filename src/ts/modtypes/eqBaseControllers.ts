/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { Controllers, ModuleType } from "./moduleType"
import { EqControllerValues } from "./eqControllerValues"
// @ts-ignore
// noinspection ES6UnusedImports
import { Channels } from "./eqEnums"
export class EqBaseControllers implements Controllers {
  constructor(
    readonly module: ModuleType,
    readonly controllerValues: EqControllerValues
  ) {}
  // noinspection JSUnusedGlobalSymbols
  get low(): number {
    return this.controllerValues.low
  }
  // noinspection JSUnusedGlobalSymbols
  set low(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 512)
    controllerValues.low = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get middle(): number {
    return this.controllerValues.middle
  }
  // noinspection JSUnusedGlobalSymbols
  set middle(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 512)
    controllerValues.middle = newValue
  }
  // noinspection JSUnusedGlobalSymbols
  get high(): number {
    return this.controllerValues.high
  }
  // noinspection JSUnusedGlobalSymbols
  set high(newValue: number) {
    const { controllerValues } = this
    newValue = Math.min(Math.max(newValue, 0), 512)
    controllerValues.high = newValue
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
