import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the filter.sunsynth file", () => {
  const filePath = "tests/files/filter.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Filter.Module
    expect(mod.flags).toEqual(1105)
    expect(mod.name).toEqual("Filter")
    const { c } = mod
    expect(c.volume).toEqual(172)
    expect(c.freq).toEqual(10617)
    expect(c.resonance).toEqual(890)
    expect(c.type).toEqual(m.Filter.Type.Notch)
    expect(c.response).toEqual(91)
    expect(c.mode).toEqual(m.Filter.Mode.Lq)
    expect(c.impulse).toEqual(11576)
    expect(c.mix).toEqual(106)
    expect(c.lfoFreq).toEqual(474)
    expect(c.lfoAmp).toEqual(250)
    expect(c.setLfoPhase).toEqual(32)
    expect(c.exponentialFreq).toEqual(false)
    expect(c.rollOff).toEqual(m.Filter.RollOff.Db_36)
    expect(c.lfoFreqUnit).toEqual(m.Filter.LfoFreqUnit.Hz)
    expect(c.lfoWaveform).toEqual(m.Filter.LfoWaveform.Saw)
  })
})
