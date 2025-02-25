/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { MidiMap, ControllerMidiMap, ControllerMidiMaps } from "../controllerMidiMap"
import { Project } from "../project"
import { ModuleBase } from "./moduleBase"
import { ModuleType, OptionValues, Options } from "./moduleType"
import { GlideBehavior } from "./glideBehavior"
import { GlideControllers } from "./glideControllers"
import { GlideControllerValues } from "./glideControllerValues"
export namespace Glide {
  export enum CtlNum {
    Response = 1,
    SampleRate = 2,
    ResetOnFirstNote = 3,
    Polyphony = 4,
    Pitch = 5,
    PitchScale = 6,
    Reset = 7,
    Octave = 8,
    FreqMultiply = 9,
    FreqDivide = 10,
  }
  interface GlideControllerMidiMaps extends ControllerMidiMaps {
    response: ControllerMidiMap
    sampleRate: ControllerMidiMap
    resetOnFirstNote: ControllerMidiMap
    polyphony: ControllerMidiMap
    pitch: ControllerMidiMap
    pitchScale: ControllerMidiMap
    reset: ControllerMidiMap
    octave: ControllerMidiMap
    freqMultiply: ControllerMidiMap
    freqDivide: ControllerMidiMap
  }
  interface GlideOptionValues extends OptionValues {}
  class GlideOptions implements Options {
    constructor(readonly optionValues: GlideOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "Glide"
    flags = 0x60049
    readonly typeName = "Glide"
    readonly controllerSetters = [
      (val: number) => {
        this.controllerValues.response = val
      },
      (val: number) => {
        this.controllerValues.sampleRate = val
      },
      (val: number) => {
        this.controllerValues.resetOnFirstNote = Boolean(val)
      },
      (val: number) => {
        this.controllerValues.polyphony = Boolean(val)
      },
      (val: number) => {
        this.controllerValues.pitch = val
      },
      (val: number) => {
        this.controllerValues.pitchScale = val
      },
      (val: number) => {
        this.controllerValues.reset = Boolean(val)
      },
      (val: number) => {
        this.controllerValues.octave = val
      },
      (val: number) => {
        this.controllerValues.freqMultiply = val
      },
      (val: number) => {
        this.controllerValues.freqDivide = val
      },
    ]
    readonly controllerValues: GlideControllerValues = {
      response: 500,
      sampleRate: 150,
      resetOnFirstNote: false,
      polyphony: true,
      pitch: 0,
      pitchScale: 100,
      reset: false,
      octave: 0,
      freqMultiply: 1,
      freqDivide: 1,
    }
    readonly controllers: GlideControllers = new GlideControllers(
      this,
      this.controllerValues
    )
    readonly c = this.controllers
    readonly midiMaps: GlideControllerMidiMaps = {
      response: new ControllerMidiMap(),
      sampleRate: new ControllerMidiMap(),
      resetOnFirstNote: new ControllerMidiMap(),
      polyphony: new ControllerMidiMap(),
      pitch: new ControllerMidiMap(),
      pitchScale: new ControllerMidiMap(),
      reset: new ControllerMidiMap(),
      octave: new ControllerMidiMap(),
      freqMultiply: new ControllerMidiMap(),
      freqDivide: new ControllerMidiMap(),
    }
    readonly optionValues: GlideOptionValues = {}
    readonly options: GlideOptions = new GlideOptions(this.optionValues)
    readonly o = this.options
    behavior?: GlideBehavior
    constructor() {
      super()
      this.behavior = new GlideBehavior(this)
    }
    attachTo(project: Project): AttachedModule {
      return super.attachTo(project) as AttachedModule
    }
    setRawControllerValue(ctlNum: number, value: number) {
      const { controllerValues: cv } = this
      switch (ctlNum) {
        case 1:
          cv.response = value
          break
        case 2:
          cv.sampleRate = value
          break
        case 3:
          cv.resetOnFirstNote = Boolean(value)
          break
        case 4:
          cv.polyphony = Boolean(value)
          break
        case 5:
          cv.pitch = value
          break
        case 6:
          cv.pitchScale = value
          break
        case 7:
          cv.reset = Boolean(value)
          break
        case 8:
          cv.octave = value
          break
        case 9:
          cv.freqMultiply = value
          break
        case 10:
          cv.freqDivide = value
          break
      }
    }
    *rawControllerValues(): Generator<number> {
      const { controllerValues: cv } = this
      yield cv.response
      yield cv.sampleRate
      yield Number(cv.resetOnFirstNote)
      yield Number(cv.polyphony)
      yield cv.pitch
      yield cv.pitchScale
      yield Number(cv.reset)
      yield cv.octave
      yield cv.freqMultiply
      yield cv.freqDivide
    }
    setMidiMaps(midiMaps: MidiMap[]) {
      this.midiMaps.response = midiMaps[0] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.sampleRate = midiMaps[1] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.resetOnFirstNote = midiMaps[2] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.polyphony = midiMaps[3] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.pitch = midiMaps[4] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.pitchScale = midiMaps[5] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.reset = midiMaps[6] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.octave = midiMaps[7] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.freqMultiply = midiMaps[8] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.freqDivide = midiMaps[9] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
    }
    midiMapsArray(): MidiMap[] {
      const a: MidiMap[] = []
      a.push(this.midiMaps.response)
      a.push(this.midiMaps.sampleRate)
      a.push(this.midiMaps.resetOnFirstNote)
      a.push(this.midiMaps.polyphony)
      a.push(this.midiMaps.pitch)
      a.push(this.midiMaps.pitchScale)
      a.push(this.midiMaps.reset)
      a.push(this.midiMaps.octave)
      a.push(this.midiMaps.freqMultiply)
      a.push(this.midiMaps.freqDivide)
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
