export interface ModuleDataChunk {
  chnm: number
  chdt?: Uint8Array
  chff?: number
  chfr?: number
}

export type ModuleDataChunks = ModuleDataChunk[]
