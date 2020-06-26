// import Pattern from '../Pattern'
// import PatternClone from '../PatternClone'
//
// export default function *patternChunks(pattern) {
//   if (Pattern.isPattern(pattern)) {
//     yield { type: 'PDTA', data: { bytes: pattern.data } }
//     if (pattern.name) {
//       yield { type: 'PNME', data: { cstring: pattern.name } }
//     }
//     yield { type: 'PCHN', data: { uint32: pattern.tracks } }
//     yield { type: 'PLIN', data: { uint32: pattern.lines } }
//     yield { type: 'PYSZ', data: { uint32: pattern.height } }
//     yield { type: 'PFLG', data: { patternAppearanceFlags: pattern.appearanceFlags } }
//     yield { type: 'PICO', data: { bytes: pattern.icon } }
//     yield { type: 'PFGC', data: { color: pattern.foregroundColor } }
//     yield { type: 'PBGC', data: { color: pattern.backgroundColor } }
//   }
//   if (PatternClone.isPatternClone(pattern)) {
//     yield { type: 'PPAR', data: { uint32: pattern.index } }
//   }
//   if (pattern) {
//     yield { type: 'PFFF', data: { patternFlags: pattern.flags } }
//     yield { type: 'PXXX', data: { int32: pattern.x } }
//     yield { type: 'PYYY', data: { int32: pattern.y } }
//   }
// }

import { Event, Pattern, PatternClone } from "../pattern"
import { Chunk } from "../chunks/chunk"

export function* patternChunks(pattern: Pattern | PatternClone): Generator<Chunk> {
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
    yield { name: "PFLG", type: "uint32", value: pattern.appearance }
    yield { name: "PICO", type: "bytes", value: pattern.icon }
    yield { name: "PFGC", type: "color", value: pattern.fgColor }
    yield { name: "PBGC", type: "color", value: pattern.bgColor }
    yield { name: "PFFF", type: "uint32", value: pattern.flags }
    yield { name: "PXXX", type: "int32", value: pattern.x }
    yield { name: "PYYY", type: "int32", value: pattern.y }
  } else {
    yield { name: "PPAR", type: "uint32", value: pattern.parent }
    yield { name: "PFFF", type: "uint32", value: pattern.flags }
    yield { name: "PXXX", type: "int32", value: pattern.x }
    yield { name: "PYYY", type: "int32", value: pattern.y }
  }
}
