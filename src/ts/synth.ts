import { SunVoxContainer } from "./containers"
import { ModuleBase } from "./modtypes/moduleBase"
import { SunVoxVersion } from "./sunVoxVersion"

export class Synth implements SunVoxContainer {
  sunVoxVersion: SunVoxVersion = [1, 9, 5, 2]

  constructor(readonly module: ModuleBase) {}
}
