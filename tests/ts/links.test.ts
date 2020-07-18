import { m, Project } from "@radiant-voices"
import { Linkables } from "@radiant-voices/links"

type Amp = m.Amplifier.Module

describe("linking modules together", () => {
  let project: Project
  let mod1: Amp
  let mod2: Amp
  let mod3: Amp
  let mod4: Amp
  beforeEach(() => {
    project = new Project()
    mod1 = m.amplifier().attachTo(project)
    mod2 = m.amplifier().attachTo(project)
    mod3 = m.amplifier().attachTo(project)
    mod4 = m.amplifier().attachTo(project)
  })
  test("linkFrom module-module", () => {
    const result = mod1.linkFrom(mod2).linkFrom(mod3).linkFrom(mod4)
    expect(result).toBe(mod4)
    expect(mod1.incomingLinks).toContain(mod2.index)
    expect(mod2.incomingLinks).toContain(mod3.index)
    expect(mod3.incomingLinks).toContain(mod4.index)
  })
  test("linkTo module-module", () => {
    const result = mod1.linkTo(mod2).linkTo(mod3).linkTo(mod4)
    expect(result).toBe(mod4)
    expect(mod2.incomingLinks).toContain(mod1.index)
    expect(mod3.incomingLinks).toContain(mod2.index)
    expect(mod4.incomingLinks).toContain(mod3.index)
  })
  test("linkFrom module-modules", () => {
    const result = mod1.linkFrom([mod2, mod3, mod4])
    expect(result).toBeInstanceOf(Linkables)
    expect((result as Linkables).members).toContain(mod2)
    expect((result as Linkables).members).toContain(mod3)
    expect((result as Linkables).members).toContain(mod4)
    expect(mod1.incomingLinks).toContain(mod2.index)
    expect(mod1.incomingLinks).toContain(mod3.index)
    expect(mod1.incomingLinks).toContain(mod4.index)
  })
  test("linkTo module-modules", () => {
    const result = mod1.linkTo([mod2, mod3, mod4])
    expect(result).toBeInstanceOf(Linkables)
    expect((result as Linkables).members).toContain(mod2)
    expect((result as Linkables).members).toContain(mod3)
    expect((result as Linkables).members).toContain(mod4)
    expect(mod2.incomingLinks).toContain(mod1.index)
    expect(mod3.incomingLinks).toContain(mod1.index)
    expect(mod4.incomingLinks).toContain(mod1.index)
  })
  test("linkFrom modules-modules", () => {
    mod1.linkFrom([mod2, mod3]).linkFrom(mod4)
    expect(mod1.incomingLinks).toContain(mod2.index)
    expect(mod1.incomingLinks).toContain(mod3.index)
    expect(mod2.incomingLinks).toContain(mod4.index)
    expect(mod3.incomingLinks).toContain(mod4.index)
  })
  test("linkFrom and linkTo", () => {
    mod1.linkFrom([mod2, mod3]).linkTo(mod4)
    expect(mod1.incomingLinks).toContain(mod2.index)
    expect(mod1.incomingLinks).toContain(mod3.index)
    expect(mod4.incomingLinks).toContain(mod2.index)
    expect(mod4.incomingLinks).toContain(mod3.index)
  })
})
