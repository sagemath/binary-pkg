Binary Packaging
================

This utility helps with creating binaries for distribution. Similar to
conda, it builds the source tree in a long directory name which is
then patched at install time. 


Usage
-----

Building and packaging of an application is configured with a yaml
file in the repository root. As an example, there is test.yaml and
sage.yaml. To create a binary tarball for Sage, for example, all you
have to do is run

    make package-sage

This creates a tarball with an added ``relocate-once.py`` file that patches
any hard-coded paths.


Configuration Syntax
--------------------

As a simplified example, let us look at the test application in the
test.yaml file. It starts with the name:

    name: PackagingTest

which will be the name of the root directory in the binary
tarball. Our basic assumption is that your source code lives in a git
repository, which we specify next:

    repository: https://github.com/octol/minimal-gtest-autotools
    branch: master

Then we have a (bash) build script to build the application

    build: |
        autoreconf -vfi
        ./configure
        make

After the build is complete, we need to know the version. Typically
this can be gotten via a command line switch of the application,
though in this case we cheat. In any case, the output of this script
is the version:

    version: |
        echo 1.0

Finally, we define how to package the built source tree. There may be
more than one way to package the application, each of which is
distinguished by an internal name.

    package:
      - name: Full binary tarball
        command: |
            tar cjf {dist}/test-{version}-{osname}-{arch}.tar.bz2 {path}
        files:
          - include: '**'
        rewrite_path:
          - exclude: '**/*.a'
    
The `files` section is a list of include/exclude directives, to be
read from the bottom up. That is, later directives override earlier
ones. The `rewrite_path` section defines a subset of the files that
are to be ignored when rewriting hard-coded paths. In this example,
all files are included but paths in static archives are not patched.

