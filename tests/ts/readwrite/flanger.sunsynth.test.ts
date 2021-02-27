import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the flanger.sunsynth file", () => {
  const filePath = "tests/files/flanger.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Flanger.Module
    expect(mod.flags).toEqual(1105)
    expect(mod.name).toEqual("Flanger")
    const { c } = mod
    expect(c.dry).toEqual(136)
    expect(c.wet).toEqual(150)
    expect(c.feedback).toEqual(22)
    expect(c.delay).toEqual(93)
    expect(c.response).toEqual(134)
    expect(c.lfoFreq).toEqual(102)
    expect(c.lfoAmp).toEqual(203)
    expect(c.lfoWaveform).toEqual(m.Flanger.LfoWaveform.Hsin)
    expect(c.setLfoPhase).toEqual(37)
    expect(c.lfoFreqUnit).toEqual(m.Flanger.LfoFreqUnit.Hz_0_05)
  })
})
