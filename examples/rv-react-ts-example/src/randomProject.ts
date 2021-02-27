import { Note, Pattern, Project, m } from "radiant-voices"

export interface ProjectOptions {
  name: string
  initialBpm: number
  modules: ModuleOptions[]
  lines: number
  notes: Note[]
  velocities: number[]
}

export interface ModuleOptions {
  cAttack: number
  cRelease: number
  mAttack: number
  mRelease: number
}

export function randomProject({
  name,
  initialBpm,
  modules,
  lines,
  notes,
  velocities,
}: ProjectOptions) {
  const project = new Project()
  project.initialBpm = initialBpm
  project.name = name

  const mods: m.Fm.AttachedModule[] = []
  for (const module of modules) {
    const mod = m.fm().attachTo(project)
    mods.push(mod)
    mod.c.cAttack = module.cAttack
    mod.c.cRelease = module.cRelease
    mod.c.mAttack = module.mAttack
    mod.c.mRelease = module.mRelease
    mod.c.mSustain = 0
    mod.c.cSustain = 0
  }
  project.outputModule.linkFrom(mods)
  const pat = new Pattern(lines, mods.length).attachTo(project)
  for (let line = 0; line < lines; ++line) {
    const modsIndex = line % mods.length
    const note = pat.data[line][modsIndex]
    const mod = mods[modsIndex]
    note.module = mod.index + 1
    const notesIndex = line % notes.length
    note.note = notes[notesIndex]
    const velocitiesIndex = line % velocities.length
    note.velocity = velocities[velocitiesIndex]
  }
  return { project: project, filename: `${name}.sunvox` }
}
