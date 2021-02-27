Changelog
=========


1.0.0
-----

The themes of this release are:

- New JavaScript version of Radiant Voices.

- Support for new modules, controllers, options, and curves in SunVox 1.9.6c.

- Improved general compatibility with the SunVox file format.

- Improved documentation of the SunVox file format.

- Radiant Voices API improvements.


Major change: ``genrv`` code generator
......................................

To support porting Radiant Voices to more languages than just Python,
and keeping these ports in sync with new versions of SunVox,
this release introduces a new code-generation tool, ``genrv``.

``genrv`` is written in Python, and uses Jinja2 templates to generate
source code in various target languages, based on a spec written in YAML.

The generated code is run through code-formatting tools,
saved directly into the final package structure,
and committed to the git repository as any other code would be.

Base classes for all module types are generated this way.
They include controllers, options, and controller value enums.
The actual classes for each module inherit from these base classes
and add module-specific behavior maintained by hand.


Major change: JavaScript port
.............................

Radiant Voices now has a JavaScript port, written in TypeScript.
It pairs well with the JavaScript/WebAssembly version of the SunVox library.

It is not a 1-to-1 port from the Python version, although
it is designed to allow you to do the same things.

As of this release, each version has strengths and weaknesses compared to the other.
Over time, we will work towards parity as we strive toward 100% compatibility with
SunVox.


Additions (all versions)
........................

- Adds ``Project.receive_sync_midi`` and ``Project.receive_sync_other`` flags.

- Adds ``ADSR`` module.

- Adds ``Ctl2Note`` module.

- Adds ``Pitch Detector`` module.

- Adds ``harmonics`` to enum for ``AnalogGenerator.waveform`` controller.

- Adds new values to enum for ``SpectraVoice.h_type`` controller:
  ``overtones1+``, ``overtones2+``, ``overtones3+``, ``overtones4+``, ``metal``.

- Adds ``Amplifier.gain`` controller.

- Adds ``AnalogGenerator.true_zero_attack_release`` option.

- Adds new values to enum for ``AnalogGenerator.waveform`` controller:
  ``noise_with_spline_interpolation``,
  ``white_noise``,
  ``pink_noise``,
  ``red_noise``,
  ``blue_noise``,
  ``violet_noise``,
  ``grey_noise``.

- Adds ``LFO.freq_scale_pct`` controller.

- Adds ``LFO.smooth_transitions`` controller.

- Adds ``Sound2Ctl.send_only_changed_values`` option.

- Adds new options to ``MetaModule``:
  ``receive_notes_from_keyboard``, ``do_not_receive_notes_from_keyboard``.

- Adds ``PitchShifter.bypass_if_pitch_eq_0`` controller.

- Adds new value to enum for ``Compressor.mode`` controller:
  ``peak_zero_latency``.

- Adds new values and value names to enum for ``Distortion.type`` controller:
  ``clipping`` is the new name for ``lim``.
  ``foldback`` is the new name for ``sat``.
  ``foldback2``, ``foldback3``, ``overflow`` are new values.

- Adds new value to enum for ``Lfo.waveform`` controller:
  ``random_interpolated``.

- Adds ``DrumSynth.bass_panning`` controller.

- Adds ``DrumSynth.hihat_panning`` controller.

- Adds ``DrumSynth.snare_panning`` controller.

- Adds ``MultiCtl.response`` controller.

- Adds ``MultiCtl.sample_rate_hz`` controller.

- Increases the maximum value of ``Gpio.pin_in`` and ``Gpio.pin_out``
  controllers to ``256``.

- Renames ``Kicker.vol_addition`` controller to ``Kicker.boost``,
  to reflect naming in SunVox 1.9.4.

Additions (Python version)
..........................

- Ports all test cases from JavaScript version.
  Note: A limited number of test cases are not yet completely ported.

- Adds ``Project.restart_position`` attribute.

- Adds ``Project.detach_module(module)`` method.

- Adds ``patch_decompiler`` tool.

- Adds ``Pattern.project`` attribute, set once attached to a project.

- Adds ``Note.pattern`` and ``Note.project`` to allow notes to be project-aware.

- Adds ``Note.module_index`` property, converts ``Note.module`` to 0-based index.

- Adds ``Note.mod`` property, allows setting a note's module via an actual
  `Module` instance (instead of an int).

Changes (All versions)
......................

- Updates module option reading, writing, and setting to reflect
  changes in SunVox 1.9.6.

Changes (Python version)
........................

- Uses `dict` instead of `OrderedDict`, as modern Python's built-in `dict`
  maintains key order.

- Renames ``incoming_links`` to ``in_links``.

- Renames ``controller_number`` to ``ctl_index``, and ``gain_percentage`` to ``gain_pct``,
  to more closely reflect the naming in the JavaScript version.

- Adds type annotations to support static analysis tools and IDEs.

- Renames "dirty waveform" to "drawn waveform".

- Updates default ``sunvox_version`` and ``based_on_version`` of
  newly-created ``Project`` containers to reflect file format version 1.9.6.1.

