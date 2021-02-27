import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the vocal-filter.sunsynth file", () => {
  const filePath = "tests/files/vocal-filter.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.VocalFilter.Module
    expect(mod.flags).toEqual(81)
    expect(mod.name).toEqual("Vocal filter")
    const { c } = mod
    expect(c.volume).toEqual(271)
    expect(c.formantWidthHz).toEqual(249)
    expect(c.intensity).toEqual(207)
    expect(c.formants).toEqual(3)
    expect(c.vowel).toEqual(243)
    expect(c.voiceType).toEqual(m.VocalFilter.VoiceType.Bass)
    expect(c.channels).toEqual(m.VocalFilter.Channels.Stereo)
  })
})
