import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"
import { MessageType, MidiMap, Slope } from "@radiant-voices/controllerMidiMap"
import { Chunk } from "@radiant-voices/chunks/chunk"

const expectedDrawnWaveform = new Int8Array([
  0,
  -100,
  -90,
  0,
  -35,
  -35,
  -35,
  -35,
  -35,
  -35,
  -35,
  -32,
  -24,
  -17,
  -4,
  12,
  36,
  94,
  77,
  50,
  33,
  27,
  50,
  32,
  -90,
  -120,
  100,
  90,
  59,
  21,
  0,
  54,
])
describe("Reading the analog-generator.sunsynth file", () => {
  const filePath = "tests/files/analog-generator.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.AnalogGenerator.Module
    expect(mod.flags).toEqual(0x49)
    expect(mod.name).toEqual("analog-generator")
    expect(mod.behavior?.drawnWaveform).toEqual(expectedDrawnWaveform)
    const { c } = mod
    expect(c.volume).toEqual(103)
    expect(c.waveform).toEqual(m.AnalogGenerator.Waveform.Drawn)
    expect(c.panning).toEqual(-19)
    expect(c.attack).toEqual(91)
    expect(c.release).toEqual(97)
    expect(c.sustain).toEqual(true)
    expect(c.exponentialEnvelope).toEqual(true)
    expect(c.dutyCycle).toEqual(534)
    expect(c.freq2).toEqual(1393)
    expect(c.filter).toEqual(m.AnalogGenerator.Filter.Bp_12db)
    expect(c.fFreqHz).toEqual(5611)
    expect(c.fResonance).toEqual(1183)
    expect(c.fExponentialFreq).toEqual(false)
    expect(c.fAttack).toEqual(87)
    expect(c.fRelease).toEqual(58)
    expect(c.fEnvelope).toEqual(m.AnalogGenerator.FilterEnvelope.Off)
    expect(c.polyphonyCh).toEqual(32)
    expect(c.mode).toEqual(m.AnalogGenerator.Mode.Lq)
    expect(c.noise).toEqual(9)
    const { o } = mod
    expect(o.volumeEnvelopeScalingPerKey).toEqual(true)
    expect(o.filterEnvelopeScalingPerKey).toEqual(false)
    expect(o.volumeScalingPerKey).toEqual(true)
    expect(o.filterFreqScalingPerKey).toEqual(false)
    expect(o.filterFreqScalingPerKeyReverse).toEqual(true)
    expect(o.filterFreqEqNoteFreq).toEqual(false)
    expect(o.velocityDependentFilterFrequency).toEqual(true)
    expect(o.velocityDependentFilterResonance).toEqual(false)
    expect(o.frequencyDiv_2).toEqual(true)
    expect(o.smoothFrequencyChange).toEqual(false)
    expect(o.retainPhase).toEqual(true)
    expect(o.randomPhase).toEqual(false)
    expect(o.trueZeroAttackRelease).toEqual(true)
  })
  test("has correct chunks when written out", () => {
    const chunks = objectChunks(synth)
    const v = () => chunks.next().value
    const expectChunk = (chunk: Chunk) => {
      expect(v()).toEqual(chunk)
    }
    const expectCval = (value: number) => {
      expectChunk({ name: "CVAL", type: "int32", value })
    }
    expectChunk({ name: "SSYN", type: "empty" })
    expectChunk({ name: "VERS", type: "version", value: [1, 9, 5, 2] })
    expectChunk({ name: "SFFF", type: "uint32", value: 0x49 })
    expectChunk({ name: "SNAM", type: "fixedString", value: "analog-generator" })
    expectChunk({ name: "STYP", type: "cstring", value: "Analog generator" })
    expectChunk({ name: "SFIN", type: "int32", value: 1 })
    expectChunk({ name: "SREL", type: "int32", value: 2 })
    expectChunk({ name: "SSCL", type: "uint32", value: 0x1dd })
    expectChunk({ name: "SCOL", type: "color", value: [174, 255, 0] })
    expectChunk({ name: "SMII", type: "uint32", value: 0 })
    expectChunk({ name: "SMIC", type: "uint32", value: 0 })
    expectChunk({ name: "SMIB", type: "int32", value: -1 })
    expectChunk({ name: "SMIP", type: "int32", value: -1 })
    expectCval(103)
    expectCval(4)
    expectCval(109)
    expectCval(91)
    expectCval(97)
    expectCval(1)
    expectCval(1)
    expectCval(534)
    expectCval(1393)
    expectCval(3)
    expectCval(5611)
    expectCval(1183)
    expectCval(0)
    expectCval(87)
    expectCval(58)
    expectCval(0)
    expectCval(32)
    expectCval(2)
    expectCval(9)
    const { name, type, values } = v()
    expect({ name, type }).toEqual({ name: "CMID", type: "midiMaps" })
    expect((values as Array<MidiMap>).length).toEqual(19)
    expect(values[0]).toEqual({
      channel: 1,
      messageType: MessageType.ControlChange,
      messageParameter: 2,
      slope: Slope.Exp1,
    } as MidiMap)
    expect(values[1]).toEqual({
      channel: 0,
      messageType: MessageType.Unset,
      messageParameter: 0,
      slope: Slope.Linear,
    } as MidiMap)
    expectChunk({ name: "CHNK", type: "uint32", value: 2 })
    expectChunk({ name: "CHNM", type: "uint32", value: 1 })
    expectChunk({
      name: "CHDT",
      type: "bytes",
      value: new Uint8Array([1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1]), // [TODO] should be padded to 64 bytes
    })
    expectChunk({ name: "CHNM", type: "uint32", value: 0 })
    expectChunk({
      name: "CHDT",
      type: "bytes",
      value: new Uint8Array(expectedDrawnWaveform),
    })
    expectChunk({ name: "CHFR", type: "uint32", value: 44100 })
    expect(chunks.next().value).toEqual({ name: "SEND", type: "empty" })
    expect(chunks.next().done).toBeTruthy()
  })
})
