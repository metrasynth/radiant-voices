import {
  BytesChunk,
  Chunk,
  ColorChunk,
  EventsChunk,
  Int32Chunk,
  Uint32Chunk,
} from "../chunks/chunk"
import { Event, Pattern } from "../pattern"

interface HandlerContext {
  events?: Event[]
  tracks?: number
  lines?: number
}

interface HandlerFunc {
  (
    pattern: Pattern | undefined,
    chunk: Chunk,
    chunks: Generator<Chunk>,
    ctx: HandlerContext
  ): boolean | Pattern | void
}

const handlers: Record<string, HandlerFunc> = {
  PBGC: (pattern, chunk) => {
    ;(pattern as Pattern).bgColor = (chunk as ColorChunk).value
  },
  PCHN: (pattern, chunk, chunks, ctx) => {
    const { value } = chunk as Uint32Chunk
    ctx.tracks = value
    if (ctx.lines !== undefined && ctx.events) {
      const { tracks, lines, events } = ctx
      return new Pattern(tracks, lines, events)
    } else {
      return
    }
  },
  PDTA: (pattern, chunk, chunks, ctx) => {
    const { values: events } = chunk as EventsChunk
    ctx.events = events
  },
  PEND: () => true,
  PFFF: (pattern, chunk) => {
    ;(pattern as Pattern).flags = (chunk as Uint32Chunk).value
  },
  PFGC: (pattern, chunk) => {
    ;(pattern as Pattern).fgColor = (chunk as ColorChunk).value
  },
  PFLG: (pattern, chunk) => {
    ;(pattern as Pattern).appearance = (chunk as Uint32Chunk).value
  },
  PICO: (pattern, chunk) => {
    ;(pattern as Pattern).icon = (chunk as BytesChunk).value
  },
  PLIN: (pattern, chunk, chunks, ctx) => {
    const { value } = chunk as Uint32Chunk
    ctx.lines = value
    if (ctx.tracks !== undefined && ctx.events) {
      const { tracks, lines, events } = ctx
      return new Pattern(lines, tracks, events)
    } else {
      return
    }
  },
  PXXX: (pattern, chunk) => {
    ;(pattern as Pattern).x = (chunk as Int32Chunk).value
  },
  PYSZ: (pattern, chunk) => {
    ;(pattern as Pattern).ySize = (chunk as Uint32Chunk).value
  },
  PYYY: (pattern, chunk) => {
    ;(pattern as Pattern).y = (chunk as Int32Chunk).value
  },
}

export function readPattern(
  index: number | null,
  chunks: Generator<Chunk>,
  chunk: Chunk
): Pattern {
  const ctx: HandlerContext = {}
  let pattern: Pattern | undefined = undefined
  while (true) {
    const { name } = chunk
    const handler = handlers[name]
    if (handler) {
      const result = handler(pattern, chunk, chunks, ctx)
      if (result === true) {
        if (pattern) {
          return pattern
        } else {
          throw new Error("Pattern finished without being defined")
        }
      } else if (result instanceof Pattern) {
        pattern = result
      }
    }
    const next = chunks.next()
    const { value, done } = next
    if (done) {
      throw new Error("Unexpected end of file")
    }
    chunk = value
  }
}
