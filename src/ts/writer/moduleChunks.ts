import { ModuleBase } from "../modtypes/moduleBase"
import { Chunk } from "../chunks/chunk"
import { Output } from "../modtypes/m"

export function* moduleChunks(module: ModuleBase): Generator<Chunk> {
  yield { name: "SFFF", type: "uint32", value: module.flags }
  yield { name: "SNAM", type: "fixedString", value: module.name }
  const isOutputModule = module instanceof Output.Module
  if (!isOutputModule) {
    yield { name: "STYP", type: "cstring", value: module.typeName }
  }
  yield { name: "SFIN", type: "int32", value: module.finetune }
  yield { name: "SREL", type: "int32", value: module.relativeNote }
  if (module.project) {
    yield { name: "SXXX", type: "int32", value: module.x }
    yield { name: "SYYY", type: "int32", value: module.y }
    yield { name: "SZZZ", type: "uint32", value: module.layer }
    yield { name: "SVPR", type: "uint32", value: module.visualization }
  }
  yield { name: "SSCL", type: "uint32", value: module.scale }
  yield { name: "SCOL", type: "color", value: module.color }
  yield {
    name: "SMII",
    type: "uint32",
    value: (Number(module.midiInAlways) & 1) | (module.midiInChannel << 1),
  }
  if (module.midiOutName) {
    yield { name: "SMIN", type: "cstring", value: module.midiOutName }
  }
  yield { name: "SMIC", type: "uint32", value: module.midiOutChannel }
  yield {
    name: "SMIB",
    type: "int32",
    value: module.midiOutBank !== undefined ? module.midiOutBank : -1,
  }
  yield {
    name: "SMIP",
    type: "int32",
    value: module.midiOutProgram !== undefined ? module.midiOutProgram : -1,
  }
  if (module.project) {
    yield { name: "SLNK", type: "links", values: module.incomingLinks }
  }
  for (const cval of module.rawControllerValues()) {
    yield { name: "CVAL", type: "uint32", value: cval }
  }
  if (!isOutputModule) {
    yield { name: "CMID", type: "midiMaps", values: module.midiMapsArray() }
  }
  const chnkValue = module.chnk()
  if (chnkValue) {
    yield { name: "CHNK", type: "uint32", value: chnkValue }
  }
  if (module.optionsChnm !== undefined) {
    yield { name: "CHNM", type: "uint32", value: module.optionsChnm }
    yield { name: "CHDT", type: "bytes", value: module.rawOptionBytes() }
  }
  if (module.behavior) {
    yield* module.behavior.typeSpecificChunks()
  }
}
