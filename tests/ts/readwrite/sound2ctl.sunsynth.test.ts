import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the sound2ctl.sunsynth file", () => {
  const filePath = "tests/files/sound2ctl.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Sound2Ctl.Module
    expect(mod.flags).toEqual(393297)
    expect(mod.name).toEqual("Sound2Ctl")
    const { c } = mod
    expect(c.sampleRateHz).toEqual(14687)
    expect(c.channels).toEqual(m.Sound2Ctl.Channels.Mono)
    expect(c.absolute).toEqual(false)
    expect(c.gain).toEqual(741)
    expect(c.smooth).toEqual(24)
    expect(c.mode).toEqual(m.Sound2Ctl.Mode.Lq)
    expect(c.outMin).toEqual(12054)
    expect(c.outMax).toEqual(21842)
    expect(c.outController).toEqual(223) // [TODO] out of range
  })
})
