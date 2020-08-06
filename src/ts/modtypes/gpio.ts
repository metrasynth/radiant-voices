/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { MidiMap, ControllerMidiMap, ControllerMidiMaps } from "../controllerMidiMap"
import { Project } from "../project"
import { ModuleBase } from "./moduleBase"
import { ModuleType, OptionValues, Options } from "./moduleType"
import { GpioBehavior } from "./gpioBehavior"
import { GpioControllers } from "./gpioControllers"
import { GpioControllerValues } from "./gpioControllerValues"
export namespace Gpio {
  export enum CtlNum {
    Out = 1,
    OutPin = 2,
    OutThreshold = 3,
    In = 4,
    InPin = 5,
    InNote = 6,
    InAmplitude = 7,
  }
  interface GpioControllerMidiMaps extends ControllerMidiMaps {
    out: ControllerMidiMap
    outPin: ControllerMidiMap
    outThreshold: ControllerMidiMap
    in: ControllerMidiMap
    inPin: ControllerMidiMap
    inNote: ControllerMidiMap
    inAmplitude: ControllerMidiMap
  }
  interface GpioOptionValues extends OptionValues {}
  class GpioOptions implements Options {
    constructor(readonly optionValues: GpioOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "GPIO"
    flags = 81
    readonly typeName = "GPIO"
    readonly controllerSetters = [
      (val: number) => {
        this.controllerValues.out = Boolean(val)
      },
      (val: number) => {
        this.controllerValues.outPin = val
      },
      (val: number) => {
        this.controllerValues.outThreshold = val
      },
      (val: number) => {
        this.controllerValues.in = Boolean(val)
      },
      (val: number) => {
        this.controllerValues.inPin = val
      },
      (val: number) => {
        this.controllerValues.inNote = val
      },
      (val: number) => {
        this.controllerValues.inAmplitude = val
      },
    ]
    readonly controllerValues: GpioControllerValues = {
      out: false,
      outPin: 0,
      outThreshold: 50,
      in: false,
      inPin: 0,
      inNote: 0,
      inAmplitude: 100,
    }
    readonly controllers: GpioControllers = new GpioControllers(
      this,
      this.controllerValues
    )
    readonly c = this.controllers
    readonly midiMaps: GpioControllerMidiMaps = {
      out: new ControllerMidiMap(),
      outPin: new ControllerMidiMap(),
      outThreshold: new ControllerMidiMap(),
      in: new ControllerMidiMap(),
      inPin: new ControllerMidiMap(),
      inNote: new ControllerMidiMap(),
      inAmplitude: new ControllerMidiMap(),
    }
    readonly optionValues: GpioOptionValues = {}
    readonly options: GpioOptions = new GpioOptions(this.optionValues)
    readonly o = this.options
    behavior?: GpioBehavior
    constructor() {
      super()
      this.behavior = new GpioBehavior(this)
    }
    attachTo(project: Project): AttachedModule {
      return super.attachTo(project) as AttachedModule
    }
    setRawControllerValue(ctlNum: number, value: number) {
      const { controllerValues: cv } = this
      switch (ctlNum) {
        case 1:
          cv.out = Boolean(value)
          break
        case 2:
          cv.outPin = value
          break
        case 3:
          cv.outThreshold = value
          break
        case 4:
          cv.in = Boolean(value)
          break
        case 5:
          cv.inPin = value
          break
        case 6:
          cv.inNote = value
          break
        case 7:
          cv.inAmplitude = value
          break
      }
    }
    *rawControllerValues(): Generator<number> {
      const { controllerValues: cv } = this
      yield Number(cv.out)
      yield cv.outPin
      yield cv.outThreshold
      yield Number(cv.in)
      yield cv.inPin
      yield cv.inNote
      yield cv.inAmplitude
    }
    setMidiMaps(midiMaps: MidiMap[]) {
      this.midiMaps.out = midiMaps[0]
      this.midiMaps.outPin = midiMaps[1]
      this.midiMaps.outThreshold = midiMaps[2]
      this.midiMaps.in = midiMaps[3]
      this.midiMaps.inPin = midiMaps[4]
      this.midiMaps.inNote = midiMaps[5]
      this.midiMaps.inAmplitude = midiMaps[6]
    }
    midiMapsArray(): MidiMap[] {
      const a: MidiMap[] = []
      a.push(this.midiMaps.out)
      a.push(this.midiMaps.outPin)
      a.push(this.midiMaps.outThreshold)
      a.push(this.midiMaps.in)
      a.push(this.midiMaps.inPin)
      a.push(this.midiMaps.inNote)
      a.push(this.midiMaps.inAmplitude)
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
