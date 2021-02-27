import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the delay.sunsynth file", () => {
  const filePath = "tests/files/delay.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Delay.Module
    expect(mod.flags).toEqual(1105)
    expect(mod.name).toEqual("d e l a y")
    const { c } = mod
    expect(c.dry).toEqual(158)
    expect(c.wet).toEqual(273)
    expect(c.delayL).toEqual(242)
    expect(c.delayR).toEqual(43)
    expect(c.volumeL).toEqual(179)
    expect(c.volumeR).toEqual(57)
    expect(c.channels).toEqual(m.Delay.Channels.Stereo)
    expect(c.inverse).toEqual(true)
    expect(c.delayUnit).toEqual(m.Delay.DelayUnit.Line_2)
  })
})
