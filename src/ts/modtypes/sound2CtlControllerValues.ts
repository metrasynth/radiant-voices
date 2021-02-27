/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { ControllerValues } from "./moduleType"
// @ts-ignore
// noinspection ES6UnusedImports
import { Channels } from "./sound2CtlEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { Mode } from "./sound2CtlEnums"
export interface Sound2CtlControllerValues extends ControllerValues {
  sampleRateHz: number
  channels: Channels
  absolute: boolean
  gain: number
  smooth: number
  mode: Mode
  outMin: number
  outMax: number
  outController: number
}
