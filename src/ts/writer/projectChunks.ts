// import { chunks } from './index'
//
import { Project } from "../project"
import { Chunk } from "../chunks/chunk"
import { moduleChunks } from "./moduleChunks"
import { patternChunks } from "./patternChunks"

export function* projectChunks(project: Project): Generator<Chunk> {
  yield { name: "SVOX", type: "empty" }
  yield { name: "VERS", type: "version", value: project.sunVoxVersion }
  yield { name: "BVER", type: "version", value: project.basedOnVersion }
  if (project.flags) {
    yield { name: "FLGS", type: "uint32", value: project.flags }
  }
  yield {
    name: "SFGS",
    type: "uint32",
    value: project.receiveSyncMidi | (project.receiveSyncOther << 3),
  }
  yield { name: "BPM ", type: "uint32", value: project.initialBpm }
  yield { name: "SPED", type: "uint32", value: project.initialTpl }
  yield { name: "TGRD", type: "uint32", value: project.timeGrid }
  yield { name: "TGD2", type: "uint32", value: project.timeGrid2 }
  yield { name: "GVOL", type: "uint32", value: project.globalVolume }
  yield { name: "NAME", type: "cstring", value: project.name }
  yield { name: "MSCL", type: "uint32", value: project.modulesScale }
  yield { name: "MZOO", type: "uint32", value: project.modulesZoom }
  yield { name: "MXOF", type: "int32", value: project.modulesXOffset }
  yield { name: "MYOF", type: "int32", value: project.modulesYOffset }
  yield { name: "LMSK", type: "uint32", value: project.modulesLayerMask }
  yield { name: "CURL", type: "uint32", value: project.modulesCurrentLayer }
  yield { name: "TIME", type: "int32", value: project.timelinePosition }
  yield { name: "SELS", type: "uint32", value: project.selectedModule }
  yield { name: "LGEN", type: "uint32", value: project.lastSelectedGenerator }
  yield { name: "PATN", type: "uint32", value: project.currentPattern }
  yield { name: "PATT", type: "uint32", value: project.currentTrack }
  yield { name: "PATL", type: "uint32", value: project.currentLine }

  for (let pattern of project.patterns) {
    if (pattern) {
      yield* patternChunks(pattern)
    }
    yield { name: "PEND", type: "empty" }
  }

  for (let module of project.modules) {
    if (module) {
      yield* moduleChunks(module)
    }
    yield { name: "SEND", type: "empty" }
  }
}
