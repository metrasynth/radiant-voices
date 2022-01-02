import { PatternBase } from "./pattern"
import { m } from "./modtypes"
import { SunVoxContainer } from "./containers"
import { ModuleBase } from "./modtypes/moduleBase"
import { SunVoxVersion } from "./sunVoxVersion"

export interface ModuleConnection {
  src: number
  dest: number
}

export enum SyncCommand {
  StartStop = 1 << 0,
  Tempo = 1 << 1,
  Position = 1 << 2,
}

export class Project implements SunVoxContainer {
  basedOnVersion: SunVoxVersion = [1, 9, 6, 1]
  currentLine = 1
  currentPattern = 0
  currentTrack = 0
  flags = 0
  globalVolume = 80
  initialBpm = 125
  initialTpl = 6
  lastSelectedGenerator = 0
  modulesCurrentLayer = 0
  modulesLayerMask = 0x00000000
  modulesScale = 256
  modulesXOffset = 0
  modulesYOffset = 0
  modulesZoom = 256
  name = "Project"
  receiveSyncMidi = SyncCommand.StartStop
  receiveSyncOther = SyncCommand.StartStop
  selectedModule = 0
  sunVoxVersion: SunVoxVersion = [1, 9, 6, 1]
  timeGrid = 4
  timeGrid2 = 4
  timelinePosition = 0

  readonly patterns: Array<PatternBase | undefined> = []
  readonly modules: Array<ModuleBase | undefined> = []

  get outputModule(): m.Output.Module {
    return this.modules[0] as m.Output.Module
  }

  constructor() {
    m.output().attachTo(this)
  }

  attach(obj: ModuleBase): Project
  attach(obj: PatternBase): Project
  attach(obj: any): Project {
    if (obj instanceof ModuleBase) {
      obj.index = this.modules.length
      obj.project = this
      this.modules.push(obj)
    } else if (obj instanceof PatternBase) {
      obj.index = this.patterns.length
      obj.project = this
      this.patterns.push(obj)
    } else {
      throw new Error("Cannot attach")
    }
    return this
  }
}
