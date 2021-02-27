export enum MessageType {
  Unset,
  Note,
  KeyPressure,
  ControlChange,
  Nrpn,
  Rpn,
  ProgramChange,
  ChannelPressure,
  PitchBend,
}

export enum Slope {
  Linear,
  Exp1,
  Exp2,
  SCurve,
  Cut,
  Toggle,
}

export interface MidiMap {
  channel: number
  messageType: MessageType
  messageParameter: number
  slope: Slope
}

export class ControllerMidiMap implements MidiMap {
  channel = 0
  messageType = MessageType.Unset
  messageParameter = 0
  slope = Slope.Linear
}

export interface ControllerMidiMaps {
  [key: string]: ControllerMidiMap
}
