import { Chunk, VersionChunk } from "../chunks/chunk"
import { readModule } from "./readModule"
import { Synth } from "../synth"
import { ModuleBase } from "../modtypes/moduleBase"
import { SunVoxVersion } from "../sunVoxVersion"

interface HandlerContext {
  module?: ModuleBase
  sunVoxVersion: SunVoxVersion
}

interface HandlerFunc {
  (chunk: Chunk, chunks: Generator<Chunk>, ctx: HandlerContext): void
}

const handlers: Record<string, HandlerFunc> = {
  SFFF: (chunk, chunks, ctx) => {
    ctx.module = readModule(undefined, chunks, chunk)
  },
  VERS: (chunk, _, ctx) => {
    ctx.sunVoxVersion = (chunk as VersionChunk).value
  },
}

export function readSynth(chunks: Generator<Chunk>): Synth {
  const ctx: HandlerContext = { sunVoxVersion: [0, 0, 0, 0] }
  for (const chunk of chunks) {
    const { name } = chunk
    const handler = handlers[name]
    if (handler) {
      handler(chunk, chunks, ctx)
    } else {
      // console.warn(`No handler for chunk ${name}`)
    }
  }
  if (!ctx.module) {
    throw new Error("Did not find module in sunsynth container")
  }
  const synth = new Synth(ctx.module)
  synth.sunVoxVersion = ctx.sunVoxVersion
  return synth
}
