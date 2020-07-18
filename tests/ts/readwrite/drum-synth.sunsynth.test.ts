import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the drum-synth.sunsynth file", () => {
  const filePath = "tests/files/drum-synth.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.DrumSynth.Module
    expect(mod.flags).toEqual(73)
    expect(mod.name).toEqual("drums")
    const { c } = mod
    expect(c.volume).toEqual(255)
    expect(c.panning).toEqual(1)
    expect(c.polyphonyCh).toEqual(3)
    expect(c.bassVolume).toEqual(201)
    expect(c.bassPower).toEqual(255)
    expect(c.bassTone).toEqual(65)
    expect(c.bassLength).toEqual(63)
    expect(c.hihatVolume).toEqual(257)
    expect(c.hihatLength).toEqual(63)
    expect(c.snareVolume).toEqual(257)
    expect(c.snareTone).toEqual(127)
    expect(c.snareLength).toEqual(65)
    expect(c.bassPanning).toEqual(-1)
    expect(c.hihatPanning).toEqual(1)
    expect(c.snarePanning).toEqual(-1)
  })
})
