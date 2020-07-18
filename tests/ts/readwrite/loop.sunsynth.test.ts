import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the loop.sunsynth file", () => {
  const filePath = "tests/files/loop.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Loop.Module
    expect(mod.flags).toEqual(1105)
    expect(mod.name).toEqual("Loop")
    const { c } = mod
    expect(c.volume).toEqual(200)
    expect(c.delay).toEqual(110)
    expect(c.channels).toEqual(m.Loop.Channels.Mono)
    expect(c.repeats).toEqual(35)
    expect(c.mode).toEqual(m.Loop.Mode.Normal)
  })
})
