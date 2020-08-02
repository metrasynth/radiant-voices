import { ModuleSpecificBehavior } from "./moduleSpecificBehavior"
import { Project } from "../project"
import { ModuleDataChunk, ModuleDataChunks } from "../moduleDataChunk"
import { Chunk } from "../chunks/chunk"
import { fromIffBuffer } from "../chunks/fromIffBuffer"
import { toIffBuffer } from "../chunks/toIffBuffer"
import { objectChunks } from "../writer/objectChunks"
import { readSunVoxFile } from "../reader/readSunVoxFile"

export class MetaModuleBehavior extends ModuleSpecificBehavior {
  project?: Project
  readonly mappings = defaultMappings()
  readonly controllerNames: Array<string | undefined> = Array.from(
    defaultControllerNames
  )

  chnk(): number {
    return 8 + 27
  }

  processDataChunks(dataChunks: ModuleDataChunks) {
    for (const dataChunk of dataChunks) {
      switch (dataChunk.chnm) {
        case 0:
          this.processProjectData(dataChunk)
          continue
        case 1:
          this.processMappingData(dataChunk)
          continue
      }
      if (dataChunk.chnm >= 8) {
        this.processControllerName(dataChunk)
      }
    }
  }

  private processProjectData(dataChunk: ModuleDataChunk) {
    const { chdt } = dataChunk
    if (!chdt) return
    this.project = readSunVoxFile(fromIffBuffer(chdt.buffer)) as Project
  }

  private processMappingData(dataChunk: ModuleDataChunk) {
    const { chdt } = dataChunk
    if (!chdt) return
    const rawValues = new Uint16Array(chdt.buffer, chdt.byteOffset)
    for (let i = 0; i < 64; ++i) {
      const mapping = this.mappings[i]
      mapping.module = rawValues[i * 2]
      mapping.controller = rawValues[i * 2 + 1]
    }
  }

  private processControllerName(dataChunk: ModuleDataChunk) {
    let { chnm, chdt } = dataChunk
    if (!chdt) return
    const index = chnm - 8
    if (chdt[chdt.length - 1] == 0) {
      chdt = new Uint8Array(chdt.buffer, chdt.byteOffset, chdt.length - 1)
    }
    this.controllerNames[index] = new TextDecoder().decode(chdt)
  }

  *typeSpecificChunks(): Generator<Chunk> {
    if (this.project) {
      const f = toIffBuffer(objectChunks(this.project))
      yield { name: "CHNM", type: "uint32", value: 0 }
      yield { name: "CHDT", type: "bytes", value: new Uint8Array(f.buffer) }
    }

    const rawValues = new Uint16Array(64 * 2)
    for (let i = 0; i < 64; ++i) {
      const mapping = this.mappings[i]
      rawValues[i * 2] = mapping.module
      rawValues[i * 2 + 1] = mapping.controller
    }

    yield { name: "CHNM", type: "uint32", value: 1 }
    yield {
      name: "CHDT",
      type: "bytes",
      value: new Uint8Array(
        rawValues.buffer,
        rawValues.byteOffset,
        rawValues.byteLength
      ),
    }

    const { controllerNames } = this
    for (let i = 0; i < 27; ++i) {
      const name = controllerNames[i]
      if (name !== undefined) {
        yield { name: "CHNM", type: "uint32", value: 8 + i }
        yield { name: "CHDT", type: "cstring", value: name }
      }
    }
  }
}

interface Mapping {
  module: number
  controller: number
}

function defaultMappings(): Mapping[] {
  return [
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
    { module: 0, controller: 0 },
  ]
}

const defaultControllerNames = [
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
]
