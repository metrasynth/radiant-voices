import { Amplifier } from "./amplifier"
import { DcBlocker } from "./dcBlocker"
import { Delay } from "./delay"
import { Distortion } from "./distortion"
import { Echo } from "./echo"
import { Eq } from "./eq"
import { Filter } from "./filter"
import { Flanger } from "./flanger"
import { FilterPro } from "./filterPro"
import { Lfo } from "./lfo"
import { Loop } from "./loop"
import { ModuleBase } from "./moduleBase"
import { PitchShifter } from "./pitchShifter"
import { Reverb } from "./reverb"
import { Channels, EnvelopeFlags, Format, LoopType, VibratoType } from "./samplerEnums"
import { VocalFilter } from "./vocalFilter"
import { Vibrato } from "./vibrato"
import { WaveShaper } from "./waveShaper"

import { ModuleSpecificBehavior } from "./moduleSpecificBehavior"
import { Chunk } from "../chunks/chunk"
import { fromIffBuffer } from "../chunks/fromIffBuffer"
import { ModuleDataChunk, ModuleDataChunks } from "../moduleDataChunk"
import { Note } from "../note"
import { readSunVoxFile } from "../reader/readSunVoxFile"
import { Synth } from "../synth"
import { toIffBuffer } from "../chunks/toIffBuffer"
import { objectChunks } from "../writer/objectChunks"

type EffectModule =
  | Amplifier.Module
  | DcBlocker.Module
  | Delay.Module
  | Distortion.Module
  | Echo.Module
  | Eq.Module
  | Filter.Module
  | FilterPro.Module
  | Flanger.Module
  | Lfo.Module
  | Loop.Module
  | PitchShifter.Module
  | Reverb.Module
  | VocalFilter.Module
  | Vibrato.Module
  | WaveShaper.Module

type SampleData = Int8Array | Int16Array | Float32Array | Uint8Array

export class SamplerBehavior extends ModuleSpecificBehavior {
  vibratoType: VibratoType = VibratoType.Sin
  vibratoAttack: number = 0
  vibratoDepth: number = 0
  vibratoRate: number = 0
  volumeFadeout: number = 0

  noteSampleMap = defaultNoteSampleMap()
  samples = defaultSamples()
  effect?: EffectModule

  volumeEnvelope = new VolumeEnvelope()
  panningEnvelope = new PanningEnvelope()
  pitchEnvelope = new PitchEnvelope()
  effectControl1Envelope = new EffectControlEnvelope(0x105)
  effectControl2Envelope = new EffectControlEnvelope(0x106)
  effectControl3Envelope = new EffectControlEnvelope(0x107)
  effectControl4Envelope = new EffectControlEnvelope(0x108)

  chnk(): number {
    return 0x10b
  }

  processDataChunks(dataChunks: ModuleDataChunks) {
    for (const chunk of dataChunks) {
      const { chnm } = chunk
      if (chnm === 0) {
        this.processSamplerConfigChunk(chunk)
      } else if (chnm < 0x101 && chnm % 2 === 1) {
        this.processSampleMetaChunk(chunk)
      } else if (chnm < 0x101 && chnm % 2 === 0) {
        this.processSampleDataChunk(chunk)
      } else if (chnm === 0x101) {
        // unknown
      } else if (chnm === 0x102) {
        this.volumeEnvelope.processChunk(chunk)
      } else if (chnm === 0x103) {
        this.panningEnvelope.processChunk(chunk)
      } else if (chnm === 0x104) {
        this.pitchEnvelope.processChunk(chunk)
      } else if (chnm === 0x105) {
        this.effectControl1Envelope.processChunk(chunk)
      } else if (chnm === 0x106) {
        this.effectControl2Envelope.processChunk(chunk)
      } else if (chnm === 0x107) {
        this.effectControl3Envelope.processChunk(chunk)
      } else if (chnm === 0x108) {
        this.effectControl4Envelope.processChunk(chunk)
      } else if (chnm === 0x10a) {
        this.processEffectSynthChunk(chunk)
      }
    }
  }

