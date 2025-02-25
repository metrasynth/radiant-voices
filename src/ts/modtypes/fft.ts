/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { MidiMap, ControllerMidiMap, ControllerMidiMaps } from "../controllerMidiMap"
import { Project } from "../project"
import { ModuleBase } from "./moduleBase"
import { ModuleType, OptionValues, Options } from "./moduleType"
import { FftBehavior } from "./fftBehavior"
import { FftControllers } from "./fftControllers"
import { FftControllerValues } from "./fftControllerValues"
export namespace Fft {
  // Intentionally duplicated enums - see also fftEnums.ts
  // (TypeScript does not allow exporting imported enums from inside a namespace)
  export enum SampleRate {
    // noinspection JSUnusedGlobalSymbols
    _8000hz = 0,
    _11025hz = 1,
    _16000hz = 2,
    _22050hz = 3,
    _32000hz = 4,
    _44100hz = 5,
    _48000hz = 6,
    _88200hz = 7,
    _96000hz = 8,
    _119200hz = 9,
  }
  export enum Channels {
    // noinspection JSUnusedGlobalSymbols
    Mono = 0,
    Stereo = 1,
  }
  export enum Buffer {
    // noinspection JSUnusedGlobalSymbols
    _64 = 0,
    _128 = 1,
    _256 = 2,
    _512 = 3,
    _1024 = 4,
    _2048 = 5,
    _4096 = 6,
    _8192 = 7,
  }
  export enum BufferOverlap {
    // noinspection JSUnusedGlobalSymbols
    _0 = 0,
    _2x = 1,
    _4x = 2,
  }
  export enum CtlNum {
    SampleRate = 1,
    Channels = 2,
    Buffer = 3,
    BufOverlap = 4,
    Feedback = 5,
    NoiseReduction = 6,
    PhaseGain = 7,
    AllPassFilter = 8,
    FrequencySpread = 9,
    RandomPhase = 10,
    RandomPhaseLite = 11,
    FreqShift = 12,
    Deform1 = 13,
    Deform2 = 14,
    HpCutoff = 15,
    LpCutoff = 16,
    Volume = 17,
  }
  interface FftControllerMidiMaps extends ControllerMidiMaps {
    sampleRate: ControllerMidiMap
    channels: ControllerMidiMap
    buffer: ControllerMidiMap
    bufOverlap: ControllerMidiMap
    feedback: ControllerMidiMap
    noiseReduction: ControllerMidiMap
    phaseGain: ControllerMidiMap
    allPassFilter: ControllerMidiMap
    frequencySpread: ControllerMidiMap
    randomPhase: ControllerMidiMap
    randomPhaseLite: ControllerMidiMap
    freqShift: ControllerMidiMap
    deform1: ControllerMidiMap
    deform2: ControllerMidiMap
    hpCutoff: ControllerMidiMap
    lpCutoff: ControllerMidiMap
    volume: ControllerMidiMap
  }
  interface FftOptionValues extends OptionValues {}
  class FftOptions implements Options {
    constructor(readonly optionValues: FftOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "FFT"
    flags = 0x51
    readonly typeName = "FFT"
    readonly controllerSetters = [
      (val: number) => {
        this.controllerValues.sampleRate = val
      },
      (val: number) => {
        this.controllerValues.channels = val
      },
      (val: number) => {
        this.controllerValues.buffer = val
      },
      (val: number) => {
        this.controllerValues.bufOverlap = val
      },
      (val: number) => {
        this.controllerValues.feedback = val
      },
      (val: number) => {
        this.controllerValues.noiseReduction = val
      },
      (val: number) => {
        this.controllerValues.phaseGain = val
      },
      (val: number) => {
        this.controllerValues.allPassFilter = val
      },
      (val: number) => {
        this.controllerValues.frequencySpread = val
      },
      (val: number) => {
        this.controllerValues.randomPhase = val
      },
      (val: number) => {
        this.controllerValues.randomPhaseLite = val
      },
      (val: number) => {
        this.controllerValues.freqShift = val
      },
      (val: number) => {
        this.controllerValues.deform1 = val
      },
      (val: number) => {
        this.controllerValues.deform2 = val
      },
      (val: number) => {
        this.controllerValues.hpCutoff = val
      },
      (val: number) => {
        this.controllerValues.lpCutoff = val
      },
      (val: number) => {
        this.controllerValues.volume = val
      },
    ]
    readonly controllerValues: FftControllerValues = {
      sampleRate: SampleRate._44100hz,
      channels: Channels.Mono,
      buffer: Buffer._1024,
      bufOverlap: BufferOverlap._2x,
      feedback: 0,
      noiseReduction: 0,
      phaseGain: 16384,
      allPassFilter: 0,
      frequencySpread: 0,
      randomPhase: 0,
      randomPhaseLite: 0,
      freqShift: 0,
      deform1: 0,
      deform2: 0,
      hpCutoff: 0,
      lpCutoff: 32768,
      volume: 32768,
    }
    readonly controllers: FftControllers = new FftControllers(
      this,
      this.controllerValues
    )
    readonly c = this.controllers
    readonly midiMaps: FftControllerMidiMaps = {
      sampleRate: new ControllerMidiMap(),
      channels: new ControllerMidiMap(),
      buffer: new ControllerMidiMap(),
      bufOverlap: new ControllerMidiMap(),
      feedback: new ControllerMidiMap(),
      noiseReduction: new ControllerMidiMap(),
      phaseGain: new ControllerMidiMap(),
      allPassFilter: new ControllerMidiMap(),
      frequencySpread: new ControllerMidiMap(),
      randomPhase: new ControllerMidiMap(),
      randomPhaseLite: new ControllerMidiMap(),
      freqShift: new ControllerMidiMap(),
      deform1: new ControllerMidiMap(),
      deform2: new ControllerMidiMap(),
      hpCutoff: new ControllerMidiMap(),
      lpCutoff: new ControllerMidiMap(),
      volume: new ControllerMidiMap(),
    }
    readonly optionValues: FftOptionValues = {}
    readonly options: FftOptions = new FftOptions(this.optionValues)
    readonly o = this.options
    behavior?: FftBehavior
    constructor() {
      super()
      this.behavior = new FftBehavior(this)
    }
    attachTo(project: Project): AttachedModule {
      return super.attachTo(project) as AttachedModule
    }
    setRawControllerValue(ctlNum: number, value: number) {
      const { controllerValues: cv } = this
      switch (ctlNum) {
        case 1:
          cv.sampleRate = value
          break
        case 2:
          cv.channels = value
          break
        case 3:
          cv.buffer = value
          break
        case 4:
          cv.bufOverlap = value
          break
        case 5:
          cv.feedback = value
          break
        case 6:
          cv.noiseReduction = value
          break
        case 7:
          cv.phaseGain = value
          break
        case 8:
          cv.allPassFilter = value
          break
        case 9:
          cv.frequencySpread = value
          break
        case 10:
          cv.randomPhase = value
          break
        case 11:
          cv.randomPhaseLite = value
          break
        case 12:
          cv.freqShift = value
          break
        case 13:
          cv.deform1 = value
          break
        case 14:
          cv.deform2 = value
          break
        case 15:
          cv.hpCutoff = value
          break
        case 16:
          cv.lpCutoff = value
          break
        case 17:
          cv.volume = value
          break
      }
    }
    *rawControllerValues(): Generator<number> {
      const { controllerValues: cv } = this
      yield cv.sampleRate
      yield cv.channels
      yield cv.buffer
      yield cv.bufOverlap
      yield cv.feedback
      yield cv.noiseReduction
      yield cv.phaseGain
      yield cv.allPassFilter
      yield cv.frequencySpread
      yield cv.randomPhase
      yield cv.randomPhaseLite
      yield cv.freqShift
      yield cv.deform1
      yield cv.deform2
      yield cv.hpCutoff
      yield cv.lpCutoff
      yield cv.volume
    }
    setMidiMaps(midiMaps: MidiMap[]) {
      this.midiMaps.sampleRate = midiMaps[0] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.channels = midiMaps[1] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.buffer = midiMaps[2] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.bufOverlap = midiMaps[3] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.feedback = midiMaps[4] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.noiseReduction = midiMaps[5] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.phaseGain = midiMaps[6] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.allPassFilter = midiMaps[7] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.frequencySpread = midiMaps[8] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.randomPhase = midiMaps[9] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.randomPhaseLite = midiMaps[10] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.freqShift = midiMaps[11] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.deform1 = midiMaps[12] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.deform2 = midiMaps[13] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.hpCutoff = midiMaps[14] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.lpCutoff = midiMaps[15] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.volume = midiMaps[16] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
    }
    midiMapsArray(): MidiMap[] {
      const a: MidiMap[] = []
      a.push(this.midiMaps.sampleRate)
      a.push(this.midiMaps.channels)
      a.push(this.midiMaps.buffer)
      a.push(this.midiMaps.bufOverlap)
      a.push(this.midiMaps.feedback)
      a.push(this.midiMaps.noiseReduction)
      a.push(this.midiMaps.phaseGain)
      a.push(this.midiMaps.allPassFilter)
      a.push(this.midiMaps.frequencySpread)
      a.push(this.midiMaps.randomPhase)
      a.push(this.midiMaps.randomPhaseLite)
      a.push(this.midiMaps.freqShift)
      a.push(this.midiMaps.deform1)
      a.push(this.midiMaps.deform2)
      a.push(this.midiMaps.hpCutoff)
      a.push(this.midiMaps.lpCutoff)
      a.push(this.midiMaps.volume)
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
