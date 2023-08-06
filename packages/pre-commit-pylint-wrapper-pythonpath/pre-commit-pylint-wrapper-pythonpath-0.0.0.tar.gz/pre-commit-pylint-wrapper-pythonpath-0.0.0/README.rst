pre-commit-pylint-pythonpath
============================

This is a simple pre-commit hook wrapper around ``pylint``.

In contrast to the 'official' pre-commit provided mirror this wrapper adds the
to-be-checked project root to the ``PYTHONPATH`` inside the hook venv created by 
pre-commit which is necessary for some configurations (e.g. to use repo local 
pylint plugins).

.. note:: This can potentially have unintended side-effects if anything in the
          project root shadows any of the pylint dependencies.
