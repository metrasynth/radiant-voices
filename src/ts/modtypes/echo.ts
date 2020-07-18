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
import { EchoBehavior } from "./echoBehavior"
export namespace Echo {
  export const enum Channels {
    // noinspection JSUnusedGlobalSymbols
    Mono = 0,
    Stereo = 1,
  }
  export const enum DelayUnit {
    // noinspection JSUnusedGlobalSymbols
    Sec_256 = 0,
    Ms = 1,
    Hz = 2,
    Tick = 3,
    Line = 4,
    Line_2 = 5,
    Line_3 = 6,
  }
  interface EchoControllerValues extends ControllerValues {
    dry: number
    wet: number
    feedback: number
    delay: number
    channels: Channels
    delayUnit: DelayUnit
  }
  class EchoControllers implements Controllers {
    constructor(readonly controllerValues: EchoControllerValues) {}
    // noinspection JSUnusedGlobalSymbols
    get dry(): number {
      return this.controllerValues.dry
    }
    // noinspection JSUnusedGlobalSymbols
    set dry(newValue: number) {
      const { controllerValues } = this
      newValue = Math.min(Math.max(newValue, 0), 256)
      controllerValues.dry = newValue
    }
    // noinspection JSUnusedGlobalSymbols
    get wet(): number {
      return this.controllerValues.wet
    }
    // noinspection JSUnusedGlobalSymbols
    set wet(newValue: number) {
      const { controllerValues } = this
      newValue = Math.min(Math.max(newValue, 0), 256)
      controllerValues.wet = newValue
    }
    // noinspection JSUnusedGlobalSymbols
    get feedback(): number {
      return this.controllerValues.feedback
    }
    // noinspection JSUnusedGlobalSymbols
    set feedback(newValue: number) {
      const { controllerValues } = this
      newValue = Math.min(Math.max(newValue, 0), 256)
      controllerValues.feedback = newValue
    }
    // noinspection JSUnusedGlobalSymbols
    get delay(): number {
      return this.controllerValues.delay
    }
    // noinspection JSUnusedGlobalSymbols
    set delay(newValue: number) {
      const { controllerValues } = this
      newValue = Math.min(Math.max(newValue, 0), 256)
      controllerValues.delay = newValue
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
    get delayUnit(): DelayUnit {
      return this.controllerValues.delayUnit
    }
    // noinspection JSUnusedGlobalSymbols
    set delayUnit(newValue: DelayUnit) {
      const { controllerValues } = this
      controllerValues.delayUnit = newValue
    }
  }
  interface EchoControllerMidiMaps extends ControllerMidiMaps {
    dry: ControllerMidiMap
    wet: ControllerMidiMap
    feedback: ControllerMidiMap
    delay: ControllerMidiMap
    channels: ControllerMidiMap
    delayUnit: ControllerMidiMap
  }
  interface EchoOptionValues extends OptionValues {}
  class EchoOptions implements Options {
    constructor(readonly optionValues: EchoOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "Echo"
    flags = 1105
    readonly typeName = "Echo"
    readonly controllerSetters = [
      (val: number) => {
        this.controllerValues.dry = val
      },
      (val: number) => {
        this.controllerValues.wet = val
      },
      (val: number) => {
        this.controllerValues.feedback = val
      },
      (val: number) => {
        this.controllerValues.delay = val
      },
      (val: number) => {
        this.controllerValues.channels = val
      },
      (val: number) => {
        this.controllerValues.delayUnit = val
      },
    ]
    readonly controllerValues: EchoControllerValues = {
      dry: 256,
      wet: 128,
      feedback: 128,
      delay: 256,
      channels: Channels.Stereo,
      delayUnit: DelayUnit.Sec_256,
    }
    readonly controllers: EchoControllers = new EchoControllers(this.controllerValues)
    readonly c = this.controllers
    readonly midiMaps: EchoControllerMidiMaps = {
      dry: new ControllerMidiMap(),
      wet: new ControllerMidiMap(),
      feedback: new ControllerMidiMap(),
      delay: new ControllerMidiMap(),
      channels: new ControllerMidiMap(),
      delayUnit: new ControllerMidiMap(),
    }
    readonly optionValues: EchoOptionValues = {}
    readonly options: EchoOptions = new EchoOptions(this.optionValues)
    readonly o = this.options
    behavior?: EchoBehavior
    constructor() {
      super()
      this.behavior = new EchoBehavior(this)
    }
    attachTo(project: Project): Module {
      return super.attachTo(project) as Module
    }
    *rawControllerValues(): Generator<number> {
      const { controllerValues: cv } = this
      yield cv.dry
      yield cv.wet
      yield cv.feedback
      yield cv.delay
      yield cv.channels
      yield cv.delayUnit
    }
    setMidiMaps(midiMaps: MidiMap[]) {
      this.midiMaps.dry = midiMaps[0]
      this.midiMaps.wet = midiMaps[1]
      this.midiMaps.feedback = midiMaps[2]
      this.midiMaps.delay = midiMaps[3]
      this.midiMaps.channels = midiMaps[4]
      this.midiMaps.delayUnit = midiMaps[5]
    }
    midiMapsArray(): MidiMap[] {
      const a: MidiMap[] = []
      a.push(this.midiMaps.dry)
      a.push(this.midiMaps.wet)
      a.push(this.midiMaps.feedback)
      a.push(this.midiMaps.delay)
      a.push(this.midiMaps.channels)
      a.push(this.midiMaps.delayUnit)
      return a
    }
  }
}
