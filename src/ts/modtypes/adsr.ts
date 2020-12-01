/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { MidiMap, ControllerMidiMap, ControllerMidiMaps } from "../controllerMidiMap"
import { Project } from "../project"
import { ModuleBase } from "./moduleBase"
import { ModuleType, OptionValues, Options } from "./moduleType"
import { AdsrBehavior } from "./adsrBehavior"
import { AdsrControllers } from "./adsrControllers"
import { AdsrControllerValues } from "./adsrControllerValues"
export namespace Adsr {
  // Intentionally duplicated enums - see also adsrEnums.ts
  // (TypeScript does not allow exporting imported enums from inside a namespace)
  export enum Curve {
    // noinspection JSUnusedGlobalSymbols
    Linear = 0,
    Exp1 = 1,
    Exp2 = 2,
    NegExp1 = 3,
    NegExp2 = 4,
    Sin = 5,
  }
  export enum State {
    // noinspection JSUnusedGlobalSymbols
    Stop = 0,
    Start = 1,
  }
  export enum OnNoteOn {
    // noinspection JSUnusedGlobalSymbols
    DoNothing = 0,
    StartOnFirstNote = 1,
    Start = 2,
  }
  export enum OnNoteOff {
    // noinspection JSUnusedGlobalSymbols
    DoNothing = 0,
    StopOnLastNote = 1,
    Stop = 2,
  }
  export enum Mode {
    // noinspection JSUnusedGlobalSymbols
    Generator = 0,
    AmpModulatorMono = 1,
    AmpModulatorStereo = 2,
  }
  export enum SmoothTransitions {
    // noinspection JSUnusedGlobalSymbols
    Off = 0,
    RestartAndVolumeChange = 1,
    RestartSmootherAndVolumeChange = 2,
  }
  export enum CtlNum {
    Volume = 1,
    AttackMs = 2,
    DecayMs = 3,
    SustainLevel = 4,
    ReleaseMs = 5,
    AttackCurve = 6,
    DecayCurve = 7,
    ReleaseCurve = 8,
    Sustain = 9,
    SustainPedal = 10,
    State = 11,
    OnNoteOn = 12,
    OnNoteOff = 13,
    Mode = 14,
    SmoothTransitions = 15,
  }
  interface AdsrControllerMidiMaps extends ControllerMidiMaps {
    volume: ControllerMidiMap
    attackMs: ControllerMidiMap
    decayMs: ControllerMidiMap
    sustainLevel: ControllerMidiMap
    releaseMs: ControllerMidiMap
    attackCurve: ControllerMidiMap
    decayCurve: ControllerMidiMap
    releaseCurve: ControllerMidiMap
    sustain: ControllerMidiMap
    sustainPedal: ControllerMidiMap
    state: ControllerMidiMap
    onNoteOn: ControllerMidiMap
    onNoteOff: ControllerMidiMap
    mode: ControllerMidiMap
    smoothTransitions: ControllerMidiMap
  }
  interface AdsrOptionValues extends OptionValues {}
  class AdsrOptions implements Options {
    constructor(readonly optionValues: AdsrOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "ADSR"
    flags = 89
    readonly typeName = "ADSR"
    readonly controllerSetters = [
      (val: number) => {
        this.controllerValues.volume = val
      },
      (val: number) => {
        this.controllerValues.attackMs = val
      },
      (val: number) => {
        this.controllerValues.decayMs = val
      },
      (val: number) => {
        this.controllerValues.sustainLevel = val
      },
      (val: number) => {
        this.controllerValues.releaseMs = val
      },
      (val: number) => {
        this.controllerValues.attackCurve = val
      },
      (val: number) => {
        this.controllerValues.decayCurve = val
      },
      (val: number) => {
        this.controllerValues.releaseCurve = val
      },
      (val: number) => {
        this.controllerValues.sustain = Boolean(val)
      },
      (val: number) => {
        this.controllerValues.sustainPedal = Boolean(val)
      },
      (val: number) => {
        this.controllerValues.state = val
      },
      (val: number) => {
        this.controllerValues.onNoteOn = val
      },
      (val: number) => {
        this.controllerValues.onNoteOff = val
      },
      (val: number) => {
        this.controllerValues.mode = val
      },
      (val: number) => {
        this.controllerValues.smoothTransitions = val
      },
    ]
    readonly controllerValues: AdsrControllerValues = {
      volume: 32768,
      attackMs: 100,
      decayMs: 100,
      sustainLevel: 16384,
      releaseMs: 100,
      attackCurve: Curve.Linear,
      decayCurve: Curve.Linear,
      releaseCurve: Curve.Linear,
      sustain: true,
      sustainPedal: false,
      state: State.Stop,
      onNoteOn: OnNoteOn.StartOnFirstNote,
      onNoteOff: OnNoteOff.StopOnLastNote,
      mode: Mode.Generator,
      smoothTransitions: SmoothTransitions.RestartSmootherAndVolumeChange,
    }
    readonly controllers: AdsrControllers = new AdsrControllers(
      this,
      this.controllerValues
    )
    readonly c = this.controllers
    readonly midiMaps: AdsrControllerMidiMaps = {
      volume: new ControllerMidiMap(),
      attackMs: new ControllerMidiMap(),
      decayMs: new ControllerMidiMap(),
      sustainLevel: new ControllerMidiMap(),
      releaseMs: new ControllerMidiMap(),
      attackCurve: new ControllerMidiMap(),
      decayCurve: new ControllerMidiMap(),
      releaseCurve: new ControllerMidiMap(),
      sustain: new ControllerMidiMap(),
      sustainPedal: new ControllerMidiMap(),
      state: new ControllerMidiMap(),
      onNoteOn: new ControllerMidiMap(),
      onNoteOff: new ControllerMidiMap(),
      mode: new ControllerMidiMap(),
      smoothTransitions: new ControllerMidiMap(),
    }
    readonly optionValues: AdsrOptionValues = {}
    readonly options: AdsrOptions = new AdsrOptions(this.optionValues)
    readonly o = this.options
    behavior?: AdsrBehavior
    constructor() {
      super()
      this.behavior = new AdsrBehavior(this)
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
          cv.attackMs = value
          break
        case 3:
          cv.decayMs = value
          break
        case 4:
          cv.sustainLevel = value
          break
        case 5:
          cv.releaseMs = value
          break
        case 6:
          cv.attackCurve = value
          break
        case 7:
          cv.decayCurve = value
          break
        case 8:
          cv.releaseCurve = value
          break
        case 9:
          cv.sustain = Boolean(value)
          break
        case 10:
          cv.sustainPedal = Boolean(value)
          break
        case 11:
          cv.state = value
          break
        case 12:
          cv.onNoteOn = value
          break
        case 13:
          cv.onNoteOff = value
          break
        case 14:
          cv.mode = value
          break
        case 15:
          cv.smoothTransitions = value
          break
      }
    }
    *rawControllerValues(): Generator<number> {
      const { controllerValues: cv } = this
      yield cv.volume
      yield cv.attackMs
      yield cv.decayMs
      yield cv.sustainLevel
      yield cv.releaseMs
      yield cv.attackCurve
      yield cv.decayCurve
      yield cv.releaseCurve
      yield Number(cv.sustain)
      yield Number(cv.sustainPedal)
      yield cv.state
      yield cv.onNoteOn
      yield cv.onNoteOff
      yield cv.mode
      yield cv.smoothTransitions
    }
    setMidiMaps(midiMaps: MidiMap[]) {
      this.midiMaps.volume = midiMaps[0]
      this.midiMaps.attackMs = midiMaps[1]
      this.midiMaps.decayMs = midiMaps[2]
      this.midiMaps.sustainLevel = midiMaps[3]
      this.midiMaps.releaseMs = midiMaps[4]
      this.midiMaps.attackCurve = midiMaps[5]
      this.midiMaps.decayCurve = midiMaps[6]
      this.midiMaps.releaseCurve = midiMaps[7]
      this.midiMaps.sustain = midiMaps[8]
      this.midiMaps.sustainPedal = midiMaps[9]
      this.midiMaps.state = midiMaps[10]
      this.midiMaps.onNoteOn = midiMaps[11]
      this.midiMaps.onNoteOff = midiMaps[12]
      this.midiMaps.mode = midiMaps[13]
      this.midiMaps.smoothTransitions = midiMaps[14]
    }
    midiMapsArray(): MidiMap[] {
      const a: MidiMap[] = []
      a.push(this.midiMaps.volume)
      a.push(this.midiMaps.attackMs)
      a.push(this.midiMaps.decayMs)
      a.push(this.midiMaps.sustainLevel)
      a.push(this.midiMaps.releaseMs)
      a.push(this.midiMaps.attackCurve)
      a.push(this.midiMaps.decayCurve)
      a.push(this.midiMaps.releaseCurve)
      a.push(this.midiMaps.sustain)
      a.push(this.midiMaps.sustainPedal)
      a.push(this.midiMaps.state)
      a.push(this.midiMaps.onNoteOn)
      a.push(this.midiMaps.onNoteOff)
      a.push(this.midiMaps.mode)
      a.push(this.midiMaps.smoothTransitions)
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
