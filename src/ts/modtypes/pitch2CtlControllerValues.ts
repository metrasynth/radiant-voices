/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { ControllerValues } from "./moduleType"
// @ts-ignore
// noinspection ES6UnusedImports
import { Mode } from "./pitch2CtlEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { NoteOffAction } from "./pitch2CtlEnums"
export interface Pitch2CtlControllerValues extends ControllerValues {
  mode: Mode
  noteOffAction: NoteOffAction
  firstNote: number
  range: number
  outMin: number
  outMax: number
  outController: number
}
