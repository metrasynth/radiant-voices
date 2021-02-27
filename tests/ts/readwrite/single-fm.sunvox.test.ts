import { Project } from "@radiant-voices"

import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { base2to10 } from "@radiant-voices/conversions"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import {
  BytesChunk,
  Chunk,
  EventsChunk,
  MidiMapsChunk,
} from "@radiant-voices/chunks/chunk"
import { SyncCommand } from "@radiant-voices/project"
import { Event } from "@radiant-voices/pattern"

describe("Reading the single-fm.sunvox file", () => {
  const filePath = "tests/files/single-fm.sunvox"
  let project: Project
  beforeAll(() => {
    const f = readFileSync(filePath)
    const chunks = fromIffBuffer(f)
    project = readSunVoxFile(chunks) as Project
  })
  test("has correctly read properties and controllers", () => {
    expect(project.name).toEqual("single fm")
    expect(project.receiveSyncMidi).toEqual(SyncCommand.Tempo)
    expect(project.receiveSyncOther).toEqual(
      SyncCommand.StartStop | SyncCommand.Position
    )
    expect(project.initialBpm).toEqual(126)
    expect(project.initialTpl).toEqual(7)
    expect(project.globalVolume).toEqual(80)
    expect(project.sunVoxVersion).toEqual([1, 9, 5, 2])
    expect(project.basedOnVersion).toEqual([1, 9, 5, 2])
    expect(project.modules.length).toEqual(2)
    const { outputModule } = project
    expect(outputModule.finetune).toEqual(0)
    expect(outputModule.relativeNote).toEqual(0)
    expect(outputModule.layer).toEqual(0)
    expect(base2to10(outputModule.scale)).toEqual(100)
    const fm = project.modules[1] as m.Fm.Module
    expect(fm.name).toEqual("FM")
    const { c } = fm
    expect(c.cVolume).toEqual(129)
    expect(c.mVolume).toEqual(49)
    expect(c.panning).toEqual(1)
    expect(c.cFreqRatio).toEqual(2)
    expect(c.mFreqRatio).toEqual(2)
    expect(c.mFeedback).toEqual(1)
    expect(c.cAttack).toEqual(33)
    expect(c.cDecay).toEqual(33)
    expect(c.cSustain).toEqual(129)
    expect(c.cRelease).toEqual(65)
    expect(c.mAttack).toEqual(33)
    expect(c.mDecay).toEqual(33)
    expect(c.mSustain).toEqual(129)
    expect(c.mRelease).toEqual(65)
    expect(c.mScalingPerKey).toEqual(1)
    expect(c.polyphonyCh).toEqual(5)
    expect(c.mode).toEqual(m.Fm.Mode.Lq)
  })
  test("has correct chunks when written out", () => {
    const chunks = objectChunks(project)
    const v = () => chunks.next().value as Chunk
    const expectChunk = (chunk: Chunk) => {
      expect(v()).toEqual(chunk)
    }
    const expectCval = (value: number) => {
      expectChunk({ name: "CVAL", type: "int32", value })
    }
    expectChunk({ name: "SVOX", type: "empty" })
    expectChunk({ name: "VERS", type: "version", value: [1, 9, 5, 2] })
    expectChunk({ name: "BVER", type: "version", value: [1, 9, 5, 2] })
    expectChunk({ name: "SFGS", type: "uint32", value: 0x2a })
    expectChunk({ name: "BPM ", type: "uint32", value: 126 })
    expectChunk({ name: "SPED", type: "uint32", value: 7 })
    expectChunk({ name: "TGRD", type: "uint32", value: 3 })
    expectChunk({ name: "TGD2", type: "uint32", value: 5 })
    expectChunk({ name: "GVOL", type: "uint32", value: 0x50 })
    expectChunk({ name: "NAME", type: "cstring", value: "single fm" })
    expectChunk({ name: "MSCL", type: "uint32", value: 0x100 })
    expectChunk({ name: "MZOO", type: "uint32", value: 0x160 })
    expectChunk({ name: "MXOF", type: "int32", value: 0 })
    expectChunk({ name: "MYOF", type: "int32", value: 0 })
    expectChunk({ name: "LMSK", type: "uint32", value: 0 })
    expectChunk({ name: "CURL", type: "uint32", value: 0 })
    expectChunk({ name: "TIME", type: "int32", value: -45 })
    expectChunk({ name: "SELS", type: "uint32", value: 1 })
    expectChunk({ name: "LGEN", type: "uint32", value: 1 })
    expectChunk({ name: "PATN", type: "uint32", value: 0 })
    expectChunk({ name: "PATT", type: "uint32", value: 1 })
    expectChunk({ name: "PATL", type: "uint32", value: 1 })

    let c: Chunk = v() as EventsChunk
    expect(c.name).toEqual("PDTA")
    expect(c.values).toHaveLength(8)
    const event: Event = c.values[3]
    expect(event.note).toEqual(49)
    expect(event.velocity).toEqual(0x30)
    expect(event.module).toEqual(2)
    expect(event.controller).toEqual(3)
    expect(event.effect).toEqual(0)
    expect(event.parameter).toEqual(0x4567)

    expectChunk({ name: "PCHN", type: "uint32", value: 2 })
    expectChunk({ name: "PLIN", type: "uint32", value: 4 })
    expectChunk({ name: "PYSZ", type: "uint32", value: 0x20 })
    expectChunk({ name: "PFLG", type: "uint32", value: 0 })

    c = v() as BytesChunk
    expect(c.name).toEqual("PICO")
    expect(c.value).toHaveLength(32)

    expectChunk({ name: "PFGC", type: "color", value: [0, 0, 0] })
    expectChunk({ name: "PBGC", type: "color", value: [0xff, 0xff, 0xff] })
    expectChunk({ name: "PFFF", type: "uint32", value: 0 })
    expectChunk({ name: "PXXX", type: "int32", value: 0 })
    expectChunk({ name: "PYYY", type: "int32", value: 0 })
    expectChunk({ name: "PEND", type: "empty" })

    expectChunk({ name: "PPAR", type: "uint32", value: 0 })
    expectChunk({ name: "PFFF", type: "uint32", value: 3 })
    expectChunk({ name: "PXXX", type: "int32", value: 4 })
    expectChunk({ name: "PYYY", type: "int32", value: 0 })
    expectChunk({ name: "PEND", type: "empty" })

    expectChunk({ name: "SFFF", type: "uint32", value: 0x43 })
    expectChunk({ name: "SNAM", type: "fixedString", value: "Output" })
    expectChunk({ name: "SFIN", type: "int32", value: 0 })
    expectChunk({ name: "SREL", type: "int32", value: 0 })
    expectChunk({ name: "SXXX", type: "int32", value: 0x200 })
    expectChunk({ name: "SYYY", type: "int32", value: 0x200 })
    expectChunk({ name: "SZZZ", type: "uint32", value: 0 })
    expectChunk({ name: "SVPR", type: "uint32", value: 0x9a3202c2 })
    expectChunk({ name: "SSCL", type: "uint32", value: 0x100 })
    expectChunk({ name: "SCOL", type: "color", value: [0xff, 0xff, 0xff] })
    expectChunk({ name: "SMII", type: "uint32", value: 0 })
    expectChunk({ name: "SMIC", type: "uint32", value: 0 })
    expectChunk({ name: "SMIB", type: "int32", value: -1 })
    expectChunk({ name: "SMIP", type: "int32", value: -1 })
    expectChunk({ name: "SLNK", type: "links", values: [1] })
    expectChunk({ name: "SLnK", type: "links", values: [0] })
    expectChunk({ name: "SEND", type: "empty" })

    expectChunk({ name: "SFFF", type: "uint32", value: 0x49 })
    expectChunk({ name: "SNAM", type: "fixedString", value: "FM" })
    expectChunk({ name: "STYP", type: "cstring", value: "FM" })
    expectChunk({ name: "SFIN", type: "int32", value: 1 })
    expectChunk({ name: "SREL", type: "int32", value: 1 })
    expectChunk({ name: "SXXX", type: "int32", value: 0x138 })
    expectChunk({ name: "SYYY", type: "int32", value: 0x208 })
    expectChunk({ name: "SZZZ", type: "uint32", value: 0 })
    expectChunk({ name: "SVPR", type: "uint32", value: 0x9a3202c2 })
    expectChunk({ name: "SSCL", type: "uint32", value: 0x100 })
    expectChunk({ name: "SCOL", type: "color", value: [0, 0xe3, 0xff] })
    expectChunk({ name: "SMII", type: "uint32", value: 0 })
    expectChunk({ name: "SMIC", type: "uint32", value: 0 })
    expectChunk({ name: "SMIB", type: "int32", value: -1 })
    expectChunk({ name: "SMIP", type: "int32", value: -1 })
    expectChunk({ name: "SLNK", type: "links", values: [] })
    expectChunk({ name: "SLnK", type: "links", values: [] })
    expectCval(0x81)
    expectCval(0x31)
    expectCval(0x81)
    expectCval(2)
    expectCval(2)
    expectCval(1)
    expectCval(0x21)
    expectCval(0x21)
    expectCval(0x81)
    expectCval(0x41)
    expectCval(0x21)
    expectCval(0x21)
    expectCval(0x81)
    expectCval(0x41)
    expectCval(1)
    expectCval(5)
    expectCval(2)
    c = v() as MidiMapsChunk
    expect(c.name).toEqual("CMID")
    expect(c.values).toHaveLength(17)
    expectChunk({ name: "SEND", type: "empty" })

    expect(chunks.next().done).toBeTruthy()
  })
})
