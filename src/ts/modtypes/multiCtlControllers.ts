import { MultiCtlBaseControllers } from "./multiCtlBaseControllers"
import { MultiCtl } from "./multiCtl"

export class MultiCtlControllers extends MultiCtlBaseControllers {
  get value(): number {
    return super.value
  }

  set value(newValue: number) {
    super.value = newValue
    const module = this.module as MultiCtl.Module
    const project = module.project
    if (!project) return
    const mappings = module.behavior?.mappings
    if (!mappings) throw new Error("[TODO] error message")
    for (const [index, { ctl }] of mappings.entries()) {
      const destModIndex = module.outLinks[index]
      if (!destModIndex) continue
      const destMod = project.modules[destModIndex]
      if (!destMod) throw new Error("[TODO] error message")
      destMod.setRawControllerValue(ctl, newValue)
    }
  }
}
