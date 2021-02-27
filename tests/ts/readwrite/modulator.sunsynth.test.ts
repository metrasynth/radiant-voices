import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the modulator.sunsynth file", () => {
  const filePath = "tests/files/modulator.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Modulator.Module
    expect(mod.flags).toEqual(8273)
    expect(mod.name).toEqual("Modulator")
    const { c } = mod
    expect(c.volume).toEqual(141)
    expect(c.modulationType).toEqual(m.Modulator.ModulationType.PhaseAbs)
    expect(c.channels).toEqual(m.Modulator.Channels.Mono)
  })
})
