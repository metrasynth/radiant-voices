/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { MidiMap, ControllerMidiMap, ControllerMidiMaps } from "../controllerMidiMap"
import { Project } from "../project"
import { ModuleBase } from "./moduleBase"
import { ModuleType, OptionValues, Options } from "./moduleType"
import { LfoBehavior } from "./lfoBehavior"
import { LfoControllers } from "./lfoControllers"
import { LfoControllerValues } from "./lfoControllerValues"
export namespace Lfo {
  // Intentionally duplicated enums - see also lfoEnums.ts
  // (TypeScript does not allow exporting imported enums from inside a namespace)
  export enum Type {
    // noinspection JSUnusedGlobalSymbols
    Amplitude = 0,
    Panning = 1,
  }
  export enum Waveform {
    // noinspection JSUnusedGlobalSymbols
    Sin = 0,
    Square = 1,
    Sin2 = 2,
    Saw = 3,
    Saw2 = 4,
    Random = 5,
    Triangle = 6,
    RandomInterpolated = 7,
  }
  export enum Channels {
    // noinspection JSUnusedGlobalSymbols
    Stereo = 0,
    Mono = 1,
  }
  export enum FrequencyUnit {
    // noinspection JSUnusedGlobalSymbols
    HzDiv_64 = 0,
    Ms = 1,
    Hz = 2,
    Tick = 3,
    Line = 4,
    LineDiv_2 = 5,
    LineDiv_3 = 6,
  }
  export enum SmoothTransitions {
    // noinspection JSUnusedGlobalSymbols
    Off = 0,
    Waveform = 1,
  }
  export enum CtlNum {
    Volume = 1,
    Type = 2,
    Amplitude = 3,
    Freq = 4,
    Waveform = 5,
    SetPhase = 6,
    Channels = 7,
    FrequencyUnit = 8,
    DutyCycle = 9,
    Generator = 10,
    FreqScale = 11,
    SmoothTransitions = 12,
  }
  interface LfoControllerMidiMaps extends ControllerMidiMaps {
    volume: ControllerMidiMap
    type: ControllerMidiMap
    amplitude: ControllerMidiMap
    freq: ControllerMidiMap
    waveform: ControllerMidiMap
    setPhase: ControllerMidiMap
    channels: ControllerMidiMap
    frequencyUnit: ControllerMidiMap
    dutyCycle: ControllerMidiMap
    generator: ControllerMidiMap
    freqScale: ControllerMidiMap
    smoothTransitions: ControllerMidiMap
  }
  interface LfoOptionValues extends OptionValues {}
  class LfoOptions implements Options {
    constructor(readonly optionValues: LfoOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "LFO"
    flags = 0x451
    readonly typeName = "LFO"
    readonly controllerSetters = [
      (val: number) => {
        this.controllerValues.volume = val
      },
      (val: number) => {
        this.controllerValues.type = val
      },
      (val: number) => {
        this.controllerValues.amplitude = val
      },
      (val: number) => {
        this.controllerValues.freq = val
      },
      (val: number) => {
        this.controllerValues.waveform = val
      },
      (val: number) => {
        this.controllerValues.setPhase = val
      },
      (val: number) => {
        this.controllerValues.channels = val
      },
      (val: number) => {
        this.controllerValues.frequencyUnit = val
      },
      (val: number) => {
        this.controllerValues.dutyCycle = val
      },
      (val: number) => {
        this.controllerValues.generator = Boolean(val)
      },
      (val: number) => {
        this.controllerValues.freqScale = val
      },
      (val: number) => {
        this.controllerValues.smoothTransitions = val
      },
    ]
    readonly controllerValues: LfoControllerValues = {
      volume: 256,
      type: Type.Amplitude,
      amplitude: 256,
      freq: 256,
      waveform: Waveform.Sin,
      setPhase: 0,
      channels: Channels.Stereo,
      frequencyUnit: FrequencyUnit.HzDiv_64,
      dutyCycle: 128,
      generator: false,
      freqScale: 100,
      smoothTransitions: SmoothTransitions.Waveform,
    }
    readonly controllers: LfoControllers = new LfoControllers(
      this,
      this.controllerValues
    )
    readonly c = this.controllers
    readonly midiMaps: LfoControllerMidiMaps = {
      volume: new ControllerMidiMap(),
      type: new ControllerMidiMap(),
      amplitude: new ControllerMidiMap(),
      freq: new ControllerMidiMap(),
      waveform: new ControllerMidiMap(),
      setPhase: new ControllerMidiMap(),
      channels: new ControllerMidiMap(),
      frequencyUnit: new ControllerMidiMap(),
      dutyCycle: new ControllerMidiMap(),
      generator: new ControllerMidiMap(),
      freqScale: new ControllerMidiMap(),
      smoothTransitions: new ControllerMidiMap(),
    }
    readonly optionValues: LfoOptionValues = {}
    readonly options: LfoOptions = new LfoOptions(this.optionValues)
    readonly o = this.options
    behavior?: LfoBehavior
    constructor() {
      super()
      this.behavior = new LfoBehavior(this)
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
          cv.type = value
          break
        case 3:
          cv.amplitude = value
          break
        case 4:
          cv.freq = value
          break
        case 5:
          cv.waveform = value
          break
        case 6:
          cv.setPhase = value
          break
        case 7:
          cv.channels = value
          break
        case 8:
          cv.frequencyUnit = value
          break
        case 9:
          cv.dutyCycle = value
          break
        case 10:
          cv.generator = Boolean(value)
          break
        case 11:
          cv.freqScale = value
          break
        case 12:
          cv.smoothTransitions = value
          break
      }
    }
    *rawControllerValues(): Generator<number> {
      const { controllerValues: cv } = this
      yield cv.volume
      yield cv.type
      yield cv.amplitude
      yield cv.freq
      yield cv.waveform
      yield cv.setPhase
      yield cv.channels
      yield cv.frequencyUnit
      yield cv.dutyCycle
      yield Number(cv.generator)
      yield cv.freqScale
      yield cv.smoothTransitions
    }
    setMidiMaps(midiMaps: MidiMap[]) {
      this.midiMaps.volume = midiMaps[0] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.type = midiMaps[1] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.amplitude = midiMaps[2] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.freq = midiMaps[3] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.waveform = midiMaps[4] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.setPhase = midiMaps[5] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.channels = midiMaps[6] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.frequencyUnit = midiMaps[7] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.dutyCycle = midiMaps[8] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.generator = midiMaps[9] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.freqScale = midiMaps[10] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.smoothTransitions = midiMaps[11] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
    }
    midiMapsArray(): MidiMap[] {
      const a: MidiMap[] = []
      a.push(this.midiMaps.volume)
      a.push(this.midiMaps.type)
      a.push(this.midiMaps.amplitude)
      a.push(this.midiMaps.freq)
      a.push(this.midiMaps.waveform)
      a.push(this.midiMaps.setPhase)
      a.push(this.midiMaps.channels)
      a.push(this.midiMaps.frequencyUnit)
      a.push(this.midiMaps.dutyCycle)
      a.push(this.midiMaps.generator)
      a.push(this.midiMaps.freqScale)
      a.push(this.midiMaps.smoothTransitions)
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
