import { readFileSync } from "fs"
import * as glob from "glob"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"

describe("Reading from the extra files dir", () => {
  const extraFilesPath = "tests/files/extra/"
  const moduleFiles: string[] = glob.sync(`${extraFilesPath}/**/*.sunsynth`)
  const projectFiles: string[] = glob.sync(`${extraFilesPath}/**/*.sunvox`)
  moduleFiles.forEach((filePath) => {
    test(`can read module ${filePath}`, () => {
      const f = readFileSync(filePath)
      readSunVoxFile(fromIffBuffer(f))
    })
  })
  projectFiles.forEach((filePath) => {
    test(`can read project ${filePath}`, () => {
      const f = readFileSync(filePath)
      readSunVoxFile(fromIffBuffer(f))
    })
  })
  if (moduleFiles.length + projectFiles.length === 0) {
    test("Dummy test - no extra files present", () => {
      // no op
    })
  }
})
