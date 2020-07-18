import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the filter-pro.sunsynth file", () => {
  const filePath = "tests/files/filter-pro.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.FilterPro.Module
    expect(mod.flags).toEqual(1105)
    expect(mod.name).toEqual("Filter Pro")
    const { c } = mod
    expect(c.volume).toEqual(25562)
    expect(c.type).toEqual(m.FilterPro.Type.Lp)
    expect(c.freqHz).toEqual(21049)
    expect(c.freqFinetune).toEqual(-944)
    expect(c.freqScale).toEqual(63)
    expect(c.exponentialFreq).toEqual(true)
    expect(c.q).toEqual(7962)
    expect(c.gain).toEqual(2934)
    expect(c.rollOff).toEqual(m.FilterPro.RollOff.Db_36)
    expect(c.response).toEqual(956)
    expect(c.mode).toEqual(m.FilterPro.Mode.Mono)
    expect(c.mix).toEqual(1945)
    expect(c.lfoFreq).toEqual(452)
    expect(c.lfoAmp).toEqual(29983)
    expect(c.lfoWaveform).toEqual(m.Filter.LfoWaveform.Saw)
    expect(c.setLfoPhase).toEqual(30)
    expect(c.lfoFreqUnit).toEqual(m.Filter.LfoFreqUnit.Line_3)
  })
})
