# import { m } from "@radiant-voices/modtypes"
# import HarmonicType = m.SpectraVoice.HarmonicType
#
# describe("SpectraVoice controllers", () => {
#   let mod: m.SpectraVoice.Module
#   beforeEach(() => {
#     mod = m.spectraVoice()
#   })
#   test("changing harmonic index controller changes
#   harmonic value controllers", () => {
#     expect(mod.c.harmonic).toEqual(0)
#     expect(mod.c.hFreqHz).toEqual(1098)
#     expect(mod.c.hVolume).toEqual(255)
#     expect(mod.c.hWidth).toEqual(3)
#     expect(mod.c.hType).toEqual(HarmonicType.Hsin)
#
#     mod.c.harmonic = 1
#     expect(mod.c.harmonic).toEqual(1)
#     expect(mod.c.hFreqHz).toEqual(0)
#     expect(mod.c.hVolume).toEqual(0)
#     expect(mod.c.hWidth).toEqual(0)
#     expect(mod.c.hType).toEqual(HarmonicType.Hsin)
#   })
#   test("changing harmonic value controllers updates
#   harmonic tables", () => {
#     expect(mod.c.harmonic).toEqual(0)
#     expect(mod.c.hFreqHz).toEqual(1098)
#     expect(mod.c.hVolume).toEqual(255)
#     expect(mod.c.hWidth).toEqual(3)
#     expect(mod.c.hType).toEqual(HarmonicType.Hsin)
#     expect(mod.behavior?.harmonicFrequencies[0]).toEqual(1098)
#     expect(mod.behavior?.harmonicVolumes[0]).toEqual(255)
#     expect(mod.behavior?.harmonicWidths[0]).toEqual(3)
#     expect(mod.behavior?.harmonicTypes[0]).toEqual(HarmonicType.Hsin)
#     mod.c.hFreqHz = 1099
#     mod.c.hVolume = 254
#     mod.c.hWidth = 4
#     mod.c.hType = HarmonicType.Overtones1
#     expect(mod.behavior?.harmonicFrequencies[0]).toEqual(1099)
#     expect(mod.behavior?.harmonicVolumes[0]).toEqual(254)
#     expect(mod.behavior?.harmonicWidths[0]).toEqual(4)
#     expect(mod.behavior?.harmonicTypes[0]).toEqual(HarmonicType.Overtones1)
#   })
# })
