import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the fft.sunsynth file", () => {
  const filePath = "tests/files/fft.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Fft.Module
    expect(mod.flags).toEqual(0x02000051)
    expect(mod.name).toEqual("FFT")
    const { c } = mod

    expect(c.sampleRate).toEqual(m.Fft.SampleRate._44100hz)
    expect(c.channels).toEqual(m.Fft.Channels.Mono)
    expect(c.buffer).toEqual(m.Fft.Buffer._128)
    expect(c.bufOverlap).toEqual(m.Fft.BufferOverlap._4x)
    expect(c.feedback).toEqual(5064)
    expect(c.noiseReduction).toEqual(27057)
    expect(c.phaseGain).toEqual(9600)
    expect(c.allPassFilter).toEqual(12317)
    expect(c.frequencySpread).toEqual(13403)
    expect(c.randomPhase).toEqual(18439)
    expect(c.randomPhaseLite).toEqual(9270)
    expect(c.freqShift).toEqual(3913)
    expect(c.deform1).toEqual(3948)
    expect(c.deform2).toEqual(19358)
    expect(c.hpCutoff).toEqual(25357)
    expect(c.lpCutoff).toEqual(12632)
    expect(c.volume).toEqual(13740)
  })
})
