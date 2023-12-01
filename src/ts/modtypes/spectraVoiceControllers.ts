import { SpectraVoiceBaseControllers } from "./spectraVoiceBaseControllers"
import { SpectraVoice } from "./spectraVoice"
import { HarmonicType } from "./spectraVoiceEnums"

export class SpectraVoiceControllers extends SpectraVoiceBaseControllers {
  get harmonic() {
    return super.harmonic
  }

  set harmonic(newValue: number) {
    const { behavior } = this.module as SpectraVoice.Module
    super.harmonic = newValue
    const index = this.harmonic
    if (behavior) {
      super.hFreq = behavior.harmonicFrequencies[index]
      super.hVolume = behavior.harmonicVolumes[index]
      super.hWidth = behavior.harmonicWidths[index]
      super.hType = behavior.harmonicTypes[index]
    }
  }

  get hFreq(): number {
    return super.hFreq
  }

  set hFreq(newValue: number) {
    const { behavior } = this.module as SpectraVoice.Module
    super.hFreq = newValue
    if (behavior) {
      behavior.harmonicFrequencies[this.harmonic] = this.hFreq
    }
  }

  get hVolume(): number {
    return super.hVolume
  }

  set hVolume(newValue: number) {
    const { behavior } = this.module as SpectraVoice.Module
    super.hVolume = newValue
    if (behavior) {
      behavior.harmonicVolumes[this.harmonic] = this.hVolume
    }
  }

  get hWidth(): number {
    return super.hWidth
  }

  set hWidth(newValue: number) {
    const { behavior } = this.module as SpectraVoice.Module
    super.hWidth = newValue
    if (behavior) {
      behavior.harmonicWidths[this.harmonic] = this.hWidth
    }
  }

  get hType(): HarmonicType {
    return super.hType
  }

  set hType(newValue: HarmonicType) {
    const { behavior } = this.module as SpectraVoice.Module
    super.hType = newValue
    if (behavior) {
      behavior.harmonicTypes[this.harmonic] = this.hType
    }
  }
}
