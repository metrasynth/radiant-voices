import {
  BytesChunk,
  Chunk,
  ColorChunk,
  CStringChunk,
  Int32Chunk,
  LinksChunk,
  MidiMapsChunk,
  Uint32Chunk,
} from "../chunks/chunk"
import { m, ModuleType } from "../modtypes"
import { ModuleDataChunk, ModuleDataChunks } from "../moduleDataChunk"
import { ModuleBase } from "../modtypes/moduleBase"

interface ModulePlaceholder {
  index: number | null
  flags: number
  name?: string
}

interface HandlerContext {
  ctlIndex: number
  dataChunks: ModuleDataChunks
  currentDataChunk?: ModuleDataChunk
}

interface HandlerFunc {
  (
    module: ModuleBase | ModulePlaceholder,
    chunk: Chunk,
    chunks: Generator<Chunk>,
    ctx: HandlerContext
  ): boolean | ModuleBase | void
}

const handlers: Record<string, HandlerFunc> = {
  CMID: (module, chunk) => {
    const midiMaps = (chunk as MidiMapsChunk).values
    ;(module as ModuleBase).setMidiMaps(midiMaps)
  },
  CHNK: () =>
    // Do nothing; CHNK is used to allocate memory in SunVox.
    // For reading files in radiant-voices, we can ignore it.
    undefined,
  CHNM: (module, chunk, chunks, ctx) => {
    const dataChunk: ModuleDataChunk = { chnm: (chunk as Uint32Chunk).value }
    ctx.dataChunks.push(dataChunk)
    ctx.currentDataChunk = dataChunk
  },
  CHDT: (module, chunk, chunks, ctx) => {
    if (ctx.currentDataChunk) {
      ctx.currentDataChunk.chdt = (chunk as BytesChunk).value
    }
  },
  CVAL: (module, chunk, chunks, ctx) => {
    const cval = (chunk as Uint32Chunk).value
    const controllerSetter = ((module as unknown) as ModuleType).controllerSetters[
      ctx.ctlIndex
    ]
    controllerSetter(cval as number)
    ctx.ctlIndex += 1
  },
  SEND: (module, chunk, chunks, ctx) => {
    ;(module as ModuleBase).processDataChunks(ctx.dataChunks)
    return true
  },
  SFIN: (module, chunk) => {
    ;(module as ModuleBase).finetune = (chunk as Int32Chunk).value
  },
  SLNK: (module, chunk) => {
    ;(module as ModuleBase).incomingLinks = (chunk as LinksChunk).values
  },
  SMIB: (module, chunk) => {
    const { value } = chunk as Int32Chunk
    ;(module as ModuleBase).midiOutBank = value > -1 ? value : undefined
  },
  SMIC: (module, chunk) => {
    ;(module as ModuleBase).midiOutChannel = (chunk as Uint32Chunk).value
  },
  SMII: (module, chunk) => {
    const m = module as ModuleBase
    const v = (chunk as Uint32Chunk).value
    m.midiInAlways = (v & 1) === 1
    m.midiInChannel = v >> 1
  },
  SMIN: (module, chunk) => {
    ;(module as ModuleBase).midiOutName = (chunk as CStringChunk).value
  },
  SMIP: (module, chunk) => {
    const { value } = chunk as Int32Chunk
    ;(module as ModuleBase).midiOutProgram = value > -1 ? value : undefined
  },
  SNAM: (placeholder, chunk) => {
    ;(placeholder as ModulePlaceholder).name = (chunk as CStringChunk).value
  },
  SREL: (module, chunk) => {
    ;(module as ModuleBase).relativeNote = (chunk as Int32Chunk).value
  },
  SSCL: (module, chunk) => {
    ;(module as ModuleBase).scale = (chunk as Uint32Chunk).value
  },
  SCOL: (module, chunk) => {
    ;(module as ModuleBase).color = (chunk as ColorChunk).value
  },
  STYP: (placeholder, chunk) => {
    const type = (chunk as CStringChunk).value
    if (placeholder instanceof ModuleBase) {
      console.warn("Module type already determined")
      return placeholder
    }
    const module = new m.moduleTypesByName[type]()
    module.index = placeholder.index
    module.flags = placeholder.flags
    module.name = placeholder.name as string
    return module
  },
  SVPR: (module, chunk) => {
    ;(module as ModuleBase).visualization = (chunk as Uint32Chunk).value
  },
  SXXX: (module, chunk) => {
    ;(module as ModuleBase).x = (chunk as Int32Chunk).value
  },
  SYYY: (module, chunk) => {
    ;(module as ModuleBase).y = (chunk as Int32Chunk).value
  },
  SZZZ: (module, chunk) => {
    ;(module as ModuleBase).layer = (chunk as Uint32Chunk).value
  },
}

export function readModule(
  index: number | null,
  chunks: Generator<Chunk>,
  chunk: Chunk
): ModuleBase {
  const ctx: HandlerContext = { ctlIndex: 0, dataChunks: [] }
  const flags = (chunk as Uint32Chunk).value
  let placeholder: ModulePlaceholder = { index, flags }
  let module: ModuleBase | undefined
  const isOutputModule = index === 0
  if (isOutputModule) {
    module = m.output()
    module.index = index
    module.flags = flags
  }
  while (true) {
    const next = chunks.next()
    const { value: chunk, done } = next
    if (done) {
      throw new Error("Unexpected end of file")
    }
    const { name } = chunk
    const handler = handlers[name]
    if (handler) {
      let result
      if (module instanceof ModuleBase) {
        result = handler(module, chunk, chunks, ctx)
        if (result === true) {
          return module
        }
      } else {
        result = handler(placeholder, chunk, chunks, ctx)
        if (result instanceof ModuleBase) {
          module = result
        }
      }
    }
  }
}
