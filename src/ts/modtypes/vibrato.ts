/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { MidiMap, ControllerMidiMap, ControllerMidiMaps } from "../controllerMidiMap"
import { Project } from "../project"
import { ModuleBase } from "./moduleBase"
import { ModuleType, OptionValues, Options } from "./moduleType"
import { VibratoBehavior } from "./vibratoBehavior"
import { VibratoControllers } from "./vibratoControllers"
import { VibratoControllerValues } from "./vibratoControllerValues"
export namespace Vibrato {
  // Intentionally duplicated enums - see also vibratoEnums.ts
  // (TypeScript does not allow exporting imported enums from inside a namespace)
  export enum Channels {
    // noinspection JSUnusedGlobalSymbols
    Stereo = 0,
    Mono = 1,
  }
  export enum FrequencyUnit {
    // noinspection JSUnusedGlobalSymbols
    Hz_64 = 0,
    Ms = 1,
    Hz = 2,
    Tick = 3,
    Line = 4,
    Line_2 = 5,
    Line_3 = 6,
  }
  export enum CtlNum {
    Volume = 1,
    Amplitude = 2,
    Freq = 3,
    Channels = 4,
    SetPhase = 5,
    FrequencyUnit = 6,
    ExponentialAmplitude = 7,
  }
  interface VibratoControllerMidiMaps extends ControllerMidiMaps {
    volume: ControllerMidiMap
    amplitude: ControllerMidiMap
    freq: ControllerMidiMap
    channels: ControllerMidiMap
    setPhase: ControllerMidiMap
    frequencyUnit: ControllerMidiMap
    exponentialAmplitude: ControllerMidiMap
  }
  interface VibratoOptionValues extends OptionValues {}
  class VibratoOptions implements Options {
    constructor(readonly optionValues: VibratoOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "Vibrato"
    flags = 1105
    readonly typeName = "Vibrato"
    readonly controllerSetters = [
      (val: number) => {
        this.controllerValues.volume = val
      },
      (val: number) => {
        this.controllerValues.amplitude = val
      },
      (val: number) => {
        this.controllerValues.freq = val
      },
      (val: number) => {
        this.controllerValues.channels = val
      },
      (val: number) => {
        this.controllerValues.setPhase = val
      },
      (val: number) => {
        this.controllerValues.frequencyUnit = val
      },
      (val: number) => {
        this.controllerValues.exponentialAmplitude = Boolean(val)
      },
    ]
    readonly controllerValues: VibratoControllerValues = {
      volume: 256,
      amplitude: 16,
      freq: 256,
      channels: Channels.Stereo,
      setPhase: 0,
      frequencyUnit: FrequencyUnit.Hz_64,
      exponentialAmplitude: false,
    }
    readonly controllers: VibratoControllers = new VibratoControllers(
      this,
      this.controllerValues
    )
    readonly c = this.controllers
    readonly midiMaps: VibratoControllerMidiMaps = {
      volume: new ControllerMidiMap(),
      amplitude: new ControllerMidiMap(),
      freq: new ControllerMidiMap(),
      channels: new ControllerMidiMap(),
      setPhase: new ControllerMidiMap(),
      frequencyUnit: new ControllerMidiMap(),
      exponentialAmplitude: new ControllerMidiMap(),
    }
    readonly optionValues: VibratoOptionValues = {}
    readonly options: VibratoOptions = new VibratoOptions(this.optionValues)
    readonly o = this.options
    behavior?: VibratoBehavior
    constructor() {
      super()
      this.behavior = new VibratoBehavior(this)
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
          cv.amplitude = value
          break
        case 3:
          cv.freq = value
          break
        case 4:
          cv.channels = value
          break
        case 5:
          cv.setPhase = value
          break
        case 6:
          cv.frequencyUnit = value
          break
        case 7:
          cv.exponentialAmplitude = Boolean(value)
          break
      }
    }
    *rawControllerValues(): Generator<number> {
      const { controllerValues: cv } = this
      yield cv.volume
      yield cv.amplitude
      yield cv.freq
      yield cv.channels
      yield cv.setPhase
      yield cv.frequencyUnit
      yield Number(cv.exponentialAmplitude)
    }
    setMidiMaps(midiMaps: MidiMap[]) {
      this.midiMaps.volume = midiMaps[0] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.amplitude = midiMaps[1] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.freq = midiMaps[2] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.channels = midiMaps[3] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.setPhase = midiMaps[4] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.frequencyUnit = midiMaps[5] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.exponentialAmplitude = midiMaps[6] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
    }
    midiMapsArray(): MidiMap[] {
      const a: MidiMap[] = []
      a.push(this.midiMaps.volume)
      a.push(this.midiMaps.amplitude)
      a.push(this.midiMaps.freq)
      a.push(this.midiMaps.channels)
      a.push(this.midiMaps.setPhase)
      a.push(this.midiMaps.frequencyUnit)
      a.push(this.midiMaps.exponentialAmplitude)
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
