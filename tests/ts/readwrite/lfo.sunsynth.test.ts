import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the lfo.sunsynth file", () => {
  const filePath = "tests/files/lfo.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Lfo.Module
    expect(mod.flags).toEqual(1105)
    expect(mod.name).toEqual("LFO")
    const { c } = mod
    expect(c.volume).toEqual(440)
    expect(c.type).toEqual(m.Lfo.Type.Amplitude)
    expect(c.amplitude).toEqual(54)
    expect(c.freq).toEqual(66)
    expect(c.waveform).toEqual(m.Lfo.Waveform.Square)
    expect(c.setPhase).toEqual(77)
    expect(c.channels).toEqual(m.Lfo.Channels.Stereo)
    expect(c.frequencyUnit).toEqual(m.Lfo.FrequencyUnit.Tick)
    expect(c.dutyCycle).toEqual(64)
    expect(c.generator).toEqual(false)
  })
})
