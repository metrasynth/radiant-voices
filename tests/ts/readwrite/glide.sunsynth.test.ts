import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the glide.sunsynth file", () => {
  const filePath = "tests/files/glide.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Glide.Module
    expect(mod.flags).toEqual(135241)
    expect(mod.name).toEqual("Glide")
    const { c } = mod
    expect(c.response).toEqual(220)
    expect(c.sampleRateHz).toEqual(8676)
    expect(c.resetOnFirstNote).toEqual(false)
    expect(c.polyphony).toEqual(true)
    expect(c.pitch).toEqual(-537)
    expect(c.pitchScale).toEqual(48)
    expect(c.reset).toEqual(false)
  })
})
