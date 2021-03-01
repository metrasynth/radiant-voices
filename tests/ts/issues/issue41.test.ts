import { Project } from "@radiant-voices/project"
import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading issue41/sample.sunvox file", () => {
  const filePath = "tests/files/issue41/sample.sunvox"
  let project: Project
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    project = readSunVoxFile(fromIffBuffer(f)) as Project
    const f2 = toIffBuffer(objectChunks(project))
    project = readSunVoxFile(fromIffBuffer(f2)) as Project
  })
  test("has expected delay values", () => {
    const delay = project.modules[1] as m.Delay.Module
    const { c } = delay
    expect(c.delayL).toEqual(8192)
    expect(c.delayR).toEqual(8192)
    expect(c.delayUnit).toEqual(m.Delay.DelayUnit.Hz)
  })
})
