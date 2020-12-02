from enum import IntEnum

from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.drumsynth import BaseDrumSynth


class DrumSynth(BaseDrumSynth, Module):

    behaviors = {B.receives_notes, B.sends_audio}


class DRUMNOTE(IntEnum):

    (
        BD01,
        BD02,
        BD03,
        BD04,
        HH01,
        HH02,
        HH03,
        SD01,
        SD02,
        SD03,
        SD04,
        SD05,
        BD11,
        BD12,
        BD13,
        BD14,
        HH11,
        HH12,
        HH13,
        SD11,
        SD12,
        SD13,
        SD14,
        SD15,
        BD21,
        BD22,
        BD23,
        BD24,
        HH21,
        HH22,
        HH23,
        SD21,
        SD22,
        SD23,
        SD24,
        SD25,
        BD31,
        BD32,
        BD33,
        BD34,
        HH31,
        HH32,
        HH33,
        SD31,
        SD32,
        SD33,
        SD34,
        SD35,
        BD41,
        BD42,
        BD43,
        BD44,
        HH41,
        HH42,
        HH43,
        SD41,
        SD42,
        SD43,
        SD44,
        SD45,
        BD51,
        BD52,
        BD53,
        BD54,
        HH51,
        HH52,
        HH53,
        SD51,
        SD52,
        SD53,
        SD54,
        SD55,
        BD61,
        BD62,
        BD63,
        BD64,
        HH61,
        HH62,
        HH63,
        SD61,
        SD62,
        SD63,
        SD64,
        SD65,
        BD71,
        BD72,
        BD73,
        BD74,
        HH71,
        HH72,
        HH73,
        SD71,
        SD72,
        SD73,
        SD74,
        SD75,
        BD81,
        BD82,
        BD83,
        BD84,
        HH81,
        HH82,
        HH83,
        SD81,
        SD82,
        SD83,
        SD84,
        SD85,
        BD91,
        BD92,
        BD93,
        BD94,
        HH91,
        HH92,
        HH93,
        SD91,
        SD92,
        SD93,
        SD94,
        SD95,
    ) = range(1, 121)


class BDNOTE(IntEnum):

    BD01, BD02, BD03, BD04 = DRUMNOTE.BD01, DRUMNOTE.BD02, DRUMNOTE.BD03, DRUMNOTE.BD04
    BD11, BD12, BD13, BD14 = DRUMNOTE.BD11, DRUMNOTE.BD12, DRUMNOTE.BD13, DRUMNOTE.BD14
    BD21, BD22, BD23, BD24 = DRUMNOTE.BD21, DRUMNOTE.BD22, DRUMNOTE.BD23, DRUMNOTE.BD24
    BD31, BD32, BD33, BD34 = DRUMNOTE.BD31, DRUMNOTE.BD32, DRUMNOTE.BD33, DRUMNOTE.BD34
    BD41, BD42, BD43, BD44 = DRUMNOTE.BD41, DRUMNOTE.BD42, DRUMNOTE.BD43, DRUMNOTE.BD44
    BD51, BD52, BD53, BD54 = DRUMNOTE.BD51, DRUMNOTE.BD52, DRUMNOTE.BD53, DRUMNOTE.BD54
    BD61, BD62, BD63, BD64 = DRUMNOTE.BD61, DRUMNOTE.BD62, DRUMNOTE.BD63, DRUMNOTE.BD64
    BD71, BD72, BD73, BD74 = DRUMNOTE.BD71, DRUMNOTE.BD72, DRUMNOTE.BD73, DRUMNOTE.BD74
    BD81, BD82, BD83, BD84 = DRUMNOTE.BD81, DRUMNOTE.BD82, DRUMNOTE.BD83, DRUMNOTE.BD84
    BD91, BD92, BD93, BD94 = DRUMNOTE.BD91, DRUMNOTE.BD92, DRUMNOTE.BD93, DRUMNOTE.BD94


