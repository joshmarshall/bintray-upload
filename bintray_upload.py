#!/usr/bin/env python

import argparse
import os
import os.path
import re
import subprocess
import sys

USERNAME = os.environ["BINTRAY_USERNAME"]
API_KEY = os.environ["BINTRAY_API_KEY"]
API_BASE = os.environ.get("BINTRAY_URL", "https://api.bintray.com/content")
ORGANIZATION = os.environ.get("BINTRAY_ORGANIZATION")
# these can be overridden with the --architecture flag
ALLOWED_ARCH = ["amd64", "i386", "armel", "powerpc"]


VERSION_RE = re.compile("^\d+(\.\d+)+([^\-]+)?\-([\da-z]+)$")
VERIFY_FORMAT = """
Does this look correct?
- Name: {a.name}
- Version: {a.version}
- Architecture: {a.architecture}
- Distribution: {a.distribution}
- Component: {a.component}
- BinTray Repo: {a.org}/{a.repo}

(Please enter y/n): """


def main():
    parser = argparse.ArgumentParser(description="Upload BinTray package.")
    parser.add_argument("package")
    parser.add_argument("--version", "-v")
    parser.add_argument("--name", "-n")
    parser.add_argument("--no-confirm", action='store_true', default=False)
    parser.add_argument("--repo", "-r", default="ubuntu")
    parser.add_argument("--org", "-o", default=ORGANIZATION)
    parser.add_argument("--component", "-c", default="main")
    parser.add_argument("--architecture", "-a")
    parser.add_argument("--distribution", "-d", default="trusty")

    args = parser.parse_args()
    basename = os.path.basename(args.package)

    if not os.path.isfile(args.package):
        raise ValueError("File {0} is not valid / does not exist.".format(
            args.package))

    if not args.org:
        raise ValueError("Organization is missing.")

    if not args.version or not args.name or not args.architecture:
        # trying to determine name and version from
        base, _ = os.path.splitext(basename)
        base, arch = base.rsplit("_", 1)
        if arch not in ALLOWED_ARCH:
            raise ValueError("Architecture {0} not discoverable".format(arch))
        name, version = base.split("_", 1)
        if not VERSION_RE.match(version):
            raise ValueError("Version not discoverable ({0})".format(version))
        args.version = args.version or version
        args.architecture = args.architecture or arch
        args.name = args.name or name

    url = "{url}/{a.org}/{a.repo}/{a.name}/{a.version}/pool/{a.component}" \
        "/{a.name[0]}/{basename}?publish=1".format(
            url=API_BASE, a=args, basename=basename)

    if not args.no_confirm:
        sys.stdout.write(VERIFY_FORMAT.format(a=args))
        if not sys.stdin.readline().rstrip() == "y":
            print("\nNot submitting package.")
            return

    print("Submitting package.")
    command = [
        "curl", "-s", "-T", args.package, "-u",
        "{0}:{1}".format(USERNAME, API_KEY), url,
        "-H", "X-Bintray-Debian-Distribution: {0.distribution}".format(args),
        "-H", "X-Bintray-Debian-Architecture: {0.architecture}".format(args),
        "-H", "X-Bintray-Debian-Component: {0.component}".format(args)
    ]

    result = subprocess.check_output(command)
    print result


if __name__ == "__main__":
    main()
