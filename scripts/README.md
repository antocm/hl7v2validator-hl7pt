# Release Scripts

This directory contains scripts to help with creating GitHub releases for hl7validator-hl7pt.

## Prerequisites

1. **GitHub CLI (gh)**: Install from [https://cli.github.com/](https://cli.github.com/)
2. **Authentication**: Run `gh auth login` to authenticate with GitHub
3. **Python Build Tools**: Install with `pip install build twine`

## Scripts

### create_release.sh (Bash)

A Bash script for creating GitHub releases on Unix-like systems (Linux, macOS).

**Usage:**
```bash
./scripts/create_release.sh <version> [--draft] [--prerelease]
```

**Examples:**
```bash
# Create a regular release
./scripts/create_release.sh 2.0.1

# Create a pre-release
./scripts/create_release.sh 2.1.0-beta --prerelease

# Create a draft release
./scripts/create_release.sh 2.0.2 --draft

# Create a draft pre-release
./scripts/create_release.sh 2.1.0-rc1 --draft --prerelease
```

### create_release.py (Python)

A Python script for creating GitHub releases, works cross-platform (Linux, macOS, Windows).

**Usage:**
```bash
python scripts/create_release.py <version> [--draft] [--prerelease]
```

**Examples:**
```bash
# Create a regular release
python scripts/create_release.py 2.0.1

# Create a pre-release
python scripts/create_release.py 2.1.0-beta --prerelease

# Create a draft release
python scripts/create_release.py 2.0.2 --draft

# Create a draft pre-release
python scripts/create_release.py 2.1.0-rc1 --draft --prerelease
```

## What the Scripts Do

1. **Validate version format**: Ensures the version follows semantic versioning (e.g., 2.0.1 or 2.1.0-beta)
2. **Check prerequisites**: Verifies that GitHub CLI is installed and authenticated
3. **Check for existing tags**: Ensures the version tag doesn't already exist
4. **Build the package**: Runs `python -m build` to create wheel and source distributions
5. **Extract release notes**: Attempts to extract release notes from CHANGELOG.md for the specified version
6. **Create and push git tag**: Creates an annotated tag (e.g., v2.0.1) and pushes it to the remote repository
7. **Create GitHub release**: Uses `gh release create` to create the release with:
   - Release title
   - Release notes (from CHANGELOG.md or default message)
   - Attached distribution files (wheel and tarball)
   - Draft/prerelease flags if specified

## Version Format

The scripts expect semantic versioning format:
- **Regular releases**: `X.Y.Z` (e.g., 2.0.1, 2.1.0)
- **Pre-releases**: `X.Y.Z-LABEL` (e.g., 2.1.0-beta, 2.0.0-rc1, 2.1.0-alpha.1)

## Release Notes

The scripts automatically extract release notes from `CHANGELOG.md` if available. The CHANGELOG should follow this format:

```markdown
## [2.0.1] - 2025-12-03

### Fixed
- Bug fix description

### Added
- New feature description

## [2.0.0] - 2025-11-15
...
```

If no release notes are found, a default message will be used.

## Workflow

### Creating a Regular Release

1. Update the version in `pyproject.toml`
2. Update `CHANGELOG.md` with the changes for this version
3. Commit the changes:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "Prepare release 2.0.1"
   git push
   ```
4. Run the release script:
   ```bash
   ./scripts/create_release.sh 2.0.1
   # or
   python scripts/create_release.py 2.0.1
   ```
5. Verify the release on GitHub
6. (Optional) Publish to PyPI:
   ```bash
   python -m twine upload dist/*
   ```

### Creating a Pre-release

Pre-releases are useful for beta versions, release candidates, etc.

1. Follow the same steps as above, but use the `--prerelease` flag:
   ```bash
   ./scripts/create_release.sh 2.1.0-beta --prerelease
   ```

### Creating a Draft Release

Draft releases are not visible to the public until published.

1. Use the `--draft` flag:
   ```bash
   ./scripts/create_release.sh 2.0.2 --draft
   ```
2. Edit and publish the draft on GitHub when ready

## Troubleshooting

### "gh: command not found"
Install GitHub CLI from [https://cli.github.com/](https://cli.github.com/)

### "Not authenticated with GitHub"
Run `gh auth login` and follow the prompts

### "Tag already exists"
If you need to recreate a release:
```bash
# Delete local tag
git tag -d v2.0.1

# Delete remote tag
git push origin :refs/tags/v2.0.1

# Delete the GitHub release
gh release delete v2.0.1
```

### "Build failed"
Ensure build tools are installed:
```bash
pip install --upgrade build
```

### "Working directory is not clean"
Commit or stash your changes before creating a release:
```bash
git status
git add .
git commit -m "Your changes"
```

## Notes

- The scripts will create a git tag in the format `vX.Y.Z` (e.g., `v2.0.1`)
- Distribution files are automatically attached to the GitHub release
- The scripts check for a clean working directory but can proceed if you confirm
- Both scripts produce identical results - choose based on your preference
