import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the amplifier.sunsynth file", () => {
  const filePath = "tests/files/amplifier.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Amplifier.Module
    expect(mod.flags).toEqual(81)
    expect(mod.name).toEqual("amp")
    const { c } = mod
    expect(c.volume).toEqual(378)
    expect(c.balance).toEqual(-63)
    expect(c.dcOffset).toEqual(-33)
    expect(c.inverse).toEqual(true)
    expect(c.stereoWidth).toEqual(44)
    expect(c.absolute).toEqual(false)
    expect(c.fineVolume).toEqual(21087)
    expect(c.gain).toEqual(3948)
  })
})
