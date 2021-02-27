import { ModuleSpecificBehavior } from "./moduleSpecificBehavior"
import { ModuleDataChunk, ModuleDataChunks } from "@radiant-voices/moduleDataChunk"
import { Chunk } from "@radiant-voices/chunks/chunk"
export class VorbisPlayerBehavior extends ModuleSpecificBehavior {
  data?: Uint8Array

  chnk(): number {
    return 1
  }

  processDataChunks(dataChunks: ModuleDataChunks) {
    for (const dataChunk of dataChunks) {
      if (dataChunk.chnm === 0) {
        this.processData(dataChunk)
      }
    }
  }

  private processData(dataChunk: ModuleDataChunk) {
    const { chdt } = dataChunk
    if (chdt) {
      this.data = chdt
    }
  }

  *typeSpecificChunks(): Generator<Chunk> {
    if (this.data) {
      yield { name: "CHNM", type: "uint32", value: 0 }
      yield { name: "CHDT", type: "bytes", value: this.data }
    }
  }
}
