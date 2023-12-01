import { Note, NoteCmd } from "./note"
import { Effect } from "./effect"
import { Color } from "./color"
import { Project } from "./project"

export interface Event {
  note: Note | NoteCmd
  velocity: number
  module: number
  controller: number
  effect: Effect
  parameter: number
}

export type Line = Event[]

export type PatternData = Line[]

export enum PatternFlagsPFLG {
  NoIcon = 1 << 0,
  ContinueNotesAtEnd = 2 << 0,
}

export enum PatternFlagsPFFF {
  Clone = 1 << 0,
  Selected = 1 << 1,
  Mute = 1 << 3,
  Solo = 1 << 4,
}

export class PatternBase {
  project?: Project
  _index?: number
  parent?: number
  x = 0
  y = 0
  flagsPFFF: PatternFlagsPFFF = 0

  get index(): number | undefined {
    if (this._index === undefined) {
      throw new Error("Pattern index is not assigned")
    }
    return this._index
  }

  set index(newIndex: number | undefined) {
    if (this._index !== undefined) {
      throw new Error("Module index can only be assigned once")
    }
    this._index = newIndex
  }

  attachTo(project: Project): PatternBase {
    project.attach(this)
    return this
  }
}

export class Pattern extends PatternBase {
  readonly parent = undefined
  name?: string
  tracks = 4
  lines = 32
  ySize = 32
  flagsPFLG: PatternFlagsPFLG = 0
  icon = new Uint8Array(32)
  fgColor: Color = [0, 0, 0]
  bgColor: Color = [255, 255, 255]
  data: PatternData

  constructor(lines = 32, tracks = 4, events?: Event[]) {
    super()
    this.tracks = tracks
    this.lines = lines
    this.data = this.initData(events)
  }

  attachTo(project: Project): Pattern {
    return super.attachTo(project) as Pattern
  }

  initData(events?: Event[]): PatternData {
    const data: PatternData = []
    const { lines, tracks } = this
    for (let lineIdx = 0; lineIdx < lines; ++lineIdx) {
      const line = []
      for (let trackIdx = 0; trackIdx < tracks; ++trackIdx) {
        const event: Event = events
          ? events[lineIdx * tracks + trackIdx]
          : {
              note: NoteCmd.Empty,
              velocity: 0,
              module: 0,
              controller: 0,
              effect: 0,
              parameter: 0,
            }
        line.push(event)
      }
      data.push(line)
    }
    return data
  }
}

export class PatternClone extends PatternBase {
  flagsPFFF = PatternFlagsPFFF.Clone
  constructor(readonly parent: number) {
    super()
  }

  attachTo(project: Project): PatternClone {
    return super.attachTo(project) as PatternClone
  }
}
