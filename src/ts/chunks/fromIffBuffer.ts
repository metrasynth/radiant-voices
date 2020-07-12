import DataStream from "datastream-js"
import { chunkTypes } from "./chunkTypes"
import encoding from "./encoding"
import { Chunk } from "./chunk"
import { MessageType, MidiMap, Slope } from "../controllerMidiMap"
import { Event } from "../pattern"
import { NoteCmd } from "../note"
import { Effect } from "../effect"

interface TransformerFunc {
  (ds: DataStream, length: number): any
}

const transformers: Record<string, TransformerFunc> = {
  bytes: (ds, length) => ({
    value: ds.readUint8Array(length),
  }),
  color: (ds) => ({
    value: [ds.readUint8(), ds.readUint8(), ds.readUint8()],
  }),
  cstring: (ds, length) => ({
    value: ds.readCString(length),
  }),
  empty: () => {},
  fixedString: (ds, length) => ({
    value: ds.readCString(length),
  }),
  events: (ds, length) => {
    const values: Event[] = []
    for (let idx = 0; idx < length / 8; ++idx) {
      const note = ds.readUint8() as NoteCmd
      const velocity = ds.readUint8()
      const module = ds.readUint16()
      const effect = ds.readUint8() as Effect
      const controller = ds.readUint8()
      const parameter = ds.readUint16()
      const event: Event = { note, velocity, module, controller, effect, parameter }
      values.push(event)
    }
    return { values }
  },
  int32: (ds) => ({ value: ds.readInt32() }),
  links: (ds, length) => {
    const values = Array.from(ds.readInt32Array(length / 4))
    while (values[values.length - 1] == -1) {
      values.length -= 1
    }
    return { values }
  },
  midiMaps: (ds, length) => {
    const midiMaps: MidiMap[] = []
    for (let idx = 0; idx < length / 8; ++idx) {
      const messageType = ds.readUint8() as MessageType
      const channel = ds.readUint8()
      const slope = ds.readUint8() as Slope
      ds.readUint8()
      const messageParameter = ds.readUint16()
      ds.readUint8()
      ds.readUint8()
      const midiMap: MidiMap = { channel, messageType, messageParameter, slope }
      midiMaps.push(midiMap)
    }
    return { values: midiMaps }
  },
  uint32: (ds) => ({ value: ds.readUint32() }),
  version: (ds) => {
    const patch = ds.readUint8()
    const point = ds.readUint8()
    const minor = ds.readUint8()
    const major = ds.readUint8()
    return { value: [major, minor, point, patch] }
  },
}

export function* fromIffBuffer(
  buffer: ArrayBuffer | DataStream,
  { raw = false } = {}
): Generator<Chunk> {
  const ds = new DataStream(buffer)
  while (!ds.isEof()) {
    const startPos = ds.position
    const name = ds.readString(4, encoding)
    const length = ds.readUint32()
    const chunkLength = length + 8
    const endPos = startPos + chunkLength
    const type = chunkTypes[name]
    const transformer = transformers[type]
    if (transformer !== undefined) {
      const value = transformer(ds, length)
      yield { type, name, ...value } as Chunk
    } else if (raw) {
      yield { name, type: "raw", raw: ds.readUint8Array(length) }
    }
    ds.position = endPos
  }
}
