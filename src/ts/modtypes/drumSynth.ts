/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { MidiMap, ControllerMidiMap, ControllerMidiMaps } from "../controllerMidiMap"
import { Project } from "../project"
import { ModuleBase } from "./moduleBase"
import { ModuleType, OptionValues, Options } from "./moduleType"
import { DrumSynthBehavior } from "./drumSynthBehavior"
import { DrumSynthControllers } from "./drumSynthControllers"
import { DrumSynthControllerValues } from "./drumSynthControllerValues"
export namespace DrumSynth {
  export enum CtlNum {
    Volume = 1,
    Panning = 2,
    Polyphony = 3,
    BassVolume = 4,
    BassPower = 5,
    BassTone = 6,
    BassLength = 7,
    HihatVolume = 8,
    HihatLength = 9,
    SnareVolume = 10,
    SnareTone = 11,
    SnareLength = 12,
    BassPanning = 13,
    HihatPanning = 14,
    SnarePanning = 15,
  }
  interface DrumSynthControllerMidiMaps extends ControllerMidiMaps {
    volume: ControllerMidiMap
    panning: ControllerMidiMap
    polyphony: ControllerMidiMap
    bassVolume: ControllerMidiMap
    bassPower: ControllerMidiMap
    bassTone: ControllerMidiMap
    bassLength: ControllerMidiMap
    hihatVolume: ControllerMidiMap
    hihatLength: ControllerMidiMap
    snareVolume: ControllerMidiMap
    snareTone: ControllerMidiMap
    snareLength: ControllerMidiMap
    bassPanning: ControllerMidiMap
    hihatPanning: ControllerMidiMap
    snarePanning: ControllerMidiMap
  }
  interface DrumSynthOptionValues extends OptionValues {}
  class DrumSynthOptions implements Options {
    constructor(readonly optionValues: DrumSynthOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "DrumSynth"
    flags = 0x49
    readonly typeName = "DrumSynth"
    readonly controllerSetters = [
      (val: number) => {
        this.controllerValues.volume = val
      },
      (val: number) => {
        this.controllerValues.panning = val
      },
      (val: number) => {
        this.controllerValues.polyphony = val
      },
      (val: number) => {
        this.controllerValues.bassVolume = val
      },
      (val: number) => {
        this.controllerValues.bassPower = val
      },
      (val: number) => {
        this.controllerValues.bassTone = val
      },
      (val: number) => {
        this.controllerValues.bassLength = val
      },
      (val: number) => {
        this.controllerValues.hihatVolume = val
      },
      (val: number) => {
        this.controllerValues.hihatLength = val
      },
      (val: number) => {
        this.controllerValues.snareVolume = val
      },
      (val: number) => {
        this.controllerValues.snareTone = val
      },
      (val: number) => {
        this.controllerValues.snareLength = val
      },
      (val: number) => {
        this.controllerValues.bassPanning = val
      },
      (val: number) => {
        this.controllerValues.hihatPanning = val
      },
      (val: number) => {
        this.controllerValues.snarePanning = val
      },
    ]
    readonly controllerValues: DrumSynthControllerValues = {
      volume: 256,
      panning: 0,
      polyphony: 4,
      bassVolume: 200,
      bassPower: 256,
      bassTone: 64,
      bassLength: 64,
      hihatVolume: 256,
      hihatLength: 64,
      snareVolume: 256,
      snareTone: 128,
      snareLength: 64,
      bassPanning: 0,
      hihatPanning: 0,
      snarePanning: 0,
    }
    readonly controllers: DrumSynthControllers = new DrumSynthControllers(
      this,
      this.controllerValues
    )
    readonly c = this.controllers
    readonly midiMaps: DrumSynthControllerMidiMaps = {
      volume: new ControllerMidiMap(),
      panning: new ControllerMidiMap(),
      polyphony: new ControllerMidiMap(),
      bassVolume: new ControllerMidiMap(),
      bassPower: new ControllerMidiMap(),
      bassTone: new ControllerMidiMap(),
      bassLength: new ControllerMidiMap(),
      hihatVolume: new ControllerMidiMap(),
      hihatLength: new ControllerMidiMap(),
      snareVolume: new ControllerMidiMap(),
      snareTone: new ControllerMidiMap(),
      snareLength: new ControllerMidiMap(),
      bassPanning: new ControllerMidiMap(),
      hihatPanning: new ControllerMidiMap(),
      snarePanning: new ControllerMidiMap(),
    }
    readonly optionValues: DrumSynthOptionValues = {}
    readonly options: DrumSynthOptions = new DrumSynthOptions(this.optionValues)
    readonly o = this.options
    behavior?: DrumSynthBehavior
    constructor() {
      super()
      this.behavior = new DrumSynthBehavior(this)
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
          cv.panning = value
          break
        case 3:
          cv.polyphony = value
          break
        case 4:
          cv.bassVolume = value
          break
        case 5:
          cv.bassPower = value
          break
        case 6:
          cv.bassTone = value
          break
        case 7:
          cv.bassLength = value
          break
        case 8:
          cv.hihatVolume = value
          break
        case 9:
          cv.hihatLength = value
          break
        case 10:
          cv.snareVolume = value
          break
        case 11:
          cv.snareTone = value
          break
        case 12:
          cv.snareLength = value
          break
        case 13:
          cv.bassPanning = value
          break
        case 14:
          cv.hihatPanning = value
          break
        case 15:
          cv.snarePanning = value
          break
      }
    }
    *rawControllerValues(): Generator<number> {
      const { controllerValues: cv } = this
      yield cv.volume
      yield cv.panning
      yield cv.polyphony
      yield cv.bassVolume
      yield cv.bassPower
      yield cv.bassTone
      yield cv.bassLength
      yield cv.hihatVolume
      yield cv.hihatLength
      yield cv.snareVolume
      yield cv.snareTone
      yield cv.snareLength
      yield cv.bassPanning
      yield cv.hihatPanning
      yield cv.snarePanning
    }
    setMidiMaps(midiMaps: MidiMap[]) {
      this.midiMaps.volume = midiMaps[0] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.panning = midiMaps[1] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.polyphony = midiMaps[2] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.bassVolume = midiMaps[3] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.bassPower = midiMaps[4] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.bassTone = midiMaps[5] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.bassLength = midiMaps[6] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.hihatVolume = midiMaps[7] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.hihatLength = midiMaps[8] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.snareVolume = midiMaps[9] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.snareTone = midiMaps[10] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.snareLength = midiMaps[11] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.bassPanning = midiMaps[12] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.hihatPanning = midiMaps[13] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
      this.midiMaps.snarePanning = midiMaps[14] || {
        channel: 0,
        messageType: 0,
        messageParameter: 0,
        slope: 0,
      }
    }
    midiMapsArray(): MidiMap[] {
      const a: MidiMap[] = []
      a.push(this.midiMaps.volume)
      a.push(this.midiMaps.panning)
      a.push(this.midiMaps.polyphony)
      a.push(this.midiMaps.bassVolume)
      a.push(this.midiMaps.bassPower)
      a.push(this.midiMaps.bassTone)
      a.push(this.midiMaps.bassLength)
      a.push(this.midiMaps.hihatVolume)
      a.push(this.midiMaps.hihatLength)
      a.push(this.midiMaps.snareVolume)
      a.push(this.midiMaps.snareTone)
      a.push(this.midiMaps.snareLength)
      a.push(this.midiMaps.bassPanning)
      a.push(this.midiMaps.hihatPanning)
      a.push(this.midiMaps.snarePanning)
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
