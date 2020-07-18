import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the gpio.sunsynth file", () => {
  const filePath = "tests/files/gpio.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Gpio.Module
    expect(mod.flags).toEqual(81)
    expect(mod.name).toEqual("GPIO")
    const { c } = mod
    expect(c.out).toEqual(false)
    expect(c.outPin).toEqual(213)
    expect(c.outThreshold).toEqual(46)
    expect(c.in).toEqual(true)
    expect(c.inPin).toEqual(210)
    expect(c.inNote).toEqual(0)
    expect(c.inAmplitude).toEqual(93)
  })
})
