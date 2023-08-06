pyjawk
######

Python-based stream editor for json files.  It is a simple setup that
effectively works as a json-parsing ``awk``, similar to jq, but allowing
in-place editing and output of json documents as well, and using Python as the
working language.

Motivation
----------

This program exists for fairly minor convenience, and mostly for my own use.
Whenever I end up needing to quickly edit some json, I find myself opening a
Python REPL, writing a bunch of obvious loading code to load in the json, work
on it a little bit, and then dump it back out to the relevant file.  Also,
whenever I end up needing to inspect json from a web page, I either curl it to a
file and then do the same, or use requests or something to pull it directly in
a Python REPL so I can properly inspect it, or I pipe it through Python's
``json.tool`` and ``less``.

This is meant to supplant those use cases entirely for my own uses.  If you find
it inconvenient to repeatedly undergo the busy work associated with working with
or inspecting json data, and especially if you are most familiar and comfortable
with the stream-editing way of doing things or spending time in a REPL, this
tool might make things a little more convenient for you.

Why not jq?
^^^^^^^^^^^

`jq <https://stedolan.github.io/jq/>`_ is a really great tool for a lot of what
you would use this.  I wrote this because jq doesn't provide the user with a
REPL to mangle data, and because Python is a much more powerful and flexible
language for the modification process, especially if you want to access the
filesystem or other I/O.

jq is a powerful program with a lot of development, active maintenence,
maintainers, and its own filter language.  If that's what you want, use that.
If you want a simple tool for loading json and working on it with python in
either a stream or REPL fashion, this is probably a better fit.

Installation
------------

.. code-block:: shell

   pip install --user pyjawk

Use
---

The program is passed an input string either through stdin or a ``-i`` argument,
and an output through ``-o`` or stdout.  The document is put into a ``data``
object in the environment.  ``-f`` arguments may pass in script files that are
run first, and literal script chunks can be passed in as positional parameters.
The ``data`` object is then serialized and output.

If ``-r`` / ``--repl`` is specified, instead of writing output after processing,
the function to write to the output is registered in the environment as
``write``, the arguments structure is registered as ``args``, and a ``ptpython``
REPL is started up with the same environment.

Examples
--------

Retroarch Playlists
^^^^^^^^^^^^^^^^^^^

If you had an issue with the way that RetroArch generates its playlist files for
the Playstation (by default, it searches for .cue files, but not .bin), and
had something like this in your directory, all playstation games::

   Alpha.bin
   Alpha.cue
   Bravo.bin
   Charlie.bin
   Delta.bin
   Delta.cue

You might end up with a playlist file like this:

.. code-block:: json

   {
     "version": "1.2",
     "default_core_path": "/home/user/.local/share/retroarch/cores/pcsx_rearmed_libretro.so",
     "default_core_name": "Sony - PlayStation (PCSX ReARMed)",
     "label_display_mode": 0,
     "right_thumbnail_mode": 0,
     "left_thumbnail_mode": 0,
     "items": [
       {
         "path": "/home/user/Roms/psx/Alpha.cue",
         "label": "Alpha",
         "core_path": "/home/user/.local/share/retroarch/cores/pcsx_rearmed_libretro.so",
         "core_name": "Sony - PlayStation (PCSX ReARMed)",
         "crc32": "00000000|crc",
         "db_name": "Sony - PlayStation.lpl"
       },
       {
         "path": "/home/user/Roms/psx/Delta.cue",
         "label": "Delta",
         "core_path": "/home/user/.local/share/retroarch/cores/pcsx_rearmed_libretro.so",
         "core_name": "Sony - PlayStation (PCSX ReARMed)",
         "crc32": "00000000|crc",
         "db_name": "Sony - PlayStation.lpl"
       }
     ]
   }

If you want the file to just have the bins, you can easily scan the directory
for these files and modify the json using this tool with this:

.. code-block:: shell

   pyjawk -i 'Sony - PlayStation.lpl' -o 'Sony - PlayStation.lpl' 'from pathlib import Path' 'data["items"] = [{"path": str(path), "label": path.stem, "core_path": data["default_core_path"], "core_name": data["default_core_name"], "crc32": "00000000|crc", "db_name": "Sony - PlayStation.lpl"} for path in (Path.home() / "Roms" / "psx").iterdir() if path.suffix == ".bin"]'

That might look heavy up-front, but you can rewrite it as a script file:

.. code-block:: python

   from pathlib import Path
   data["items"] = [{
         "path": str(path),
         "label": path.stem,
         "core_path": data["default_core_path"],
         "core_name": data["default_core_name"],
         "crc32": "00000000|crc",
         "db_name": "Sony - PlayStation.lpl",
   } for path in (Path.home() / "Fast" / "Roms" / "psx").iterdir() if path.suffix == ".bin"]

and run it with pyjawk as so:

.. code-block:: shell

   pyjawk -i 'Sony - PlayStation.lpl' -o 'Sony - PlayStation.lpl' -f script.py

Or instead load it into a repl to work on it in real time with this:

.. code-block:: shell

   pyjawk -i 'Sony - PlayStation.lpl' -r

.. code-block:: python

   >>> args
   Namespace(compact=0, files=[], input='Sony - PlayStation.lpl', no_input=False, output='-', repl=True, scripts=[])

   >>> data['items'] = []

   >>> write()
   {
     "version": "1.2",
     "default_core_path": "/home/user/.local/share/retroarch/cores/pcsx_rearmed_libretro.so",
     "default_core_name": "Sony - PlayStation (PCSX ReARMed)",
     "label_display_mode": 0,
     "right_thumbnail_mode": 0,
     "left_thumbnail_mode": 0,
     "items": []
   }

   >>> args.compact = 2

   >>> write()
   {"version":"1.2","default_core_path":"/home/user/.local/share/retroarch/cores/pcsx_rearmed_libretro.so","default_core_name":"Sony - PlayStation (PCSX ReARMed)","label_display_mode":0,"right_thumbnail_mode":0,"left_thumbnail_mode":0,"items":[]}

   >>> exit()

Just make sure you call ``write()`` in the repl, or nothing will be written.

Plans
-----

Just to make this complete, I plan to add yaml and xml support to this toolkit
(along with convenience console entrypoints pyxawk and pyyawk), plus whatever
else people might find useful that makes sense (like msgpack, raw output, or
printing and parsing as a Python expression).

I don't plan to add too much to this, as I want it to be useful but also as lean
and manageable as it possibly can be.


