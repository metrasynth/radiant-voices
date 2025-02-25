import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the multisynth.sunsynth file", () => {
  const filePath = "tests/files/multisynth.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.MultiSynth.Module
    expect(mod.flags).toEqual(0x03021049)
    expect(mod.name).toEqual("MultiSynth")
    expect(mod.behavior?.noteVelocityCurve).toEqual(expectedNoteVelocityCurve)
    expect(mod.behavior?.velocityVelocityCurve).toEqual(expectedVelocityVelocityCurve)
    expect(mod.behavior?.notePitchCurve).toEqual(expectedNotePitchCurve)

    const { c } = mod
    expect(c.transpose).toEqual(-29)
    expect(c.randomPitch).toEqual(3704)
    expect(c.velocity).toEqual(50)
    expect(c.finetune).toEqual(-25)
    expect(c.randomPhase).toEqual(2078)
    expect(c.randomVelocity).toEqual(17602)
    expect(c.phase).toEqual(15216)
    expect(c.curve2Influence).toEqual(204)

    const { o } = mod
    expect(o.useStaticNote_C5).toEqual(true)
    expect(o.ignoreNotesWithZeroVelocity).toEqual(false)
    expect(o.trigger).toEqual(true)
    expect(o.activeCurve).toEqual(m.MultiSynth.ActiveCurve.NotePitch)
    expect(o.generateMissedNoteOffCommands).toEqual(true)
    expect(o.roundNoteX).toEqual(false)
    expect(o.roundPitchY).toEqual(true)
    expect(o.recordNotesToScaleCurve).toEqual(false)
    expect(o.outNoteOutNoteMinusInNotePlus_C5).toEqual(true)
    expect(o.outPortMode).toEqual(m.MultiSynth.OutPortMode.Cyclic)
  })
})
const expectedNoteVelocityCurve = new Uint8Array([
  116, 113, 113, 113, 115, 117, 119, 120, 122, 123, 125, 128, 134, 140, 139, 131, 118,
  105, 91, 79, 67, 58, 50, 46, 45, 45, 47, 51, 55, 60, 64, 69, 74, 79, 84, 89, 94, 100,
  104, 109, 114, 120, 126, 131, 136, 140, 144, 148, 152, 155, 157, 157, 154, 148, 140,
  132, 125, 119, 113, 107, 102, 97, 93, 89, 85, 81, 77, 74, 72, 70, 68, 67, 66, 66, 66,
  66, 66, 67, 69, 72, 75, 79, 84, 90, 96, 103, 109, 116, 123, 131, 139, 147, 153, 157,
  161, 164, 167, 171, 173, 175, 177, 180, 182, 185, 187, 190, 193, 196, 198, 201, 204,
  207, 212, 217, 221, 226, 230, 234, 237, 238, 236, 232, 224, 214, 202, 182, 149, 103,
])
const expectedVelocityVelocityCurve = new Uint8Array([
  165, 151, 139, 129, 121, 114, 109, 106, 105, 106, 108, 111, 113, 116, 118, 121, 123,
  126, 128, 131, 133, 136, 138, 141, 143, 146, 148, 151, 153, 156, 158, 161, 163, 164,
  165, 164, 163, 160, 157, 152, 148, 143, 138, 133, 128, 123, 118, 113, 108, 103, 99,
  96, 93, 90, 87, 84, 82, 80, 79, 78, 77, 76, 75, 74, 73, 72, 71, 70, 69, 68, 67, 66,
  65, 64, 63, 62, 61, 61, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60,
  60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 60, 61, 63, 66, 69, 72,
  76, 80, 84, 88, 92, 96, 100, 104, 108, 112, 116, 120, 124, 127, 131, 134, 138, 141,
  145, 147, 149, 149, 149, 148, 147, 144, 142, 139, 137, 134, 132, 129, 127, 124, 122,
  119, 117, 114, 112, 109, 107, 104, 102, 99, 96, 93, 90, 87, 84, 81, 78, 75, 72, 69,
  66, 63, 61, 61, 62, 65, 70, 75, 80, 85, 90, 95, 100, 104, 109, 113, 118, 122, 127,
  131, 135, 138, 142, 145, 149, 152, 156, 159, 162, 165, 167, 170, 172, 175, 177, 180,
  182, 185, 187, 190, 192, 195, 197, 200, 201, 202, 202, 201, 200, 198, 197, 195, 194,
  192, 191, 189, 188, 186, 185, 183, 182, 180, 178, 176, 174, 172, 170, 168, 166, 164,
  162, 160, 158, 156, 154, 152, 150, 148, 146, 144, 142, 140, 138, 136, 134, 132, 130,
  129, 128,
])

const expectedNotePitchCurve = new Uint16Array([
  33717, 34667, 34904, 35142, 35854, 36211, 36448, 36685, 36804, 36804, 36804, 36448,
  34905, 32768, 30987, 30037, 29206, 28375, 27662, 27069, 26891, 26713, 26534, 26356,
  26297, 26238, 26000, 26000, 26000, 26000, 26238, 26534, 26831, 27128, 27425, 27781,
  28137, 28731, 29324, 29799, 30393, 30630, 30868, 30868, 30868, 30868, 30868, 30749,
  30630, 30512, 30393, 30393, 30393, 30393, 30512, 30749, 30987, 31343, 31580, 31818,
  31936, 31936, 31936, 31936, 31580, 30868, 30512, 30215, 29918, 29443, 29383, 29324,
  29206, 29206, 29206, 29206, 29443, 30037, 30749, 30927, 31343, 31462, 31580, 31580,
  31580, 31580, 31462, 31224, 31105, 30808, 30512, 30393, 30274, 30156, 30037, 29918,
  29799, 29681, 29562, 29562, 29562, 29562, 29740, 29918, 30393, 30868, 31303, 31738,
  32174, 32827, 33480, 34133, 34786, 35439, 36092, 36448, 36804, 37160, 37635, 38110,
  38229, 38407, 38585, 38585, 38585, 38585, 38110, 34073,
])
