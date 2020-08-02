import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"
import { Chunk } from "@radiant-voices/chunks/chunk"
import { MidiMap } from "@radiant-voices/controllerMidiMap"
import HarmonicType = m.SpectraVoice.HarmonicType

describe("Reading the spectravoice.sunsynth file", () => {
  const filePath = "tests/files/spectravoice.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.SpectraVoice.Module
    expect(mod.flags).toEqual(0x49)
    expect(mod.name).toEqual("SpectraVoice")
    expect(mod.behavior?.harmonicFrequencies).toEqual(
      Uint16Array.from([
        17916,
        7063,
        5426,
        7235,
        18002,
        10594,
        775,
        20586,
        10853,
        16279,
        14729,
        4479,
        12231,
        3876,
        19036,
        21275,
      ])
    )
    expect(mod.behavior?.harmonicVolumes).toEqual(
      Uint8Array.from([
        114,
        203,
        245,
        42,
        191,
        102,
        243,
        195,
        184,
        59,
        224,
        144,
        213,
        182,
        21,
        238,
      ])
    )
    expect(mod.behavior?.harmonicWidths).toEqual(
      Uint8Array.from([
        99,
        242,
        70,
        26,
        245,
        9,
        43,
        10,
        219,
        135,
        94,
        235,
        66,
        124,
        114,
        16,
      ])
    )
    expect(mod.behavior?.harmonicTypes).toEqual([
      HarmonicType.Org2,
      HarmonicType.Rect,
      HarmonicType.Overtones4,
      HarmonicType.Sin,
      HarmonicType.Overtones4,
      HarmonicType.Overtones4,
      HarmonicType.Triangle1,
      HarmonicType.Overtones1,
      HarmonicType.Org4,
      HarmonicType.Rect,
      HarmonicType.Overtones2,
      HarmonicType.Overtones3,
      HarmonicType.Org4,
      HarmonicType.Overtones4,
      HarmonicType.Org1,
      HarmonicType.Overtones1,
    ] as HarmonicType[])
    const { c } = mod
    expect(c.volume).toEqual(219)
    expect(c.panning).toEqual(-77)
    expect(c.attack).toEqual(234)
    expect(c.release).toEqual(324)
    expect(c.polyphonyCh).toEqual(21)
    expect(c.mode).toEqual(m.SpectraVoice.Mode.LqMono)
    expect(c.sustain).toEqual(false)
    expect(c.spectrumResolution).toEqual(4)
    expect(c.harmonic).toEqual(10)
    expect(c.hFreqHz).toEqual(14729)
    expect(c.hVolume).toEqual(224)
    expect(c.hWidth).toEqual(94)
    expect(c.hType).toEqual(m.SpectraVoice.HarmonicType.Overtones2)
  })
  test("has correct chunks when written out", () => {
    const chunks = objectChunks(synth)
    const v = () => chunks.next().value
    const expectChunk = (chunk: Chunk) => {
      expect(v()).toEqual(chunk)
    }
    const expectCval = (value: number) => {
      expectChunk({ name: "CVAL", type: "int32", value })
    }
    expectChunk({ name: "SSYN", type: "empty" })
    expectChunk({ name: "VERS", type: "version", value: [1, 9, 5, 2] })
    expectChunk({ name: "SFFF", type: "uint32", value: 0x49 })
    expectChunk({ name: "SNAM", type: "fixedString", value: "SpectraVoice" })
    expectChunk({ name: "STYP", type: "cstring", value: "SpectraVoice" })
    expectChunk({ name: "SFIN", type: "int32", value: 0 })
    expectChunk({ name: "SREL", type: "int32", value: 4 })
    expectChunk({ name: "SSCL", type: "uint32", value: 0x100 })
    expectChunk({ name: "SCOL", type: "color", value: [255, 0, 232] })
    expectChunk({ name: "SMII", type: "uint32", value: 0 })
    expectChunk({ name: "SMIC", type: "uint32", value: 0 })
    expectChunk({ name: "SMIB", type: "int32", value: -1 })
    expectChunk({ name: "SMIP", type: "int32", value: -1 })
    expectCval(219)
    expectCval(51)
    expectCval(234)
    expectCval(324)
    expectCval(21)
    expectCval(3)
    expectCval(0)
    expectCval(4)
    expectCval(10)
    expectCval(14729)
    expectCval(224)
    expectCval(94)
    expectCval(11)
    const { name, type, values } = v()
    expect({ name, type }).toEqual({ name: "CMID", type: "midiMaps" })
    expect((values as Array<MidiMap>).length).toEqual(13)
    expectChunk({ name: "CHNK", type: "uint32", value: 4 })
    expectChunk({ name: "CHNM", type: "uint32", value: 0 })
    expectChunk({
      name: "CHDT",
      type: "bytes",
      value: new Uint8Array([
        252,
        69,
        151,
        27,
        50,
        21,
        67,
        28,
        82,
        70,
        98,
        41,
        7,
        3,
        106,
        80,
        101,
        42,
        151,
        63,
        137,
        57,
        127,
        17,
        199,
        47,
        36,
        15,
        92,
        74,
        27,
        83,
      ]),
    })
    expectChunk({ name: "CHNM", type: "uint32", value: 1 })
    expectChunk({
      name: "CHDT",
      type: "bytes",
      value: new Uint8Array([
        114,
        203,
        245,
        42,
        191,
        102,
        243,
        195,
        184,
        59,
        224,
        144,
        213,
        182,
        21,
        238,
      ]),
    })
    expectChunk({ name: "CHNM", type: "uint32", value: 2 })
    expectChunk({
      name: "CHDT",
      type: "bytes",
      value: new Uint8Array([
        99,
        242,
        70,
        26,
        245,
        9,
        43,
        10,
        219,
        135,
        94,
        235,
        66,
        124,
        114,
        16,
      ]),
    })
    expectChunk({ name: "CHNM", type: "uint32", value: 3 })
    expectChunk({
      name: "CHDT",
      type: "bytes",
      value: new Uint8Array([3, 1, 13, 6, 13, 13, 8, 10, 5, 1, 11, 12, 5, 13, 2, 10]),
    })
    expect(chunks.next().value).toEqual({ name: "SEND", type: "empty" })
    expect(chunks.next().done).toBeTruthy()
  })
})
