import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

const expectedDrawnWaveform = new Int8Array([
  0,
  -100,
  -90,
  0,
  90,
  -119,
  -55,
  -38,
  6,
  44,
  68,
  68,
  52,
  19,
  -31,
  -49,
  -58,
  -58,
  -50,
  -25,
  38,
  58,
  58,
  58,
  -90,
  -120,
  100,
  90,
  59,
  21,
  0,
  54,
])
describe("Reading the generator.sunsynth file", () => {
  const filePath = "tests/files/generator.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Generator.Module
    expect(mod.flags).toEqual(0x59)
    expect(mod.name).toEqual("gen")
    expect(mod.behavior?.drawnWaveform).toEqual(expectedDrawnWaveform)
    const { c } = mod
    expect(c.volume).toEqual(136)
    expect(c.waveform).toEqual(m.Generator.Waveform.Drawn)
    expect(c.panning).toEqual(-85)
    expect(c.attack).toEqual(359)
    expect(c.release).toEqual(115)
    expect(c.polyphonyCh).toEqual(6)
    expect(c.mode).toEqual(m.Generator.Mode.Mono)
    expect(c.sustain).toEqual(true)
    expect(c.freqModulationByInput).toEqual(99)
    expect(c.dutyCycle).toEqual(283)
  })
})