- Updates ``MetaModule.behaviors`` to include ``sends_notes``.

- Now uses black_ to format all Python modules.

..  _black:
    https://black.readthedocs.io/en/stable/

- ``Project.attach_module`` now raises ``ModuleOwnershipError``
  if the module is already attached to a project.

- ``Project.attach_module`` now re-uses empty module indexes,
  instead of always appending to the end.

- ``Project.connect`` now raises ``ModuleOwnershipError`` if modules
  do not share a common parent.

- Python 3.8 is now required.

- ``Project.attach_pattern`` now returns the index of the attached pattern.

Fixes (all versions)
....................

- Correctly reads and writes ``SLnK`` chunks,
  thus correctly keeping the connection order between modules
  that have more than one connection going in or out.

- Renames ``Sample.loop_end`` to ``Sample.loop_len``.

- Fixes how effects embedded into ``Sampler.effect`` are serialized.

- Updates ``out_controller`` of ``Pitch2Ctl``, ``Sound2Ctl``, and ``Velocity2Ctl``
  to have correct range of 0..255.


Fixes (Python version)
......................

- Fixes writing of controller values to use signed ints instead of unsigned.

- Fixes reading/writing of ``VorbisPlayer.finetune`` controller values.

- Updates the ``helloworld`` example to use correct APIs.

- Parses chunk IDs in a case-sensitive way, to prevent incorrect
  parsing of chunks such as ``SLnK``.


0.4.0.dev2 (2018-03-11)
-----------------------

Fixes
.....

- Corrects a packaging error that included unnecessary cache data from
  documentation builds.


0.4.0.dev1 (2018-03-11)
-----------------------

Additions
.........

- Adds documentation about the SunVox file format.

- Adds equality checking to ``Range``.

- Adds ``Module.midi_in_always`` attribute, defaulting to ``False``.
  When ``True``, the module will respond to MIDI events regardless of
  whether it's selected in the SunVox UI.

- Adds ``Module.midi_in_channel`` attribute, defaulting to ``0`` (all channels).
  Set to 1-16 to make the module respond to only a specific MIDI channel.

- Adds ``Project.time_grid2`` attribute.

- Adds ``MultiSynth.curve2_influence`` controller.

- Adds ``MetaModule.event_output`` option (default: ``True``).

- Adds ``MultiSynth.trigger`` option (default: ``False``).

- Adds ``ModuleFlags`` and ``VisibleModuleFlags`` enums for reading/writing
  ``Module.flags``.

- Adds ``PatternFlags`` and ``PatternAppearanceFlags`` enums for reading/writing
  ``Pattern.flags`` and ``Pattern.appearance_flags``.

- Adds ``Visualization``, ``LevelMode``, ``Orientation``, and ``OscilloscopeMode``
  for reading/writing the ``Module.visualization`` structure.

- Adds ``Project.selected_generator`` attribute.

- Adds ``Lfo.Waveform.triangle`` constant.

- Adds ``Lfo.generator`` controller.

- Adds ``Reverb.random_seed`` controller.

- Adds ``Sampler.pitch_envelope`` and ``Sampler.effect_control_envelopes[]``
  containing new envelopes from SunVox 1.9.3.

- Adds ``Sampler.effect`` to contain an optional ``SunSynth`` instance
  which in turn contains the effect being modulated by the
  effect control envelopes.

- Adds ``Sampler.Sample.loop_sustain`` flag.

- Adds ``Sampler.ignore_velocity_for_volume`` option.

- Adds ``Container.clone()`` method.

- Adds ``Project.pattern_lines()`` method, which iterates over a range of project lines
  and yields information about the active pattern lines for each project line.

- Adds ``Pattern.source_method()`` and ``PatternClone.source_method()``,
  to determine the source pattern for any given pattern or pattern clone.

Changes
.......

- Python 3.6 is now required.

- While writing files, ``CHFF`` and ``CHFR`` chunks will not be written
  if they always have a value of ``0``.

- ``AnalogGenerator.unsmooth_frequency_change`` option is now inverted to
  ``.smooth_frequency_change``.

- Updates ``Sampler`` and ``Sampler.Envelope`` to support SunVox 1.9.3 format.
  When a pre-1.9.3 formatted Sampler is loaded, it will be upgraded to 1.9.3 format.

- More detailed exception message when attempting to set an out-of-range value
  to a controller.

- Ignores chunk types no longer used by modern SunVox versions:
  ``PSYN``, ``PCTL``, and ``PAMD``.

- Ignores value of ``CHNK`` when reading module-specific chunks.

- Does not write the optional -1 to the end of ``SLNK`` chunks.

- Uses the value mapping curve when converting a ``MultiCtl.value``
  to downstream controllers.

- Updates ``MetaModule.play_patterns``, which is now of type
  ``MetaModule.PlayPatterns`` instead of ``bool``.
  This introduces support for the new
  ``MetaModule.PlayPatterns.on_no_repeat`` value.

- Uses the Fruchterman-Reingold layout algorithm from NetworkX
  for auto-layout of modules, not PyGraphviz neato algorithm.
  This affects the arguments accepted by ``Project.layout()``.

