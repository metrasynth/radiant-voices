import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the reverb.sunsynth file", () => {
  const filePath = "tests/files/reverb.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Reverb.Module
    expect(mod.flags).toEqual(81)
    expect(mod.name).toEqual("Reverb")
    const { c } = mod
    expect(c.dry).toEqual(140)
    expect(c.wet).toEqual(134)
    expect(c.feedback).toEqual(146)
    expect(c.damp).toEqual(0)
    expect(c.stereoWidth).toEqual(75)
    expect(c.freeze).toEqual(true)
    expect(c.mode).toEqual(m.Reverb.Mode.Lq)
    expect(c.allPassFilter).toEqual(true)
    expect(c.roomSize).toEqual(32)
    expect(c.randomSeed).toEqual(23552)
  })
})
