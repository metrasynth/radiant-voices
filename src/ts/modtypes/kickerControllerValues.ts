/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { ControllerValues } from "./moduleType"
// @ts-ignore
// noinspection ES6UnusedImports
import { Waveform } from "./kickerEnums"
export interface KickerControllerValues extends ControllerValues {
  volume: number
  waveform: Waveform
  panning: number
  attack: number
  release: number
  boost: number
  acceleration: number
  polyphony: number
  noClick: boolean
}
