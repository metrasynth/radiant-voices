import { Project } from "@radiant-voices/project"
import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading issue54/sample.sunvox file", () => {
  const filePath = "tests/files/issue54/test1.sunvox"
  let project: Project
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    project = readSunVoxFile(fromIffBuffer(f)) as Project
    const f2 = toIffBuffer(objectChunks(project))
    project = readSunVoxFile(fromIffBuffer(f2)) as Project
  })
  test("has expected modules", () => {
    const [mod0, mod1, mod2, mod3] = project.modules
    expect(mod0).toBe(project.outputModule)
    expect(mod1).toBeInstanceOf(m.Reverb.Module)
    expect(mod2).toBeUndefined()
    expect(mod3).toBeInstanceOf(m.Reverb.Module)
  })
})
