/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { MidiMap, ControllerMidiMap, ControllerMidiMaps } from "../controllerMidiMap"
import { Project } from "../project"
import { ModuleBase } from "./moduleBase"
import { ModuleType, OptionValues, Options } from "./moduleType"
import { KickerBehavior } from "./kickerBehavior"
import { KickerControllers } from "./kickerControllers"
import { KickerControllerValues } from "./kickerControllerValues"
export namespace Kicker {
  // Intentionally duplicated enums - see also kickerEnums.ts
  // (TypeScript does not allow exporting imported enums from inside a namespace)
  export enum Waveform {
    // noinspection JSUnusedGlobalSymbols
    Triangle = 0,
    Square = 1,
    Sin = 2,
  }
  export enum CtlNum {
    Volume = 1,
    Waveform = 2,
    Panning = 3,
    Attack = 4,
    Release = 5,
    Boost = 6,
    Acceleration = 7,
    PolyphonyCh = 8,
    NoClick = 9,
  }
  interface KickerControllerMidiMaps extends ControllerMidiMaps {
    volume: ControllerMidiMap
    waveform: ControllerMidiMap
    panning: ControllerMidiMap
    attack: ControllerMidiMap
    release: ControllerMidiMap
    boost: ControllerMidiMap
    acceleration: ControllerMidiMap
    polyphonyCh: ControllerMidiMap
    noClick: ControllerMidiMap
  }
  interface KickerOptionValues extends OptionValues {}
  class KickerOptions implements Options {
    constructor(readonly optionValues: KickerOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "Kicker"
    flags = 73
    readonly typeName = "Kicker"
    readonly controllerSetters = [
      (val: number) => {
        this.controllerValues.volume = val
      },
      (val: number) => {
        this.controllerValues.waveform = val
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
        this.controllerValues.boost = val
      },
      (val: number) => {
        this.controllerValues.acceleration = val
      },
      (val: number) => {
        this.controllerValues.polyphonyCh = val
      },
      (val: number) => {
        this.controllerValues.noClick = Boolean(val)
      },
    ]
    readonly controllerValues: KickerControllerValues = {
      volume: 256,
      waveform: Waveform.Triangle,
      panning: 0,
      attack: 0,
      release: 32,
      boost: 0,
      acceleration: 256,
      polyphonyCh: 1,
      noClick: false,
    }
    readonly controllers: KickerControllers = new KickerControllers(
      this,
      this.controllerValues
    )
    readonly c = this.controllers
    readonly midiMaps: KickerControllerMidiMaps = {
      volume: new ControllerMidiMap(),
      waveform: new ControllerMidiMap(),
      panning: new ControllerMidiMap(),
      attack: new ControllerMidiMap(),
      release: new ControllerMidiMap(),
      boost: new ControllerMidiMap(),
      acceleration: new ControllerMidiMap(),
      polyphonyCh: new ControllerMidiMap(),
      noClick: new ControllerMidiMap(),
    }
    readonly optionValues: KickerOptionValues = {}
    readonly options: KickerOptions = new KickerOptions(this.optionValues)
    readonly o = this.options
    behavior?: KickerBehavior
    constructor() {
      super()
      this.behavior = new KickerBehavior(this)
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
          cv.waveform = value
          break
        case 3:
          cv.panning = value
          break
        case 4:
          cv.attack = value
          break
        case 5:
          cv.release = value
          break
        case 6:
          cv.boost = value
          break
        case 7:
          cv.acceleration = value
          break
        case 8:
          cv.polyphonyCh = value
          break
        case 9:
          cv.noClick = Boolean(value)
          break
      }
    }
    *rawControllerValues(): Generator<number> {
      const { controllerValues: cv } = this
      yield cv.volume
      yield cv.waveform
      yield cv.panning
      yield cv.attack
      yield cv.release
      yield cv.boost
      yield cv.acceleration
      yield cv.polyphonyCh
      yield Number(cv.noClick)
    }
    setMidiMaps(midiMaps: MidiMap[]) {
      this.midiMaps.volume = midiMaps[0]
      this.midiMaps.waveform = midiMaps[1]
      this.midiMaps.panning = midiMaps[2]
      this.midiMaps.attack = midiMaps[3]
      this.midiMaps.release = midiMaps[4]
      this.midiMaps.boost = midiMaps[5]
      this.midiMaps.acceleration = midiMaps[6]
      this.midiMaps.polyphonyCh = midiMaps[7]
      this.midiMaps.noClick = midiMaps[8]
    }
    midiMapsArray(): MidiMap[] {
      const a: MidiMap[] = []
      a.push(this.midiMaps.volume)
      a.push(this.midiMaps.waveform)
      a.push(this.midiMaps.panning)
      a.push(this.midiMaps.attack)
      a.push(this.midiMaps.release)
      a.push(this.midiMaps.boost)
      a.push(this.midiMaps.acceleration)
      a.push(this.midiMaps.polyphonyCh)
      a.push(this.midiMaps.noClick)
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
