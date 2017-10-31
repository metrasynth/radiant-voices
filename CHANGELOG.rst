Changelog
=========

0.4.0 (under development)
-------------------------

The major theme of this release is support for SunVox 1.9.3.

Additions
.........

- Add equality checking to ``Range``.

- Add ``Module.midi_in_always`` attribute, defaulting to ``False``.
  When ``True``, the module will respond to MIDI events regardless of
  whether it's selected in the SunVox UI.

- Add ``Module.midi_in_channel`` attribute, defaulting to ``0`` (all channels).
  Set to 1-16 to make the module respond to only a specific MIDI channel.

- Add ``Project.time_grid2`` attribute.

- Add ``MetaModule.event_output`` option (default: ``True``).


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
