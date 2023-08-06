BIO pype
========

Simple and slim python framework to build, organize and standardize
bioinformatics analyses.

    The system is built around the python
    `argparse <https://docs.python.org/2/library/argparse.html>`__
    module, to provide command line interface to run the configured
    analyses. The framework is heavily customizable and provides basic
    method to access to `Environment
    Modules <http://modules.sourceforge.net>`__ and implements various
    queuing systems such as
    `moab/torque <http://www.adaptivecomputing.com/>`__.

Install
-------

**From Pypi**

::

    pip install bio_pype

**The development version from git**

::

    git clone https://bitbucket.org/ffavero/bio_pype
    cd bio_pype
    python setup.py test
    python setup.py install

**Installation with virtualenv in the `computerome
HPC <https://computerome.dtu.dk>`__ system:**

(Or in any system where virtualenv is not installed at system level)

::

    mkdir ~/venv_files

    # Download virtualenv files (not installed in the python version used in computerome)
    curl -L -o ~/venv_files/setuptools-20.2.2-py2.py3-none-any.whl https://github.com/pypa/virtualenv/raw/develop/virtualenv_support/setuptools-20.2.2-py2.py3-none-any.whl
    curl -L -o ~/venv_files/pip-8.1.0-py2.py3-none-any.whl https://github.com/pypa/virtualenv/raw/develop/virtualenv_support/pip-8.1.0-py2.py3-none-any.whl
    curl -L -o ~/venv_files/virtualenv.py https://github.com/pypa/virtualenv/raw/develop/virtualenv.py

    # Create a virtual environment
    python ~/venv_files/virtualenv.py --extra-search-dir=~/venv_files ~/venv_bio_pype
    # Activate the environment
    source ~/venv_bio_pype/bin/activate

    # Install bio_pype as instructed above

    # The pype command line utility will be available upon the "activation" of the environment or by specifying the full path, in this case:

    # ~/venv_bio_pype/bin/pype

    # To deactivate the virtual env:
    deactivate

Basic usage
-----------

Access first level modules:

::

    $ pype
    usage: pype [-p PROFILE] {pipelines,profiles,repos,snippets} ...

    Slim and simple framework to ease the managements of data, tools and pipelines in the computerome HPC

    positional arguments:
        pipelines       Workflows built by assembling pipelines and snippets
        profiles        Set of databases softwares and meta information
        repos           Management of pype modules
        snippets        Single tasks implementations

    optional arguments:
      -p PROFILE, --profile PROFILE
                        Select the profile. This will define things like
                        databases, reference genomes paths,specific version of
                        programs to loads and other similar configurations.
                        Default: default

    This is version 0.9.0 - Francesco Favero - 15 May 2017

Install Repos:
--------------

By default the repository of modules is empty.

To install a desired repository, list the available repository:

::

    $ pype repos list -a

Install a selected repository:

::

    $ pype repos install -f sequenza

More Details
------------

It is possible to pass local modules for snippets and profiles via
environment variables, An example with the package test modules:

::

    $ PYPE_SNIPPETS=test/data/snippets pype snippets
    error: too few arguments
    usage: pype snippets {reverse_fa,complement_fa,lower_fa,test} ...

    positional arguments:
      {reverse_fa,complement_fa,lower_fa,test}
        reverse_fa          reverse a fasta sequence
        complement_fa       lower case a fasta sequence
        lower_fa            lower case a fasta sequence
        test                test_snippets    

**Snippets**

The snippets are python modules that perform a given task:

::

    $ PYPE_SNIPPETS=test/data/snippets pype snippets test
    error: argument --test is required
    usage: pype snippets test --test TEST [-o OPT]

    optional arguments:
      --test TEST  Test metavar
      -o OPT       test option

::

    $ PYPE_SNIPPETS=test/data/snippets pype snippets test --test World
    Hello World

::

    $ PYPE_SNIPPETS=test/data/snippets pype snippets test --test mate -o Cheers
    Cheers mate

**Pipeline:**

The pipelines are yaml files tbat group any snippets or other pipelines,
with the desired dependency order.

::

    $ PYPE_SNIPPETS=test/data/snippets PYPE_PIPELINES=test/data/pipelines pype pipelines
    error: too few arguments
    usage: pype pipelines [--queue {echo,none}] {rev_compl_low_fa} ...

    positional arguments:
      {rev_compl_low_fa}
        rev_compl_low_fa   Reverse Complement Lower case a fasta

    optional arguments:
      --queue {msub,echo,none}
                            Select the queuing system to run the pipeline
      --log LOG             Path used to write the pipeline logs. Default working
                            directory.

The arguments for a pipeline are parsed on the fly from a YAML file,
which defines the tools and the flow of the execution:

::

    info:
       description: Reverse Complement Lower case a fasta
       date:        06/07/2016
    items:
      - name: lower_fa
        type: snippet
        arguments:
          -i: '%(complement_fa)s'
          -o: '%(output)s'
        dependencies:
          items:
            - name: complement_fa
              type: snippet
              arguments:
                -i: '%(reverse_fa)s'
                -o: '%(complement_fa)s'
              dependencies:
                items:
                  - name: reverse_fa
                    type: snippet
                    arguments:
                      -i: '%(input_fa)s'
                      -o: '%(reverse_fa)s'

resulting argparse interface:

::

    $ PYPE_SNIPPETS=test/data/snippets PYPE_PIPELINES=test/data/pipelines pype pipelines rev_compl_low_fa
    error: argument --complement_fa is required
    usage: pype pipelines rev_compl_low_fa --complement_fa COMPLEMENT_FA --output
                                           OUTPUT --reverse_fa REVERSE_FA
                                           --input_fa INPUT_FA

    optional arguments:
      --complement_fa COMPLEMENT_FA
                            complement_fa type: str
      --output OUTPUT       output type: str
      --reverse_fa REVERSE_FA
                            reverse_fa type: str
      --input_fa INPUT_FA   input_fa type: str

More details on `read the docs <http://bio-pype.readthedocs.io>`__
(slowly documenting the various features/changes).