- Improves variable names generated from MetaModule
  user defined controller labels.

Fixes
.....

- ``SMIN`` (module MIDI output device name) is now correctly read and written.

- ``SMII`` and ``SMIC`` chunks are now encoded as unsigned int32
  (was previously signed).

- Strings now use UTF-8 encoding.

- All module types now have a correct default ``.flags`` attribute.

- After ``MetaModule.update_user_defined_controllers()`` is called,
  user defined controllers will have correct ``value_type`` set.
  (This avoids errors such as 44100 being out of the 0..32768 range.)

- In ``MetaModule``, when a user defined controller mapping points to
  a non-existent module, the mapping will be ignored.
  (Was throwing an ``AttributeError``)

- When ``Module`` options are loaded from older projects,
  assume ``0`` as a default value if there are not enough bytes.
  (Was throwing an ``IndexError``)

- Range validation for ``Lfo.freq`` and ``Vibrato.freq``
  now depends on the value of the ``frequency_unit`` controller.
  Some modules created in earlier versions of SunVox have out-of-range values.
  These are only warned about using ``logging``,
  instead of the standard behavior of raising an exception.

- Writes correct value of ``CHNK`` when writing module-specific chunks.

- Default to signed 8-bit int when a ``CHFF`` value was 0.


0.3.0 (2017-04-18)
------------------

Additions
.........

- Adds ``propagate`` argument to ``MultiCtl.reflect()``.
  Defaults to ``True`` which causes the new ``MultiCtl.value`` to
  immediately propagate to all mapped controllers,
  including the one that was just reflected.

  Set to ``False`` if you only want to set ``MultiCtl.value``
  without propagating to mapped controllers.

- Pass a value for ``initial`` when calling ``MultiCtl.macro()`` to
  set and propagate an initial value. Default behavior is to not set a value.

Changes
.......

- The ``repr`` of a ``CompactRange`` instance now shows that class name,
  instead of ``Range``.

Fixes
.....

- Fixes algorithm for propagating ``MultiCtl.value`` changes to
  mapped controllers.

- Fixes algorithm for reflecting mapped controllers back to ``MultiCtl.value``.


0.2.0 (2017-04-02)
------------------

Additions
.........

- Adds ``Controller.pattern_value()`` instance method, to map a controller's
  value to a pattern value in the range of 0x0000-0x8000.

- Adds ``ALL_NOTES`` constant to see if a ``NOTECMD`` is a note or a command.
  (Example: ``if some_note in ALL_NOTES: ...``)

- Adds ``tabular_repr()`` instance methods to ``Note`` and ``Pattern``,
  returning a tabular representation suitable for inclusion in text documents.

- Adds ``behaviors`` attribute to all module classes, describing the
  types of information each module can send and receive.

- Adds package-specific exception base classes to ``rv.errors``.

- Adds support for reading, writing, and modifying controller MIDI mappings.

- Adds a ``MultiCtl.macro()`` static method, for quickly creating a
  ``MultiCtl`` that controls several similar controllers on connected modules.

- Adds a ``MultiCtl.reflect()`` instance method, for setting a ``MultiCtl``'s
  value based on the destination controller mapped at a given index.

- Adds ``# TODO: ...`` notes to indicate unimplemented features.

- Allows property-style access to user-defined controllers on ``MetaModule``s
  using a ``u_`` prefix. For example, if there's a user-defined controller
  named "Attack", it will be accessible via the ``.u_attack`` property.

- Adds ``ArrayChunk.set_via_fn()`` method, for setting various curves using
  the output of a function.

- Adds ``DRUMNOTE``, ``BDNOTE``, ``HHNOTE``, and ``SDNOTE`` enumerations to
  ``DrumSynth`` class, providing note aliases for easier programming of
  drum sequences.

- Adds ``Pattern.set_via_fn()`` and ``.set_via_gen()`` instance methods,
  for altering a pattern based on the output of a function or generator.

Changes
.......

- Renames ``Output`` module's module group to ``"Output"``.

- When using ``Project.layout()``, default to using ``dot`` layout engine.

- Uses a direct port of SunVox's algorithm for mapping ``MultiCtl`` values
  to destination controllers.

- Uses 1.9.2.0 as SunVox version number when writing projects to files.

- Allows using separate x/y offsets and factors during ``Project.layout()``

Fixes
.....

- Uses same sharp note notation as used by SunVox (lowercase indicates sharp).

- Honor ``prog`` keyword arg when passed into ``Project.layout()`` method.

- Does not require pattern ``x`` or ``y`` to be divisible by 4.

- Assigns correct controller number to user-defined controllers on
  ``MetaModule``.

- Corrects the max value allowed in a ``MultiSynth`` velocity/velocity curve.

- Moves ``pygraphviz`` from ``requirements/base.txt`` to ``.../tools.txt``
  to be more Windows-friendly.


0.1.1 (2016-11-09)
------------------

- Fixes upload to PyPI.


0.1.0 (2016-11-09)
------------------

- Initial release.
