import re
import argparse
import semver


def parse_version(version_str):
    # Parse semver: MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.-]+))?(?:\+([a-zA-Z0-9.-]+))?$', version_str)
    if not match:
        raise ValueError(f"Invalid semver format: {version_str}")
    major, minor, patch, prerelease, build = match.groups()
    return int(major), int(minor), int(patch), prerelease, build

def format_version(major, minor, patch, prerelease=None, build=None):
    version = f"{major}.{minor}.{patch}"
    if prerelease:
        version += f"-{prerelease}"
    if build:
        version += f"+{build}"
    return version

def bump_major(major, minor, patch, prerelease, build):
    return major + 1, 0, 0, None, None

def bump_minor(major, minor, patch, prerelease, build):
    return major, minor + 1, 0, None, None

def bump_patch(major, minor, patch, prerelease, build):
    return major, minor, patch + 1, None, None

def main():
    parser = argparse.ArgumentParser(description="Bump version in version.txt")
    parser.add_argument("bump_type", choices=["major", "minor", "patch"], help="Type of version bump")
    args = parser.parse_args()

    with open("version.txt", "r") as f:
        current_version = f.read().strip()

    major, minor, patch, prerelease, build = parse_version(current_version)

    if args.bump_type == "major":
        new_major, new_minor, new_patch, new_prerelease, new_build = bump_major(major, minor, patch, prerelease, build)
    elif args.bump_type == "minor":
        new_major, new_minor, new_patch, new_prerelease, new_build = bump_minor(major, minor, patch, prerelease, build)
    elif args.bump_type == "patch":
        new_major, new_minor, new_patch, new_prerelease, new_build = bump_patch(major, minor, patch, prerelease, build)

    new_version = format_version(new_major, new_minor, new_patch, new_prerelease, new_build)

    with open("version.txt", "w") as f:
        f.write(new_version)

    print(f"Version bumped from {current_version} to {new_version}")

if __name__ == "__main__":
    main()