/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { MidiMap, ControllerMidiMap, ControllerMidiMaps } from "../controllerMidiMap"
import { Project } from "../project"
import { ModuleBase } from "./moduleBase"
import {
  ControllerValues,
  Controllers,
  ModuleType,
  OptionValues,
  Options,
} from "./moduleType"
import { VibratoBehavior } from "./vibratoBehavior"
export namespace Vibrato {
  export const enum Channels {
    // noinspection JSUnusedGlobalSymbols
    Stereo = 0,
    Mono = 1,
  }
  export const enum FrequencyUnit {
    // noinspection JSUnusedGlobalSymbols
    Hz_64 = 0,
    Ms = 1,
    Hz = 2,
    Tick = 3,
    Line = 4,
    Line_2 = 5,
    Line_3 = 6,
  }
  interface VibratoControllerValues extends ControllerValues {
    volume: number
    amplitude: number
    freq: number
    channels: Channels
    setPhase: number
    frequencyUnit: FrequencyUnit
    exponentialAmplitude: boolean
  }
  class VibratoControllers implements Controllers {
    constructor(readonly controllerValues: VibratoControllerValues) {}
    // noinspection JSUnusedGlobalSymbols
    get volume(): number {
      return this.controllerValues.volume
    }
    // noinspection JSUnusedGlobalSymbols
    set volume(newValue: number) {
      const { controllerValues } = this
      newValue = Math.min(Math.max(newValue, 0), 256)
      controllerValues.volume = newValue
    }
    // noinspection JSUnusedGlobalSymbols
    get amplitude(): number {
      return this.controllerValues.amplitude
    }
    // noinspection JSUnusedGlobalSymbols
    set amplitude(newValue: number) {
      const { controllerValues } = this
      newValue = Math.min(Math.max(newValue, 0), 256)
      controllerValues.amplitude = newValue
    }
    // noinspection JSUnusedGlobalSymbols
    get freq(): number {
      return this.controllerValues.freq
    }
    // noinspection JSUnusedGlobalSymbols
    set freq(newValue: number) {
      const { controllerValues } = this
      switch (this.controllerValues.frequencyUnit) {
        case FrequencyUnit.Hz_64:
          newValue = Math.min(Math.max(newValue, 1), 2048)
          break
        case FrequencyUnit.Ms:
          newValue = Math.min(Math.max(newValue, 1), 4000)
          break
        case FrequencyUnit.Hz:
          newValue = Math.min(Math.max(newValue, 1), 16384)
          break
        case FrequencyUnit.Tick:
          newValue = Math.min(Math.max(newValue, 1), 2048)
          break
        case FrequencyUnit.Line:
          newValue = Math.min(Math.max(newValue, 1), 2048)
          break
        case FrequencyUnit.Line_2:
          newValue = Math.min(Math.max(newValue, 1), 2048)
          break
        case FrequencyUnit.Line_3:
          newValue = Math.min(Math.max(newValue, 1), 2048)
          break
      }
      controllerValues.freq = newValue
    }
    // noinspection JSUnusedGlobalSymbols
    get channels(): Channels {
      return this.controllerValues.channels
    }
    // noinspection JSUnusedGlobalSymbols
    set channels(newValue: Channels) {
      const { controllerValues } = this
      controllerValues.channels = newValue
    }
    // noinspection JSUnusedGlobalSymbols
    get setPhase(): number {
      return this.controllerValues.setPhase
    }
    // noinspection JSUnusedGlobalSymbols
    set setPhase(newValue: number) {
      const { controllerValues } = this
      newValue = Math.min(Math.max(newValue, 0), 256)
      controllerValues.setPhase = newValue
    }
    // noinspection JSUnusedGlobalSymbols
    get frequencyUnit(): FrequencyUnit {
      return this.controllerValues.frequencyUnit
    }
    // noinspection JSUnusedGlobalSymbols
    set frequencyUnit(newValue: FrequencyUnit) {
      const { controllerValues } = this
      controllerValues.frequencyUnit = newValue
      this.freq = this.freq
    }
    // noinspection JSUnusedGlobalSymbols
    get exponentialAmplitude(): boolean {
      return this.controllerValues.exponentialAmplitude
    }
    // noinspection JSUnusedGlobalSymbols
    set exponentialAmplitude(newValue: boolean) {
      const { controllerValues } = this
      controllerValues.exponentialAmplitude = newValue
    }
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
    attachTo(project: Project): Module {
      return super.attachTo(project) as Module
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
      this.midiMaps.volume = midiMaps[0]
      this.midiMaps.amplitude = midiMaps[1]
      this.midiMaps.freq = midiMaps[2]
      this.midiMaps.channels = midiMaps[3]
      this.midiMaps.setPhase = midiMaps[4]
      this.midiMaps.frequencyUnit = midiMaps[5]
      this.midiMaps.exponentialAmplitude = midiMaps[6]
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
}
