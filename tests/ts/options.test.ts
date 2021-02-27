import { m } from "../../src/ts/modtypes"

describe("Module options", () => {
  let module: m.AnalogGenerator.Module

  beforeEach(() => {
    module = m.analogGenerator()
  })

  test("has an option that defaults to false", () => {
    expect(module.o.volumeEnvelopeScalingPerKey).toEqual(false)
  })
  test("has an option that defaults to true", () => {
    expect(module.o.smoothFrequencyChange).toEqual(true)
  })
  test("has an option that can change from false to true", () => {
    module.o.smoothFrequencyChange = false
    expect(module.o.smoothFrequencyChange).toEqual(false)
  })
})
