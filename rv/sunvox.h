/*

    You can use SunVox library freely, but the following text should be included in your products (e.g. in About window).

    SunVox modular synthesizer
    Copyright (c) 2008 - 2015, Alexander Zolotov <nightradio@gmail.com>, WarmPlace.ru

    Ogg Vorbis 'Tremor' integer playback codec
    Copyright (c) 2002, Xiph.org Foundation

*/

#ifndef __SUNVOX_H__
#define __SUNVOX_H__

#include <stdio.h>

#define NOTECMD_NOTE_OFF	128
#define NOTECMD_ALL_NOTES_OFF	129 /* notes of all synths off */
#define NOTECMD_CLEAN_SYNTHS	130 /* stop and clean all synths */
#define NOTECMD_STOP		131
#define NOTECMD_PLAY		132

//sv_send_event() parameters:
//  slot;
//  track_num: from 0 to 15;
//  note: 0 - nothing; 1..127 - note num; 128 - note off; 129, 130... - see NOTECMD_xxx defines;
//  vel: velocity 1..129; 0 - default;
//  module: 0 - nothing; 1..255 - module number;
//  ctl: CCXX. CC - number of controller. XX - std effect;
//  ctl_val: value of controller.

typedef struct
{
    unsigned char	note;           //0 - nothing; 1..127 - note num; 128 - note off; 129, 130... - see NOTECMD_xxx defines
    unsigned char       vel;            //Velocity 1..129; 0 - default
    unsigned char       module;         //0 - nothing; 1..255 - module number (real module number + 1)
    unsigned char       nothing;
    unsigned short      ctl;            //CCEE. CC - number of a controller (1..255). EE - std effect
    unsigned short      ctl_val;        //XXYY. Value of controller/effect
} sunvox_note;

#define SV_INIT_FLAG_NO_DEBUG_OUTPUT 		( 1 << 0 )
#define SV_INIT_FLAG_USER_AUDIO_CALLBACK 	( 1 << 1 ) /* Interaction with sound card is on the user side */
#define SV_INIT_FLAG_AUDIO_INT16 		( 1 << 2 )
#define SV_INIT_FLAG_AUDIO_FLOAT32 		( 1 << 3 )
#define SV_INIT_FLAG_ONE_THREAD			( 1 << 4 ) /* Audio callback and song modification functions are in single thread */

#define SV_MODULE_FLAG_EXISTS 1
#define SV_MODULE_FLAG_EFFECT 2
#define SV_MODULE_INPUTS_OFF 16
#define SV_MODULE_INPUTS_MASK ( 255 << SV_MODULE_INPUTS_OFF )
#define SV_MODULE_OUTPUTS_OFF ( 16 + 8 )
#define SV_MODULE_OUTPUTS_MASK ( 255 << SV_MODULE_OUTPUTS_OFF )

#define SV_STYPE_INT16 0
#define SV_STYPE_INT32 1
#define SV_STYPE_FLOAT32 2
#define SV_STYPE_FLOAT64 3

#if defined(_WIN32) || defined(_WIN32_WCE) || defined(__WIN32__)
    #define WIN
    #define LIBNAME "sunvox.dll"
#endif
#if defined(__APPLE__)
    #define OSX
    #define LIBNAME "sunvox.dylib"
#endif
#if defined(__linux__) || defined(linux)
    #define LINUX
    #define LIBNAME "./sunvox.so"
#endif
#if defined(OSX) || defined(LINUX)
    #define UNIX
#endif

#ifdef WIN
    #ifdef __GNUC__
	#define SUNVOX_FN_ATTR __attribute__((stdcall))
    #else
	#define SUNVOX_FN_ATTR __stdcall
    #endif
#endif
#ifndef SUNVOX_FN_ATTR
    #define SUNVOX_FN_ATTR /**/
#endif

#ifdef SUNVOX_STATIC_LIB

