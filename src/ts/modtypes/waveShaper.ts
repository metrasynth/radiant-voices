/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { MidiMap, ControllerMidiMap, ControllerMidiMaps } from "../controllerMidiMap"
import { Project } from "../project"
import { ModuleBase } from "./moduleBase"
import { ModuleType, OptionValues, Options } from "./moduleType"
import { WaveShaperBehavior } from "./waveShaperBehavior"
import { WaveShaperControllers } from "./waveShaperControllers"
import { WaveShaperControllerValues } from "./waveShaperControllerValues"
export namespace WaveShaper {
  // Intentionally duplicated enums - see also waveShaperEnums.ts
  // (TypeScript does not allow exporting imported enums from inside a namespace)
  export enum Mode {
    // noinspection JSUnusedGlobalSymbols
    Hq = 0,
    HqMono = 1,
    Lq = 2,
    LqMono = 3,
  }
  export enum CtlNum {
    InputVolume = 1,
    Mix = 2,
    OutputVolume = 3,
    Symmetric = 4,
    Mode = 5,
    DcBlocker = 6,
  }
  interface WaveShaperControllerMidiMaps extends ControllerMidiMaps {
    inputVolume: ControllerMidiMap
    mix: ControllerMidiMap
    outputVolume: ControllerMidiMap
    symmetric: ControllerMidiMap
    mode: ControllerMidiMap
    dcBlocker: ControllerMidiMap
  }
  interface WaveShaperOptionValues extends OptionValues {}
  class WaveShaperOptions implements Options {
    constructor(readonly optionValues: WaveShaperOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "WaveShaper"
    flags = 81
    readonly typeName = "WaveShaper"
    readonly controllerSetters = [
      (val: number) => {
        this.controllerValues.inputVolume = val
      },
      (val: number) => {
        this.controllerValues.mix = val
      },
      (val: number) => {
        this.controllerValues.outputVolume = val
      },
      (val: number) => {
        this.controllerValues.symmetric = Boolean(val)
      },
      (val: number) => {
        this.controllerValues.mode = val
      },
      (val: number) => {
        this.controllerValues.dcBlocker = Boolean(val)
      },
    ]
    readonly controllerValues: WaveShaperControllerValues = {
      inputVolume: 256,
      mix: 256,
      outputVolume: 256,
      symmetric: true,
      mode: Mode.Hq,
      dcBlocker: true,
    }
    readonly controllers: WaveShaperControllers = new WaveShaperControllers(
      this,
      this.controllerValues
    )
    readonly c = this.controllers
    readonly midiMaps: WaveShaperControllerMidiMaps = {
      inputVolume: new ControllerMidiMap(),
      mix: new ControllerMidiMap(),
      outputVolume: new ControllerMidiMap(),
      symmetric: new ControllerMidiMap(),
      mode: new ControllerMidiMap(),
      dcBlocker: new ControllerMidiMap(),
    }
    readonly optionValues: WaveShaperOptionValues = {}
    readonly options: WaveShaperOptions = new WaveShaperOptions(this.optionValues)
    readonly o = this.options
    behavior?: WaveShaperBehavior
    constructor() {
      super()
      this.behavior = new WaveShaperBehavior(this)
    }
    attachTo(project: Project): AttachedModule {
      return super.attachTo(project) as AttachedModule
    }
    setRawControllerValue(ctlNum: number, value: number) {
      const { controllerValues: cv } = this
      switch (ctlNum) {
        case 1:
          cv.inputVolume = value
          break
        case 2:
          cv.mix = value
          break
        case 3:
          cv.outputVolume = value
          break
        case 4:
          cv.symmetric = Boolean(value)
          break
        case 5:
          cv.mode = value
          break
        case 6:
          cv.dcBlocker = Boolean(value)
          break
      }
    }
    *rawControllerValues(): Generator<number> {
      const { controllerValues: cv } = this
      yield cv.inputVolume
      yield cv.mix
      yield cv.outputVolume
      yield Number(cv.symmetric)
      yield cv.mode
      yield Number(cv.dcBlocker)
    }
    setMidiMaps(midiMaps: MidiMap[]) {
      this.midiMaps.inputVolume = midiMaps[0] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.mix = midiMaps[1] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.outputVolume = midiMaps[2] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.symmetric = midiMaps[3] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.mode = midiMaps[4] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.dcBlocker = midiMaps[5] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
    }
    midiMapsArray(): MidiMap[] {
      const a: MidiMap[] = []
      a.push(this.midiMaps.inputVolume)
      a.push(this.midiMaps.mix)
      a.push(this.midiMaps.outputVolume)
      a.push(this.midiMaps.symmetric)
      a.push(this.midiMaps.mode)
      a.push(this.midiMaps.dcBlocker)
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
