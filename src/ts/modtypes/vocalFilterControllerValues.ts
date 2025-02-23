/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { ControllerValues } from "./moduleType"
// @ts-ignore
// noinspection ES6UnusedImports
import { VoiceType } from "./vocalFilterEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { Channels } from "./vocalFilterEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { Vowel } from "./vocalFilterEnums"
export interface VocalFilterControllerValues extends ControllerValues {
  volume: number
  formantWidth: number
  intensity: number
  formants: number
  vowel: number
  voiceType: VoiceType
  channels: Channels
  randomFrequency: number
  randomSeed: number
  vowel1: Vowel
  vowel2: Vowel
  vowel3: Vowel
  vowel4: Vowel
  vowel5: Vowel
}