#ifdef __cplusplus
extern "C" {
#endif

//USE LOCK/UNLOCK! - Use the functions with this label within the sv_lock_slot() / sv_unlock_slot() block only!

//sv_audio_callback() - get the next piece of SunVox audio.
//With sv_audio_callback() you can ignore the built-in SunVox sound output mechanism and use some other sound system.
//Set SV_INIT_FLAG_USER_AUDIO_CALLBACK flag in sv_init() if you want to use sv_audio_callback() function.
//Parameters:
//  buf - destination buffer of type signed short (if SV_INIT_FLAG_AUDIO_INT16 used in sv_init())
//        or float (if SV_INIT_FLAG_AUDIO_FLOAT32 used in sv_init());
//  	  stereo data will be interleaved in this buffer: LRLR... ; where the LR is the one frame (Left+Right channels);
//  frames - number of frames in destination buffer;
//  latency - audio latency (in frames);
//  out_time - output time (in ticks).
int sv_audio_callback( void* buf, int frames, int latency, unsigned int out_time ) SUNVOX_FN_ATTR;
int sv_open_slot( int slot ) SUNVOX_FN_ATTR;
int sv_close_slot( int slot ) SUNVOX_FN_ATTR;
int sv_lock_slot( int slot ) SUNVOX_FN_ATTR;
int sv_unlock_slot( int slot ) SUNVOX_FN_ATTR;
int sv_init( const char* dev, int freq, int channels, int flags ) SUNVOX_FN_ATTR;
int sv_deinit( void ) SUNVOX_FN_ATTR;
//sv_get_sample_type() - get internal sample type of the SunVox engine. Return value: one of the SV_STYPE_xxx defines.
//Use it to get the scope buffer type from get_module_scope() function.
int sv_get_sample_type( void ) SUNVOX_FN_ATTR;
int sv_load( int slot, const char* name ) SUNVOX_FN_ATTR;
int sv_load_from_memory( int slot, void* data, unsigned int data_size ) SUNVOX_FN_ATTR;
int sv_play( int slot ) SUNVOX_FN_ATTR;
int sv_play_from_beginning( int slot ) SUNVOX_FN_ATTR;
int sv_stop( int slot ) SUNVOX_FN_ATTR;
//autostop values: 0 - disable autostop; 1 - enable autostop.
//When disabled, song is playing infinitely in the loop.
int sv_set_autostop( int slot, int autostop ) SUNVOX_FN_ATTR;
//sv_end_of_song() return values: 0 - song is playing now; 1 - stopped.
int sv_end_of_song( int slot ) SUNVOX_FN_ATTR;
int sv_rewind( int slot, int line_num ) SUNVOX_FN_ATTR;
int sv_volume( int slot, int vol ) SUNVOX_FN_ATTR;
//ctl - 0xCCEE. CC - number of a controller (1..255). EE - std effect
//ctl_val - value of controller/effect
int sv_send_event( int slot, int track_num, int note, int vel, int module, int ctl, int ctl_val ) SUNVOX_FN_ATTR;
int sv_get_current_line( int slot ) SUNVOX_FN_ATTR; //Get current line number
int sv_get_current_line2( int slot ) SUNVOX_FN_ATTR; //Get current line number in fixed point format 27.5
int sv_get_current_signal_level( int slot, int channel ) SUNVOX_FN_ATTR; //From 0 to 255
const char* sv_get_song_name( int slot ) SUNVOX_FN_ATTR;
int sv_get_song_bpm( int slot ) SUNVOX_FN_ATTR;
int sv_get_song_tpl( int slot ) SUNVOX_FN_ATTR;
//Frame is one discrete of the sound. Sampling frequency 44100 Hz means, that you hear 44100 frames per second.
unsigned int sv_get_song_length_frames( int slot ) SUNVOX_FN_ATTR;
unsigned int sv_get_song_length_lines( int slot ) SUNVOX_FN_ATTR;
//sv_new_module() - create a new module;
//sv_remove_module() - remove selected module;
//sv_connect_module() - connect the source to the destination;
//sv_disconnect_module() - disconnect the source from the destination;
//sv_load_module() - load a module; supported file formats: sunsynth, xi, wav, aiff;
//sv_sampler_load() - load a sample to already created Sampler; to replace the whole sampler - set sample_slot to -1;
int sv_new_module( int slot, const char* type, const char* name, int x, int y, int z ) SUNVOX_FN_ATTR; //USE LOCK/UNLOCK!
int sv_remove_module( int slot, int mod_num ) SUNVOX_FN_ATTR; //USE LOCK/UNLOCK!
int sv_connect_module( int slot, int source, int destination ) SUNVOX_FN_ATTR; //USE LOCK/UNLOCK!
int sv_disconnect_module( int slot, int source, int destination ) SUNVOX_FN_ATTR; //USE LOCK/UNLOCK!
int sv_load_module( int slot, const char* file_name, int x, int y, int z ) SUNVOX_FN_ATTR;
int sv_sampler_load( int slot, int sampler_module, const char* file_name, int sample_slot ) SUNVOX_FN_ATTR;
int sv_get_number_of_modules( int slot ) SUNVOX_FN_ATTR;
int sv_get_module_flags( int slot, int mod_num ) SUNVOX_FN_ATTR;
int* sv_get_module_inputs( int slot, int mod_num ) SUNVOX_FN_ATTR;
int* sv_get_module_outputs( int slot, int mod_num ) SUNVOX_FN_ATTR;
const char* sv_get_module_name( int slot, int mod_num ) SUNVOX_FN_ATTR;
unsigned int sv_get_module_xy( int slot, int mod_num ) SUNVOX_FN_ATTR;
int sv_get_module_color( int slot, int mod_num ) SUNVOX_FN_ATTR;
void* sv_get_module_scope( int slot, int mod_num, int channel, int* buffer_offset, int* buffer_size ) SUNVOX_FN_ATTR;
//sv_get_module_scope2() return value = received number of samples (may be less or equal to samples_to_read).
unsigned int sv_get_module_scope2( int slot, int mod_num, int channel, signed short* read_buf, unsigned int samples_to_read ) SUNVOX_FN_ATTR;
int sv_get_number_of_module_ctls( int slot, int mod_num ) SUNVOX_FN_ATTR;
const char* sv_get_module_ctl_name( int slot, int mod_num, int ctl_num ) SUNVOX_FN_ATTR;
int sv_get_module_ctl_value( int slot, int mod_num, int ctl_num, int scaled ) SUNVOX_FN_ATTR;
int sv_get_number_of_patterns( int slot ) SUNVOX_FN_ATTR;
int sv_get_pattern_x( int slot, int pat_num ) SUNVOX_FN_ATTR;
int sv_get_pattern_y( int slot, int pat_num ) SUNVOX_FN_ATTR;
int sv_get_pattern_tracks( int slot, int pat_num ) SUNVOX_FN_ATTR;
int sv_get_pattern_lines( int slot, int pat_num ) SUNVOX_FN_ATTR;
//How to use sv_get_pattern_data():
//  int pat_tracks = sv_get_pattern_tracks( slot, pat_num );
//  sunvox_note* data = sv_get_pattern_data( slot, pat_num );
//  sunvox_note* n = &data[ line_number * pat_tracks + track_number ];
//  ... and then do someting with note n
sunvox_note* sv_get_pattern_data( int slot, int pat_num ) SUNVOX_FN_ATTR;
int sv_pattern_mute( int slot, int pat_num, int mute ) SUNVOX_FN_ATTR; //USE LOCK/UNLOCK!
//SunVox engine uses its own time space, measured in ticks.
//Use sv_get_ticks() to get current tick counter (from 0 to 0xFFFFFFFF).
//Use sv_get_ticks_per_second() to get the number of SunVox ticks per second.
unsigned int sv_get_ticks( void ) SUNVOX_FN_ATTR;
unsigned int sv_get_ticks_per_second( void ) SUNVOX_FN_ATTR;

#ifdef __cplusplus
} //extern "C"
#endif

