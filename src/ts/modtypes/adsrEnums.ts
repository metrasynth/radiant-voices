/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
// Intentionally duplicated enums - see also adsr.ts
// (TypeScript does not allow exporting imported enums from inside a namespace)
export enum Curve {
  // noinspection JSUnusedGlobalSymbols
  Linear = 0,
  Exp1 = 1,
  Exp2 = 2,
  NegExp1 = 3,
  NegExp2 = 4,
  Sin = 5,
}
export enum Sustain {
  // noinspection JSUnusedGlobalSymbols
  Off = 0,
  On = 1,
  Repeat = 2,
}
export enum State {
  // noinspection JSUnusedGlobalSymbols
  Stop = 0,
  Start = 1,
}
export enum OnNoteOn {
  // noinspection JSUnusedGlobalSymbols
  DoNothing = 0,
  StartOnFirstNote = 1,
  Start = 2,
}
export enum OnNoteOff {
  // noinspection JSUnusedGlobalSymbols
  DoNothing = 0,
  StopOnLastNote = 1,
  Stop = 2,
}
export enum Mode {
  // noinspection JSUnusedGlobalSymbols
  Generator = 0,
  AmpModulatorMono = 1,
  AmpModulatorStereo = 2,
}
export enum SmoothTransitions {
  // noinspection JSUnusedGlobalSymbols
  Off = 0,
  RestartAndVolumeChange = 1,
  RestartSmootherAndVolumeChange = 2,
  VolumeChange = 3,
}