  private processSamplerConfigChunk(chunk: ModuleDataChunk) {
    const { chdt } = chunk
    if (!chdt) return

    // Controller-like values.
    this.vibratoType = chdt[0xee]
    this.vibratoAttack = chdt[0xef]
    this.vibratoDepth = chdt[0xf0]
    this.vibratoRate = chdt[0xf1]
    this.volumeFadeout = chdt[0xf2] | (chdt[0xf3] << 8)

    // Note/sample map
    const { noteSampleMap } = this
    for (let note = 0; note < 119; ++note) {
      const index = note + 0x104
      noteSampleMap[note] = chdt[index]
    }

    // TODO: rest of the bytes!
  }

  private processSampleMetaChunk(chunk: ModuleDataChunk) {
    const { chdt, chnm } = chunk
    if (!chdt) return

    const index = Math.floor((chnm - 1) / 2)
    let sample = this.samples[index]
    if (!sample) {
      this.samples[index] = sample = new Sample()
    }

    const { buffer, byteOffset } = chdt
    sample.loopStart = new Uint32Array(buffer, byteOffset + 0x04, 1)[0]
    sample.loopLength = new Uint32Array(buffer, byteOffset + 0x08, 1)[0]
    sample.volume = chdt[0x0c]
    sample.finetune = new Int8Array(buffer, byteOffset + 0x0d, 1)[0]
    sample.panning = chdt[0x0f] - 128
    sample.relativeNote = new Int8Array(buffer, byteOffset + 0x10, 1)[0]

    sample.loopType = chdt[0x0e] & 0b11
    // ignore sample format and stereo flag;
    // those are more accurately set from the sample data chunk
  }

  private processSampleDataChunk(chunk: ModuleDataChunk) {
    const { chdt, chnm, chff, chfr } = chunk
    if (!chdt || chff === undefined || chfr === undefined) return
    const index = Math.floor((chnm - 2) / 2)
    let sample = this.samples[index]
    if (!sample) {
      this.samples[index] = sample = new Sample()
    }
    sample.rate = chfr || 44100
    sample.format = chff & 0b0111
    sample.channels = chff & 0b1000
    switch (sample.format) {
      case Format.Int8:
        sample.data = new Int8Array(chdt.buffer, chdt.byteOffset)
        break
      case Format.Int16:
        sample.data = new Int16Array(chdt.buffer, chdt.byteOffset)
        break
      case Format.Float32:
        sample.data = new Float32Array(chdt.buffer, chdt.byteOffset)
        break
      default:
        console.warn(`Unknown sample format ${sample.format}`)
    }
  }

  private processEffectSynthChunk(chunk: ModuleDataChunk) {
    const { chdt } = chunk
    if (!chdt) return
    this.effect = (readSunVoxFile(fromIffBuffer(chdt.buffer)) as Synth)
      .module as EffectModule
  }

