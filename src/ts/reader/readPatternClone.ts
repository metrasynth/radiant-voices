import { Chunk, Int32Chunk, Uint32Chunk } from "../chunks/chunk"
import { Event, PatternClone } from "../pattern"

interface HandlerContext {
  events?: Event[]
  tracks?: number
  lines?: number
}

interface HandlerFunc {
  (
    pattern: PatternClone | undefined,
    chunk: Chunk,
    chunks: Generator<Chunk>,
    ctx: HandlerContext
  ): boolean | PatternClone | void
}

const handlers: Record<string, HandlerFunc> = {
  PEND: () => true,
  PFFF: (pattern, chunk) => {
    ;(pattern as PatternClone).flags = (chunk as Uint32Chunk).value
  },
  PPAR: (pattern, chunk) => {
    const { value: source } = chunk as Uint32Chunk
    pattern = new PatternClone(source)
    return pattern
  },
  PXXX: (pattern, chunk) => {
    ;(pattern as PatternClone).x = (chunk as Int32Chunk).value
  },
  PYYY: (pattern, chunk) => {
    ;(pattern as PatternClone).y = (chunk as Int32Chunk).value
  },
}

export function readPatternClone(
  index: number | null,
  chunks: Generator<Chunk>,
  chunk: Chunk
): PatternClone {
  const ctx: HandlerContext = {}
  let pattern: PatternClone | undefined = undefined
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
      } else if (result instanceof PatternClone) {
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
