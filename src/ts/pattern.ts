import { NoteCmd } from "./note"
import { Effect } from "./effect"
import { Color } from "./color"
import { Project } from "./project"

export interface Event {
  note: NoteCmd
  velocity: number
  module: number
  controller: number
  effect: Effect
  parameter: number
}

export type Line = Event[]

export type PatternData = Line[]

export enum PatternAppearanceFlags {
  NoIcon = 1 << 0,
}

export enum PatternFlags {
  Clone = 1 << 0,
  Selected = 1 << 1,
  Mute = 1 << 3,
  Solo = 1 << 4,
}

export interface PatternCommon {
  project?: Project
  _index?: number
  parent?: number
  x: number
  y: number
  flags: PatternFlags
}

export class Pattern implements PatternCommon {
  readonly parent = undefined
  project?: Project
  _index?: number
  name?: string
  x = 0
  y = 0
  flags = 0
  tracks = 4
  lines = 32
  ySize = 32
  appearance = 0
  icon = new Uint8Array(32)
  fgColor: Color = [0, 0, 0]
  bgColor: Color = [255, 255, 255]
  data: PatternData

  constructor(lines = 32, tracks = 4, events?: Event[]) {
    this.tracks = tracks
    this.lines = lines
    this.data = this.initData(events)
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

export class PatternClone implements PatternCommon {
  project?: Project
  _index?: number
  flags = PatternFlags.Clone
  x = 0
  y = 0
  constructor(readonly parent: number) {}
}
