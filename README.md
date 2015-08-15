# BinTray Upload

Super simple upload tool for BinTray Debian packages. Requires environment
variables and command line arguments, although it can also derive some
information from a fairly standard package name. Pretty much a wrapper for
a single cURL command.

## Installation

This requires cURL installed on the machine.

```bash
pip install bintray-upload
# or
python setup.py install
```

## Usage

First, set up a BinTray account and organization if necessary. Next,
set your username, organization, and API key as environment variables. For
instance:

```bash
BINTRAY_USERNAME=joebrigs
BINTRAY_ORGANIZATION=softcorpllc
BINTRAY_API_KEY=7646edfabeca4c5c89993307d685db01
```

Now uploading a Debian package is pretty straightforward:

```bash
$ bintray-upload project_2015.0621.052040-5c8999b_amd64.deb

Does this look correct?
- Name: project
- Version: 2015.0621.052040-5c8999b
- Architecture: amd64
- Distribution: trusty
- Component: main
- BinTray Repo: softcorpllc/ubuntu

(Please enter y/n):
```

Alternatively you can provide all of the metadata options via command line
parameters. A more verbose example:

```bash
$ bintray-upload --version 1.1.5 --name widget --repo myrepo --org megacorp \
    --component multiverse --distribution warty --architecture i386 package.deb

Does this look correct?
- Name: widget
- Version: 1.1.5
- Architecture: i386
- Distribution: warty
- Component: multiverse
- BinTray Repo: megacorp/myrepo

(Please enter y/n):
```

Finally, there's a `--no-confirm` option for running the script in CI /
automated environments where no mistakes will ever happen, ever.

*Feedback welcome. There are no tests!*
