from rv.api import m


def test_fmx(read_write_read_synth):
    mod: m.Fmx = read_write_read_synth("fmx").module

    assert mod.flags == 0x02000059
    assert mod.name == "FMX"

    assert mod.custom_waveform.values == EXPECTED_CUSTOM_WAVEFORM

    assert mod.volume == 24762
    assert mod.panning == 69
    assert mod.sample_rate == mod.SampleRate._11025hz
    assert mod.polyphony == 15
    assert mod.channels == mod.Channels.stereo
    assert mod.input_to_operator == 0
    assert mod.input_to_custom_waveform == mod.InputCustomWaveform.continuous
    assert mod.adsr_smooth_transitions == mod.AdsrSmoothTransitions.off
    assert mod.noise_filter == 9897
    assert mod.op1_volume == 20098
    assert mod.op2_volume == 20987
    assert mod.op3_volume == 21450
    assert mod.op4_volume == 17213
    assert mod.op5_volume == 31592
    assert mod.op1_attack == 5679
    assert mod.op2_attack == 5951
    assert mod.op3_attack == 7917
    assert mod.op4_attack == 1259
    assert mod.op5_attack == 4740
    assert mod.op1_decay == 1799
    assert mod.op2_decay == 8041
    assert mod.op3_decay == 9284
    assert mod.op4_decay == 6614
    assert mod.op5_decay == 653
    assert mod.op1_sustain_level == 1506
    assert mod.op2_sustain_level == 2534
    assert mod.op3_sustain_level == 3252
    assert mod.op4_sustain_level == 23034
    assert mod.op5_sustain_level == 3503
    assert mod.op1_release == 6497
    assert mod.op2_release == 2429
    assert mod.op3_release == 3023
    assert mod.op4_release == 9900
    assert mod.op5_release == 6740
    assert mod.op1_attack_curve == mod.AdsrCurve.exp1
    assert mod.op2_attack_curve == mod.AdsrCurve.exp2
    assert mod.op3_attack_curve == mod.AdsrCurve.exp2
    assert mod.op4_attack_curve == mod.AdsrCurve.exp2
    assert mod.op5_attack_curve == mod.AdsrCurve.neg_exp2
    assert mod.op1_decay_curve == mod.AdsrCurve.linear
    assert mod.op2_decay_curve == mod.AdsrCurve.exp1
    assert mod.op3_decay_curve == mod.AdsrCurve.exp2
    assert mod.op4_decay_curve == mod.AdsrCurve.exp2
    assert mod.op5_decay_curve == mod.AdsrCurve.sin
    assert mod.op1_release_curve == mod.AdsrCurve.neg_exp2
    assert mod.op2_release_curve == mod.AdsrCurve.exp1
    assert mod.op3_release_curve == mod.AdsrCurve.exp2
    assert mod.op4_release_curve == mod.AdsrCurve.neg_exp2
    assert mod.op5_release_curve == mod.AdsrCurve.sin
    assert mod.op1_sustain == mod.Sustain.on
    assert mod.op2_sustain == mod.Sustain.on
    assert mod.op3_sustain == mod.Sustain.repeat
    assert mod.op4_sustain == mod.Sustain.on
    assert mod.op5_sustain == mod.Sustain.repeat
    assert mod.op1_sustain_pedal is False
    assert mod.op2_sustain_pedal is True
    assert mod.op3_sustain_pedal is True
    assert mod.op4_sustain_pedal is False
    assert mod.op5_sustain_pedal is True
    assert mod.op1_envelope_scaling_per_key == -77
    assert mod.op2_envelope_scaling_per_key == 125
    assert mod.op3_envelope_scaling_per_key == -60
    assert mod.op4_envelope_scaling_per_key == -57
    assert mod.op5_envelope_scaling_per_key == 43
    assert mod.op1_volume_scaling_per_key == -100
    assert mod.op2_volume_scaling_per_key == 41
    assert mod.op3_volume_scaling_per_key == 1
    assert mod.op4_volume_scaling_per_key == -32
    assert mod.op5_volume_scaling_per_key == -63
    assert mod.op1_velocity_sensitivity == 36
    assert mod.op2_velocity_sensitivity == -50
    assert mod.op3_velocity_sensitivity == -117
    assert mod.op4_velocity_sensitivity == 3
    assert mod.op5_velocity_sensitivity == 99
    assert mod.op1_waveform == mod.Waveform.hsin
    assert mod.op2_waveform == mod.Waveform.asin
    assert mod.op3_waveform == mod.Waveform.sin
    assert mod.op4_waveform == mod.Waveform.triangle_pow_3
    assert mod.op5_waveform == mod.Waveform.saw_pow_3
    assert mod.op1_noise == 18063
    assert mod.op2_noise == 12653
    assert mod.op3_noise == 20322
    assert mod.op4_noise == 12541
    assert mod.op5_noise == 3300
    assert mod.op1_phase == 4269
    assert mod.op2_phase == 16359
    assert mod.op3_phase == 21738
    assert mod.op4_phase == 13193
    assert mod.op5_phase == 25224
    assert mod.op1_freq_multiply == 22923
    assert mod.op2_freq_multiply == 31970
    assert mod.op3_freq_multiply == 7673
    assert mod.op4_freq_multiply == 26613
    assert mod.op5_freq_multiply == 2735
    assert mod.op1_constant_pitch == -694
    assert mod.op2_constant_pitch == 1841
    assert mod.op3_constant_pitch == -3511
    assert mod.op4_constant_pitch == 1062
    assert mod.op5_constant_pitch == 2358
    assert mod.op1_self_modulation == 11895
    assert mod.op2_self_modulation == 720
    assert mod.op3_self_modulation == 11736
    assert mod.op4_self_modulation == 16926
    assert mod.op5_self_modulation == 23405
    assert mod.op1_feedback == 24510
    assert mod.op2_feedback == 25778
    assert mod.op3_feedback == 9683
    assert mod.op4_feedback == 26614
    assert mod.op5_feedback == 17200
    assert mod.op1_modulation_type == mod.ModulationType.sub
    assert mod.op2_modulation_type == mod.ModulationType.frequency
    assert mod.op3_modulation_type == mod.ModulationType.amplitude_mul
    assert mod.op4_modulation_type == mod.ModulationType.min
    assert mod.op5_modulation_type == mod.ModulationType.sub
    assert mod.op1_output_mode == 0
    assert mod.op2_output_mode == 15
    assert mod.op3_output_mode == 1
    assert mod.op4_output_mode == 2


