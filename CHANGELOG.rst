Changelog
=========


0.4 series
----------

The major themes of this release are:

- Support for SunVox 1.9.3 and 1.9.4.

- Improved compatibility with the SunVox file format.

- Full documentation of the SunVox file format.


0.4.0.dev3 (not released)
-------------------------

Additions
.........

- Add ``Amplifier.gain`` controller.


0.4.0.dev2 (2018-03-11)
-----------------------

Fixes
.....

- Correct a packaging error that included unnecessary cache data from
  documentation builds.


0.4.0.dev1 (2018-03-11)
-----------------------

Additions
.........

- Add documentation about the SunVox file format.

- Add equality checking to ``Range``.

- Add ``Module.midi_in_always`` attribute, defaulting to ``False``.
  When ``True``, the module will respond to MIDI events regardless of
  whether it's selected in the SunVox UI.

- Add ``Module.midi_in_channel`` attribute, defaulting to ``0`` (all channels).
  Set to 1-16 to make the module respond to only a specific MIDI channel.

- Add ``Project.time_grid2`` attribute.

- Add ``MultiSynth.curve2_influence`` controller.

- Add ``MetaModule.event_output`` option (default: ``True``).

- Add ``MultiSynth.trigger`` option (default: ``False``).

- Add ``ModuleFlags`` and ``VisibleModuleFlags`` enums for reading/writing
  ``Module.flags``.

- Add ``PatternFlags`` and ``PatternAppearanceFlags`` enums for reading/writing
  ``Pattern.flags`` and ``Pattern.appearance_flags``.

- Add ``Visualization``, ``LevelMode``, ``Orientation``, and ``OscilloscopeMode``
  for reading/writing the ``Module.visualization`` structure.

- Add ``Project.selected_generator`` attribute.

- Add ``Lfo.Waveform.triangle`` constant.

- Add ``Lfo.generator`` controller.

- Add ``Reverb.random_seed`` controller.

- Add ``Sampler.pitch_envelope`` and ``Sampler.effect_control_envelopes[]``
  containing new envelopes from SunVox 1.9.3.

- Add ``Sampler.effect`` to contain an optional ``SunSynth`` instance
  which in turn contains the effect being modulated by the
  effect control envelopes.

- Add ``Sampler.Sample.loop_sustain`` flag.

- Add ``Sampler.ignore_velocity_for_volume`` option.

- Add ``Container.clone()`` method.

- Add ``Project.pattern_lines()`` method, which iterates over a range of project lines
  and yields information about the active pattern lines for each project line.

- Add ``Pattern.source_method()`` and ``PatternClone.source_method()``,
  to determine the source pattern for any given pattern or pattern clone.

Changes
.......

- Python 3.6 is now required.

- While writing files, ``CHFF`` and ``CHFR`` chunks will not be written
  if they always have a value of ``0``.

- ``AnalogGenerator.unsmooth_frequency_change`` option is now inverted to
  ``.smooth_frequency_change``.

- Update ``Sampler`` and ``Sampler.Envelope`` to support SunVox 1.9.3 format.
  When a pre-1.9.3 formatted Sampler is loaded, it will be upgraded to 1.9.3 format.

- More detailed exception message when attempting to set an out-of-range value
  to a controller.

- Ignore chunk types no longer used by modern SunVox versions:
  ``PSYN``, ``PCTL``, and ``PAMD``.

- Ignore value of ``CHNK`` when reading module-specific chunks.

- Do not write the optional -1 to the end of ``SLNK`` chunks.

- Use the value mapping curve when converting a ``MultiCtl.value``
  to downstream controllers.

- Update ``MetaModule.play_patterns``, which is now of type
  ``MetaModule.PlayPatterns`` instead of ``bool``.
  This introduces support for the new
  ``MetaModule.PlayPatterns.on_no_repeat`` value.

- Use the Fruchterman-Reingold layout algorithm from NetworkX
  for auto-layout of modules, not PyGraphviz neato algorithm.
  This affects the arguments accepted by ``Project.layout()``.

- Improvements to variable names generated from MetaModule
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

- Write correct value of ``CHNK`` when writing module-specific chunks.

- Default to signed 8-bit int when a ``CHFF`` value was 0.


0.3.0 (2017-04-18)
------------------

Additions
.........

- Add ``propagate`` argument to ``MultiCtl.reflect()``.
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

- Fix algorithm for propagating ``MultiCtl.value`` changes to
  mapped controllers.

- Fix algorithm for reflecting mapped controllers back to ``MultiCtl.value``.


0.2.0 (2017-04-02)
------------------

Additions
.........

- Add ``Controller.pattern_value()`` instance method, to map a controller's
  value to a pattern value in the range of 0x0000-0x8000.

- Add ``ALL_NOTES`` constant to see if a ``NOTECMD`` is a note or a command.
  (Example: ``if some_note in ALL_NOTES: ...``)

- Add ``tabular_repr()`` instance methods to ``Note`` and ``Pattern``,
  returning a tabular representation suitable for inclusion in text documents.

- Add ``behaviors`` attribute to all module classes, describing the
  types of information each module can send and receive.

- Add package-specific exception base classes to ``rv.errors``.

- Add support for reading, writing, and modifying controller MIDI mappings.

- Add a ``MultiCtl.macro()`` static method, for quickly creating a
  ``MultiCtl`` that controls several similar controllers on connected modules.

- Add a ``MultiCtl.reflect()`` instance method, for setting a ``MultiCtl``'s
  value based on the destination controller mapped at a given index.

- Add ``# TODO: ...`` notes to indicate unimplemented features.

- Allow property-style access to user-defined controllers on ``MetaModule``s
  using a ``u_`` prefix. For example, if there's a user-defined controller
  named "Attack", it will be accessible via the ``.u_attack`` property.

- Add ``ArrayChunk.set_via_fn()`` method, for setting various curves using
  the output of a function.

- Add ``DRUMNOTE``, ``BDNOTE``, ``HHNOTE``, and ``SDNOTE`` enumerations to
  ``DrumSynth`` class, providing note aliases for easier programming of
  drum sequences.

- Add ``Pattern.set_via_fn()`` and ``.set_via_gen()`` instance methods,
  for altering a pattern based on the output of a function or generator.

Changes
.......

- Rename ``Output`` module's module group to ``"Output"``.

- When using ``Project.layout()``, default to using ``dot`` layout engine.

- Use a direct port of SunVox's algorithm for mapping ``MultiCtl`` values
  to destination controllers.

- Use 1.9.2.0 as SunVox version number when writing projects to files.

- Allow using separate x/y offsets and factors during ``Project.layout()``

Fixes
.....

- Use same sharp note notation as used by SunVox (lowercase indicates sharp).

- Honor ``prog`` keyword arg when passed into ``Project.layout()`` method.

- Do not require pattern ``x`` or ``y`` to be divisible by 4.

- Assign correct controller number to user-defined controllers on
  ``MetaModule``s.

- Correct the max value allowed in a ``MultiSynth`` velocity/velocity curve.

- Move ``pygraphviz`` from ``requirements/base.txt`` to ``.../tools.txt``
  to be more Windows-friendly.


0.1.1 (2016-11-09)
------------------

- Fix upload to PyPI.


0.1.0 (2016-11-09)
------------------

- Initial release.
