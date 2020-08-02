/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { MidiMap, ControllerMidiMap, ControllerMidiMaps } from "../controllerMidiMap"
import { Project } from "../project"
import { ModuleBase } from "./moduleBase"
import { ModuleType, OptionValues, Options } from "./moduleType"
import { DelayBehavior } from "./delayBehavior"
import { DelayControllers } from "./delayControllers"
import { DelayControllerValues } from "./delayControllerValues"
import { Channels as _Channels } from "./delayEnums"
import { DelayUnit as _DelayUnit } from "./delayEnums"
export namespace Delay {
  export const Channels = _Channels
  export const DelayUnit = _DelayUnit
  interface DelayControllerMidiMaps extends ControllerMidiMaps {
    dry: ControllerMidiMap
    wet: ControllerMidiMap
    delayL: ControllerMidiMap
    delayR: ControllerMidiMap
    volumeL: ControllerMidiMap
    volumeR: ControllerMidiMap
    channels: ControllerMidiMap
    inverse: ControllerMidiMap
    delayUnit: ControllerMidiMap
  }
  interface DelayOptionValues extends OptionValues {}
  class DelayOptions implements Options {
    constructor(readonly optionValues: DelayOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "Delay"
    flags = 1105
    readonly typeName = "Delay"
    readonly controllerSetters = [
      (val: number) => {
        this.controllerValues.dry = val
      },
      (val: number) => {
        this.controllerValues.wet = val
      },
      (val: number) => {
        this.controllerValues.delayL = val
      },
      (val: number) => {
        this.controllerValues.delayR = val
      },
      (val: number) => {
        this.controllerValues.volumeL = val
      },
      (val: number) => {
        this.controllerValues.volumeR = val
      },
      (val: number) => {
        this.controllerValues.channels = val
      },
      (val: number) => {
        this.controllerValues.inverse = Boolean(val)
      },
      (val: number) => {
        this.controllerValues.delayUnit = val
      },
    ]
    readonly controllerValues: DelayControllerValues = {
      dry: 256,
      wet: 256,
      delayL: 128,
      delayR: 160,
      volumeL: 256,
      volumeR: 256,
      channels: Channels.Stereo,
      inverse: false,
      delayUnit: DelayUnit.Sec_16384,
    }
    readonly controllers: DelayControllers = new DelayControllers(
      this,
      this.controllerValues
    )
    readonly c = this.controllers
    readonly midiMaps: DelayControllerMidiMaps = {
      dry: new ControllerMidiMap(),
      wet: new ControllerMidiMap(),
      delayL: new ControllerMidiMap(),
      delayR: new ControllerMidiMap(),
      volumeL: new ControllerMidiMap(),
      volumeR: new ControllerMidiMap(),
      channels: new ControllerMidiMap(),
      inverse: new ControllerMidiMap(),
      delayUnit: new ControllerMidiMap(),
    }
    readonly optionValues: DelayOptionValues = {}
    readonly options: DelayOptions = new DelayOptions(this.optionValues)
    readonly o = this.options
    behavior?: DelayBehavior
    constructor() {
      super()
      this.behavior = new DelayBehavior(this)
    }
    attachTo(project: Project): AttachedModule {
      return super.attachTo(project) as AttachedModule
    }
    *rawControllerValues(): Generator<number> {
      const { controllerValues: cv } = this
      yield cv.dry
      yield cv.wet
      yield cv.delayL
      yield cv.delayR
      yield cv.volumeL
      yield cv.volumeR
      yield cv.channels
      yield Number(cv.inverse)
      yield cv.delayUnit
    }
    setMidiMaps(midiMaps: MidiMap[]) {
      this.midiMaps.dry = midiMaps[0]
      this.midiMaps.wet = midiMaps[1]
      this.midiMaps.delayL = midiMaps[2]
      this.midiMaps.delayR = midiMaps[3]
      this.midiMaps.volumeL = midiMaps[4]
      this.midiMaps.volumeR = midiMaps[5]
      this.midiMaps.channels = midiMaps[6]
      this.midiMaps.inverse = midiMaps[7]
      this.midiMaps.delayUnit = midiMaps[8]
    }
    midiMapsArray(): MidiMap[] {
      const a: MidiMap[] = []
      a.push(this.midiMaps.dry)
      a.push(this.midiMaps.wet)
      a.push(this.midiMaps.delayL)
      a.push(this.midiMaps.delayR)
      a.push(this.midiMaps.volumeL)
      a.push(this.midiMaps.volumeR)
      a.push(this.midiMaps.channels)
      a.push(this.midiMaps.inverse)
      a.push(this.midiMaps.delayUnit)
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