EXPECTED_CUSTOM_WAVEFORM = [
    0.23258860409259796,
    0.28716719150543213,
    0.33988499641418457,
    0.3905003070831299,
    0.43874162435531616,
    0.4843390882015228,
    0.5272365808486938,
    0.5672786235809326,
    0.6041287779808044,
    0.6377434730529785,
    0.6680856943130493,
    0.6950294971466064,
    0.718247652053833,
    0.7379667162895203,
    0.7541000843048096,
    0.7664385437965393,
    0.7750416398048401,
    0.7800208926200867,
    0.7814271450042725,
    0.7789393663406372,
    0.772946298122406,
    0.7635419964790344,
    0.8365955948829651,
    0.8237184882164001,
    0.8068667054176331,
    0.7860580086708069,
    0.7628260850906372,
    0.7345373034477234,
    0.7025718092918396,
    0.6699537038803101,
    0.6312897205352783,
    0.5893936157226562,
    0.544437050819397,
    0.5012393593788147,
    0.4510851502418518,
    0.3985336422920227,
    0.3437948226928711,
    0.2933891713619232,
    0.23541350662708282,
    0.17610563337802887,
    0.12288980931043625,
    0.06199882552027702,
    0.0006794976070523262,
    -0.060750387609004974,
    -0.114327073097229,
    -0.1749647706747055,
    -0.23475059866905212,
    -0.2859053313732147,
    -0.343142569065094,
    -0.39861631393432617,
    -0.45199453830718994,
    -0.4964962601661682,
    -0.5451078414916992,
    -0.5907776355743408,
    -0.6332420110702515,
    -0.6677308082580566,
    -0.7035722732543945,
    -0.7355403900146484,
    -0.761013388633728,
    -0.7853280305862427,
    -0.8052794337272644,
    -0.8207546472549438,
    -0.8323591947555542,
    -0.8393306732177734,
    -0.8415870070457458,
    -0.8425549268722534,
    -0.8361444473266602,
    -0.8250311613082886,
    -0.8092741966247559,
    -0.7958842515945435,
    -0.7718666791915894,
    -0.7435323596000671,
    -0.7110217809677124,
    -0.6845620274543762,
    -0.6449171304702759,
    -0.6017055511474609,
    -0.5671621561050415,
    -0.5180232524871826,
    -0.4661105275154114,
    -0.41174858808517456,
    -0.3687247335910797,
    -0.3105382025241852,
    -0.25084754824638367,
    -0.2039089798927307,
    -0.14217057824134827,
    -0.07994867116212845,
    -0.017657138407230377,
    0.03120145946741104,
    0.09301437437534332,
    0.15382125973701477,
    0.21325230598449707,
    0.2600589692592621,
    0.31650879979133606,
    0.37059485912323,
    0.41352012753486633,
    0.46296000480651855,
    0.509142279624939,
    0.5518043637275696,
    0.586479663848877,
    0.6226131916046143,
    0.6545447111129761,
    0.6815400123596191,
    0.7059248685836792,
    0.7256537079811096,
    0.7406331300735474,
    0.7554891109466553,
    0.7621375918388367,
    0.7638754844665527,
    0.7607458829879761,
    0.7625833749771118,
    0.7510920166969299,
    0.7349019646644592,
    0.7273757457733154,
    0.7032579779624939,
    0.6748769283294678,
    0.6424469947814941,
    0.6230509281158447,
    0.583917498588562,
    0.5414230823516846,
    0.5146118998527527,
    0.46669110655784607,
    0.4162820279598236,
    0.3637271225452423,
    0.32909584045410156,
    0.27325761318206787,
    0.21629741787910461,
    0.15865042805671692,
    0.1194186806678772,
    0.06085902452468872,
    0.0026753395795822144,
    -0.037727177143096924,
    -0.09500941634178162,
    -0.1508598029613495,
    -0.20491887629032135,
    -0.24377082288265228,
    -0.29458335041999817,
    -0.34262585639953613,
    -0.3875787854194641,
    -0.42161351442337036,
    -0.46132758259773254,
    -0.4972194731235504,
    -0.5259842276573181,
    -0.5554612874984741,
    -0.5805566906929016,
    -0.6011256575584412,
    -0.620720624923706,
    -0.6338445544242859,
    -0.6421701908111572,
    -0.6542209386825562,
    -0.6547582745552063,
    -0.6504875421524048,
    -0.6414929628372192,
    -0.6426220536231995,
    -0.6260185837745667,
    -0.604975163936615,
    -0.5797035694122314,
    -0.5702730417251587,
    -0.5382753610610962,
    -0.5026274919509888,
    -0.4862741231918335,
    -0.444942831993103,
    -0.40072768926620483,
    -0.35400837659835815,
    -0.3297971785068512,
    -0.27923211455345154,
    -0.22711940109729767,
    -0.1988571137189865,
    -0.14455834031105042,
    -0.08971892297267914,
    -0.034773483872413635,
    -0.0032774358987808228,
    0.05166421830654144,
    0.10567985475063324,
    0.15833929181098938,
    0.1900215893983841,
    0.2404107302427292,
    0.28846144676208496,
    0.318450927734375,
    0.36270684003829956,
    0.4037582278251648,
    0.4413085877895355,
    0.46650227904319763,
    0.4984695017337799,
    0.5262860655784607,
    0.5466063022613525,
    0.5678738355636597,
    0.5844971537590027,
    0.5963878035545349,
    0.6084100008010864,
    0.6129369735717773,
    0.6125881671905518,
    0.6073499917984009,
    0.6100589632987976,
    0.5973415374755859,
    0.5798882246017456,
    0.5757607221603394,
    0.5511680245399475,
    0.5222228169441223,
    0.48917868733406067,
    0.47606852650642395,
    0.4368879497051239,
    0.39428162574768066,
    0.37547004222869873,
    0.3278135061264038,
    0.277525931596756,
    0.22500203549861908,
    0.19999893009662628,
    0.14435580372810364,
    0.08744654059410095,
    0.029727116227149963,
    0.0009678304195404053,
    -0.057664625346660614,
    -0.11603009700775146,
    -0.14588646590709686,
    -0.20350223779678345,
    -0.2598009705543518,
    -0.31434154510498047,
    -0.3431132435798645,
    -0.39464202523231506,
    -0.44345176219940186,
    -0.4697651267051697,
    -0.5140451192855835,
    -0.5547241568565369,
    -0.5914567708969116,
    -0.6121114492416382,
    -0.642626941204071,
    -0.6685411930084229,
    -0.6896885633468628,
    -0.7026157975196838,
    -0.7163175344467163,
    -0.7248663902282715,
    -0.7313686013221741,
    -0.7319871783256531,
    -0.7272921800613403,
    -0.7172779440879822,
    -0.7141537070274353,
    -0.6961480379104614,
    -0.6729942560195923,
    -0.6629302501678467,
    -0.6321297287940979,
    -0.5965664386749268,
    -0.5564976334571838,
    -0.5373690128326416,
    -0.49072349071502686,
    -0.4402046799659729,
    -0.3861745595932007,
    -0.359448105096817,
    -0.3004870116710663,
    -0.23893007636070251,
    -0.20792485773563385,
    -0.1428895741701126,
    -0.07629040628671646,
    -0.008521927520632744,
    0.02612357586622238,
    0.0950724333524704,
    0.16405576467514038,
]
