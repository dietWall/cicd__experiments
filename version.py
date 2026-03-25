#! /usr/bin/env python3

import os
import argparse
from typing import Union
from semver.version import Version
from git_utils import *



def get_version(path: Union[str, os.PathLike]) -> Version:
    """
    Construct a Version object from a file

    :param path: A text file only containing the semantic version
    :return: A :class:`Version` object containing the semantic
             version from the file.
    """
    version = open(path,"r").read().strip()
    return Version.parse(version)

def increase_version(version: Version, bump_type: str) -> Version:
    """
    Increase a version by a given bump type

    :param version: The version to increase
    :param bump_type: The type of increase, either "major", "minor" or "patch"
    :return: A new :class:`Version` object with the increased version
    """
    if bump_type == "major":
        return version.bump_major()
    elif bump_type == "minor":
        return version.bump_minor()
    elif bump_type == "patch":
        return version.bump_patch()
    else:
        return version.bump_build()


def get_bump_type_from_branch(branch: str) -> str:
    """
    Get the bump type from a branch name

    :param branch: The branch name to get the bump type from
    :return: The bump type, either "major", "minor" or "patch"
    """
    if branch.startswith("release/"):
        return "minor"
    elif branch.startswith("hotfix/"):
        return "patch"
    elif branch.startswith("feature/"):
        return "patch"
    else:
        return "patch"


def main():
    parser = argparse.ArgumentParser(description="Bump version in version")
    parser.add_argument("--bump_type", choices=["major", "minor", "patch"], help="Type of version bump")
    parser.add_argument("--file", default="version", help="File containing the current version")
    args = parser.parse_args()

    current_version = get_version(args.file)

    branch = get_branch_name()

    if args.bump_type:
        bump_type = args.bump_type
    else:
        bump_type = get_bump_type_from_branch(branch)

    new_version = increase_version(current_version, bump_type)

    with open(args.file, "w") as f:
        f.write(str(new_version))

    print(f"Version bumped from {current_version} to {new_version}")


if __name__ == "__main__":
    main()