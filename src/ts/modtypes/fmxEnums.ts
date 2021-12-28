/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
// Intentionally duplicated enums - see also fmx.ts
// (TypeScript does not allow exporting imported enums from inside a namespace)
export enum SampleRate {
  // noinspection JSUnusedGlobalSymbols
  _8000hz = 0,
  _11025hz = 1,
  _16000hz = 2,
  _22050hz = 3,
  _32000hz = 4,
  _44100hz = 5,
  Native = 6,
}
export enum Channels {
  // noinspection JSUnusedGlobalSymbols
  Mono = 0,
  Stereo = 1,
}
export enum InputCustomWaveform {
  // noinspection JSUnusedGlobalSymbols
  Off = 0,
  SingleCycle = 1,
  Continuous = 2,
}
export enum AdsrSmoothTransitions {
  // noinspection JSUnusedGlobalSymbols
  Off = 0,
  RestartAndVolumeChange = 1,
  RestartSmootherAndVolumeChange = 2,
  VolumeChange = 3,
}
export enum AdsrCurve {
  // noinspection JSUnusedGlobalSymbols
  Linear = 0,
  Exp1 = 1,
  Exp2 = 2,
  _negExp1 = 3,
  _negExp2 = 4,
  Sin = 5,
}
export enum Sustain {
  // noinspection JSUnusedGlobalSymbols
  Off = 0,
  On = 1,
  Repeat = 2,
}
export enum Waveform {
  // noinspection JSUnusedGlobalSymbols
  Custom = 0,
  Triangle = 1,
  TrianglePow_3 = 2,
  Saw = 3,
  SawPow_3 = 4,
  Square = 5,
  Sin = 6,
  Hsin = 7,
  Asin = 8,
  SinPow_3 = 9,
}
export enum ModulationType {
  // noinspection JSUnusedGlobalSymbols
  Phase = 0,
  Frequency = 1,
  AmplitudeMul = 2,
  Add = 3,
  Sub = 4,
  Min = 5,
  Max = 6,
  BitwiseAnd = 7,
  BitwiseXor = 8,
}
