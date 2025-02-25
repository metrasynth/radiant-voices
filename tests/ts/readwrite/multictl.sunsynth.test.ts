import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the multictl.sunsynth file", () => {
  const filePath = "tests/files/multictl.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.MultiCtl.Module
    expect(mod.flags).toEqual(393297)
    expect(mod.name).toEqual("MultiCtl")
    expect(mod.behavior?.mappings).toEqual(expectedMappings)
    expect(mod.behavior?.curve).toEqual(Uint16Array.from(expectedCurve))
    const { c } = mod
    expect(c.value).toEqual(16312)
    expect(c.gain).toEqual(365)
    expect(c.quantization).toEqual(6784)
    expect(c.outOffset).toEqual(-2354)
    expect(c.response).toEqual(193)
    expect(c.sampleRate).toEqual(9133)
  })
})

const expectedMappings = [
  { min: 12224, max: 23408, ctl: 1 },
  { min: 19824, max: 7808, ctl: 2 },
  { min: 0, max: 0x8000, ctl: 0 },
  { min: 0, max: 0x8000, ctl: 0 },
  { min: 0, max: 0x8000, ctl: 0 },
  { min: 0, max: 0x8000, ctl: 0 },
  { min: 0, max: 0x8000, ctl: 0 },
  { min: 0, max: 0x8000, ctl: 0 },
  { min: 0, max: 0x8000, ctl: 0 },
  { min: 0, max: 0x8000, ctl: 0 },
  { min: 0, max: 0x8000, ctl: 0 },
  { min: 0, max: 0x8000, ctl: 0 },
  { min: 0, max: 0x8000, ctl: 0 },
  { min: 0, max: 0x8000, ctl: 0 },
  { min: 0, max: 0x8000, ctl: 0 },
  { min: 0, max: 0x8000, ctl: 0 },
]

const expectedCurve = Uint16Array.from([
  18444, 18732, 19021, 19309, 19598, 19887, 20175, 20464, 20752, 21041, 21330, 21742,
  22154, 22325, 22497, 22669, 22944, 23219, 23494, 23803, 24112, 24421, 24730, 24884,
  25039, 25451, 25451, 25451, 24730, 23906, 23081, 22051, 21020, 19990, 18960, 18444,
  17826, 17208, 16693, 16074, 15559, 15250, 14941, 14323, 13498, 12983, 12571, 12365,
  12365, 12365, 12777, 13292, 13601, 13910, 14838, 15662, 15971, 16899, 17311, 17826,
  18341, 18754, 18960, 19063, 19063, 19063, 19063, 18857, 18032, 16693, 15868, 15559,
  15559, 15765, 16384, 17105, 17414, 17929, 18135, 18341, 18444, 18444, 17620, 16384,
  15044, 13601, 12983, 11643, 10716, 8758, 10407, 13704, 14632, 15044, 15868, 16177,
  16693, 17208, 17723, 18547, 19578, 20814, 22360, 24936, 25967, 27409, 28027, 28131,
  28131, 27924, 27254, 26585, 25606, 24627, 23905, 23184, 22463, 21604, 20745, 19887,
  19028, 18169, 17311, 16589, 15868, 15147, 14426, 13292, 12364, 11437, 10613, 9789,
  9170, 8603, 8037, 7213, 6697, 6491, 6903, 7419, 7831, 8243, 8655, 9067, 9480, 10304,
  10922, 11540, 11918, 12296, 12674, 13086, 13446, 13807, 14323, 14632, 15044, 15095,
  15147, 15250, 15250, 15250, 15250, 15198, 15147, 14803, 14460, 14117, 13395, 12674,
  12124, 11574, 11025, 10201, 9720, 9239, 8758, 8140, 7213, 6852, 6491, 6182, 5873,
  5667, 5461, 5255, 5255, 5255, 5255, 5667, 6079, 6800, 7212, 7625, 8552, 8861, 9119,
  9377, 9686, 9789, 9892, 9995, 10098, 10098, 10098, 10098, 10098, 10098, 10098, 10098,
  10098, 10098, 10304, 10510, 10716, 10922, 11128, 11643, 12468, 13034, 13601, 14013,
  14426, 15456, 16590, 17620, 18650, 19681, 21330, 22772, 23390, 24112, 24730, 24936,
  25451, 25657, 25967, 26070, 26070, 25967, 25142, 24524, 24318, 23700, 23287, 23081,
  22772, 22720, 22566, 22566, 22566, 22566, 22566, 22566, 22772, 22978, 28543,
])
