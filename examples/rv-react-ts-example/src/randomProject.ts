import { Pattern, Project, m } from "radiant-voices"

export function randomProject() {
  const project = new Project()
  project.initialBpm = 150
  const fm = m.fm().attachTo(project)
  fm.linkTo(project.outputModule)
  fm.name = "FreqMod"
  const pat = new Pattern(8, 1).attachTo(project)
  pat.data[0][0].note = 49
  pat.data[0][0].module = fm.index + 1
  pat.data[1][0].note = 128 // note off
  return { project: project, filename: "fromWebBrowser.sunvox" }
}
