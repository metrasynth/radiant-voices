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
    expect(c.panning).toEqual(197)
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
    expect(c.op3SustainLevel).toEqual(3252)
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
    expect(c.op2ModulationType).toEqual(m.Fmx.ModulationType.Frequency)
    expect(c.op3ModulationType).toEqual(m.Fmx.ModulationType.AmplitudeMul)
    expect(c.op4ModulationType).toEqual(m.Fmx.ModulationType.Min)
    expect(c.op5ModulationType).toEqual(m.Fmx.ModulationType.Sub)
    expect(c.op1OutputMode).toEqual(0)
    expect(c.op2OutputMode).toEqual(15)
    expect(c.op3OutputMode).toEqual(1)
    expect(c.op4OutputMode).toEqual(2)
  })
})

const expectedCustomWaveform = new Float32Array([
  0.23258860409259796, 0.28716719150543213, 0.33988499641418457, 0.3905003070831299,
  0.43874162435531616, 0.4843390882015228, 0.5272365808486938, 0.5672786235809326,
  0.6041287779808044, 0.6377434730529785, 0.6680856943130493, 0.6950294971466064,
  0.718247652053833, 0.7379667162895203, 0.7541000843048096, 0.7664385437965393,
  0.7750416398048401, 0.7800208926200867, 0.7814271450042725, 0.7789393663406372,
  0.772946298122406, 0.7635419964790344, 0.8365955948829651, 0.8237184882164001,
  0.8068667054176331, 0.7860580086708069, 0.7628260850906372, 0.7345373034477234,
  0.7025718092918396, 0.6699537038803101, 0.6312897205352783, 0.5893936157226562,
  0.544437050819397, 0.5012393593788147, 0.4510851502418518, 0.3985336422920227,
  0.3437948226928711, 0.2933891713619232, 0.23541350662708282, 0.17610563337802887,
  0.12288980931043625, 0.06199882552027702, 0.0006794976070523262,
  -0.060750387609004974, -0.114327073097229, -0.1749647706747055, -0.23475059866905212,
  -0.2859053313732147, -0.343142569065094, -0.39861631393432617, -0.45199453830718994,
  -0.4964962601661682, -0.5451078414916992, -0.5907776355743408, -0.6332420110702515,
  -0.6677308082580566, -0.7035722732543945, -0.7355403900146484, -0.761013388633728,
  -0.7853280305862427, -0.8052794337272644, -0.8207546472549438, -0.8323591947555542,
  -0.8393306732177734, -0.8415870070457458, -0.8425549268722534, -0.8361444473266602,
  -0.8250311613082886, -0.8092741966247559, -0.7958842515945435, -0.7718666791915894,
  -0.7435323596000671, -0.7110217809677124, -0.6845620274543762, -0.6449171304702759,
  -0.6017055511474609, -0.5671621561050415, -0.5180232524871826, -0.4661105275154114,
  -0.41174858808517456, -0.3687247335910797, -0.3105382025241852, -0.25084754824638367,
  -0.2039089798927307, -0.14217057824134827, -0.07994867116212845,
  -0.017657138407230377, 0.03120145946741104, 0.09301437437534332, 0.15382125973701477,
  0.21325230598449707, 0.2600589692592621, 0.31650879979133606, 0.37059485912323,
  0.41352012753486633, 0.46296000480651855, 0.509142279624939, 0.5518043637275696,
  0.586479663848877, 0.6226131916046143, 0.6545447111129761, 0.6815400123596191,
  0.7059248685836792, 0.7256537079811096, 0.7406331300735474, 0.7554891109466553,
  0.7621375918388367, 0.7638754844665527, 0.7607458829879761, 0.7625833749771118,
  0.7510920166969299, 0.7349019646644592, 0.7273757457733154, 0.7032579779624939,
  0.6748769283294678, 0.6424469947814941, 0.6230509281158447, 0.583917498588562,
  0.5414230823516846, 0.5146118998527527, 0.46669110655784607, 0.4162820279598236,
  0.3637271225452423, 0.32909584045410156, 0.27325761318206787, 0.21629741787910461,
  0.15865042805671692, 0.1194186806678772, 0.06085902452468872, 0.0026753395795822144,
  -0.037727177143096924, -0.09500941634178162, -0.1508598029613495,
  -0.20491887629032135, -0.24377082288265228, -0.29458335041999817,
  -0.34262585639953613, -0.3875787854194641, -0.42161351442337036, -0.46132758259773254,
  -0.4972194731235504, -0.5259842276573181, -0.5554612874984741, -0.5805566906929016,
  -0.6011256575584412, -0.620720624923706, -0.6338445544242859, -0.6421701908111572,
  -0.6542209386825562, -0.6547582745552063, -0.6504875421524048, -0.6414929628372192,
  -0.6426220536231995, -0.6260185837745667, -0.604975163936615, -0.5797035694122314,
  -0.5702730417251587, -0.5382753610610962, -0.5026274919509888, -0.4862741231918335,
  -0.444942831993103, -0.40072768926620483, -0.35400837659835815, -0.3297971785068512,
  -0.27923211455345154, -0.22711940109729767, -0.1988571137189865, -0.14455834031105042,
  -0.08971892297267914, -0.034773483872413635, -0.0032774358987808228,
  0.05166421830654144, 0.10567985475063324, 0.15833929181098938, 0.1900215893983841,
  0.2404107302427292, 0.28846144676208496, 0.318450927734375, 0.36270684003829956,
  0.4037582278251648, 0.4413085877895355, 0.46650227904319763, 0.4984695017337799,
  0.5262860655784607, 0.5466063022613525, 0.5678738355636597, 0.5844971537590027,
  0.5963878035545349, 0.6084100008010864, 0.6129369735717773, 0.6125881671905518,
  0.6073499917984009, 0.6100589632987976, 0.5973415374755859, 0.5798882246017456,
  0.5757607221603394, 0.5511680245399475, 0.5222228169441223, 0.48917868733406067,
  0.47606852650642395, 0.4368879497051239, 0.39428162574768066, 0.37547004222869873,
  0.3278135061264038, 0.277525931596756, 0.22500203549861908, 0.19999893009662628,
  0.14435580372810364, 0.08744654059410095, 0.029727116227149963, 0.0009678304195404053,
  -0.057664625346660614, -0.11603009700775146, -0.14588646590709686,
  -0.20350223779678345, -0.2598009705543518, -0.31434154510498047, -0.3431132435798645,
  -0.39464202523231506, -0.44345176219940186, -0.4697651267051697, -0.5140451192855835,
  -0.5547241568565369, -0.5914567708969116, -0.6121114492416382, -0.642626941204071,
  -0.6685411930084229, -0.6896885633468628, -0.7026157975196838, -0.7163175344467163,
  -0.7248663902282715, -0.7313686013221741, -0.7319871783256531, -0.7272921800613403,
  -0.7172779440879822, -0.7141537070274353, -0.6961480379104614, -0.6729942560195923,
  -0.6629302501678467, -0.6321297287940979, -0.5965664386749268, -0.5564976334571838,
  -0.5373690128326416, -0.49072349071502686, -0.4402046799659729, -0.3861745595932007,
  -0.359448105096817, -0.3004870116710663, -0.23893007636070251, -0.20792485773563385,
  -0.1428895741701126, -0.07629040628671646, -0.008521927520632744, 0.02612357586622238,
  0.0950724333524704, 0.16405576467514038,
])
