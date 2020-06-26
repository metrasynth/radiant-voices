// import { chunks } from './index'
//
import { Chunk } from "../chunks/chunk"
import { Synth } from "../synth"
import { objectChunks } from "./objectChunks"

export default function* synthChunks(synth: Synth): Generator<Chunk> {
  yield { name: "SSYN", type: "empty" }
  yield { name: "VERS", type: "version", value: synth.sunVoxVersion }
  yield* objectChunks(synth.module)
  yield { name: "SEND", type: "empty" }
}
