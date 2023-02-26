/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { MidiMap, ControllerMidiMap, ControllerMidiMaps } from "../controllerMidiMap"
import { Project } from "../project"
import { ModuleBase } from "./moduleBase"
import { ModuleType, OptionValues, Options } from "./moduleType"
import { FmBehavior } from "./fmBehavior"
import { FmControllers } from "./fmControllers"
import { FmControllerValues } from "./fmControllerValues"
export namespace Fm {
  // Intentionally duplicated enums - see also fmEnums.ts
  // (TypeScript does not allow exporting imported enums from inside a namespace)
  export enum Mode {
    // noinspection JSUnusedGlobalSymbols
    Hq = 0,
    HqMono = 1,
    Lq = 2,
    LqMono = 3,
  }
  export enum CtlNum {
    CVolume = 1,
    MVolume = 2,
    Panning = 3,
    CFreqRatio = 4,
    MFreqRatio = 5,
    MSelfModulation = 6,
    CAttack = 7,
    CDecay = 8,
    CSustain = 9,
    CRelease = 10,
    MAttack = 11,
    MDecay = 12,
    MSustain = 13,
    MRelease = 14,
    MScalingPerKey = 15,
    Polyphony = 16,
    Mode = 17,
  }
  interface FmControllerMidiMaps extends ControllerMidiMaps {
    cVolume: ControllerMidiMap
    mVolume: ControllerMidiMap
    panning: ControllerMidiMap
    cFreqRatio: ControllerMidiMap
    mFreqRatio: ControllerMidiMap
    mSelfModulation: ControllerMidiMap
    cAttack: ControllerMidiMap
    cDecay: ControllerMidiMap
    cSustain: ControllerMidiMap
    cRelease: ControllerMidiMap
    mAttack: ControllerMidiMap
    mDecay: ControllerMidiMap
    mSustain: ControllerMidiMap
    mRelease: ControllerMidiMap
    mScalingPerKey: ControllerMidiMap
    polyphony: ControllerMidiMap
    mode: ControllerMidiMap
  }
  interface FmOptionValues extends OptionValues {}
  class FmOptions implements Options {
    constructor(readonly optionValues: FmOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "FM"
    flags = 0x49
    readonly typeName = "FM"
    readonly controllerSetters = [
      (val: number) => {
        this.controllerValues.cVolume = val
      },
      (val: number) => {
        this.controllerValues.mVolume = val
      },
      (val: number) => {
        this.controllerValues.panning = val
      },
      (val: number) => {
        this.controllerValues.cFreqRatio = val
      },
      (val: number) => {
        this.controllerValues.mFreqRatio = val
      },
      (val: number) => {
        this.controllerValues.mSelfModulation = val
      },
      (val: number) => {
        this.controllerValues.cAttack = val
      },
      (val: number) => {
        this.controllerValues.cDecay = val
      },
      (val: number) => {
        this.controllerValues.cSustain = val
      },
      (val: number) => {
        this.controllerValues.cRelease = val
      },
      (val: number) => {
        this.controllerValues.mAttack = val
      },
      (val: number) => {
        this.controllerValues.mDecay = val
      },
      (val: number) => {
        this.controllerValues.mSustain = val
      },
      (val: number) => {
        this.controllerValues.mRelease = val
      },
      (val: number) => {
        this.controllerValues.mScalingPerKey = val
      },
      (val: number) => {
        this.controllerValues.polyphony = val
      },
      (val: number) => {
        this.controllerValues.mode = val
      },
    ]
    readonly controllerValues: FmControllerValues = {
      cVolume: 128,
      mVolume: 48,
      panning: 0,
      cFreqRatio: 1,
      mFreqRatio: 1,
      mSelfModulation: 0,
      cAttack: 32,
      cDecay: 32,
      cSustain: 128,
      cRelease: 64,
      mAttack: 32,
      mDecay: 32,
      mSustain: 128,
      mRelease: 64,
      mScalingPerKey: 0,
      polyphony: 4,
      mode: Mode.HqMono,
    }
    readonly controllers: FmControllers = new FmControllers(this, this.controllerValues)
    readonly c = this.controllers
    readonly midiMaps: FmControllerMidiMaps = {
      cVolume: new ControllerMidiMap(),
      mVolume: new ControllerMidiMap(),
      panning: new ControllerMidiMap(),
      cFreqRatio: new ControllerMidiMap(),
      mFreqRatio: new ControllerMidiMap(),
      mSelfModulation: new ControllerMidiMap(),
      cAttack: new ControllerMidiMap(),
      cDecay: new ControllerMidiMap(),
      cSustain: new ControllerMidiMap(),
      cRelease: new ControllerMidiMap(),
      mAttack: new ControllerMidiMap(),
      mDecay: new ControllerMidiMap(),
      mSustain: new ControllerMidiMap(),
      mRelease: new ControllerMidiMap(),
      mScalingPerKey: new ControllerMidiMap(),
      polyphony: new ControllerMidiMap(),
      mode: new ControllerMidiMap(),
    }
    readonly optionValues: FmOptionValues = {}
    readonly options: FmOptions = new FmOptions(this.optionValues)
    readonly o = this.options
    behavior?: FmBehavior
    constructor() {
      super()
      this.behavior = new FmBehavior(this)
    }
    attachTo(project: Project): AttachedModule {
      return super.attachTo(project) as AttachedModule
    }
    setRawControllerValue(ctlNum: number, value: number) {
      const { controllerValues: cv } = this
      switch (ctlNum) {
        case 1:
          cv.cVolume = value
          break
        case 2:
          cv.mVolume = value
          break
        case 3:
          cv.panning = value
          break
        case 4:
          cv.cFreqRatio = value
          break
        case 5:
          cv.mFreqRatio = value
          break
        case 6:
          cv.mSelfModulation = value
          break
        case 7:
          cv.cAttack = value
          break
        case 8:
          cv.cDecay = value
          break
        case 9:
          cv.cSustain = value
          break
        case 10:
          cv.cRelease = value
          break
        case 11:
          cv.mAttack = value
          break
        case 12:
          cv.mDecay = value
          break
        case 13:
          cv.mSustain = value
          break
        case 14:
          cv.mRelease = value
          break
        case 15:
          cv.mScalingPerKey = value
          break
        case 16:
          cv.polyphony = value
          break
        case 17:
          cv.mode = value
          break
      }
    }
    *rawControllerValues(): Generator<number> {
      const { controllerValues: cv } = this
      yield cv.cVolume
      yield cv.mVolume
      yield cv.panning
      yield cv.cFreqRatio
      yield cv.mFreqRatio
      yield cv.mSelfModulation
      yield cv.cAttack
      yield cv.cDecay
      yield cv.cSustain
      yield cv.cRelease
      yield cv.mAttack
      yield cv.mDecay
      yield cv.mSustain
      yield cv.mRelease
      yield cv.mScalingPerKey
      yield cv.polyphony
      yield cv.mode
    }
    setMidiMaps(midiMaps: MidiMap[]) {
      this.midiMaps.cVolume = midiMaps[0] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.mVolume = midiMaps[1] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.panning = midiMaps[2] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.cFreqRatio = midiMaps[3] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.mFreqRatio = midiMaps[4] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.mSelfModulation = midiMaps[5] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.cAttack = midiMaps[6] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.cDecay = midiMaps[7] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.cSustain = midiMaps[8] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.cRelease = midiMaps[9] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.mAttack = midiMaps[10] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.mDecay = midiMaps[11] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.mSustain = midiMaps[12] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.mRelease = midiMaps[13] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.mScalingPerKey = midiMaps[14] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.polyphony = midiMaps[15] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.mode = midiMaps[16] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
    }
    midiMapsArray(): MidiMap[] {
      const a: MidiMap[] = []
      a.push(this.midiMaps.cVolume)
      a.push(this.midiMaps.mVolume)
      a.push(this.midiMaps.panning)
      a.push(this.midiMaps.cFreqRatio)
      a.push(this.midiMaps.mFreqRatio)
      a.push(this.midiMaps.mSelfModulation)
      a.push(this.midiMaps.cAttack)
      a.push(this.midiMaps.cDecay)
      a.push(this.midiMaps.cSustain)
      a.push(this.midiMaps.cRelease)
      a.push(this.midiMaps.mAttack)
      a.push(this.midiMaps.mDecay)
      a.push(this.midiMaps.mSustain)
      a.push(this.midiMaps.mRelease)
      a.push(this.midiMaps.mScalingPerKey)
      a.push(this.midiMaps.polyphony)
      a.push(this.midiMaps.mode)
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
