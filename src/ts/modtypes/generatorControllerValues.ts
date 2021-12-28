/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { ControllerValues } from "./moduleType"
// @ts-ignore
// noinspection ES6UnusedImports
import { Waveform } from "./generatorEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { Mode } from "./generatorEnums"
export interface GeneratorControllerValues extends ControllerValues {
  volume: number
  waveform: Waveform
  panning: number
  attack: number
  release: number
  polyphony: number
  mode: Mode
  sustain: boolean
  freqModulationByInput: number
  dutyCycle: number
}
