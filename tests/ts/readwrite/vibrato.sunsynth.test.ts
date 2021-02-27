import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the vibrato.sunsynth file", () => {
  const filePath = "tests/files/vibrato.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Vibrato.Module
    expect(mod.flags).toEqual(1105)
    expect(mod.name).toEqual("Vibrato")
    const { c } = mod
    expect(c.volume).toEqual(122)
    expect(c.amplitude).toEqual(228)
    expect(c.freq).toEqual(1403)
    expect(c.channels).toEqual(m.Vibrato.Channels.Stereo)
    expect(c.setPhase).toEqual(117)
    expect(c.frequencyUnit).toEqual(m.Vibrato.FrequencyUnit.Line)
    expect(c.exponentialAmplitude).toEqual(true)
  })
})
