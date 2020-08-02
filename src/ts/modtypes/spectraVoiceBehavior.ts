import { ModuleSpecificBehavior } from "./moduleSpecificBehavior"
import { SpectraVoice } from "./spectraVoice"
import { Chunk } from "@radiant-voices/chunks/chunk"
import { ModuleDataChunk, ModuleDataChunks } from "@radiant-voices/moduleDataChunk"

export class SpectraVoiceBehavior extends ModuleSpecificBehavior {
  harmonicFrequencies = Uint16Array.from(defaultHarmonicFrequencies)
  harmonicVolumes = Uint8Array.from(defaultHarmonicVolumes)
  harmonicWidths = Uint8Array.from(defaultHarmonicWidths)
  harmonicTypes: SpectraVoice.HarmonicType[] = Array.from(defaultHarmonicTypes)

  chnk(): number {
    return 4
  }

  processDataChunks(dataChunks: ModuleDataChunks) {
    for (const dataChunk of dataChunks) {
      switch (dataChunk.chnm) {
        case 0:
          this.processHarmonicFrequenciesChunk(dataChunk)
          continue
        case 1:
          this.processHarmonicVolumesChunk(dataChunk)
          continue
        case 2:
          this.processHarmonicWidthsChunk(dataChunk)
          continue
        case 3:
          this.processHarmonicTypesChunk(dataChunk)
      }
    }
  }

  private processHarmonicFrequenciesChunk(dataChunk: ModuleDataChunk) {
    const { chdt } = dataChunk
    if (chdt) {
      this.harmonicFrequencies = new Uint16Array(chdt.buffer, chdt.byteOffset)
    }
  }

  private processHarmonicVolumesChunk(dataChunk: ModuleDataChunk) {
    const { chdt } = dataChunk
    if (chdt) {
      this.harmonicVolumes = chdt
    }
  }
  private processHarmonicWidthsChunk(dataChunk: ModuleDataChunk) {
    const { chdt } = dataChunk
    if (chdt) {
      this.harmonicWidths = chdt
    }
  }
  private processHarmonicTypesChunk(dataChunk: ModuleDataChunk) {
    const { chdt } = dataChunk
    if (chdt) {
      this.harmonicTypes = Array.from(chdt)
    }
  }

  *typeSpecificChunks(): Generator<Chunk> {
    yield { name: "CHNM", type: "uint32", value: 0 }
    yield {
      name: "CHDT",
      type: "bytes",
      value: new Uint8Array(
        this.harmonicFrequencies.buffer,
        this.harmonicFrequencies.byteOffset,
        this.harmonicFrequencies.byteLength
      ),
    }
    yield { name: "CHNM", type: "uint32", value: 1 }
    yield { name: "CHDT", type: "bytes", value: this.harmonicVolumes }
    yield { name: "CHNM", type: "uint32", value: 2 }
    yield { name: "CHDT", type: "bytes", value: this.harmonicWidths }
    yield { name: "CHNM", type: "uint32", value: 3 }
    yield { name: "CHDT", type: "bytes", value: Uint8Array.from(this.harmonicTypes) }
  }
}

const defaultHarmonicFrequencies = [1098, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
const defaultHarmonicVolumes = [255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
const defaultHarmonicWidths = [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
const defaultHarmonicTypes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
