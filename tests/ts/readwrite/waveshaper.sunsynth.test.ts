import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

const expectedCurve = new Uint16Array([
  18754, 16280, 16280, 16280, 16280, 16280, 30913, 31737, 33180, 34313, 35447, 37714,
  39156, 40599, 41423, 42659, 43896, 45029, 46163, 47193, 48224, 48945, 49667, 50388,
  51109, 52346, 52964, 53582, 53788, 53995, 54407, 54819, 55025, 55128, 55231, 55231,
  55231, 55231, 55231, 55231, 55231, 55025, 54201, 51934, 50285, 46988, 44515, 42041,
  41423, 38126, 37508, 34828, 32355, 31119, 29470, 26791, 25142, 24214, 21639, 20402,
  19166, 17723, 16487, 15456, 14013, 13498, 12983, 12159, 11334, 11025, 10716, 10407,
  10098, 9892, 9892, 9892, 9892, 9892, 9892, 9995, 10098, 10716, 11334, 12055, 12777,
  13601, 14426, 15147, 15868, 16692, 17517, 17929, 18478, 19028, 19578, 19990, 20608,
  21227, 21227, 21433, 21639, 21845, 22051, 22051, 22051, 22051, 22051, 22051, 22051,
  22051, 22051, 22051, 22051, 22051, 22051, 22051, 22051, 21845, 21432, 21020, 19990,
  19681, 19372, 18547, 17517, 16280, 16074, 15868, 15044, 14941, 14838, 14632, 14632,
  14632, 14632, 14632, 14735, 14838, 14941, 15044, 15662, 16211, 16761, 17311, 18135,
  18960, 19990, 21020, 21775, 22531, 23287, 24042, 24798, 25554, 26584, 27615, 28645,
  29676, 30500, 31325, 32046, 32768, 33180, 33798, 34416, 35034, 35653, 35756, 35859,
  35859, 35859, 35859, 35859, 35756, 35653, 35034, 34416, 32974, 32355, 31737, 31015,
  30294, 29676, 29058, 28027, 27409, 26791, 26379, 25554, 24936, 24318, 24112, 23700,
  23494, 23287, 23287, 23287, 23287, 23287, 23287, 23287, 23287, 23287, 23287, 23287,
  23287, 23287, 23287, 23287, 23287, 23287, 23356, 23425, 23494, 23631, 23768, 23906,
  24249, 24592, 24936, 25554, 26173, 26791, 27409, 28130, 28852, 30707, 31634, 32561,
  33437, 34313, 35189, 36065, 37507, 38950, 40392, 41835, 42556, 43278, 44308, 45338,
  46369, 47193, 48017, 48842, 49735, 50628, 51522, 52552, 53582, 54303, 55025, 56880,
  57292, 58735, 63475,
])
describe("Reading the waveshaper.sunsynth file", () => {
  const filePath = "tests/files/waveshaper.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.WaveShaper.Module
    expect(mod.flags).toEqual(81)
    expect(mod.name).toEqual("WaveShaper")
    expect(mod.behavior?.curve).toEqual(expectedCurve)
    const { c } = mod
    expect(c.inputVolume).toEqual(144)
    expect(c.mix).toEqual(195)
    expect(c.outputVolume).toEqual(77)
    expect(c.symmetric).toEqual(true)
    expect(c.mode).toEqual(m.WaveShaper.Mode.HqMono)
    expect(c.dcBlocker).toEqual(true)
  })
})
