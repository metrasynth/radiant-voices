import { readFileSync } from "fs"
import { fromIffBuffer } from "@radiant-voices/chunks/fromIffBuffer"
import { readSunVoxFile } from "@radiant-voices/reader/readSunVoxFile"
import { Synth } from "@radiant-voices/synth"
import { m } from "@radiant-voices/modtypes"
import { objectChunks } from "@radiant-voices/writer/objectChunks"
import { toIffBuffer } from "@radiant-voices/chunks/toIffBuffer"

describe("Reading the fmx.sunsynth file", () => {
  const filePath = "tests/files/fmx.sunsynth"
  let synth: Synth
  beforeAll(() => {
    // read, write, read
    const f = readFileSync(filePath)
    synth = readSunVoxFile(fromIffBuffer(f)) as Synth
    const f2 = toIffBuffer(objectChunks(synth))
    synth = readSunVoxFile(fromIffBuffer(f2)) as Synth
  })
  test("has correct properties, controllers, and options", () => {
    const mod = synth.module as m.Fmx.Module
    expect(mod.flags).toEqual(0x02000059)
    expect(mod.name).toEqual("FMX")
    expect(mod.behavior?.customWaveform).toEqual(expectedCustomWaveform)
    const { c } = mod

    expect(c.volume).toEqual(24762)
    expect(c.panning).toEqual(69)
    expect(c.sampleRate).toEqual(m.Fmx.SampleRate._11025hz)
    expect(c.polyphony).toEqual(15)
    expect(c.channels).toEqual(m.Fmx.Channels.Stereo)
    expect(c.inputToOperator).toEqual(0)
    expect(c.inputToCustomWaveform).toEqual(m.Fmx.InputCustomWaveform.Continuous)
    expect(c.adsrSmoothTransitions).toEqual(m.Fmx.AdsrSmoothTransitions.Off)
    expect(c.noiseFilter).toEqual(9897)
    expect(c.op1Volume).toEqual(20098)
    expect(c.op2Volume).toEqual(20987)
    expect(c.op3Volume).toEqual(21450)
    expect(c.op4Volume).toEqual(17213)
    expect(c.op5Volume).toEqual(31592)
    expect(c.op1Attack).toEqual(5679)
    expect(c.op2Attack).toEqual(5951)
    expect(c.op3Attack).toEqual(7917)
    expect(c.op4Attack).toEqual(1259)
    expect(c.op5Attack).toEqual(4740)
    expect(c.op1Decay).toEqual(1799)
    expect(c.op2Decay).toEqual(8041)
    expect(c.op3Decay).toEqual(9284)
    expect(c.op4Decay).toEqual(6614)
    expect(c.op5Decay).toEqual(653)
    expect(c.op1SustainLevel).toEqual(1506)
    expect(c.op2SustainLevel).toEqual(2534)
    expect(c.op3SustainLevel).toEqual(3234)
    expect(c.op4SustainLevel).toEqual(23034)
    expect(c.op5SustainLevel).toEqual(3503)
    expect(c.op1Release).toEqual(6497)
    expect(c.op2Release).toEqual(2429)
    expect(c.op3Release).toEqual(3023)
    expect(c.op4Release).toEqual(9900)
    expect(c.op5Release).toEqual(6740)
    expect(c.op1AttackCurve).toEqual(m.Fmx.AdsrCurve.Exp1)
    expect(c.op2AttackCurve).toEqual(m.Fmx.AdsrCurve.Exp2)
    expect(c.op3AttackCurve).toEqual(m.Fmx.AdsrCurve.Exp2)
    expect(c.op4AttackCurve).toEqual(m.Fmx.AdsrCurve.Exp2)
    expect(c.op5AttackCurve).toEqual(m.Fmx.AdsrCurve.NegExp2)
    expect(c.op1DecayCurve).toEqual(m.Fmx.AdsrCurve.Linear)
    expect(c.op2DecayCurve).toEqual(m.Fmx.AdsrCurve.Exp1)
    expect(c.op3DecayCurve).toEqual(m.Fmx.AdsrCurve.Exp2)
    expect(c.op4DecayCurve).toEqual(m.Fmx.AdsrCurve.Exp2)
    expect(c.op5DecayCurve).toEqual(m.Fmx.AdsrCurve.Sin)
    expect(c.op1ReleaseCurve).toEqual(m.Fmx.AdsrCurve.NegExp2)
    expect(c.op2ReleaseCurve).toEqual(m.Fmx.AdsrCurve.Exp1)
    expect(c.op3ReleaseCurve).toEqual(m.Fmx.AdsrCurve.Exp2)
    expect(c.op4ReleaseCurve).toEqual(m.Fmx.AdsrCurve.NegExp2)
    expect(c.op5ReleaseCurve).toEqual(m.Fmx.AdsrCurve.Sin)
    expect(c.op1Sustain).toEqual(m.Fmx.Sustain.On)
    expect(c.op2Sustain).toEqual(m.Fmx.Sustain.On)
    expect(c.op3Sustain).toEqual(m.Fmx.Sustain.Repeat)
    expect(c.op4Sustain).toEqual(m.Fmx.Sustain.On)
    expect(c.op5Sustain).toEqual(m.Fmx.Sustain.Repeat)
    expect(c.op1SustainPedal).toEqual(false)
    expect(c.op2SustainPedal).toEqual(true)
    expect(c.op3SustainPedal).toEqual(true)
    expect(c.op4SustainPedal).toEqual(false)
    expect(c.op5SustainPedal).toEqual(true)
    expect(c.op1EnvelopeScalingPerKey).toEqual(-77)
    expect(c.op2EnvelopeScalingPerKey).toEqual(125)
    expect(c.op3EnvelopeScalingPerKey).toEqual(-60)
    expect(c.op4EnvelopeScalingPerKey).toEqual(-57)
    expect(c.op5EnvelopeScalingPerKey).toEqual(43)
    expect(c.op1VolumeScalingPerKey).toEqual(-100)
    expect(c.op2VolumeScalingPerKey).toEqual(41)
    expect(c.op3VolumeScalingPerKey).toEqual(1)
    expect(c.op4VolumeScalingPerKey).toEqual(-32)
    expect(c.op5VolumeScalingPerKey).toEqual(-63)
    expect(c.op1VelocitySensitivity).toEqual(36)
    expect(c.op2VelocitySensitivity).toEqual(-50)
    expect(c.op3VelocitySensitivity).toEqual(-117)
    expect(c.op4VelocitySensitivity).toEqual(3)
    expect(c.op5VelocitySensitivity).toEqual(99)
    expect(c.op1Waveform).toEqual(m.Fmx.Waveform.Hsin)
    expect(c.op2Waveform).toEqual(m.Fmx.Waveform.Asin)
    expect(c.op3Waveform).toEqual(m.Fmx.Waveform.Sin)
    expect(c.op4Waveform).toEqual(m.Fmx.Waveform.TrianglePow_3)
    expect(c.op5Waveform).toEqual(m.Fmx.Waveform.SawPow_3)
    expect(c.op1Noise).toEqual(18063)
    expect(c.op2Noise).toEqual(12653)
    expect(c.op3Noise).toEqual(20322)
    expect(c.op4Noise).toEqual(12541)
    expect(c.op5Noise).toEqual(3300)
    expect(c.op1Phase).toEqual(4269)
    expect(c.op2Phase).toEqual(16359)
    expect(c.op3Phase).toEqual(21738)
    expect(c.op4Phase).toEqual(13193)
    expect(c.op5Phase).toEqual(25224)
    expect(c.op1FreqMultiply).toEqual(22923)
    expect(c.op2FreqMultiply).toEqual(31970)
    expect(c.op3FreqMultiply).toEqual(7673)
    expect(c.op4FreqMultiply).toEqual(26613)
    expect(c.op5FreqMultiply).toEqual(2735)
    expect(c.op1ConstantPitch).toEqual(-694)
    expect(c.op2ConstantPitch).toEqual(1841)
    expect(c.op3ConstantPitch).toEqual(-3511)
    expect(c.op4ConstantPitch).toEqual(1062)
    expect(c.op5ConstantPitch).toEqual(2358)
    expect(c.op1SelfModulation).toEqual(11895)
    expect(c.op2SelfModulation).toEqual(720)
    expect(c.op3SelfModulation).toEqual(11736)
    expect(c.op4SelfModulation).toEqual(16926)
    expect(c.op5SelfModulation).toEqual(23405)
    expect(c.op1Feedback).toEqual(24510)
    expect(c.op2Feedback).toEqual(25778)
    expect(c.op3Feedback).toEqual(9683)
    expect(c.op4Feedback).toEqual(26614)
    expect(c.op5Feedback).toEqual(17200)
    expect(c.op1ModulationType).toEqual(m.Fmx.ModulationType.Sub)
    expect(c.op2ModulationType).toEqual(m.Fmx.ModulationType.MinAbs)
    expect(c.op3ModulationType).toEqual(m.Fmx.ModulationType.MaxAbs)
    expect(c.op4ModulationType).toEqual(m.Fmx.ModulationType.Min)
    expect(c.op5ModulationType).toEqual(m.Fmx.ModulationType.Sub)
    expect(c.op1OutputMode).toEqual(0)
    expect(c.op2OutputMode).toEqual(15)
    expect(c.op3OutputMode).toEqual(1)
    expect(c.op4OutputMode).toEqual(2)
  })
})

const expectedCustomWaveform = new Float32Array([
  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
  0.0,
])
