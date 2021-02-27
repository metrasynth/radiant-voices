import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the kicker.sunsynth file", () => {
  const filePath = "tests/files/kicker.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Kicker.Module
    expect(mod.flags).toEqual(73)
    expect(mod.name).toEqual("kickadee")
    const { c } = mod
    expect(c.volume).toEqual(137)
    expect(c.waveform).toEqual(m.Kicker.Waveform.Triangle)
    expect(c.panning).toEqual(37)
    expect(c.attack).toEqual(392)
    expect(c.release).toEqual(399)
    expect(c.boost).toEqual(842)
    expect(c.acceleration).toEqual(155)
    expect(c.polyphonyCh).toEqual(1)
    expect(c.noClick).toEqual(false)
  })
})