  *typeSpecificChunks(): Generator<Chunk> {
    // sampler config
    const configBlob = new Uint8Array(0x184)

    // sampler config: controller-like values
    configBlob[0xee] = this.vibratoType
    configBlob[0xef] = this.vibratoAttack
    configBlob[0xf0] = this.vibratoDepth
    configBlob[0xf1] = this.vibratoRate
    configBlob[0xf2] = this.volumeFadeout & 0xff
    configBlob[0xf3] = (this.volumeFadeout >> 8) & 0xff

    // sampler config: note/sample map
    const { noteSampleMap } = this
    for (let note = 0; note < 119; ++note) {
      const index = note + 0x104
      const sampleIndex = noteSampleMap[note]
      configBlob[index] = sampleIndex
      const legacyIndex = note + 0x24
      if (legacyIndex < 0x84) {
        configBlob[legacyIndex] = sampleIndex
      }
    }

    // sampler config: SunVox compatibility odds and ends
    let maxSampleIndex = 0
    for (let i = 0; i < this.samples.length; ++i) {
      if (this.samples[i]) {
        maxSampleIndex = i + 1
      }
    }
    configBlob[0x1c] = maxSampleIndex

    configBlob[0xf4] = 0x40
    configBlob[0xf6] = 0x80
    configBlob[0xfc] = "P".charCodeAt(0)
    configBlob[0xfd] = "M".charCodeAt(0)
    configBlob[0xfe] = "A".charCodeAt(0)
    configBlob[0xff] = "S".charCodeAt(0)
    configBlob[0x100] = 0x04

    // TODO: fill in legacy envelopes

    yield { name: "CHNM", type: "uint32", value: 0 }
    yield { name: "CHDT", type: "bytes", value: configBlob }

    // sample meta & waveforms
    for (let i = 0; i < this.samples.length; ++i) {
      const sample = this.samples[i]
      if (!sample) continue

      // meta
      const metaBlob = new Uint8Array(0x28)
      const { frames } = sample
      metaBlob[0x00] = frames & 0xff
      metaBlob[0x01] = (frames >> 8) & 0xff
      metaBlob[0x02] = (frames >> 16) & 0xff
      metaBlob[0x03] = (frames >> 24) & 0xff
      const { loopStart } = sample
      metaBlob[0x04] = loopStart & 0xff
      metaBlob[0x05] = (loopStart >> 8) & 0xff
      metaBlob[0x06] = (loopStart >> 16) & 0xff
      metaBlob[0x07] = (loopStart >> 24) & 0xff
      const { loopLength } = sample
      metaBlob[0x08] = loopLength & 0xff
      metaBlob[0x09] = (loopLength >> 8) & 0xff
      metaBlob[0x0a] = (loopLength >> 16) & 0xff
      metaBlob[0x0b] = (loopLength >> 24) & 0xff
      metaBlob[0x0c] = sample.volume
      metaBlob[0x0d] = Uint8Array.from(Int8Array.from([sample.finetune]))[0]
      metaBlob[0x0f] = sample.panning + 128
      metaBlob[0x10] = Uint8Array.from(Int8Array.from([sample.relativeNote]))[0]

      const { loopType, format, channels } = sample
      let loopFormatFlags = loopType
      if (format === Format.Int16) loopFormatFlags |= 0x10
      if (format === Format.Float32) loopFormatFlags |= 0x20
      if (channels === Channels.Stereo) loopFormatFlags |= 0x40
      metaBlob[0x0e] = loopFormatFlags

      yield { name: "CHNM", type: "uint32", value: i * 2 + 1 }
      yield { name: "CHDT", type: "bytes", value: metaBlob }

      // waveform
      yield { name: "CHNM", type: "uint32", value: i * 2 + 2 }
      yield {
        name: "CHDT",
        type: "bytes",
        value: new Uint8Array(sample.data.buffer, sample.data.byteOffset),
      }
      yield { name: "CHFF", type: "uint32", value: sample.format | sample.channels }
      yield { name: "CHFR", type: "uint32", value: sample.rate }
    }

    // envelopes
    yield* this.volumeEnvelope.chunks()
    yield* this.panningEnvelope.chunks()
    yield* this.pitchEnvelope.chunks()
    yield* this.effectControl1Envelope.chunks()
    yield* this.effectControl2Envelope.chunks()
    yield* this.effectControl3Envelope.chunks()
    yield* this.effectControl4Envelope.chunks()

    // effect
    const { effect } = this
    if (effect) {
      const synth = new Synth(this.effect as ModuleBase)
      const f = toIffBuffer(objectChunks(synth))
      yield { name: "CHNM", type: "uint32", value: 0x10a }
      yield { name: "CHDT", type: "bytes", value: new Uint8Array(f.buffer) }
    }
  }
}

function defaultNoteSampleMap() {
  const map: Record<number, number> = {}
  for (let note = Note.C0; note <= Note.a9; ++note) {
    map[note] = 0
  }
  return map
}

function defaultSamples() {
  const samples: Array<Sample | undefined> = []
  samples.length = 128
  return samples
}

class Sample {
  data: SampleData = new Float32Array(0)
  loopStart: number = 0
  loopLength: number = 0
  volume: number = 64
  finetune: number = 100
  format: Format = Format.Float32
  channels: Channels = Channels.Stereo
  rate: number = 44100
  loopType: LoopType = LoopType.Off
  loopSustain: boolean = false
  panning: number = 0
  relativeNote: number = 16

