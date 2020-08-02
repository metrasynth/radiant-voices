/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { MidiMap, ControllerMidiMap, ControllerMidiMaps } from "../controllerMidiMap"
import { Project } from "../project"
import { ModuleBase } from "./moduleBase"
import { ModuleType, OptionValues, Options } from "./moduleType"
import { VocalFilterBehavior } from "./vocalFilterBehavior"
import { VocalFilterControllers } from "./vocalFilterControllers"
import { VocalFilterControllerValues } from "./vocalFilterControllerValues"
import { VoiceType as _VoiceType } from "./vocalFilterEnums"
import { Channels as _Channels } from "./vocalFilterEnums"
export namespace VocalFilter {
  export const VoiceType = _VoiceType
  export const Channels = _Channels
  interface VocalFilterControllerMidiMaps extends ControllerMidiMaps {
    volume: ControllerMidiMap
    formantWidthHz: ControllerMidiMap
    intensity: ControllerMidiMap
    formants: ControllerMidiMap
    vowel: ControllerMidiMap
    voiceType: ControllerMidiMap
    channels: ControllerMidiMap
  }
  interface VocalFilterOptionValues extends OptionValues {}
  class VocalFilterOptions implements Options {
    constructor(readonly optionValues: VocalFilterOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "Vocal filter"
    flags = 81
    readonly typeName = "Vocal filter"
    readonly controllerSetters = [
      (val: number) => {
        this.controllerValues.volume = val
      },
      (val: number) => {
        this.controllerValues.formantWidthHz = val
      },
      (val: number) => {
        this.controllerValues.intensity = val
      },
      (val: number) => {
        this.controllerValues.formants = val
      },
      (val: number) => {
        this.controllerValues.vowel = val
      },
      (val: number) => {
        this.controllerValues.voiceType = val
      },
      (val: number) => {
        this.controllerValues.channels = val
      },
    ]
    readonly controllerValues: VocalFilterControllerValues = {
      volume: 256,
      formantWidthHz: 128,
      intensity: 128,
      formants: 5,
      vowel: 0,
      voiceType: VoiceType.Soprano,
      channels: Channels.Stereo,
    }
    readonly controllers: VocalFilterControllers = new VocalFilterControllers(
      this,
      this.controllerValues
    )
    readonly c = this.controllers
    readonly midiMaps: VocalFilterControllerMidiMaps = {
      volume: new ControllerMidiMap(),
      formantWidthHz: new ControllerMidiMap(),
      intensity: new ControllerMidiMap(),
      formants: new ControllerMidiMap(),
      vowel: new ControllerMidiMap(),
      voiceType: new ControllerMidiMap(),
      channels: new ControllerMidiMap(),
    }
    readonly optionValues: VocalFilterOptionValues = {}
    readonly options: VocalFilterOptions = new VocalFilterOptions(this.optionValues)
    readonly o = this.options
    behavior?: VocalFilterBehavior
    constructor() {
      super()
      this.behavior = new VocalFilterBehavior(this)
    }
    attachTo(project: Project): AttachedModule {
      return super.attachTo(project) as AttachedModule
    }
    *rawControllerValues(): Generator<number> {
      const { controllerValues: cv } = this
      yield cv.volume
      yield cv.formantWidthHz
      yield cv.intensity
      yield cv.formants
      yield cv.vowel
      yield cv.voiceType
      yield cv.channels
    }
    setMidiMaps(midiMaps: MidiMap[]) {
      this.midiMaps.volume = midiMaps[0]
      this.midiMaps.formantWidthHz = midiMaps[1]
      this.midiMaps.intensity = midiMaps[2]
      this.midiMaps.formants = midiMaps[3]
      this.midiMaps.vowel = midiMaps[4]
      this.midiMaps.voiceType = midiMaps[5]
      this.midiMaps.channels = midiMaps[6]
    }
    midiMapsArray(): MidiMap[] {
      const a: MidiMap[] = []
      a.push(this.midiMaps.volume)
      a.push(this.midiMaps.formantWidthHz)
      a.push(this.midiMaps.intensity)
      a.push(this.midiMaps.formants)
      a.push(this.midiMaps.vowel)
      a.push(this.midiMaps.voiceType)
      a.push(this.midiMaps.channels)
      return a
    }
  }
  export class AttachedModule extends Module {
    get index(): number {
      if (this._index === undefined) {
        throw new Error("Attached module has empty index")
      }
      return this._index
    }
    set index(_: number) {
      throw new Error("Module index can only be assigned once")
    }
  }
}
