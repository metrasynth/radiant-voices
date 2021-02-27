import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"
import { Note } from "@radiant-voices"
import EnvelopeFlags = m.Sampler.EnvelopeFlags
import EnvelopeInterpolation = m.Sampler.EnvelopeInterpolation
import LoopType = m.Sampler.LoopType
import SampleInterpolation = m.Sampler.SampleInterpolation
import VibratoType = m.Sampler.VibratoType

describe("Reading the sampler.sunsynth file", () => {
  const filePath = "tests/files/sampler.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Sampler.Module
    expect(mod.flags).toEqual(33881)
    expect(mod.name).toEqual("Sampler")

    // Controllers
    const { c } = mod
    expect(c.volume).toEqual(267)
    expect(c.panning).toEqual(50)
    expect(c.sampleInterpolation).toEqual(SampleInterpolation.Linear)
    expect(c.envelopeInterpolation).toEqual(EnvelopeInterpolation.Off)
    expect(c.polyphonyCh).toEqual(32)
    expect(c.recThreshold).toEqual(2448)

    const { behavior } = mod
    expect(behavior).toBeDefined()
    if (!behavior) throw ""

    // Global sampler config
    expect(behavior.vibratoType).toEqual(VibratoType.Square)
    expect(behavior.vibratoAttack).toEqual(50)
    expect(behavior.vibratoDepth).toEqual(118)
    expect(behavior.vibratoRate).toEqual(11)
    expect(behavior.volumeFadeout).toEqual(3696)

    // Envelopes
    const { volumeEnvelope } = behavior
    expect(volumeEnvelope.flags).toEqual(EnvelopeFlags.Enabled | EnvelopeFlags.Sustain)
    expect(volumeEnvelope.ctlIndex).toEqual(0)
    expect(volumeEnvelope.gainPct).toEqual(64)
    expect(volumeEnvelope.velocity).toEqual(32)
    expect(volumeEnvelope.sustainPoint).toEqual(0)
    expect(volumeEnvelope.loopStartPoint).toEqual(0)
    expect(volumeEnvelope.loopEndPoint).toEqual(0)
    expect(volumeEnvelope.points).toEqual([
      { tick: 0, value: 32768 },
      { tick: 33, value: 9728 },
      { tick: 98, value: 14848 },
      { tick: 133, value: 4096 },
      { tick: 256, value: 0 },
    ])

    const { panningEnvelope } = behavior
    expect(panningEnvelope.flags).toEqual(0)
    expect(panningEnvelope.ctlIndex).toEqual(0)
    expect(panningEnvelope.gainPct).toEqual(82)
    expect(panningEnvelope.velocity).toEqual(28)
    expect(panningEnvelope.sustainPoint).toEqual(0)
    expect(panningEnvelope.loopStartPoint).toEqual(0)
    expect(panningEnvelope.loopEndPoint).toEqual(0)
    expect(panningEnvelope.points).toEqual([
      { tick: 0, value: 0 },
      { tick: 36, value: -4096 },
      { tick: 68, value: 4096 },
      { tick: 115, value: 9728 },
    ])

    const { pitchEnvelope } = behavior
    expect(pitchEnvelope.flags).toEqual(0)
    expect(pitchEnvelope.ctlIndex).toEqual(0)
    expect(pitchEnvelope.gainPct).toEqual(53)
    expect(pitchEnvelope.velocity).toEqual(83)
    expect(pitchEnvelope.sustainPoint).toEqual(0)
    expect(pitchEnvelope.loopStartPoint).toEqual(0)
    expect(pitchEnvelope.loopEndPoint).toEqual(0)
    expect(pitchEnvelope.points).toEqual([
      { tick: 0, value: 3072 },
      { tick: 33, value: -6144 },
      { tick: 190, value: 9216 },
    ])

    const { effectControl1Envelope } = behavior
    expect(effectControl1Envelope.flags).toEqual(
      EnvelopeFlags.Enabled | EnvelopeFlags.Loop
    )
    expect(effectControl1Envelope.ctlIndex).toEqual(0)
    expect(effectControl1Envelope.gainPct).toEqual(69)
    expect(effectControl1Envelope.velocity).toEqual(32)
    expect(effectControl1Envelope.sustainPoint).toEqual(0)
    expect(effectControl1Envelope.loopStartPoint).toEqual(1)
    expect(effectControl1Envelope.loopEndPoint).toEqual(2)
    expect(effectControl1Envelope.points).toEqual([
      { tick: 0, value: 32768 },
      { tick: 23, value: 28160 },
      { tick: 52, value: 25088 },
      { tick: 64, value: 32768 },
    ])

    const { effectControl2Envelope } = behavior
    expect(effectControl2Envelope.flags).toEqual(EnvelopeFlags.Enabled)
    expect(effectControl2Envelope.ctlIndex).toEqual(1)
    expect(effectControl2Envelope.gainPct).toEqual(30)
    expect(effectControl2Envelope.velocity).toEqual(83)
    expect(effectControl2Envelope.sustainPoint).toEqual(0)
    expect(effectControl2Envelope.loopStartPoint).toEqual(0)
    expect(effectControl2Envelope.loopEndPoint).toEqual(0)
    expect(effectControl2Envelope.points).toEqual([
      { tick: 0, value: 23040 },
      { tick: 88, value: 29696 },
    ])

    const { effectControl3Envelope } = behavior
    expect(effectControl3Envelope.flags).toEqual(EnvelopeFlags.Enabled)
    expect(effectControl3Envelope.ctlIndex).toEqual(2)
    expect(effectControl3Envelope.gainPct).toEqual(28)
    expect(effectControl3Envelope.velocity).toEqual(74)
    expect(effectControl3Envelope.sustainPoint).toEqual(0)
    expect(effectControl3Envelope.loopStartPoint).toEqual(0)
    expect(effectControl3Envelope.loopEndPoint).toEqual(0)
    expect(effectControl3Envelope.points).toEqual([
      { tick: 0, value: 15360 },
      { tick: 178, value: 31232 },
    ])

    const { effectControl4Envelope } = behavior
    expect(effectControl4Envelope.flags).toEqual(0)
    expect(effectControl4Envelope.ctlIndex).toEqual(3)
    expect(effectControl4Envelope.gainPct).toEqual(70)
    expect(effectControl4Envelope.velocity).toEqual(58)
    expect(effectControl4Envelope.sustainPoint).toEqual(0)
    expect(effectControl4Envelope.loopStartPoint).toEqual(0)
    expect(effectControl4Envelope.loopEndPoint).toEqual(0)
    expect(effectControl4Envelope.points).toEqual([
      { tick: 0, value: 5632 },
      { tick: 191, value: 11264 },
    ])

    // Effect
    const { effect } = behavior
    expect(effect).toBeDefined()
    if (!effect) throw ""
    expect(effect).toBeInstanceOf(m.Reverb.Module)

    // Note/sample map
    const { noteSampleMap } = behavior
    expect(noteSampleMap[Note.C4 - 1]).toEqual(0)
    expect(noteSampleMap[Note.G4 - 1]).toEqual(1)
    expect(noteSampleMap[Note.G5 - 1]).toEqual(2)

    // Samples
    const { samples } = behavior
    const [sample1, sample2, sample3] = [samples[0], samples[1], samples[2]]
    expect(sample1).toBeDefined()
    expect(sample2).toBeDefined()
    expect(sample3).toBeDefined()
    if (!(sample1 && sample2 && sample3)) throw ""

    expect(sample1.frames).toEqual(32)
    expect(sample1.loopStart).toEqual(8)
    expect(sample1.loopLength).toEqual(13)
    expect(sample1.loopType).toEqual(LoopType.Forward)
    expect(sample1.volume).toEqual(44)
    expect(sample1.finetune).toEqual(72)
    expect(sample1.panning).toEqual(58)
    expect(sample1.relativeNote).toEqual(28)
    // prettier-ignore
    expect(sample1.data).toEqual(new Int8Array([
      43,  42,  40,  37,  14,  -1,  -8, -16,
      -24, -29,  -4,  14,  22,  20,  10,  -3,
      -11, -17, -21, -24, -25, -25, -25, -22,
      -18, -13,  -9,  -8, -10, -13, -17, -19
    ]))

    expect(sample2.frames).toEqual(32)
    expect(sample2.loopStart).toEqual(0)
    expect(sample2.loopLength).toEqual(0)
    expect(sample2.loopType).toEqual(LoopType.Off)
    expect(sample2.volume).toEqual(49)
    expect(sample2.finetune).toEqual(78)
    expect(sample2.panning).toEqual(-27)
    expect(sample2.relativeNote).toEqual(-16)
    // prettier-ignore
    expect(sample2.data).toEqual(new Int16Array([
       -9088,  -8960,  -8960,  -8896,
       -9152, -11648, -14656, -16256,
      -16256, -15808, -15040, -14336,
      -13504, -13120, -11584, -10944,
       -4992,   5504,  13056,  21184,
       27008,  28096,  25664,  23040,
       20992,  17984,  16000,  14400,
       12992,  11968,  11136,  10432
    ]))

    expect(sample3.frames).toEqual(16)
    expect(sample3.loopStart).toEqual(8)
    expect(sample3.loopLength).toEqual(1)
    expect(sample3.loopType).toEqual(LoopType.PingPong)
    expect(sample3.volume).toEqual(46)
    expect(sample3.finetune).toEqual(-49)
    expect(sample3.panning).toEqual(37)
    expect(sample3.relativeNote).toEqual(8)
    // prettier-ignore
    expect(sample3.data).toEqual(new Float32Array([
      -0.310546875,   0.66015625,    -0.234375,
         0.6640625, -0.177734375,   0.65234375,
      -0.103515625,  0.591796875,  -0.01171875,
          0.515625,  0.052734375,  0.333984375,
       0.123046875,  0.166015625,       0.1875,
       0.017578125,  0.271484375, -0.103515625,
       0.333984375,  -0.16796875,      0.40625,
        -0.2421875,  0.458984375, -0.294921875,
       0.498046875, -0.330078125,     0.515625,
        -0.3515625,     0.515625,  -0.37890625,
          0.515625, -0.396484375
    ]))
  })
})
