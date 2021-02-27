//
// SunVox Library (modular synthesizer)
// Copyright (c) 2008 - 2020, Alexander Zolotov <nightradio@gmail.com>, WarmPlace.ru
//

const { SunVoxLib } = window as any

//
// Library init
//

export var sv_scope_buf_mptr = null
export const sv_scope_buf_numsamples = 4096
export var sv_callback_buf_mptr = null //output
export var sv_callback_buf2_mptr = null //input
export var sv_callback_buf_numframes = 0
export var sv_curve_buf_mptr = null
export var sv_curve_buf_len = 1024
export var sv_flags = 0
export var sv_channels = 0
export const svlib = SunVoxLib()

//
// Constants
//

export const NOTECMD_NOTE_OFF = 128
export const NOTECMD_ALL_NOTES_OFF = 129 /* notes of all synths off */
export const NOTECMD_CLEAN_SYNTHS = 130 /* stop and clean all synths */
export const NOTECMD_STOP = 131
export const NOTECMD_PLAY = 132

export const SV_INIT_FLAG_NO_DEBUG_OUTPUT = 1 << 0
export const SV_INIT_FLAG_USER_AUDIO_CALLBACK =
  1 << 1 /* Interaction with sound card is on the user side */
export const SV_INIT_FLAG_OFFLINE =
  1 << 1 /* Same as SV_INIT_FLAG_USER_AUDIO_CALLBACK */
export const SV_INIT_FLAG_AUDIO_INT16 = 1 << 2
export const SV_INIT_FLAG_AUDIO_FLOAT32 = 1 << 3
export const SV_INIT_FLAG_ONE_THREAD =
  1 << 4 /* Audio callback and song modification functions are in single thread */

export const SV_MODULE_FLAG_EXISTS = 1 << 0
export const SV_MODULE_FLAG_EFFECT = 1 << 1
export const SV_MODULE_FLAG_MUTE = 1 << 2
export const SV_MODULE_FLAG_SOLO = 1 << 3
export const SV_MODULE_FLAG_BYPASS = 1 << 4
export const SV_MODULE_INPUTS_OFF = 16
export const SV_MODULE_INPUTS_MASK = 255 << SV_MODULE_INPUTS_OFF
export const SV_MODULE_OUTPUTS_OFF = 16 + 8
export const SV_MODULE_OUTPUTS_MASK = 255 << SV_MODULE_OUTPUTS_OFF

//
// Functions
//

//Read more information in headers/sunvox.h
//Use the functions with the label "USE LOCK/UNLOCK" within the sv_lock_slot() / sv_unlock_slot() block only!

