import { Pattern, PatternClone } from "./pattern"
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
  initialBpm = 125
  initialTpl = 6
  globalVolume = 80
  name = "Project"
  timeGrid = 4
  timeGrid2 = 4
  modulesScale = 256
  modulesZoom = 256
  modulesXOffset = 0
  modulesYOffset = 0
  modulesLayerMask = 0x00000000
  modulesCurrentLayer = 0
  timelinePosition = 0
  selectedModule = 0
  lastSelectedGenerator = 0
  currentPattern = 0
  currentTrack = 0
  currentLine = 1
  receiveSyncMidi = SyncCommand.StartStop
  receiveSyncOther = SyncCommand.StartStop

  sunVoxVersion: SunVoxVersion = [1, 9, 5, 2]
  basedOnVersion: SunVoxVersion = [1, 9, 5, 2]

  readonly patterns: Array<Pattern | PatternClone | undefined> = []
  readonly modules: Array<ModuleBase | undefined> = [m.output()]
  readonly moduleConnections: ModuleConnection[] = []

  get outputModule(): m.Output.Module {
    return this.modules[0] as m.Output.Module
  }

  constructor() {
    this.outputModule.index = 0
    this.outputModule.project = this
  }
}
