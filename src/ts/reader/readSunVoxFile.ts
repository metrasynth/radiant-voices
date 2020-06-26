import { Chunk } from "../chunks/chunk"
import { readProject } from "./readProject"
import { readSynth } from "./readSynth"
import { SunVoxContainer } from "../containers"

export function readSunVoxFile(chunks: Generator<Chunk>): SunVoxContainer {
  const { value: chunk } = chunks.next()
  const { name } = chunk
  switch (name) {
    case "SSYN":
      return readSynth(chunks)
    case "SVOX":
      return readProject(chunks)
    default:
      throw new Error(`Unknown header "${name}"`)
  }
}
