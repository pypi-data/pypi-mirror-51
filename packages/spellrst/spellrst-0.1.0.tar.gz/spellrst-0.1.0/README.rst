========
spellrst
========

Spell check reStructuredText.

Install
-------

Install with pip::

   pip install spellrst

And download the `spaCy model <https://spacy.io/models>`__ you want to use e.g. ``en_core_web_md``::

   python -m spacy download en_core_web_md

Usage
-----

After installing you can run ``spellrst`` from the command line::

   $ spellrst --help
   Usage: spellrst [OPTIONS] [FILES]...

     Spell check reStructuredText.

   Options:
     -d, --dictionary TEXT  spaCy language model (spacy.io/models), e.g.
                            en_core_web_md
     --help                 Show this message and exit.

For example, to check all rst files contained in a directory (fish)::

   spellrst **.rst

TODO
----

- whitelist
