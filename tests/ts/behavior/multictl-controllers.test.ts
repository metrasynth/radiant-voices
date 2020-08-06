import { Project, m } from "@radiant-voices"

describe("MultiCtl controllers", () => {
  let project: Project
  beforeEach(() => {
    project = new Project()
  })
  test("changing multictl value propagates value to destination controllers", () => {
    const multictl = m.multiCtl().attachTo(project)
    const amp1 = m.amplifier().attachTo(project)
    const amp2 = m.amplifier().attachTo(project)
    multictl.linkTo([amp1, amp2])
    const mappings = multictl.behavior?.mappings
    expect(mappings).toBeDefined()
    if (!mappings) return
    mappings[0].ctl = m.Amplifier.CtlNum.FineVolume
    mappings[1].ctl = m.Amplifier.CtlNum.FineVolume
    multictl.c.value = 42
    expect(amp1.c.fineVolume).toEqual(42)
    expect(amp2.c.fineVolume).toEqual(42)
  })
})
