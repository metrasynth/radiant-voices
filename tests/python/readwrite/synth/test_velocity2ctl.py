from rv.api import m


def test_velocity2ctl(read_write_read_synth):
    mod: m.Velocity2Ctl = read_write_read_synth("velocity2ctl").module
    assert mod.flags == 131145
    assert mod.name == "Velocity2Ctl"
    assert mod.note_off_action == mod.NoteOffAction.vel_up
    assert mod.out_min == 32391
    assert mod.out_max == 24497
    assert mod.out_offset == 2319
    assert mod.out_controller == 131


TODO = """
import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the velocity2ctl.sunsynth file", () => {
  const filePath = "tests/files/velocity2ctl.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Velocity2Ctl.Module
    expect(mod.flags).toEqual(131145)
    expect(mod.name).toEqual("Velocity2Ctl")
    const { c } = mod
    expect(c.noteOffAction).toEqual(m.Velocity2Ctl.NoteOffAction.VelUp)
    expect(c.outMin).toEqual(32391)
    expect(c.outMax).toEqual(24497)
    expect(c.outOffset).toEqual(2319)
    expect(c.outController).toEqual(131) // [TODO] out of range
  })
})
"""
