import { ModuleBase } from "./moduleBase"
import { ModuleDataChunks } from "../moduleDataChunk"
import { Chunk } from "../chunks/chunk"

export class ModuleSpecificBehavior {
  constructor(readonly module: ModuleBase) {}
  chnk(): number {
    return 0
  }
  processDataChunks(dataChunks: ModuleDataChunks) {}
  *typeSpecificChunks(): Generator<Chunk> {}
}
