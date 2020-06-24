import { Project } from "../../src/ts"

describe("behavior of Projects", () => {
  let project: Project
  beforeEach(() => {
    project = new Project()
  })
  test("has initial BPM of 125", () => {
    expect(project.initialBpm).toEqual(125)
  })
})