  /**
   * Get number of bytes per frame in the sample data.
   */
  get frameSize() {
    const factor = { [Channels.Mono]: 1, [Channels.Stereo]: 2 }[this.channels]
    return this.format * factor
  }

  /**
   * Get number of frames that are in the sample data.
   */
  get frames() {
    if (this.data === undefined) return 0
    return this.data.buffer.byteLength / this.frameSize
  }
}

interface Envelope {
  readonly chnm: number
  readonly min: number
  readonly max: number
  points: EnvelopePoint[]
  flags: EnvelopeFlags
  ctlIndex: number
  gainPct: number
  velocity: number
  sustainPoint: number
  loopStartPoint: number
  loopEndPoint: number
}

interface EnvelopePoint {
  tick: number
  value: number
}

class BaseEnvelope implements Envelope {
  chnm = 0
  min = 0
  max = 0x8000
  flags = 0
  points: EnvelopePoint[] = []
  ctlIndex = 0
  gainPct = 100
  velocity = 0
  sustainPoint = 0
  loopStartPoint = 0
  loopEndPoint = 0

  processChunk(chunk: ModuleDataChunk) {
    const { chdt } = chunk
    if (!chdt) return
    const { buffer, byteOffset } = chdt
    this.flags = new Uint16Array(buffer, byteOffset, 1)[0]
    this.ctlIndex = chdt[2]
    this.gainPct = chdt[3]
    this.velocity = chdt[4]
    const envelopeLength = new Uint16Array(buffer, byteOffset + 8, 1)[0]
    this.sustainPoint = new Uint16Array(buffer, byteOffset + 0xa, 1)[0]
    this.loopStartPoint = new Uint16Array(buffer, byteOffset + 0xc, 1)[0]
    this.loopEndPoint = new Uint16Array(buffer, byteOffset + 0xe, 1)[0]
    this.points = []
    for (let i = 0; i < envelopeLength; ++i) {
      const tick = new Uint16Array(buffer, byteOffset + 0x14 + 4 * i, 1)[0]
      const value = new Uint16Array(buffer, byteOffset + 0x16 + 4 * i, 1)[0] + this.min
      this.points.push({ tick, value })
    }
  }

  *chunks(): Generator<Chunk> {
    const blob = new Uint8Array(0x14 + 4 * this.points.length)
    // TODO: clearer way to set uint16 values
    blob[0] = this.flags & 0xff
    blob[1] = (this.flags >> 8) & 0xff
    blob[2] = this.ctlIndex
    blob[3] = this.gainPct
    blob[4] = this.velocity
    blob[8] = this.points.length & 0xff
    blob[9] = (this.points.length >> 8) & 0xff
    blob[0xa] = this.sustainPoint & 0xff
    blob[0xb] = (this.sustainPoint >> 8) & 0xff
    blob[0xc] = this.loopStartPoint & 0xff
    blob[0xd] = (this.loopStartPoint >> 8) & 0xff
    blob[0xe] = this.loopEndPoint & 0xff
    blob[0xf] = (this.loopEndPoint >> 8) & 0xff
    for (let i = 0; i < this.points.length; ++i) {
      let { tick, value } = this.points[i]
      value = Math.max(0, Math.min(0x8000, value - this.min))
      blob[0x14 + 4 * i] = tick & 0xff
      blob[0x15 + 4 * i] = (tick >> 8) & 0xff
      blob[0x16 + 4 * i] = value & 0xff
      blob[0x17 + 4 * i] = (value >> 8) & 0xff
    }
    yield { name: "CHNM", type: "uint32", value: this.chnm }
    yield { name: "CHDT", type: "bytes", value: blob }
  }
}

class VolumeEnvelope extends BaseEnvelope {
  chnm = 0x102
}

class PanningEnvelope extends BaseEnvelope {
  chnm = 0x103
  min = -0x4000
  max = 0x4000
}

class PitchEnvelope extends BaseEnvelope {
  chnm = 0x104
  min = -0x4000
  max = 0x4000
}

class EffectControlEnvelope extends BaseEnvelope {
  constructor(readonly chnm: number) {
    super()
  }
}
