#!/bin/bash

# Script to create a GitHub release for hl7validator-hl7pt
# This script uses the GitHub CLI (gh) to create releases
# Usage: ./scripts/create_release.sh <version> [--draft] [--prerelease]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    print_error "GitHub CLI (gh) is not installed. Please install it from https://cli.github.com/"
    exit 1
fi

# Check if user is authenticated with GitHub
if ! gh auth status &> /dev/null; then
    print_error "Not authenticated with GitHub. Please run 'gh auth login' first."
    exit 1
fi

# Parse arguments
VERSION=""
DRAFT_FLAG=""
PRERELEASE_FLAG=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --draft)
            DRAFT_FLAG="--draft"
            shift
            ;;
        --prerelease)
            PRERELEASE_FLAG="--prerelease"
            shift
            ;;
        *)
            if [[ -z "$VERSION" ]]; then
                VERSION="$1"
            else
                print_error "Unknown argument: $1"
                exit 1
            fi
            shift
            ;;
    esac
done

# Check if version is provided
if [[ -z "$VERSION" ]]; then
    print_error "Version is required."
    echo "Usage: $0 <version> [--draft] [--prerelease]"
    echo "Example: $0 2.0.1"
    echo "Example: $0 2.1.0-beta --prerelease"
    exit 1
fi

# Validate version format (semver)
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9\.]+)?$ ]]; then
    print_error "Invalid version format. Please use semantic versioning (e.g., 2.0.1 or 2.1.0-beta)"
    exit 1
fi

TAG="v$VERSION"

print_info "Creating GitHub release for version $VERSION"

# Check if tag already exists
if git rev-parse "$TAG" >/dev/null 2>&1; then
    print_error "Tag $TAG already exists. Please use a different version or delete the existing tag."
    exit 1
fi

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
print_info "Current branch: $CURRENT_BRANCH"

# Check if working directory is clean
if [[ -n $(git status --porcelain) ]]; then
    print_warning "Working directory is not clean. Please commit or stash changes first."
    read -p "Do you want to continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Build the package
print_info "Building the package..."
python -m pip install --upgrade build
python -m build

# Check if dist files were created
WHEEL_FILE=$(ls -t dist/hl7validator_hl7pt-${VERSION}-*.whl 2>/dev/null | head -1)
TARBALL_FILE=$(ls -t dist/hl7validator-hl7pt-${VERSION}.tar.gz 2>/dev/null | head -1)

if [[ ! -f "$WHEEL_FILE" ]] || [[ ! -f "$TARBALL_FILE" ]]; then
    print_error "Build failed. Distribution files not found in dist/"
    exit 1
fi

print_info "Build successful: $WHEEL_FILE and $TARBALL_FILE"

# Extract release notes from CHANGELOG.md if it exists
RELEASE_NOTES=""
if [[ -f "CHANGELOG.md" ]]; then
    print_info "Extracting release notes from CHANGELOG.md..."
    # Try to extract the section for this version
    RELEASE_NOTES=$(awk "/## \[${VERSION}\]|## ${VERSION}/,/## \[|## [0-9]/" CHANGELOG.md | sed '1d;$d' | sed '/^$/d' || true)
fi

# If no release notes found in CHANGELOG, use a default message
if [[ -z "$RELEASE_NOTES" ]]; then
    print_warning "No release notes found in CHANGELOG.md for version $VERSION"
    RELEASE_NOTES="Release $VERSION

For detailed changes, please see the [CHANGELOG](CHANGELOG.md)."
fi

# Create the tag
print_info "Creating tag $TAG..."
git tag -a "$TAG" -m "Release $VERSION"

# Push the tag
print_info "Pushing tag to remote..."
git push origin "$TAG"

# Create the GitHub release
print_info "Creating GitHub release..."

RELEASE_CMD="gh release create $TAG \
    --title \"Release $VERSION\" \
    --notes \"$RELEASE_NOTES\" \
    $DRAFT_FLAG \
    $PRERELEASE_FLAG \
    \"$WHEEL_FILE#Python Wheel Package\" \
    \"$TARBALL_FILE#Source Distribution\""

eval $RELEASE_CMD

if [[ $? -eq 0 ]]; then
    print_info "GitHub release created successfully!"
    print_info "Release URL: $(gh release view $TAG --json url -q .url)"

    if [[ -n "$DRAFT_FLAG" ]]; then
        print_warning "Release created as DRAFT. Remember to publish it when ready."
    fi

    if [[ -n "$PRERELEASE_FLAG" ]]; then
        print_info "Release marked as pre-release."
    fi

    echo ""
    print_info "Next steps:"
    echo "  1. Verify the release on GitHub"
    echo "  2. Consider publishing to PyPI with: python -m twine upload dist/*"
else
    print_error "Failed to create GitHub release"
    exit 1
fi
