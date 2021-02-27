import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the vorbis-player.sunsynth file", () => {
  const filePath = "tests/files/vorbis-player.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.VorbisPlayer.Module
    expect(mod.flags).toEqual(32841)
    expect(mod.name).toEqual("moo")
    expect(mod.behavior?.data?.length).toEqual(10785)
    const { c } = mod
    expect(c.volume).toEqual(177)
    expect(c.originalSpeed).toEqual(false)
    expect(c.finetune).toEqual(-38)
    expect(c.transpose).toEqual(16)
    expect(c.interpolation).toEqual(true)
    expect(c.polyphonyCh).toEqual(3)
    expect(c.repeat).toEqual(false)
  })
})
