# Radiant Voices

Create, modify, read, and write SunVox files.

Requires Python 3.5.

- [Radiant Voices documentation](https://metrasynth.github.io/projects/rv.html) 
- [About Metrasynth](https://metrasynth.github.io/)

## Quick start

The "hello world" example will construct a SunVox project in memory
containing a FM module connected to the Output module.
It will then load it into the SunVox DLL and send a note-on command to the
FM module.

```
$ git clone https://github.com/metrasynth/radiant-voices
$ git clone https://github.com/metrasynth/sunvox-dll-python
$ pip install -e sunvox-dll-python
$ pip install -e radiant-voices
$ wget http://www.warmplace.ru/soft/sunvox/sunvox_dll.zip
$ export SUNVOX_DLL_BASE=$PWD/sunvox_dll
$ cd radiant-voices/examples
$ python helloworld.py
```
