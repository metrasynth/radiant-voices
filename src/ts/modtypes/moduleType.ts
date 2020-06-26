interface BooleanOption {
  type: "boolean"
  name: string
  default: boolean
}

interface RangeOption {
  type: "range"
  name: string
  default: number
  min: number
  max: number
}

export type Option = BooleanOption | RangeOption

export interface ControllerValues {
  [key: string]: boolean | number
}

export interface Controllers {
  controllerValues: ControllerValues
}

export interface OptionValues {
  [key: string]: boolean | number
}

export interface Options {
  optionValues: OptionValues
}

export interface ModuleType {
  readonly c: Controllers
  readonly controllers: Controllers
  readonly controllerValues: ControllerValues
  readonly o: Options
  readonly options: Options
  readonly optionValues: OptionValues
  flags: number
  name: string
  finetune: number
  relativeNote: number
  layer: number
  scale: number
  controllerSetters: ControllerSetters
}

interface ControllerSetter {
  (val: number): void
}

type ControllerSetters = Array<ControllerSetter>
