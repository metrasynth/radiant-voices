/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { MidiMap, ControllerMidiMap, ControllerMidiMaps } from "../controllerMidiMap"
import { Project } from "../project"
import { ModuleBase } from "./moduleBase"
import { ModuleType, OptionValues, Options } from "./moduleType"
import { DistortionBehavior } from "./distortionBehavior"
import { DistortionControllers } from "./distortionControllers"
import { DistortionControllerValues } from "./distortionControllerValues"
export namespace Distortion {
  // Intentionally duplicated enums - see also distortionEnums.ts
  // (TypeScript does not allow exporting imported enums from inside a namespace)
  export enum Type {
    // noinspection JSUnusedGlobalSymbols
    Clipping = 0,
    Foldback = 1,
    Foldback2 = 2,
    Foldback3 = 3,
    Overflow = 4,
    Overflow2 = 5,
    SaturationFoldback = 6,
    SaturationFoldbackSin = 7,
    Saturation3 = 8,
    Saturation4 = 9,
    Saturation5 = 10,
  }
  export enum CtlNum {
    Volume = 1,
    Type = 2,
    Power = 3,
    BitDepth = 4,
    Freq = 5,
    Noise = 6,
  }
  interface DistortionControllerMidiMaps extends ControllerMidiMaps {
    volume: ControllerMidiMap
    type: ControllerMidiMap
    power: ControllerMidiMap
    bitDepth: ControllerMidiMap
    freq: ControllerMidiMap
    noise: ControllerMidiMap
  }
  interface DistortionOptionValues extends OptionValues {}
  class DistortionOptions implements Options {
    constructor(readonly optionValues: DistortionOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "Distortion"
    flags = 0x51
    readonly typeName = "Distortion"
    readonly controllerSetters = [
      (val: number) => {
        this.controllerValues.volume = val
      },
      (val: number) => {
        this.controllerValues.type = val
      },
      (val: number) => {
        this.controllerValues.power = val
      },
      (val: number) => {
        this.controllerValues.bitDepth = val
      },
      (val: number) => {
        this.controllerValues.freq = val
      },
      (val: number) => {
        this.controllerValues.noise = val
      },
    ]
    readonly controllerValues: DistortionControllerValues = {
      volume: 128,
      type: Type.Clipping,
      power: 0,
      bitDepth: 16,
      freq: 44100,
      noise: 0,
    }
    readonly controllers: DistortionControllers = new DistortionControllers(
      this,
      this.controllerValues
    )
    readonly c = this.controllers
    readonly midiMaps: DistortionControllerMidiMaps = {
      volume: new ControllerMidiMap(),
      type: new ControllerMidiMap(),
      power: new ControllerMidiMap(),
      bitDepth: new ControllerMidiMap(),
      freq: new ControllerMidiMap(),
      noise: new ControllerMidiMap(),
    }
    readonly optionValues: DistortionOptionValues = {}
    readonly options: DistortionOptions = new DistortionOptions(this.optionValues)
    readonly o = this.options
    behavior?: DistortionBehavior
    constructor() {
      super()
      this.behavior = new DistortionBehavior(this)
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
          cv.power = value
          break
        case 4:
          cv.bitDepth = value
          break
        case 5:
          cv.freq = value
          break
        case 6:
          cv.noise = value
          break
      }
    }
    *rawControllerValues(): Generator<number> {
      const { controllerValues: cv } = this
      yield cv.volume
      yield cv.type
      yield cv.power
      yield cv.bitDepth
      yield cv.freq
      yield cv.noise
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
      this.midiMaps.power = midiMaps[2] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.bitDepth = midiMaps[3] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.freq = midiMaps[4] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.noise = midiMaps[5] || {
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
      a.push(this.midiMaps.power)
      a.push(this.midiMaps.bitDepth)
      a.push(this.midiMaps.freq)
      a.push(this.midiMaps.noise)
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
