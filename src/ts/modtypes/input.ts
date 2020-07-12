/**
 * -- DO NOT EDIT THIS FILE DIRECTLY --
 *
 * This file was auto-generated by genrv.
 */
import { MidiMap, ControllerMidiMap, ControllerMidiMaps } from "../controllerMidiMap"
import { ModuleBase } from "./moduleBase"
import {
  ControllerValues,
  Controllers,
  ModuleType,
  OptionValues,
  Options,
} from "./moduleType"
import { InputBehavior } from "./inputBehavior"
export namespace Input {
  export const enum Channels {
    // noinspection JSUnusedGlobalSymbols
    Mono = 0,
    Stereo = 1,
  }
  interface InputControllerValues extends ControllerValues {
    volume: number
    channels: Channels
  }
  class InputControllers implements Controllers {
    constructor(readonly controllerValues: InputControllerValues) {}
    // noinspection JSUnusedGlobalSymbols
    get volume(): number {
      return this.controllerValues.volume
    }
    // noinspection JSUnusedGlobalSymbols
    set volume(newValue: number) {
      const { controllerValues } = this
      newValue = Math.min(Math.max(newValue, 0), 1024)
      controllerValues.volume = newValue
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
  }
  interface InputControllerMidiMaps extends ControllerMidiMaps {
    volume: ControllerMidiMap
    channels: ControllerMidiMap
  }
  interface InputOptionValues extends OptionValues {}
  class InputOptions implements Options {
    constructor(readonly optionValues: InputOptionValues) {}
  }
  export class Module extends ModuleBase implements ModuleType {
    name = "Input"
    flags = 0
    readonly typeName = "Input"
    readonly controllerSetters = [
      (val: number) => {
        this.controllerValues.volume = val
      },
      (val: number) => {
        this.controllerValues.channels = val
      },
    ]
    readonly controllerValues: InputControllerValues = {
      volume: 256,
      channels: Channels.Mono,
    }
    readonly controllers: InputControllers = new InputControllers(this.controllerValues)
    readonly c = this.controllers
    readonly midiMaps: InputControllerMidiMaps = {
      volume: new ControllerMidiMap(),
      channels: new ControllerMidiMap(),
    }
    readonly optionValues: InputOptionValues = {}
    readonly options: InputOptions = new InputOptions(this.optionValues)
    readonly o = this.options
    behavior?: InputBehavior
    constructor() {
      super()
      this.behavior = new InputBehavior(this)
    }
    *rawControllerValues(): Generator<number> {
      const { controllerValues: cv } = this
      yield cv.volume
      yield cv.channels
    }
    setMidiMaps(midiMaps: MidiMap[]) {
      this.midiMaps.volume = midiMaps[0]
      this.midiMaps.channels = midiMaps[1]
    }
    midiMapsArray(): MidiMap[] {
      const a: MidiMap[] = []
      a.push(this.midiMaps.volume)
      a.push(this.midiMaps.channels)
      return a
    }
  }
}