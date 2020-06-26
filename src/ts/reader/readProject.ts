import {
  Chunk,
  CStringChunk,
  Int32Chunk,
  Uint32Chunk,
  VersionChunk,
} from "../chunks/chunk"
import { Project } from "../project"
import { readModule } from "./readModule"
import { readPattern } from "./readPattern"
import { readPatternClone } from "./readPatternClone"

interface HandlerFunc {
  (project: Project, chunk: Chunk, chunks: Generator<Chunk>): void
}

const handlers: Record<string, HandlerFunc> = {
  "BPM ": (project, chunk) => {
    project.initialBpm = (chunk as Uint32Chunk).value
  },
  BVER: (project, chunk) => {
    project.basedOnVersion = (chunk as VersionChunk).value
  },
  CURL: (project, chunk) => {
    project.modulesCurrentLayer = (chunk as Uint32Chunk).value
  },
  GVOL: (project, chunk) => {
    project.globalVolume = (chunk as Uint32Chunk).value
  },
  LGEN: (project, chunk) => {
    project.lastSelectedGenerator = (chunk as Uint32Chunk).value
  },
  LMSK: (project, chunk) => {
    project.modulesLayerMask = (chunk as Uint32Chunk).value
  },
  MSCL: (project, chunk) => {
    project.modulesScale = (chunk as Uint32Chunk).value
  },
  MXOF: (project, chunk) => {
    project.modulesXOffset = (chunk as Int32Chunk).value
  },
  MYOF: (project, chunk) => {
    project.modulesYOffset = (chunk as Int32Chunk).value
  },
  MZOO: (project, chunk) => {
    project.modulesZoom = (chunk as Uint32Chunk).value
  },
  PATN: (project, chunk) => {
    project.currentPattern = (chunk as Uint32Chunk).value
  },
  PATT: (project, chunk) => {
    project.currentTrack = (chunk as Uint32Chunk).value
  },
  PATL: (project, chunk) => {
    project.currentLine = (chunk as Uint32Chunk).value
  },
  PDTA: (project, chunk, chunks) => {
    const pattern = readPattern(project.patterns.length, chunks, chunk)
    pattern.project = project
    project.patterns.push(pattern)
  },
  PEND: (project) => {
    project.patterns.push(undefined)
  },
  PPAR: (project, chunk, chunks) => {
    const pattern = readPatternClone(project.patterns.length, chunks, chunk)
    pattern.project = project
    project.patterns.push(pattern)
  },
  SELS: (project, chunk) => {
    project.selectedModule = (chunk as Uint32Chunk).value
  },
  SEND: (project) => {
    project.modules.push(undefined)
  },
  NAME: (project, chunk) => {
    project.name = (chunk as CStringChunk).value
  },
  SFGS: (project, chunk) => {
    const { value } = chunk as Uint32Chunk
    project.receiveSyncMidi = value & 0b111
    project.receiveSyncOther = (value >> 3) & 0b111
  },
  SFFF: (project, chunk, chunks) => {
    const module = readModule(project.modules.length, chunks, chunk)
    module.project = project
    project.modules.push(module)
  },
  SPED: (project, chunk) => {
    project.initialTpl = (chunk as Uint32Chunk).value
  },
  TGD2: (project, chunk) => {
    project.timeGrid2 = (chunk as Uint32Chunk).value
  },
  TGRD: (project, chunk) => {
    project.timeGrid = (chunk as Uint32Chunk).value
  },
  TIME: (project, chunk) => {
    project.timelinePosition = (chunk as Int32Chunk).value
  },
  VERS: (project, chunk) => {
    project.sunVoxVersion = (chunk as VersionChunk).value
  },
}

export function readProject(chunks: Generator<Chunk>): Project {
  const project = new Project()
  project.modules.length = 0
  for (const chunk of chunks) {
    const { name } = chunk
    const handler = handlers[name]
    if (handler) {
      handler(project, chunk, chunks)
    } else {
      // console.warn(`No handler for chunk ${name}`)
    }
  }
  return project
}
