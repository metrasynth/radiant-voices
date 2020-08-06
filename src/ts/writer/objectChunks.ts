import { Project } from "../project"
import { Chunk } from "../chunks/chunk"
import { projectChunks } from "./projectChunks"
import { ModuleBase } from "../modtypes/moduleBase"
import { Synth } from "../synth"
import synthChunks from "./synthChunks"
import { moduleChunks } from "./moduleChunks"

export function objectChunks(obj?: ModuleBase | Project | Synth): Generator<Chunk> {
  if (obj instanceof ModuleBase) return moduleChunks(obj)
  if (obj instanceof Project) return projectChunks(obj)
  if (obj instanceof Synth) return synthChunks(obj)
  // Nothing matched:
  throw new TypeError()
}
