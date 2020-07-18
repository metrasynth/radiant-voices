import { ModuleSpecificBehavior } from "./moduleSpecificBehavior"
import { ModuleDataChunk, ModuleDataChunks } from "@radiant-voices/moduleDataChunk"
import { Chunk } from "@radiant-voices/chunks/chunk"

export const defaultDrawnWaveform = new Int8Array([
  0,
  -100,
  -90,
  0,
  90,
  -119,
  -20,
  45,
  2,
  -20,
  111,
  -23,
  2,
  -98,
  60,
  32,
  100,
  50,
  0,
  -50,
  65,
  98,
  50,
  32,
  -90,
  -120,
  100,
  90,
  59,
  21,
  0,
  54,
])

export class GeneratorBehavior extends ModuleSpecificBehavior {
  drawnWaveform = new Int8Array(defaultDrawnWaveform)

  chnk(): number {
    return 4
  }

  processDataChunks(dataChunks: ModuleDataChunks) {
    for (const dataChunk of dataChunks) {
      if (dataChunk.chnm === 0) {
        this.processDrawnWaveformChunk(dataChunk)
      }
    }
  }

  private processDrawnWaveformChunk(dataChunk: ModuleDataChunk) {
    const { chdt } = dataChunk
    if (chdt) {
      this.drawnWaveform = new Int8Array(chdt)
    }
  }

  *typeSpecificChunks(): Generator<Chunk> {
    yield { name: "CHNM", type: "uint32", value: 0 }
    yield { name: "CHDT", type: "bytes", value: new Uint8Array(this.drawnWaveform) }
    yield { name: "CHFR", type: "uint32", value: 44100 }
  }
}
