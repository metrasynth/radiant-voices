import { Project } from "@radiant-voices"

import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { base2to10 } from "@radiant-voices/conversions"

describe("Reading an empty sunvox file", () => {
  const filePath = "tests/files/empty.sunvox"
  let project: Project
  beforeAll(() => {
    const f = readFileSync(filePath)
    const chunks = fromIffBuffer(f)
    project = readSunVoxFile(chunks) as Project
  })
  test("has correctly read properties", () => {
    expect(project.name).toEqual("empty")
    expect(project.initialBpm).toEqual(125)
    expect(project.initialTpl).toEqual(6)
    expect(base2to10(project.globalVolume)).toEqual(100)
    expect(project.sunVoxVersion).toEqual([1, 9, 1, 0])
    expect(project.basedOnVersion).toEqual([1, 2, 3, 4])
    expect(project.modules.length).toEqual(4)
    expect(project.modules[1]).toBeUndefined()
    expect(project.modules[2]).toBeUndefined()
    expect(project.modules[3]).toBeUndefined()
    const { outputModule } = project
    expect(outputModule.finetune).toEqual(0)
    expect(outputModule.relativeNote).toEqual(0)
    expect(outputModule.layer).toEqual(0)
    expect(base2to10(outputModule.scale)).toEqual(100)
  })
})
