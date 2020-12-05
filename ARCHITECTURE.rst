============
Architecture
============

File format specification
=========================

``specs/fileformat.yaml`` contains detailed information about the SunVox file format.

Not all of the contents of this file are used.
Eventually, we would like more of the code generation to be based off of the YAML file.

The main sections used by the code generator are the ``module_types``.

Code generation
===============

``src/python/genrv`` contains the code generator, written in Python.

The code generators for each target language are in ``genrv.codegen.*``
(e.g. ``genrv.codegen.ts``).

Each code generator class reads the file format specification,
loops through all module types,
and uses Jinja2 templates to create generated code.

Code generators also perform some post-processing,
such as filtering generated code through pretty-printers.

Code that is generated gets added to the git repo.
This allows someone to download and use Radiant Voices
without running the code generator.

Library structure
=================

Each target language has its own library.
Each library is a mix of hand-maintained and auto-generated code.

Auto-generated code is used to create a nice and consistent API for the target language,
based on the YAML specification, for the following:

- module types;
- controllers for each module;
- options for modules that have them;
- hooks for hand-maintained code to handle special behaviors.

Hand-maintained code is used for everything else:

- low-level reading and writing of IFF chunks;
- state machines needed to transform in-memory SunVox structures to/from IFF chunks;
- managing project data structures such as module connections and patterns;
- special behaviors exhibited by modules such as Sampler or MetaModule.

Details vary between target languages,
and each should eventually have their own section with some more detail.

Tests
=====

Each target language has an extensive test library.

(TODO: More detail…)

Docs
====

API docs are auto generated using the Python version of Radiant Voices.
This ensures that detailed and accurate information about
all module types and controllers can be presented in a pleasant and useful way.

Other docs are written by hand to cover additional topics.

Docs are rendered to HTML using Sphinx.

(TODO: More detail…)
