/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { MidiMap, ControllerMidiMap, ControllerMidiMaps } from "../controllerMidiMap"
import { Project } from "../project"
import { ModuleBase } from "./moduleBase"
import { ModuleType, OptionValues, Options } from "./moduleType"
import { ReverbBehavior } from "./reverbBehavior"
import { ReverbControllers } from "./reverbControllers"
import { ReverbControllerValues } from "./reverbControllerValues"
import { Mode as _Mode } from "./reverbEnums"
export namespace Reverb {
  export const Mode = _Mode
  interface ReverbControllerMidiMaps extends ControllerMidiMaps {
    dry: ControllerMidiMap
    wet: ControllerMidiMap
    feedback: ControllerMidiMap
    damp: ControllerMidiMap
    stereoWidth: ControllerMidiMap
    freeze: ControllerMidiMap
    mode: ControllerMidiMap
    allPassFilter: ControllerMidiMap
    roomSize: ControllerMidiMap
    randomSeed: ControllerMidiMap
  }
  interface ReverbOptionValues extends OptionValues {}
  class ReverbOptions implements Options {
    constructor(readonly optionValues: ReverbOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "Reverb"
    flags = 81
    readonly typeName = "Reverb"
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
        this.controllerValues.damp = val
      },
      (val: number) => {
        this.controllerValues.stereoWidth = val
      },
      (val: number) => {
        this.controllerValues.freeze = Boolean(val)
      },
      (val: number) => {
        this.controllerValues.mode = val
      },
      (val: number) => {
        this.controllerValues.allPassFilter = Boolean(val)
      },
      (val: number) => {
        this.controllerValues.roomSize = val
      },
      (val: number) => {
        this.controllerValues.randomSeed = val
      },
    ]
    readonly controllerValues: ReverbControllerValues = {
      dry: 256,
      wet: 64,
      feedback: 256,
      damp: 128,
      stereoWidth: 256,
      freeze: false,
      mode: Mode.Hq,
      allPassFilter: true,
      roomSize: 16,
      randomSeed: 0,
    }
    readonly controllers: ReverbControllers = new ReverbControllers(
      this,
      this.controllerValues
    )
    readonly c = this.controllers
    readonly midiMaps: ReverbControllerMidiMaps = {
      dry: new ControllerMidiMap(),
      wet: new ControllerMidiMap(),
      feedback: new ControllerMidiMap(),
      damp: new ControllerMidiMap(),
      stereoWidth: new ControllerMidiMap(),
      freeze: new ControllerMidiMap(),
      mode: new ControllerMidiMap(),
      allPassFilter: new ControllerMidiMap(),
      roomSize: new ControllerMidiMap(),
      randomSeed: new ControllerMidiMap(),
    }
    readonly optionValues: ReverbOptionValues = {}
    readonly options: ReverbOptions = new ReverbOptions(this.optionValues)
    readonly o = this.options
    behavior?: ReverbBehavior
    constructor() {
      super()
      this.behavior = new ReverbBehavior(this)
    }
    attachTo(project: Project): AttachedModule {
      return super.attachTo(project) as AttachedModule
    }
    *rawControllerValues(): Generator<number> {
      const { controllerValues: cv } = this
      yield cv.dry
      yield cv.wet
      yield cv.feedback
      yield cv.damp
      yield cv.stereoWidth
      yield Number(cv.freeze)
      yield cv.mode
      yield Number(cv.allPassFilter)
      yield cv.roomSize
      yield cv.randomSeed
    }
    setMidiMaps(midiMaps: MidiMap[]) {
      this.midiMaps.dry = midiMaps[0]
      this.midiMaps.wet = midiMaps[1]
      this.midiMaps.feedback = midiMaps[2]
      this.midiMaps.damp = midiMaps[3]
      this.midiMaps.stereoWidth = midiMaps[4]
      this.midiMaps.freeze = midiMaps[5]
      this.midiMaps.mode = midiMaps[6]
      this.midiMaps.allPassFilter = midiMaps[7]
      this.midiMaps.roomSize = midiMaps[8]
      this.midiMaps.randomSeed = midiMaps[9]
    }
    midiMapsArray(): MidiMap[] {
      const a: MidiMap[] = []
      a.push(this.midiMaps.dry)
      a.push(this.midiMaps.wet)
      a.push(this.midiMaps.feedback)
      a.push(this.midiMaps.damp)
      a.push(this.midiMaps.stereoWidth)
      a.push(this.midiMaps.freeze)
      a.push(this.midiMaps.mode)
      a.push(this.midiMaps.allPassFilter)
      a.push(this.midiMaps.roomSize)
      a.push(this.midiMaps.randomSeed)
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
