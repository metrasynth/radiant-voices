import { ModuleDataChunks } from "../moduleDataChunk"
import { ModuleSpecificBehavior } from "./moduleSpecificBehavior"
import { Color } from "../color"
import { ControllerMidiMaps, MidiMap } from "../controllerMidiMap"
import { Project } from "../project"
import { Linkable, Linkables } from "../links"

export class ModuleBase implements Linkable {
  private _index: number | undefined = undefined
  project?: Project
  name = ""
  typeName = ""
  flags = 0
  finetune = 0
  relativeNote = 0
  x = 512
  y = 512
  layer = 0
  scale = 256
  color: Color = [255, 255, 255]
  visualization: number = 0 // TODO defaults
  midiMaps: ControllerMidiMaps = {}
  midiInAlways: boolean = false
  midiInChannel: number = 0
  midiOutName?: string
  midiOutChannel: number = 0
  midiOutBank?: number
  midiOutProgram?: number
  incomingLinks: number[] = []
  readonly optionsChnm?: number
  behavior?: ModuleSpecificBehavior

  get index(): number | undefined {
    if (this._index === undefined) {
      throw new Error("Module index is not assigned")
    }
    return this._index
  }

  set index(newIndex: number | undefined) {
    if (this._index !== undefined) {
      throw new Error("Module index can only be assigned once")
    }
    this._index = newIndex
  }

  attachTo(project: Project): ModuleBase {
    project.attach(this)
    return this
  }

  chnk(): number {
    const chnk = this.behavior?.chnk
    return chnk ? chnk() : 0
  }

  linkFrom(other: Linkable | Linkable[]): Linkable {
    if (this.index === undefined) {
      throw new Error("Module must be attached to a project to establish links")
    }
    const o = other instanceof Array ? new Linkables(other) : other
    if (o instanceof ModuleBase) {
      if (o.index === undefined) {
        throw new Error("Module must be attached to a project to establish links")
      }
      const existingLink = this.incomingLinks.find((x) => x === o.index)
      if (existingLink === undefined) {
        this.incomingLinks.push(o.index)
      }
      return o
    } else if (o instanceof Linkables) {
      for (const linkable of o.members) {
        this.linkFrom(linkable)
      }
      return o
    } else {
      throw new Error(`Unsupported object ${typeof other}`)
    }
  }

  linkTo(other: Linkable | Linkable[]): Linkable {
    if (this.index === undefined) {
      throw new Error("Module must be attached to a project to establish links")
    }
    const o = other instanceof Array ? new Linkables(other) : other
    if (o instanceof ModuleBase) {
      if (o.index === undefined) {
        throw new Error("Module must be attached to a project to establish links")
      }
      const existingLink = o.incomingLinks.find((x) => x === this.index)
      if (existingLink === undefined) {
        o.incomingLinks.push(this.index)
      }
      return o
    } else if (o instanceof Linkables) {
      for (const linkable of o.members) {
        this.linkTo(linkable)
      }
      return o
    } else {
      throw new Error(`Unsupported object ${typeof other}`)
    }
  }

  midiMapsArray(): MidiMap[] {
    return []
  }

  processDataChunks(dataChunks: ModuleDataChunks) {
    this.setOptions(dataChunks)
    this.behavior?.processDataChunks(dataChunks)
  }

  *rawControllerValues(): Generator<number> {}

  rawOptionBytes(): Uint8Array {
    return new Uint8Array(0)
  }

  setMidiMaps(midiMaps: MidiMap[]) {}

  setOptions(dataChunks: ModuleDataChunks) {}
}

export interface ModuleConstructor {
  new (): ModuleBase
}