export function sv_init(config: any, freq: any, channels: any, flags: any) {
  var config_mptr = 0
  if (config !== 0 && config !== null)
    config_mptr = svlib.allocate(
      svlib.intArrayFromString(config),
      "i8",
      svlib.ALLOC_NORMAL
    )
  sv_flags = flags
  sv_channels = channels
  var rv = svlib._sv_init(config_mptr, freq, channels, flags)
  svlib._free(config_mptr)
  return rv
}
export function sv_deinit() {
  return svlib._sv_deinit()
}
export function sv_get_sample_rate() {
  return svlib._sv_get_sample_rate()
}
export function sv_update_input() {
  return svlib._sv_update_input()
}
export function sv_audio_callback(
  out_buf: any,
  frames: any,
  latency: any,
  out_time: any
) {
  //get the next piece of SunVox audio from the Output module to the out_buf (Int16Array or Float32Array);
  //stereo data will be interleaved in the output buffer: LRLR... ; where the LR is the one frame (Left+Right channels)
  return sv_audio_callback2(out_buf, frames, latency, out_time, 0, 0, null)
}
export function sv_audio_callback2(
  out_buf: any,
  frames: any,
  latency: any,
  out_time: any,
  in_type: any,
  in_channels: any,
  in_buf: any
) {
  //get the next piece of SunVox audio from the Output module to the out_buf (Int16Array or Float32Array);
  //data from the in_buf (Int16Array or Float32Array) will be copied to the Input buffer;
  //in_type - input buffer type: 0 - Int16Array; 1 - Float32Array;
  //in_channels - number of input channels.
  var frame_size = sv_channels * 2 //output
  var frame_size2 = in_channels * 2 //input
  if (sv_flags & SV_INIT_FLAG_AUDIO_FLOAT32) frame_size *= 2
  if (in_type === 1) frame_size2 *= 2
  if (frames > sv_callback_buf_numframes) {
    svlib._free(sv_callback_buf_mptr)
    svlib._free(sv_callback_buf2_mptr)
    sv_callback_buf_mptr = null
    sv_callback_buf2_mptr = null
  }
  if (sv_callback_buf_mptr === null) {
    sv_callback_buf_numframes = frames
    sv_callback_buf_mptr = svlib._malloc(frames * frame_size) //output
  }
  if (sv_callback_buf2_mptr === null) {
    if (frame_size2 !== 0) sv_callback_buf2_mptr = svlib._malloc(frames * frame_size2) //input
  }
  var rv, buf
  if (in_buf === null) {
    rv = svlib._sv_audio_callback(sv_callback_buf_mptr, frames, latency, out_time)
  } else {
    if (in_type === 1)
      buf = svlib.HEAPF32.subarray(
        sv_callback_buf2_mptr! >> 2,
        (sv_callback_buf2_mptr! >> 2) + frames * in_channels
      )
    else
      buf = svlib.HEAP16.subarray(
        sv_callback_buf2_mptr! >> 1,
        (sv_callback_buf2_mptr! >> 1) + frames * in_channels
      )
    buf.set(in_buf, 0) //in_buf -> buf
    rv = svlib._sv_audio_callback2(
      sv_callback_buf_mptr,
      frames,
      latency,
      out_time,
      in_type,
      in_channels,
      sv_callback_buf2_mptr
    )
  }
  if (sv_flags & SV_INIT_FLAG_AUDIO_FLOAT32)
    buf = svlib.HEAPF32.subarray(
      sv_callback_buf_mptr! >> 2,
      (sv_callback_buf_mptr! >> 2) + frames * sv_channels
    )
  else
    buf = svlib.HEAP16.subarray(
      sv_callback_buf_mptr! >> 1,
      (sv_callback_buf_mptr! >> 1) + frames * sv_channels
    )
  out_buf.set(buf, 0) //buf -> out_buf
  return rv
}
export function sv_open_slot(slot: any) {
  return svlib._sv_open_slot(slot)
}
export function sv_close_slot(slot: any) {
  return svlib._sv_close_slot(slot)
}
export function sv_lock_slot(slot: any) {
  return svlib._sv_lock_slot(slot)
}
export function sv_unlock_slot(slot: any) {
  return svlib._sv_unlock_slot(slot)
}
export function sv_load_from_memory(slot: any, byte_array: Uint8Array) {
  //load from Uint8Array
  var mptr = svlib.allocate(byte_array, "i8", svlib.ALLOC_NORMAL)
  if (mptr === 0) return -1
  var rv = svlib._sv_load_from_memory(slot, mptr, byte_array.byteLength)
  svlib._free(mptr)
  return rv
}
export function sv_play(slot: any) {
  return svlib._sv_play(slot)
}
export function sv_play_from_beginning(slot: any) {
  return svlib._sv_play_from_beginning(slot)
}
export function sv_stop(slot: any) {
  return svlib._sv_stop(slot)
}
export function sv_set_autostop(slot: any, autostop: any) {
  return svlib._sv_set_autostop(slot, autostop)
}
export function sv_get_autostop(slot: any) {
  return svlib._sv_get_autostop(slot)
}
export function sv_end_of_song(slot: any) {
  return svlib._sv_end_of_song(slot)
}
export function sv_rewind(slot: any, line_num: any) {
  return svlib._sv_rewind(slot, line_num)
}
export function sv_volume(slot: any, vol: any) {
  return svlib._sv_volume(slot, vol)
}
export function sv_set_event_t(slot: any, set: any, t: any) {
  return svlib._sv_set_event_t(slot, set, t)
}
export function sv_send_event(
  slot: any,
  track: any,
  note: any,
  vel: any,
  module: any,
  ctl: any,
  ctl_val: any
) {
  return svlib._sv_send_event(slot, track, note, vel, module, ctl, ctl_val)
}
export function sv_get_current_line(slot: any) {
  return svlib._sv_get_current_line(slot)
}
export function sv_get_current_line2(slot: any) {
  return svlib._sv_get_current_line2(slot)
}
export function sv_get_current_signal_level(slot: any, channel: any) {
  return svlib._sv_get_current_signal_level(slot, channel)
}
export function sv_get_song_name(slot: any) {
  return svlib.UTF8ToString(svlib._sv_get_song_name(slot))
}
export function sv_get_song_bpm(slot: any) {
  return svlib._sv_get_song_bpm(slot)
}
export function sv_get_song_tpl(slot: any) {
  return svlib._sv_get_song_tpl(slot)
}
export function sv_get_song_length_frames(slot: any) {
  return svlib._sv_get_song_length_frames(slot)
}
export function sv_get_song_length_lines(slot: any) {
  return svlib._sv_get_song_length_lines(slot)
}
export function sv_get_time_map(
  slot: any,
  start_line: any,
  len: any,
  dest_buf_uint32: any,
  flags: any
) {
  //save to dest_buf_uint32 (Uint32Array)
  var rv = -1
  var map_mptr = svlib._malloc(len * 4)
  if (map_mptr !== 0) {
    rv = svlib._sv_get_time_map(slot, start_line, len, map_mptr, flags)
    if (rv === 0) {
      var s = svlib.HEAPU32.subarray(map_mptr >> 2, (map_mptr >> 2) + len)
      dest_buf_uint32.set(s, 0) //copy data from s to dest_buf
    }
    svlib._free(map_mptr)
  }
  return rv
}
export function sv_new_module(slot: any, type: any, name: any, x: any, y: any, z: any) {
  //USE LOCK/UNLOCK!
  var type_mptr = svlib.allocate(
    svlib.intArrayFromString(type),
    "i8",
    svlib.ALLOC_NORMAL
  )
  if (type_mptr === 0) return -1
  var name_mptr = svlib.allocate(
    svlib.intArrayFromString(name),
    "i8",
    svlib.ALLOC_NORMAL
  )
  if (name_mptr === 0) return -1
  var rv = svlib._sv_new_module(slot, type_mptr, name_mptr, x, y, z)
  svlib._free(type_mptr)
  svlib._free(name_mptr)
  return rv
}
export function sv_remove_module(slot: any, mod_num: any) {
  return svlib._sv_remove_module(slot, mod_num)
} //USE LOCK/UNLOCK!
export function sv_connect_module(slot: any, source: any, destination: any) {
  return svlib._sv_connect_module(slot, source, destination)
} //USE LOCK/UNLOCK!
export function sv_disconnect_module(slot: any, source: any, destination: any) {
  return svlib._sv_disconnect_module(slot, source, destination)
} //USE LOCK/UNLOCK!
export function sv_load_module_from_memory(
  slot: any,
  byte_array: any,
  x: any,
  y: any,
  z: any
) {
  //load from Uint8Array
  var mptr = svlib.allocate(byte_array, "i8", svlib.ALLOC_NORMAL)
  if (mptr === 0) return -1
  var rv = svlib._sv_load_module_from_memory(slot, mptr, byte_array.byteLength, x, y, z)
  svlib._free(mptr)
  return rv
}
export function sv_sampler_load_from_memory(
  slot: any,
  sampler_module: any,
  byte_array: any,
  sample_slot: any
) {
  //load from Uint8Array
  var mptr = svlib.allocate(byte_array, "i8", svlib.ALLOC_NORMAL)
  if (mptr === 0) return -1
  var rv = svlib._sv_sampler_load_from_memory(
    slot,
    sampler_module,
    mptr,
    byte_array.byteLength,
    sample_slot
  )
  svlib._free(mptr)
  return rv
}
export function sv_get_number_of_modules(slot: any) {
  return svlib._sv_get_number_of_modules(slot)
}
export function sv_find_module(slot: any, name: any) {
  var name_mptr = svlib.allocate(
    svlib.intArrayFromString(name),
    "i8",
    svlib.ALLOC_NORMAL
  )
  if (name_mptr === 0) return -1
  var rv = svlib._sv_find_module(slot, name_mptr)
  svlib._free(name_mptr)
  return rv
}
export function sv_get_module_flags(slot: any, mod_num: any) {
  return svlib._sv_get_module_flags(slot, mod_num)
}
export function sv_get_module_inputs(slot: any, mod_num: any) {
  //return value: Int32Array
  var rv = null
  var flags = sv_get_module_flags(slot, mod_num)
  var num = (flags & SV_MODULE_INPUTS_MASK) >> SV_MODULE_INPUTS_OFF
  var mptr = svlib._sv_get_module_inputs(slot, mod_num)
  if (mptr !== 0) rv = svlib.HEAP32.subarray(mptr >> 2, (mptr >> 2) + num)
  return rv
}
export function sv_get_module_outputs(slot: any, mod_num: any) {
  //return value: Int32Array
  var rv = null
  var flags = sv_get_module_flags(slot, mod_num)
  var num = (flags & SV_MODULE_OUTPUTS_MASK) >> SV_MODULE_OUTPUTS_OFF
  var mptr = svlib._sv_get_module_outputs(slot, mod_num)
  if (mptr !== 0) rv = svlib.HEAP32.subarray(mptr >> 2, (mptr >> 2) + num) //not a new array; just a new view of the HEAP
  return rv
}
export function sv_get_module_name(slot: any, mod_num: any) {
  return svlib.UTF8ToString(svlib._sv_get_module_name(slot, mod_num))
}
export function sv_get_module_xy(slot: any, mod_num: any) {
  return svlib._sv_get_module_xy(slot, mod_num)
}
export function sv_get_module_color(slot: any, mod_num: any) {
  return svlib._sv_get_module_color(slot, mod_num)
}
export function sv_get_module_finetune(slot: any, mod_num: any) {
  return svlib._sv_get_module_finetune(slot, mod_num)
}
export function sv_get_module_scope2(
  slot: any,
  mod_num: any,
  channel: any,
  dest_buf_int16: any,
  samples_to_read: any
) {
  //save to dest_buf_int16 (Int16Array)
  if (sv_scope_buf_mptr === null) {
    sv_scope_buf_mptr = svlib._malloc(sv_scope_buf_numsamples * 2)
  }
  if (samples_to_read > sv_scope_buf_numsamples)
    samples_to_read = sv_scope_buf_numsamples
  var rv = svlib._sv_get_module_scope2(
    slot,
    mod_num,
    channel,
    sv_scope_buf_mptr,
    samples_to_read
  )
  if (rv > 0) {
    var s = svlib.HEAP16.subarray(
      sv_scope_buf_mptr! >> 1,
      (sv_scope_buf_mptr! >> 1) + rv
    )
    dest_buf_int16.set(s, 0) //copy data from s to dest_buf
  }
  return rv
}
export function sv_module_curve(
  slot: any,
  mod_num: any,
  curve_num: any,
  buf_float32: any,
  len: any,
  w: any
) {
  //read (w === 0) or write (w === 1) from/to buf_float32 (Float32Array)
  if (sv_curve_buf_mptr === null) {
    sv_curve_buf_mptr = svlib._malloc(sv_curve_buf_len * 4)
  }
  if (len > sv_curve_buf_len) len = sv_curve_buf_len
  if (w === 1) {
    //Write:
    var len2 = len
    if (len2 <= 0) len2 = buf_float32.length
    var d = svlib.HEAPF32.subarray(
      sv_curve_buf_mptr! >> 2,
      (sv_curve_buf_mptr! >> 2) + len2
    )
    d.set(buf_float32, 0)
  }
  var rv = svlib._sv_module_curve(slot, mod_num, curve_num, sv_curve_buf_mptr, len, w)
  if (w === 0 && rv > 0) {
    //Read:
    var s = svlib.HEAPF32.subarray(
      sv_curve_buf_mptr! >> 2,
      (sv_curve_buf_mptr! >> 2) + rv
    )
    buf_float32.set(s, 0) //copy data from s to buf_float32
  }
  return rv
}
export function sv_get_number_of_module_ctls(slot: any, mod_num: any) {
  return svlib._sv_get_number_of_module_ctls(slot, mod_num)
}
export function sv_get_module_ctl_name(slot: any, mod_num: any, ctl_num: any) {
  return svlib.UTF8ToString(svlib._sv_get_module_ctl_name(slot, mod_num, ctl_num))
}
export function sv_get_module_ctl_value(
  slot: any,
  mod_num: any,
  ctl_num: any,
  scaled: any
) {
  return svlib._sv_get_module_ctl_value(slot, mod_num, ctl_num, scaled)
}
export function sv_get_number_of_patterns(slot: any) {
  return svlib._sv_get_number_of_patterns(slot)
}
export function sv_find_pattern(slot: any, name: any) {
  var name_mptr = svlib.allocate(
    svlib.intArrayFromString(name),
    "i8",
    svlib.ALLOC_NORMAL
  )
  if (name_mptr === 0) return -1
  var rv = svlib._sv_find_pattern(slot, name_mptr)
  svlib._free(name_mptr)
  return rv
}
export function sv_get_pattern_x(slot: any, pat_num: any) {
  return svlib._sv_get_pattern_x(slot, pat_num)
}
export function sv_get_pattern_y(slot: any, pat_num: any) {
  return svlib._sv_get_pattern_y(slot, pat_num)
}
export function sv_get_pattern_tracks(slot: any, pat_num: any) {
  return svlib._sv_get_pattern_tracks(slot, pat_num)
}
export function sv_get_pattern_lines(slot: any, pat_num: any) {
  return svlib._sv_get_pattern_lines(slot, pat_num)
}
export function sv_get_pattern_name(slot: any, pat_num: any) {
  return svlib.UTF8ToString(svlib._sv_get_pattern_name(slot, pat_num))
}
export function sv_get_pattern_data(slot: any, pat_num: any) {
  //return value: UInt8Array; 8 bytes per event in format: NN VV MM 00 CC YY XX
  var rv = null
  var numtracks = svlib._sv_get_pattern_tracks(slot, pat_num)
  var numlines = svlib._sv_get_pattern_lines(slot, pat_num)
  if (numtracks !== 0 && numlines !== 0) {
    var mptr = svlib._sv_get_pattern_data(slot, pat_num)
    if (mptr !== 0) {
      rv = svlib.HEAPU8.subarray(mptr, mptr + numtracks * numlines * 8)
    }
  }
  return rv
}
export function sv_pattern_mute(slot: any, pat_num: any, mute: any) {
  return svlib._sv_pattern_mute(slot, pat_num, mute)
} //USE LOCK/UNLOCK!
export function sv_get_ticks() {
  return svlib._sv_get_ticks()
}
export function sv_get_ticks_per_second() {
  return svlib._sv_get_ticks_per_second()
}
export function sv_get_log(size: any) {
  return svlib.UTF8ToString(svlib._sv_get_log(size))
}
