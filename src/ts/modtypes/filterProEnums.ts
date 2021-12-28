/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
// Intentionally duplicated enums - see also filterPro.ts
// (TypeScript does not allow exporting imported enums from inside a namespace)
export enum Type {
  // noinspection JSUnusedGlobalSymbols
  Lp = 0,
  Hp = 1,
  BpConstSkirtGain = 2,
  BpConstPeakGain = 3,
  Notch = 4,
  AllPass = 5,
  Peaking = 6,
  LowShelf = 7,
  HighShelf = 8,
  Lp_6dB = 9,
  Hp_6dB = 10,
}
export enum RollOff {
  // noinspection JSUnusedGlobalSymbols
  _12dB = 0,
  _24dB = 1,
  _36dB = 2,
  _48dB = 3,
}
export enum Mode {
  // noinspection JSUnusedGlobalSymbols
  Stereo = 0,
  Mono = 1,
  StereoSmoothing = 2,
  MonoSmoothing = 3,
}
export enum LfoWaveform {
  // noinspection JSUnusedGlobalSymbols
  Sin = 0,
  Saw = 1,
  Saw2 = 2,
  Square = 3,
  Random = 4,
}
export enum LfoFreqUnit {
  // noinspection JSUnusedGlobalSymbols
  HzMul_0_02 = 0,
  Ms = 1,
  Hz = 2,
  Tick = 3,
  Line = 4,
  LineDiv_2 = 5,
  LineDiv_3 = 6,
}
