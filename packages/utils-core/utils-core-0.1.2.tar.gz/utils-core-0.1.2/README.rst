utils-core
===========

General utilities on top of Python standard libraries.

Examples for process-related utilities:

.. code-block:: python

    from utils.process import run, silent_run


    run('ls -l')
    out = run(['ls', '-l'], return_output=True)

    # Just runs without any output to stdout. Alias for: run(..., silent=True)
    silent_run('ls -l')

Examples for filesystem-related utilities:

.. code-block:: python

    import os

    from utils.fs import in_dir, in_temp_dir


    with in_temp_dir() as tmpdir:
        assert os.getcwd() == tmpdir

    with in_dir('/tmp'):
        assert os.getcwd() == '/tmp'


Links & Contact Info
====================

| PyPI Package: https://pypi.python.org/pypi/utils-core
| GitHub Source: https://github.com/maxzheng/utils-core
| Report Issues/Bugs: https://github.com/maxzheng/utils-core/issues
|
| Follow: https://twitter.com/MaxZhengX
| Connect: https://www.linkedin.com/in/maxzheng
| Contact: maxzheng.os @t gmail.com
