import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the echo.sunsynth file", () => {
  const filePath = "tests/files/echo.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Echo.Module
    expect(mod.flags).toEqual(1105)
    expect(mod.name).toEqual("echo")
    const { c } = mod
    expect(c.dry).toEqual(80)
    expect(c.wet).toEqual(88)
    expect(c.feedback).toEqual(234)
    expect(c.delay).toEqual(133)
    expect(c.channels).toEqual(m.Echo.Channels.Mono)
    expect(c.delayUnit).toEqual(m.Echo.DelayUnit.Line)
  })
})
