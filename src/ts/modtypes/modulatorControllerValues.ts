/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { ControllerValues } from "./moduleType"
// @ts-ignore
// noinspection ES6UnusedImports
import { ModulationType } from "./modulatorEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { Channels } from "./modulatorEnums"
// @ts-ignore
// noinspection ES6UnusedImports
import { MaxPhaseModulationDelay } from "./modulatorEnums"
export interface ModulatorControllerValues extends ControllerValues {
  volume: number
  modulationType: ModulationType
  channels: Channels
  maxPhaseModulationDelay: MaxPhaseModulationDelay
}
