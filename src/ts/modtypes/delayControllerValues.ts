/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { ControllerValues } from "./moduleType"
// @ts-ignore
// noinspection ES6UnusedImports
import { Channels } from "./delayEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { DelayUnit } from "./delayEnums"
export interface DelayControllerValues extends ControllerValues {
  dry: number
  wet: number
  delayL: number
  delayR: number
  volumeL: number
  volumeR: number
  channels: Channels
  inverse: boolean
  delayUnit: DelayUnit
}