#else

typedef int (SUNVOX_FN_ATTR *tsv_audio_callback)( void* buf, int frames, int latency, unsigned int out_time );
typedef int (SUNVOX_FN_ATTR *tsv_open_slot)( int slot );
typedef int (SUNVOX_FN_ATTR *tsv_close_slot)( int slot );
typedef int (SUNVOX_FN_ATTR *tsv_lock_slot)( int slot );
typedef int (SUNVOX_FN_ATTR *tsv_unlock_slot)( int slot );
typedef int (SUNVOX_FN_ATTR *tsv_init)( const char* dev, int freq, int channels, int flags );
typedef int (SUNVOX_FN_ATTR *tsv_deinit)( void );
typedef int (SUNVOX_FN_ATTR *tsv_get_sample_type)( void );
typedef int (SUNVOX_FN_ATTR *tsv_load)( int slot, const char* name );
typedef int (SUNVOX_FN_ATTR *tsv_load_from_memory)( int slot, void* data, unsigned int data_size );
typedef int (SUNVOX_FN_ATTR *tsv_play)( int slot );
typedef int (SUNVOX_FN_ATTR *tsv_play_from_beginning)( int slot );
typedef int (SUNVOX_FN_ATTR *tsv_stop)( int slot );
typedef int (SUNVOX_FN_ATTR *tsv_set_autostop)( int slot, int autostop );
typedef int (SUNVOX_FN_ATTR *tsv_end_of_song)( int slot );
typedef int (SUNVOX_FN_ATTR *tsv_rewind)( int slot, int t );
typedef int (SUNVOX_FN_ATTR *tsv_volume)( int slot, int vol );
typedef int (SUNVOX_FN_ATTR *tsv_send_event)( int slot, int track_num, int note, int vel, int module, int ctl, int ctl_val );
typedef int (SUNVOX_FN_ATTR *tsv_get_current_line)( int slot );
typedef int (SUNVOX_FN_ATTR *tsv_get_current_line2)( int slot );
typedef int (SUNVOX_FN_ATTR *tsv_get_current_signal_level)( int slot, int channel );
typedef const char* (SUNVOX_FN_ATTR *tsv_get_song_name)( int slot );
typedef int (SUNVOX_FN_ATTR *tsv_get_song_bpm)( int slot );
typedef int (SUNVOX_FN_ATTR *tsv_get_song_tpl)( int slot );
typedef unsigned int (SUNVOX_FN_ATTR *tsv_get_song_length_frames)( int slot );
typedef unsigned int (SUNVOX_FN_ATTR *tsv_get_song_length_lines)( int slot );
typedef int (SUNVOX_FN_ATTR *tsv_new_module)( int slot, const char* type, const char* name, int x, int y, int z );
typedef int (SUNVOX_FN_ATTR *tsv_remove_module)( int slot, int mod_num );
typedef int (SUNVOX_FN_ATTR *tsv_connect_module)( int slot, int source, int destination );
typedef int (SUNVOX_FN_ATTR *tsv_disconnect_module)( int slot, int source, int destination );
typedef int (SUNVOX_FN_ATTR *tsv_load_module)( int slot, const char* file_name, int x, int y, int z );
typedef int (SUNVOX_FN_ATTR *tsv_sampler_load)( int slot, int sampler_module, const char* file_name, int sample_slot );
typedef int (SUNVOX_FN_ATTR *tsv_get_number_of_modules)( int slot );
typedef int (SUNVOX_FN_ATTR *tsv_get_module_flags)( int slot, int mod_num );
typedef int* (SUNVOX_FN_ATTR *tsv_get_module_inputs)( int slot, int mod_num );
typedef int* (SUNVOX_FN_ATTR *tsv_get_module_outputs)( int slot, int mod_num );
typedef const char* (SUNVOX_FN_ATTR *tsv_get_module_name)( int slot, int mod_num );
typedef unsigned int (SUNVOX_FN_ATTR *tsv_get_module_xy)( int slot, int mod_num );
typedef int (SUNVOX_FN_ATTR *tsv_get_module_color)( int slot, int mod_num );
typedef void* (SUNVOX_FN_ATTR *tsv_get_module_scope)( int slot, int mod_num, int channel, int* buffer_offset, int* buffer_size );
typedef unsigned int (SUNVOX_FN_ATTR *tsv_get_module_scope2)( int slot, int mod_num, int channel, signed short* read_buf, unsigned int samples_to_read );
typedef int (SUNVOX_FN_ATTR *tsv_get_number_of_module_ctls)( int slot, int mod_num );
typedef const char* (SUNVOX_FN_ATTR *tsv_get_module_ctl_name)( int slot, int mod_num, int ctl_num );
typedef int (SUNVOX_FN_ATTR *tsv_get_module_ctl_value)( int slot, int mod_num, int ctl_num, int scaled );
typedef int (SUNVOX_FN_ATTR *tsv_get_number_of_patterns)( int slot );
typedef int (SUNVOX_FN_ATTR *tsv_get_pattern_x)( int slot, int pat_num );
typedef int (SUNVOX_FN_ATTR *tsv_get_pattern_y)( int slot, int pat_num );
typedef int (SUNVOX_FN_ATTR *tsv_get_pattern_tracks)( int slot, int pat_num );
typedef int (SUNVOX_FN_ATTR *tsv_get_pattern_lines)( int slot, int pat_num );
typedef sunvox_note* (SUNVOX_FN_ATTR *tsv_get_pattern_data)( int slot, int pat_num );
typedef int (SUNVOX_FN_ATTR *tsv_pattern_mute)( int slot, int pat_num, int mute );
typedef unsigned int (SUNVOX_FN_ATTR *tsv_get_ticks)( void );
typedef unsigned int (SUNVOX_FN_ATTR *tsv_get_ticks_per_second)( void );

