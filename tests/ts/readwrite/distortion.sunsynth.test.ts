import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the distortion.sunsynth file", () => {
  const filePath = "tests/files/distortion.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Distortion.Module
    expect(mod.flags).toEqual(81)
    expect(mod.name).toEqual("distortion")
    const { c } = mod
    expect(c.volume).toEqual(99)
    expect(c.type).toEqual(m.Distortion.Type.Foldback2)
    expect(c.power).toEqual(94)
    expect(c.bitDepth).toEqual(15)
    expect(c.freqHz).toEqual(23609)
    expect(c.noise).toEqual(196)
  })
})
