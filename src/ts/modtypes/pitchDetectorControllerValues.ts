/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { ControllerValues } from "./moduleType"
// @ts-ignore
// noinspection ES6UnusedImports
import { Algorithm } from "./pitchDetectorEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { RollOff } from "./pitchDetectorEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { SampleRate } from "./pitchDetectorEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { Buffer } from "./pitchDetectorEnums"
export interface PitchDetectorControllerValues extends ControllerValues {
  algorithm: Algorithm
  threshold: number
  gain: number
  microtones: boolean
  detectorFinetune: number
  lpFilterFreq: number
  lpFilterRolloff: RollOff
  alg_1_2SampleRate: SampleRate
  alg_1_2Buffer: Buffer
  alg_1_2BufferOverlap: number
  alg_1Sensitivity: number
  recordNotes: boolean
}
