import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the pitch2ctl.sunsynth file", () => {
  const filePath = "tests/files/pitch2ctl.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Pitch2Ctl.Module
    expect(mod.flags).toEqual(131145)
    expect(mod.name).toEqual("Pitch2Ctl")
    const { c } = mod
    expect(c.mode).toEqual(m.Pitch2Ctl.Mode.Pitch)
    expect(c.noteOffAction).toEqual(m.Pitch2Ctl.NoteOffAction.PitchDown)
    expect(c.firstNote).toEqual(19)
    expect(c.numberOfSemitones).toEqual(217)
    expect(c.outMin).toEqual(27327)
    expect(c.outMax).toEqual(7746)
    expect(c.outController).toEqual(239) // [TODO] out of range
  })
})
