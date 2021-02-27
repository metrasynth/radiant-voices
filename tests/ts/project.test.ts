import { Project } from "../../src/ts"
import { m } from "../../src/ts/modtypes"

describe("behavior of empty Projects", () => {
  let emptyProject: Project
  beforeEach(() => {
    emptyProject = new Project()
  })
  test("has an output module", () => {
    const { outputModule } = emptyProject
    expect(outputModule).toBeInstanceOf(m.Output.Module)
  })
  test("has one module, the output module", () => {
    const { modules, outputModule } = emptyProject
    expect(modules.length).toEqual(1)
    expect(modules[0]).toBe(outputModule)
  })
  test("has no patterns", () => {
    expect(emptyProject.patterns.length).toEqual(0)
  })
  test("appear to be built with SunVox 1.9.6.1", () => {
    expect(emptyProject.sunVoxVersion).toEqual([1, 9, 6, 1])
    expect(emptyProject.basedOnVersion).toEqual([1, 9, 6, 1])
  })
  test("has initial BPM of 125", () => {
    expect(emptyProject.initialBpm).toEqual(125)
  })
  test("has initial TPL of 6", () => {
    expect(emptyProject.initialTpl).toEqual(6)
  })
  test("has global volume of 80", () => {
    expect(emptyProject.globalVolume).toEqual(80)
  })
  test('has the name "Project"', () => {
    expect(emptyProject.name).toEqual("Project")
  })
  test("has time grid of 4", () => {
    expect(emptyProject.timeGrid).toEqual(4)
  })
  test("has modules scale of 256", () => {
    expect(emptyProject.modulesScale).toEqual(256)
  })
  test("has modules zoom of 256", () => {
    expect(emptyProject.modulesZoom).toEqual(256)
  })
  test("has modules X offset of 0", () => {
    expect(emptyProject.modulesXOffset).toEqual(0)
  })
  test("has modules Y offset of 0", () => {
    expect(emptyProject.modulesYOffset).toEqual(0)
  })
  test("has empty layer mask", () => {
    expect(emptyProject.modulesLayerMask).toEqual(0x00000000)
  })
  test("has current layer of 0", () => {
    expect(emptyProject.modulesCurrentLayer).toEqual(0)
  })
  test("has timeline position of 0", () => {
    expect(emptyProject.timelinePosition).toEqual(0)
  })
  test("has output module (0) selected", () => {
    expect(emptyProject.selectedModule).toEqual(0)
  })
  test("has current pattern of 0", () => {
    expect(emptyProject.currentPattern).toEqual(0)
  })
  test("has current track of 0", () => {
    expect(emptyProject.currentTrack).toEqual(0)
  })
  test("has current line of 1", () => {
    expect(emptyProject.currentLine).toEqual(1)
  })
})
