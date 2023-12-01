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
  FLGS: (project, chunk) => {
    project.flags = (chunk as Uint32Chunk).value
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
  initLinks(project)
  return project
}

/**
 * Initialize inLinkSlots, outLinks, and outLinkSlots after loading a project.
 *
 * https://www.warmplace.ru/forum/viewtopic.php?f=16&t=4850
 *
 * SLNK - input links of the cur_module;
 * SLNk - output links of the cur_module;
 * SLnK - slot numbers in the src_module;
 * SLnk - slot numbers in the dest_module;
 *
 * src_module1[ output slot S1 ] --> [ input slot 0 ]          [ output slot 0 ] --> [ input slot D1 ]dest_module1
 * src_module2[ output slot S2 ] --> [ input slot 1 ]cur_module[ output slot 1 ] --> [ input slot D2 ]dest_module2
 * src_module3[ output slot S3 ] --> [ input slot 2 ]          [ output slot 2 ] --> [ input slot D3 ]dest_module3
 *
 * SLNK: src_module1, src_module2, src_module3;
 * SLNk: dest_module1, dest_module2, dest_module3;
 * SLnK: S1, S2, S3;
 * SLnk: D1, D2, D3;
 */
function initLinks(project: Project): void {
  const modules = project.modules
  // inLinkSlots are not written out by SunVox if all zeros;
  // initialize them if missing.
  for (const mod of modules) {
    if (!mod) continue
    const { inLinks, inLinkSlots } = mod
    while (inLinkSlots.length < inLinks.length) {
      inLinkSlots.push(0)
    }
  }
  // generate outLinks based on inLinks
  for (const mod of modules) {
    if (!mod) continue
    const { inLinks, inLinkSlots } = mod
    if (!(inLinks && inLinkSlots)) {
      throw new Error() // [TODO] error message
    }
    for (const [inLinkIdx, inLink] of inLinks.entries()) {
      if (inLink === -1) {
        continue
      }
      const outLinkIdx = inLinkSlots[inLinkIdx]
      const srcMod = modules[inLink]
      if (!srcMod) {
        throw new Error() // [TODO] error message
      }
      const { outLinks, outLinkSlots } = srcMod
      if (!(outLinks && outLinkSlots)) {
        throw new Error() // [TODO] error message
      }
      outLinks[outLinkIdx] = mod.index
      outLinkSlots[outLinkIdx] = inLinkIdx
    }
  }
}
