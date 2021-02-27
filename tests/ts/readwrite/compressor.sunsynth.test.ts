import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the compressor.sunsynth file", () => {
  const filePath = "tests/files/compressor.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Compressor.Module
    expect(mod.flags).toEqual(8273)
    expect(mod.name).toEqual("compy")
    const { c } = mod
    expect(c.volume).toEqual(442)
    expect(c.threshold).toEqual(465)
    expect(c.slopePct).toEqual(61)
    expect(c.attackMs).toEqual(62)
    expect(c.releaseMs).toEqual(925)
    expect(c.mode).toEqual(m.Compressor.Mode.Peak)
    expect(c.sidechainInput).toEqual(32)
  })
})
