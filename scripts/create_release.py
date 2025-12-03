#!/usr/bin/env python3
"""
Script to create a GitHub release for hl7validator-hl7pt

This script uses the GitHub CLI (gh) to create releases and build the Python package.

Usage:
    python scripts/create_release.py <version> [--draft] [--prerelease]

Examples:
    python scripts/create_release.py 2.0.1
    python scripts/create_release.py 2.1.0-beta --prerelease
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    NC = '\033[0m'  # No Color


def print_info(message):
    """Print info message in green"""
    print(f"{Colors.GREEN}[INFO]{Colors.NC} {message}")


def print_warning(message):
    """Print warning message in yellow"""
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {message}")


def print_error(message):
    """Print error message in red"""
    print(f"{Colors.RED}[ERROR]{Colors.NC} {message}")


def run_command(cmd, check=True, capture_output=False):
    """Run a shell command and return the result"""
    try:
        if capture_output:
            result = subprocess.run(
                cmd, shell=True, check=check, capture_output=True, text=True
            )
            return result.stdout.strip()
        else:
            subprocess.run(cmd, shell=True, check=check)
            return None
    except subprocess.CalledProcessError as e:
        if check:
            print_error(f"Command failed: {cmd}")
            if capture_output and e.stderr:
                print_error(e.stderr)
            raise
        return None


def check_gh_installed():
    """Check if GitHub CLI is installed"""
    try:
        run_command("gh --version", capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_gh_auth():
    """Check if user is authenticated with GitHub"""
    try:
        run_command("gh auth status", capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def validate_version(version):
    """Validate version format (semantic versioning)"""
    pattern = r'^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9\.]+)?$'
    return re.match(pattern, version) is not None


def tag_exists(tag):
    """Check if a git tag already exists"""
    try:
        run_command(f"git rev-parse {tag}", capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def get_current_branch():
    """Get the current git branch name"""
    return run_command("git rev-parse --abbrev-ref HEAD", capture_output=True)


def is_working_directory_clean():
    """Check if the git working directory is clean"""
    status = run_command("git status --porcelain", capture_output=True)
    return len(status) == 0


def build_package():
    """Build the Python package"""
    print_info("Building the package...")
    run_command(f"{sys.executable} -m pip install --upgrade build")
    run_command(f"{sys.executable} -m build")


def find_dist_files(version):
    """Find the built distribution files"""
    dist_dir = Path("dist")

    # Find wheel file
    wheel_pattern = f"hl7validator_hl7pt-{version}-*.whl"
    wheel_files = list(dist_dir.glob(wheel_pattern))
    wheel_file = sorted(wheel_files, key=lambda x: x.stat().st_mtime, reverse=True)[0] if wheel_files else None

    # Find tarball file
    tarball_file = dist_dir / f"hl7validator-hl7pt-{version}.tar.gz"

    return wheel_file, tarball_file


def extract_release_notes(version):
    """Extract release notes from CHANGELOG.md"""
    changelog_path = Path("CHANGELOG.md")

    if not changelog_path.exists():
        return None

    print_info("Extracting release notes from CHANGELOG.md...")

    try:
        with open(changelog_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Find the section for this version
        start_idx = None
        end_idx = None

        version_pattern = f"## [{version}]"
        alt_version_pattern = f"## {version}"

        for i, line in enumerate(lines):
            if version_pattern in line or alt_version_pattern in line:
                start_idx = i + 1
            elif start_idx is not None and (line.startswith("## [") or line.startswith("## ")):
                end_idx = i
                break

        if start_idx is not None:
            if end_idx is None:
                end_idx = len(lines)

            notes = ''.join(lines[start_idx:end_idx]).strip()
            return notes if notes else None

    except Exception as e:
        print_warning(f"Failed to extract release notes: {e}")

    return None


def create_release(version, draft=False, prerelease=False):
    """Create a GitHub release"""
    tag = f"v{version}"

    print_info(f"Creating GitHub release for version {version}")

    # Check prerequisites
    if not check_gh_installed():
        print_error("GitHub CLI (gh) is not installed. Please install it from https://cli.github.com/")
        sys.exit(1)

    if not check_gh_auth():
        print_error("Not authenticated with GitHub. Please run 'gh auth login' first.")
        sys.exit(1)

    # Validate version
    if not validate_version(version):
        print_error("Invalid version format. Please use semantic versioning (e.g., 2.0.1 or 2.1.0-beta)")
        sys.exit(1)

    # Check if tag exists
    if tag_exists(tag):
        print_error(f"Tag {tag} already exists. Please use a different version or delete the existing tag.")
        sys.exit(1)

    # Check current branch
    current_branch = get_current_branch()
    print_info(f"Current branch: {current_branch}")

    # Check working directory status
    if not is_working_directory_clean():
        print_warning("Working directory is not clean. Please commit or stash changes first.")
        response = input("Do you want to continue anyway? (y/N) ")
        if response.lower() not in ['y', 'yes']:
            sys.exit(1)

    # Build the package
    build_package()

    # Find distribution files
    wheel_file, tarball_file = find_dist_files(version)

    if not wheel_file or not wheel_file.exists() or not tarball_file.exists():
        print_error("Build failed. Distribution files not found in dist/")
        sys.exit(1)

    print_info(f"Build successful: {wheel_file} and {tarball_file}")

    # Extract release notes
    release_notes = extract_release_notes(version)

    if not release_notes:
        print_warning(f"No release notes found in CHANGELOG.md for version {version}")
        release_notes = f"Release {version}\n\nFor detailed changes, please see the [CHANGELOG](CHANGELOG.md)."

    # Create tag
    print_info(f"Creating tag {tag}...")
    run_command(f'git tag -a {tag} -m "Release {version}"')

    # Push tag
    print_info("Pushing tag to remote...")
    run_command(f"git push origin {tag}")

    # Prepare release command
    print_info("Creating GitHub release...")

    release_cmd = [
        "gh", "release", "create", tag,
        "--title", f"Release {version}",
        "--notes", release_notes
    ]

    if draft:
        release_cmd.append("--draft")

    if prerelease:
        release_cmd.append("--prerelease")

    release_cmd.extend([
        f"{wheel_file}#Python Wheel Package",
        f"{tarball_file}#Source Distribution"
    ])

    # Create release
    try:
        subprocess.run(release_cmd, check=True)

        print_info("GitHub release created successfully!")

        # Get release URL
        release_url = run_command(f"gh release view {tag} --json url -q .url", capture_output=True)
        print_info(f"Release URL: {release_url}")

        if draft:
            print_warning("Release created as DRAFT. Remember to publish it when ready.")

        if prerelease:
            print_info("Release marked as pre-release.")

        print()
        print_info("Next steps:")
        print("  1. Verify the release on GitHub")
        print("  2. Consider publishing to PyPI with: python -m twine upload dist/*")

    except subprocess.CalledProcessError:
        print_error("Failed to create GitHub release")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Create a GitHub release for hl7validator-hl7pt",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 2.0.1
  %(prog)s 2.1.0-beta --prerelease
  %(prog)s 2.0.2 --draft
        """
    )

    parser.add_argument(
        "version",
        help="Version number in semantic versioning format (e.g., 2.0.1 or 2.1.0-beta)"
    )
    parser.add_argument(
        "--draft",
        action="store_true",
        help="Create the release as a draft"
    )
    parser.add_argument(
        "--prerelease",
        action="store_true",
        help="Mark the release as a pre-release"
    )

    args = parser.parse_args()

    create_release(args.version, draft=args.draft, prerelease=args.prerelease)


if __name__ == "__main__":
    main()
