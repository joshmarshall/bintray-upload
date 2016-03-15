#!/usr/bin/env python


from __future__ import print_function

import argparse
import os
import os.path
import re
import sys

import requests

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
        arch = args.architecture or arch
        if arch not in ALLOWED_ARCH:
            raise ValueError("Architecture {0} not discoverable".format(arch))
        name, version = base.split("_", 1)
        name = args.name or name
        version = args.version or version
        if not VERSION_RE.match(version):
            raise ValueError("Version not discoverable ({0})".format(version))
        args.version = version
        args.architecture = arch
        args.name = name

    url = "{url}/{a.org}/{a.repo}/{a.name}/{a.version}/pool/{a.component}" \
        "/{a.name[0]}/{basename}?publish=1".format(
            url=API_BASE, a=args, basename=basename)

    if not args.no_confirm:
        sys.stdout.write(VERIFY_FORMAT.format(a=args))
        if not sys.stdin.readline().rstrip() == "y":
            print("\nNot submitting package.")
            return

    print("Submitting package...")

    parameters = {"publish": "1"}
    headers = {
        "X-Bintray-Debian-Distribution": args.distribution,
        "X-Bintray-Debian-Architecture": args.architecture,
        "X-Bintray-Debian-Component": args.component
    }
    with open(args.package, "rb") as package_fp:
        response = requests.put(
            url, auth=(USERNAME, API_KEY), params=parameters,
            headers=headers, data=package_fp)

    if response.status_code != 201:
        raise Exception(
            "Failed to submit package: {0}\n{1}".format(
                response.status_code, response.text))

    print("Submitted successfully.")


if __name__ == "__main__":
    main()
