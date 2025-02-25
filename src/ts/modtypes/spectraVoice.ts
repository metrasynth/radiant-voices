/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { MidiMap, ControllerMidiMap, ControllerMidiMaps } from "../controllerMidiMap"
import { Project } from "../project"
import { ModuleBase } from "./moduleBase"
import { ModuleType, OptionValues, Options } from "./moduleType"
import { SpectraVoiceBehavior } from "./spectraVoiceBehavior"
import { SpectraVoiceControllers } from "./spectraVoiceControllers"
import { SpectraVoiceControllerValues } from "./spectraVoiceControllerValues"
export namespace SpectraVoice {
  // Intentionally duplicated enums - see also spectraVoiceEnums.ts
  // (TypeScript does not allow exporting imported enums from inside a namespace)
  export enum Mode {
    // noinspection JSUnusedGlobalSymbols
    Hq = 0,
    HqMono = 1,
    Lq = 2,
    LqMono = 3,
    HqSpline = 4,
  }
  export enum HarmonicType {
    // noinspection JSUnusedGlobalSymbols
    Hsin = 0,
    Rect = 1,
    Org1 = 2,
    Org2 = 3,
    Org3 = 4,
    Org4 = 5,
    Sin = 6,
    Random = 7,
    Triangle1 = 8,
    Triangle2 = 9,
    Overtones1 = 10,
    Overtones2 = 11,
    Overtones3 = 12,
    Overtones4 = 13,
    Overtones1Plus_ = 14,
    Overtones2Plus_ = 15,
    Overtones3Plus_ = 16,
    Overtones4Plus_ = 17,
    Metal = 18,
  }
  export enum CtlNum {
    Volume = 1,
    Panning = 2,
    Attack = 3,
    Release = 4,
    Polyphony = 5,
    Mode = 6,
    Sustain = 7,
    SpectrumResolution = 8,
    Harmonic = 9,
    HFreq = 10,
    HVolume = 11,
    HWidth = 12,
    HType = 13,
  }
  interface SpectraVoiceControllerMidiMaps extends ControllerMidiMaps {
    volume: ControllerMidiMap
    panning: ControllerMidiMap
    attack: ControllerMidiMap
    release: ControllerMidiMap
    polyphony: ControllerMidiMap
    mode: ControllerMidiMap
    sustain: ControllerMidiMap
    spectrumResolution: ControllerMidiMap
    harmonic: ControllerMidiMap
    hFreq: ControllerMidiMap
    hVolume: ControllerMidiMap
    hWidth: ControllerMidiMap
    hType: ControllerMidiMap
  }
  interface SpectraVoiceOptionValues extends OptionValues {}
  class SpectraVoiceOptions implements Options {
    constructor(readonly optionValues: SpectraVoiceOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "SpectraVoice"
    flags = 0x49
    readonly typeName = "SpectraVoice"
    readonly controllerSetters = [
      (val: number) => {
        this.controllerValues.volume = val
      },
      (val: number) => {
        this.controllerValues.panning = val
      },
      (val: number) => {
        this.controllerValues.attack = val
      },
      (val: number) => {
        this.controllerValues.release = val
      },
      (val: number) => {
        this.controllerValues.polyphony = val
      },
      (val: number) => {
        this.controllerValues.mode = val
      },
      (val: number) => {
        this.controllerValues.sustain = Boolean(val)
      },
      (val: number) => {
        this.controllerValues.spectrumResolution = val
      },
      (val: number) => {
        this.controllerValues.harmonic = val
      },
      (val: number) => {
        this.controllerValues.hFreq = val
      },
      (val: number) => {
        this.controllerValues.hVolume = val
      },
      (val: number) => {
        this.controllerValues.hWidth = val
      },
      (val: number) => {
        this.controllerValues.hType = val
      },
    ]
    readonly controllerValues: SpectraVoiceControllerValues = {
      volume: 128,
      panning: 0,
      attack: 1,
      release: 512,
      polyphony: 8,
      mode: Mode.HqSpline,
      sustain: true,
      spectrumResolution: 1,
      harmonic: 0,
      hFreq: 1098,
      hVolume: 255,
      hWidth: 3,
      hType: HarmonicType.Hsin,
    }
    readonly controllers: SpectraVoiceControllers = new SpectraVoiceControllers(
      this,
      this.controllerValues
    )
    readonly c = this.controllers
    readonly midiMaps: SpectraVoiceControllerMidiMaps = {
      volume: new ControllerMidiMap(),
      panning: new ControllerMidiMap(),
      attack: new ControllerMidiMap(),
      release: new ControllerMidiMap(),
      polyphony: new ControllerMidiMap(),
      mode: new ControllerMidiMap(),
      sustain: new ControllerMidiMap(),
      spectrumResolution: new ControllerMidiMap(),
      harmonic: new ControllerMidiMap(),
      hFreq: new ControllerMidiMap(),
      hVolume: new ControllerMidiMap(),
      hWidth: new ControllerMidiMap(),
      hType: new ControllerMidiMap(),
    }
    readonly optionValues: SpectraVoiceOptionValues = {}
    readonly options: SpectraVoiceOptions = new SpectraVoiceOptions(this.optionValues)
    readonly o = this.options
    behavior?: SpectraVoiceBehavior
    constructor() {
      super()
      this.behavior = new SpectraVoiceBehavior(this)
    }
    attachTo(project: Project): AttachedModule {
      return super.attachTo(project) as AttachedModule
    }
    setRawControllerValue(ctlNum: number, value: number) {
      const { controllerValues: cv } = this
      switch (ctlNum) {
        case 1:
          cv.volume = value
          break
        case 2:
          cv.panning = value
          break
        case 3:
          cv.attack = value
          break
        case 4:
          cv.release = value
          break
        case 5:
          cv.polyphony = value
          break
        case 6:
          cv.mode = value
          break
        case 7:
          cv.sustain = Boolean(value)
          break
        case 8:
          cv.spectrumResolution = value
          break
        case 9:
          cv.harmonic = value
          break
        case 10:
          cv.hFreq = value
          break
        case 11:
          cv.hVolume = value
          break
        case 12:
          cv.hWidth = value
          break
        case 13:
          cv.hType = value
          break
      }
    }
    *rawControllerValues(): Generator<number> {
      const { controllerValues: cv } = this
      yield cv.volume
      yield cv.panning
      yield cv.attack
      yield cv.release
      yield cv.polyphony
      yield cv.mode
      yield Number(cv.sustain)
      yield cv.spectrumResolution
      yield cv.harmonic
      yield cv.hFreq
      yield cv.hVolume
      yield cv.hWidth
      yield cv.hType
    }
    setMidiMaps(midiMaps: MidiMap[]) {
      this.midiMaps.volume = midiMaps[0] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.panning = midiMaps[1] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.attack = midiMaps[2] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.release = midiMaps[3] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.polyphony = midiMaps[4] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.mode = midiMaps[5] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.sustain = midiMaps[6] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.spectrumResolution = midiMaps[7] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.harmonic = midiMaps[8] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.hFreq = midiMaps[9] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.hVolume = midiMaps[10] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.hWidth = midiMaps[11] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.hType = midiMaps[12] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
    }
    midiMapsArray(): MidiMap[] {
      const a: MidiMap[] = []
      a.push(this.midiMaps.volume)
      a.push(this.midiMaps.panning)
      a.push(this.midiMaps.attack)
      a.push(this.midiMaps.release)
      a.push(this.midiMaps.polyphony)
      a.push(this.midiMaps.mode)
      a.push(this.midiMaps.sustain)
      a.push(this.midiMaps.spectrumResolution)
      a.push(this.midiMaps.harmonic)
      a.push(this.midiMaps.hFreq)
      a.push(this.midiMaps.hVolume)
      a.push(this.midiMaps.hWidth)
      a.push(this.midiMaps.hType)
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
