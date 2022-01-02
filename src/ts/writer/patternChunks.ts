import { Event, Pattern, PatternBase, PatternClone } from "../pattern"
import { Chunk } from "../chunks/chunk"

export function* patternChunks(pattern: PatternBase): Generator<Chunk> {
  if (pattern instanceof Pattern) {
    const events: Event[] = []
    for (let lineIdx = 0; lineIdx < pattern.lines; ++lineIdx) {
      for (let trackIdx = 0; trackIdx < pattern.tracks; ++trackIdx) {
        events.push(pattern.data[lineIdx][trackIdx])
      }
    }
    yield { name: "PDTA", type: "events", values: events }
    yield { name: "PCHN", type: "uint32", value: pattern.tracks }
    yield { name: "PLIN", type: "uint32", value: pattern.lines }
    yield { name: "PYSZ", type: "uint32", value: pattern.ySize }
    yield { name: "PFLG", type: "uint32", value: pattern.flagsPFLG }
    yield { name: "PICO", type: "bytes", value: pattern.icon }
    yield { name: "PFGC", type: "color", value: pattern.fgColor }
    yield { name: "PBGC", type: "color", value: pattern.bgColor }
    yield { name: "PFFF", type: "uint32", value: pattern.flagsPFFF }
    yield { name: "PXXX", type: "int32", value: pattern.x }
    yield { name: "PYYY", type: "int32", value: pattern.y }
  } else if (pattern instanceof PatternClone) {
    yield { name: "PPAR", type: "uint32", value: pattern.parent }
    yield { name: "PFFF", type: "uint32", value: pattern.flagsPFFF }
    yield { name: "PXXX", type: "int32", value: pattern.x }
    yield { name: "PYYY", type: "int32", value: pattern.y }
  }
}