#ifdef SUNVOX_MAIN

#ifdef WIN
#define IMPORT( Handle, Type, Function, Store ) \
    { \
	Store = (Type)GetProcAddress( Handle, Function ); \
	if( Store == 0 ) { fn_not_found = Function; break; } \
    }
#define ERROR_MSG( msg ) MessageBoxA( 0, msg, "Error", MB_OK );
#endif

#ifdef UNIX
#define IMPORT( Handle, Type, Function, Store ) \
    { \
	Store = (Type)dlsym( Handle, Function ); \
	if( Store == 0 ) { fn_not_found = Function; break; } \
    }
#define ERROR_MSG( msg ) printf( "ERROR: %s\n", msg );
#endif

tsv_audio_callback sv_audio_callback = 0;
tsv_open_slot sv_open_slot = 0;
tsv_close_slot sv_close_slot = 0;
tsv_lock_slot sv_lock_slot = 0;
tsv_unlock_slot sv_unlock_slot = 0;
tsv_init sv_init = 0;
tsv_deinit sv_deinit = 0;
tsv_get_sample_type sv_get_sample_type = 0;
tsv_load sv_load = 0;
tsv_load_from_memory sv_load_from_memory = 0;
tsv_play sv_play = 0;
tsv_play_from_beginning sv_play_from_beginning = 0;
tsv_stop sv_stop = 0;
tsv_set_autostop sv_set_autostop = 0;
tsv_end_of_song sv_end_of_song = 0;
tsv_rewind sv_rewind = 0;
tsv_volume sv_volume = 0;
tsv_send_event sv_send_event = 0;
tsv_get_current_line sv_get_current_line = 0;
tsv_get_current_line2 sv_get_current_line2 = 0;
tsv_get_current_signal_level sv_get_current_signal_level = 0;
tsv_get_song_name sv_get_song_name = 0;
tsv_get_song_bpm sv_get_song_bpm = 0;
tsv_get_song_tpl sv_get_song_tpl = 0;
tsv_get_song_length_frames sv_get_song_length_frames = 0;
tsv_get_song_length_lines sv_get_song_length_lines = 0;
tsv_new_module sv_new_module = 0;
tsv_remove_module sv_remove_module = 0;
tsv_connect_module sv_connect_module = 0;
tsv_disconnect_module sv_disconnect_module = 0;
tsv_load_module sv_load_module = 0;
tsv_sampler_load sv_sampler_load = 0;
tsv_get_number_of_modules sv_get_number_of_modules = 0;
tsv_get_module_flags sv_get_module_flags = 0;
tsv_get_module_inputs sv_get_module_inputs = 0;
tsv_get_module_outputs sv_get_module_outputs = 0;
tsv_get_module_name sv_get_module_name = 0;
tsv_get_module_xy sv_get_module_xy = 0;
tsv_get_module_color sv_get_module_color = 0;
tsv_get_module_scope sv_get_module_scope = 0;
tsv_get_module_scope2 sv_get_module_scope2 = 0;
tsv_get_number_of_module_ctls sv_get_number_of_module_ctls = 0;
tsv_get_module_ctl_name sv_get_module_ctl_name = 0;
tsv_get_module_ctl_value sv_get_module_ctl_value = 0;
tsv_get_number_of_patterns sv_get_number_of_patterns = 0;
tsv_get_pattern_x sv_get_pattern_x = 0;
tsv_get_pattern_y sv_get_pattern_y = 0;
tsv_get_pattern_tracks sv_get_pattern_tracks = 0;
tsv_get_pattern_lines sv_get_pattern_lines = 0;
tsv_get_pattern_data sv_get_pattern_data = 0;
tsv_pattern_mute sv_pattern_mute = 0;
tsv_get_ticks sv_get_ticks = 0;
tsv_get_ticks_per_second sv_get_ticks_per_second = 0;

