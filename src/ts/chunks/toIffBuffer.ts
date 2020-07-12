import DataStream from "datastream-js"
import encoding from "./encoding"
import {
  BytesChunk,
  Chunk,
  ColorChunk,
  CStringChunk,
  EventsChunk,
  FixedStringChunk,
  LinksChunk,
  MidiMapsChunk,
  Uint32Chunk,
  VersionChunk,
} from "./chunk"
import { MessageType } from "../controllerMidiMap"

interface WriterFunc {
  (ds: DataStream, chunk: Chunk): void
}

const writerFuncs: Record<string, WriterFunc> = {
  bytes: (ds, chunk) => {
    const { value } = chunk as BytesChunk
    ds.writeUint32(value.length)
    ds.writeUint8Array(value)
  },
  color: (ds, chunk) => {
    const [r, g, b] = (chunk as ColorChunk).value
    ds.writeUint32(3)
    ds.writeUint8(r)
    ds.writeUint8(g)
    ds.writeUint8(b)
  },
  cstring: (ds, chunk) => {
    const { value } = chunk as CStringChunk
    ds.writeUint32(value.length + 1) // TODO - encode to utf8 first, then get length
    ds.writeString(value, encoding, value.length)
    ds.writeUint8(0)
  },
  empty: (ds) => {
    ds.writeUint32(0)
  },
  events: (ds, chunk) => {
    const { values } = chunk as EventsChunk
    ds.writeUint32(values.length * 8)
    for (const { note, velocity, module, controller, effect, parameter } of values) {
      ds.writeUint8(note)
      ds.writeUint8(velocity)
      ds.writeUint16(module)
      ds.writeUint8(effect)
      ds.writeUint8(controller)
      ds.writeUint16(parameter)
    }
  },
  fixedString: (ds, chunk) => {
    ds.writeUint32(32)
    const { value } = chunk as FixedStringChunk
    const enc = new TextEncoder().encode(value)
    if (enc.length >= 32) {
      ds.writeUint8Array(enc.subarray(0, 32))
    } else {
      ds.writeUint8Array(enc)
      ds.writeString("", "ASCII", 32 - enc.length)
    }
  },
  int32: (ds, chunk) => {
    const { value } = chunk as Uint32Chunk
    ds.writeUint32(4)
    ds.writeInt32(value)
  },
  links: (ds, chunk) => {
    const { values } = chunk as LinksChunk
    ds.writeUint32((values.length + 1) * 4)
    for (const link of values) {
      ds.writeInt32(link)
    }
    ds.writeInt32(-1)
  },
  midiMaps: (ds, chunk) => {
    const { values } = chunk as MidiMapsChunk
    ds.writeUint32(8 * values.length)
    for (const { channel, messageType, messageParameter, slope } of values) {
      ds.writeUint8(messageType)
      ds.writeUint8(channel)
      ds.writeUint8(slope)
      ds.writeUint8(0)
      ds.writeUint16(messageParameter)
      ds.writeUint8(0)
      ds.writeUint8(messageType === MessageType.Unset ? 0xff : 0xc8)
    }
  },
  // links: (ds, value) => {
  //   ds.writeUint32(value.length * 4)
  //   for (const x of value) {
  //     ds.writeInt32(x)
  //   }
  // },
  // moduleFlags: (ds, value) => {
  //   ds.writeUint32(4)
  //   ds.writeUint32(value.toUint32())
  // },
  // patternAppearanceFlags: (ds, value) => {
  //   ds.writeUint32(4)
  //   ds.writeUint32(value.toUint32())
  // },
  // patternFlags: (ds, value) => {
  //   ds.writeUint32(4)
  //   ds.writeUint32(value.toUint32())
  // },
  uint32: (ds, chunk) => {
    const { value } = chunk as Uint32Chunk
    ds.writeUint32(4)
    ds.writeUint32(value)
  },
  version: (ds, chunk) => {
    ds.writeUint32(4)
    const {
      value: [major, minor, point, patch],
    } = chunk as VersionChunk
    ds.writeUint8(patch)
    ds.writeUint8(point)
    ds.writeUint8(minor)
    ds.writeUint8(major)
  },
}

export function toIffBuffer(chunks: Iterable<Chunk>): DataStream {
  const ds = new DataStream()
  for (const chunk of chunks) {
    const { name, type } = chunk
    ds.writeString(name, encoding, 4)
    const writerFunc = writerFuncs[type]
    writerFunc(ds, chunk)
  }
  ds.position = 0
  return ds
}
