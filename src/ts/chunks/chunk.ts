import { Color } from "../color"
import { Event } from "../pattern"
import { SunVoxVersion } from "../sunVoxVersion"
import { MidiMap } from "../controllerMidiMap"

export interface BytesChunk {
  name: string
  type: "bytes"
  value: Uint8Array
}

export interface ColorChunk {
  name: string
  type: "color"
  value: Color
}

export interface CStringChunk {
  name: string
  type: "cstring"
  value: string
}

export interface EmptyChunk {
  name: string
  type: "empty"
}

export interface EventsChunk {
  name: string
  type: "events"
  values: Event[]
}

export interface FixedStringChunk {
  name: string
  type: "fixedString"
  value: string
}

export interface Int32Chunk {
  name: string
  type: "int32"
  value: number
}

export interface LinksChunk {
  name: string
  type: "links"
  values: number[]
}

export interface MidiMapsChunk {
  name: string
  type: "midiMaps"
  values: MidiMap[]
}

export interface RawChunk {
  name: string
  type: "raw"
  raw: Uint8Array
}

export interface VersionChunk {
  name: string
  type: "version"
  value: SunVoxVersion
}

export interface Uint32Chunk {
  name: string
  type: "uint32"
  value: number
}

export type Chunk =
  | BytesChunk
  | ColorChunk
  | CStringChunk
  | EmptyChunk
  | EventsChunk
  | FixedStringChunk
  | Int32Chunk
  | LinksChunk
  | MidiMapsChunk
  | RawChunk
  | VersionChunk
  | Uint32Chunk
