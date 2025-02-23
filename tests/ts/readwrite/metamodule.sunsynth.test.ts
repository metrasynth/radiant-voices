import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the metamodule.sunsynth file", () => {
  const filePath = "tests/files/metamodule.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.MetaModule.Module
    expect(mod.flags).toEqual(32841)
    expect(mod.name).toEqual("MetaModule")
    expect(mod.behavior?.mappings).toEqual(expectedMappings)
    expect(mod.behavior?.controllerNames).toEqual(expectedControllerNames)
    const { c } = mod
    expect(c.volume).toEqual(149)
    expect(c.inputModule).toEqual(1)
    expect(c.playPatterns).toEqual(m.MetaModule.PlayPatterns.OnNoRepeat)
    expect(c.bpm).toEqual(560)
    expect(c.tpl).toEqual(30)
    const { o } = mod
    expect(o.userDefinedControllers).toEqual(2)
    expect(o.arpeggiator).toBeFalsy()
    expect(o.applyVelocityToProject).toBeFalsy()
    expect(o.eventOutput).toBeTruthy()
    expect(o.receiveNotesFromKeyboard).toBeFalsy()
    expect(o.doNotReceiveNotesFromKeyboard).toBeFalsy()

    o.receiveNotesFromKeyboard = true
    expect(o.receiveNotesFromKeyboard).toBeTruthy()
    expect(o.doNotReceiveNotesFromKeyboard).toBeFalsy()

    o.doNotReceiveNotesFromKeyboard = true
    expect(o.receiveNotesFromKeyboard).toBeFalsy()
    expect(o.doNotReceiveNotesFromKeyboard).toBeTruthy()

    const project = mod.behavior?.project
    expect(project).toBeDefined()
    expect(project?.modules[0]?.typeName).toEqual("Output")
    expect(project?.modules[1]?.typeName).toEqual("Analog generator")
  })
})

const expectedMappings = [
  { module: 1, controller: 0 },
  { module: 1, controller: 1 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
  { module: 0, controller: 0 },
]

const expectedControllerNames = [
  "V",
  "W",
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
  undefined,
]

describe("Reading the metamodule-option-7a file", () => {
  const filePath = "tests/files/metamodule-option-7a.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.MetaModule.Module
    const { o } = mod
    expect(o.autoBpmTpl).toBeTruthy()
  })
})

describe("Reading the metamodule-option-79 file", () => {
  const filePath = "tests/files/metamodule-option-79.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.MetaModule.Module
    const { o } = mod
    expect(o.ignoreEff_31AfterLastNoteOff).toBeTruthy()
  })
})

describe("Reading the metamodule-option-78 file", () => {
  const filePath = "tests/files/metamodule-option-78.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.MetaModule.Module
    const { o } = mod
    expect(o.jumpToRlPatternAfterLastNoteOff).toBeTruthy()
  })
})
