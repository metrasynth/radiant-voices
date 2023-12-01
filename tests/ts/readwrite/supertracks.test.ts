import { Pattern, Project } from "@radiant-voices"

import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { PatternFlagsPFLG } from "@radiant-voices/pattern"

describe("Reading a supertracks sunvox file", () => {
  const filePath = "tests/files/supertracks.sunvox"
  let project: Project
  beforeAll(() => {
    const f = readFileSync(filePath)
    const chunks = fromIffBuffer(f)
    project = readSunVoxFile(chunks) as Project
  })
  test("has correctly read properties", () => {
    expect(project.flags).toEqual(1)
  })
  test("has patterns with correct flags", () => {
    const [pattern1, pattern2, ..._] = project.patterns
    expect((pattern1 as Pattern).flagsPFLG).toEqual(0)
    expect((pattern2 as Pattern).flagsPFLG).toEqual(PatternFlagsPFLG.ContinueNotesAtEnd)
  })
})