#ifdef UNIX
    void* g_sv_dll = 0;
#endif

#ifdef WIN
    HMODULE g_sv_dll = 0;
#endif

int sv_load_dll( void )
{
#ifdef WIN
    g_sv_dll = LoadLibrary( TEXT(LIBNAME) );
    if( g_sv_dll == 0 )
    {
        ERROR_MSG( "sunvox.dll not found" );
        return 1;
    }
#endif
#ifdef UNIX
    g_sv_dll = dlopen( LIBNAME, RTLD_NOW );
    if( g_sv_dll == 0 )
    {
	printf( "%s\n", dlerror() );
        return 1;
    }
#endif
    const char* fn_not_found = 0;
    while( 1 )
    {
	IMPORT( g_sv_dll, tsv_audio_callback, "sv_audio_callback", sv_audio_callback );
	IMPORT( g_sv_dll, tsv_open_slot, "sv_open_slot", sv_open_slot );
	IMPORT( g_sv_dll, tsv_close_slot, "sv_close_slot", sv_close_slot );
	IMPORT( g_sv_dll, tsv_lock_slot, "sv_lock_slot", sv_lock_slot );
	IMPORT( g_sv_dll, tsv_unlock_slot, "sv_unlock_slot", sv_unlock_slot );
	IMPORT( g_sv_dll, tsv_init, "sv_init", sv_init );
	IMPORT( g_sv_dll, tsv_deinit, "sv_deinit", sv_deinit );
	IMPORT( g_sv_dll, tsv_get_sample_type, "sv_get_sample_type", sv_get_sample_type );
	IMPORT( g_sv_dll, tsv_load, "sv_load", sv_load );
	IMPORT( g_sv_dll, tsv_load_from_memory, "sv_load_from_memory", sv_load_from_memory );
	IMPORT( g_sv_dll, tsv_play, "sv_play", sv_play );
	IMPORT( g_sv_dll, tsv_play_from_beginning, "sv_play_from_beginning", sv_play_from_beginning );
	IMPORT( g_sv_dll, tsv_stop, "sv_stop", sv_stop );
	IMPORT( g_sv_dll, tsv_set_autostop, "sv_set_autostop", sv_set_autostop );
	IMPORT( g_sv_dll, tsv_end_of_song, "sv_end_of_song", sv_end_of_song );
	IMPORT( g_sv_dll, tsv_rewind, "sv_rewind", sv_rewind );
	IMPORT( g_sv_dll, tsv_volume, "sv_volume", sv_volume );
	IMPORT( g_sv_dll, tsv_send_event, "sv_send_event", sv_send_event );
	IMPORT( g_sv_dll, tsv_get_current_line, "sv_get_current_line", sv_get_current_line );
	IMPORT( g_sv_dll, tsv_get_current_line2, "sv_get_current_line2", sv_get_current_line2 );
	IMPORT( g_sv_dll, tsv_get_current_signal_level, "sv_get_current_signal_level", sv_get_current_signal_level );
	IMPORT( g_sv_dll, tsv_get_song_name, "sv_get_song_name", sv_get_song_name );
	IMPORT( g_sv_dll, tsv_get_song_bpm, "sv_get_song_bpm", sv_get_song_bpm );
	IMPORT( g_sv_dll, tsv_get_song_tpl, "sv_get_song_tpl", sv_get_song_tpl );
	IMPORT( g_sv_dll, tsv_get_song_length_frames, "sv_get_song_length_frames", sv_get_song_length_frames );
	IMPORT( g_sv_dll, tsv_get_song_length_lines, "sv_get_song_length_lines", sv_get_song_length_lines );
	IMPORT( g_sv_dll, tsv_new_module, "sv_new_module", sv_new_module );
	IMPORT( g_sv_dll, tsv_remove_module, "sv_remove_module", sv_remove_module );
	IMPORT( g_sv_dll, tsv_connect_module, "sv_connect_module", sv_connect_module );
	IMPORT( g_sv_dll, tsv_disconnect_module, "sv_disconnect_module", sv_disconnect_module );
	IMPORT( g_sv_dll, tsv_load_module, "sv_load_module", sv_load_module );
	IMPORT( g_sv_dll, tsv_sampler_load, "sv_sampler_load", sv_sampler_load );
	IMPORT( g_sv_dll, tsv_get_number_of_modules, "sv_get_number_of_modules", sv_get_number_of_modules );
	IMPORT( g_sv_dll, tsv_get_module_flags, "sv_get_module_flags", sv_get_module_flags );
	IMPORT( g_sv_dll, tsv_get_module_inputs, "sv_get_module_inputs", sv_get_module_inputs );
	IMPORT( g_sv_dll, tsv_get_module_outputs, "sv_get_module_outputs", sv_get_module_outputs );
	IMPORT( g_sv_dll, tsv_get_module_name, "sv_get_module_name", sv_get_module_name );
	IMPORT( g_sv_dll, tsv_get_module_xy, "sv_get_module_xy", sv_get_module_xy );
	IMPORT( g_sv_dll, tsv_get_module_color, "sv_get_module_color", sv_get_module_color );
	IMPORT( g_sv_dll, tsv_get_module_scope, "sv_get_module_scope", sv_get_module_scope );
	IMPORT( g_sv_dll, tsv_get_module_scope2, "sv_get_module_scope2", sv_get_module_scope2 );
	IMPORT( g_sv_dll, tsv_get_number_of_module_ctls, "sv_get_number_of_module_ctls", sv_get_number_of_module_ctls );
	IMPORT( g_sv_dll, tsv_get_module_ctl_name, "sv_get_module_ctl_name", sv_get_module_ctl_name );
	IMPORT( g_sv_dll, tsv_get_module_ctl_value, "sv_get_module_ctl_value", sv_get_module_ctl_value );
	IMPORT( g_sv_dll, tsv_get_number_of_patterns, "sv_get_number_of_patterns", sv_get_number_of_patterns );
	IMPORT( g_sv_dll, tsv_get_pattern_x, "sv_get_pattern_x", sv_get_pattern_x );
	IMPORT( g_sv_dll, tsv_get_pattern_y, "sv_get_pattern_y", sv_get_pattern_y );
	IMPORT( g_sv_dll, tsv_get_pattern_tracks, "sv_get_pattern_tracks", sv_get_pattern_tracks );
	IMPORT( g_sv_dll, tsv_get_pattern_lines, "sv_get_pattern_lines", sv_get_pattern_lines );
	IMPORT( g_sv_dll, tsv_get_pattern_data, "sv_get_pattern_data", sv_get_pattern_data );
	IMPORT( g_sv_dll, tsv_pattern_mute, "sv_pattern_mute", sv_pattern_mute );
	IMPORT( g_sv_dll, tsv_get_ticks, "sv_get_ticks", sv_get_ticks );
	IMPORT( g_sv_dll, tsv_get_ticks_per_second, "sv_get_ticks_per_second", sv_get_ticks_per_second );
	break;
    }
    if( fn_not_found )
    {
	char ts[ 256 ];
	sprintf( ts, "sunvox lib: %s() not found", fn_not_found );
	ERROR_MSG( ts );
	return -1;
    }

    return 0;
}

int sv_unload_dll( void )
{
#ifdef UNIX
    if( g_sv_dll ) dlclose( g_sv_dll );
#endif
    return 0;
}

#endif

#endif //...SUNVOX_STATIC_LIB

#endif