class HHNOTE(IntEnum):

    HH01, HH02, HH03 = DRUMNOTE.HH01, DRUMNOTE.HH02, DRUMNOTE.HH03
    HH11, HH12, HH13 = DRUMNOTE.HH11, DRUMNOTE.HH12, DRUMNOTE.HH13
    HH21, HH22, HH23 = DRUMNOTE.HH21, DRUMNOTE.HH22, DRUMNOTE.HH23
    HH31, HH32, HH33 = DRUMNOTE.HH31, DRUMNOTE.HH32, DRUMNOTE.HH33
    HH41, HH42, HH43 = DRUMNOTE.HH41, DRUMNOTE.HH42, DRUMNOTE.HH43
    HH51, HH52, HH53 = DRUMNOTE.HH51, DRUMNOTE.HH52, DRUMNOTE.HH53
    HH61, HH62, HH63 = DRUMNOTE.HH61, DRUMNOTE.HH62, DRUMNOTE.HH63
    HH71, HH72, HH73 = DRUMNOTE.HH71, DRUMNOTE.HH72, DRUMNOTE.HH73
    HH81, HH82, HH83 = DRUMNOTE.HH81, DRUMNOTE.HH82, DRUMNOTE.HH83
    HH91, HH92, HH93 = DRUMNOTE.HH91, DRUMNOTE.HH92, DRUMNOTE.HH93


class SDNOTE(IntEnum):

    SD01, SD02, SD03, SD04, SD05 = (
        DRUMNOTE.SD01,
        DRUMNOTE.SD02,
        DRUMNOTE.SD03,
        DRUMNOTE.SD04,
        DRUMNOTE.SD05,
    )
    SD11, SD12, SD13, SD14, SD15 = (
        DRUMNOTE.SD11,
        DRUMNOTE.SD12,
        DRUMNOTE.SD13,
        DRUMNOTE.SD14,
        DRUMNOTE.SD15,
    )
    SD21, SD22, SD23, SD24, SD25 = (
        DRUMNOTE.SD21,
        DRUMNOTE.SD22,
        DRUMNOTE.SD23,
        DRUMNOTE.SD24,
        DRUMNOTE.SD25,
    )
    SD31, SD32, SD33, SD34, SD35 = (
        DRUMNOTE.SD31,
        DRUMNOTE.SD32,
        DRUMNOTE.SD33,
        DRUMNOTE.SD34,
        DRUMNOTE.SD35,
    )
    SD41, SD42, SD43, SD44, SD45 = (
        DRUMNOTE.SD41,
        DRUMNOTE.SD42,
        DRUMNOTE.SD43,
        DRUMNOTE.SD44,
        DRUMNOTE.SD45,
    )
    SD51, SD52, SD53, SD54, SD55 = (
        DRUMNOTE.SD51,
        DRUMNOTE.SD52,
        DRUMNOTE.SD53,
        DRUMNOTE.SD54,
        DRUMNOTE.SD55,
    )
    SD61, SD62, SD63, SD64, SD65 = (
        DRUMNOTE.SD61,
        DRUMNOTE.SD62,
        DRUMNOTE.SD63,
        DRUMNOTE.SD64,
        DRUMNOTE.SD65,
    )
    SD71, SD72, SD73, SD74, SD75 = (
        DRUMNOTE.SD71,
        DRUMNOTE.SD72,
        DRUMNOTE.SD73,
        DRUMNOTE.SD74,
        DRUMNOTE.SD75,
    )
    SD81, SD82, SD83, SD84, SD85 = (
        DRUMNOTE.SD81,
        DRUMNOTE.SD82,
        DRUMNOTE.SD83,
        DRUMNOTE.SD84,
        DRUMNOTE.SD85,
    )
    SD91, SD92, SD93, SD94, SD95 = (
        DRUMNOTE.SD91,
        DRUMNOTE.SD92,
        DRUMNOTE.SD93,
        DRUMNOTE.SD94,
        DRUMNOTE.SD95,
    )


DrumSynth.DRUMNOTE = DRUMNOTE
DrumSynth.BDNOTE = BDNOTE
DrumSynth.HHNOTE = HHNOTE
DrumSynth.SDNOTE = SDNOTE
