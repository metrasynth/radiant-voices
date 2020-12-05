import { SunVoxContainer } from "./containers"
import { ModuleBase } from "./modtypes/moduleBase"
import { SunVoxVersion } from "./sunVoxVersion"

export class Synth implements SunVoxContainer {
  sunVoxVersion: SunVoxVersion = [1, 9, 6, 1]

  constructor(readonly module: ModuleBase) {}
}
