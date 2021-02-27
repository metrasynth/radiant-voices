import { m } from "../../src/ts/modtypes"

describe("LFO", () => {
  let module: m.Lfo.Module

  beforeEach(() => {
    module = m.lfo()
  })

  test('has a "volume" controller that defaults to 256', () => {
    expect(module.c.volume).toEqual(256)
  })
  test('has a "volume" controller that can be changed', () => {
    module.c.volume = 128
    expect(module.c.volume).toEqual(128)
  })
  test('has a "freq" controller that has limits based on "frequencyUnit"', () => {
    module.c.frequencyUnit = m.Lfo.FrequencyUnit.Ms
    module.c.freq = 4001
    expect(module.c.freq).toEqual(4000)
  })
  test('sets "freq" within new bounds whenever "frequencyUnit" changes', () => {
    module.c.frequencyUnit = m.Lfo.FrequencyUnit.Hz
    module.c.freq = 16384
    expect(module.c.freq).toEqual(16384)
    module.c.frequencyUnit = m.Lfo.FrequencyUnit.Ms
    expect(module.c.freq).toEqual(4000)
  })
})
