#!/bin/bash

# HL7 V2 Validator - Docker Build Script (Linux/Mac)
# This script builds the Docker container for the HL7 V2 Validator application

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Extract version from pyproject.toml
PACKAGE_VERSION=$(grep -E '^version = ' "$PROJECT_ROOT/pyproject.toml" | sed -E 's/version = "(.*)"/\1/')

# Configuration
IMAGE_NAME="${IMAGE_NAME:-hl7validator}"
IMAGE_TAG="${IMAGE_TAG:-v$PACKAGE_VERSION}"  # Default to package version
DOCKERFILE_PATH="$SCRIPT_DIR/Dockerfile"
BUILD_CONTEXT="$PROJECT_ROOT"
PLATFORM="${PLATFORM:-linux/amd64}"

# Parse command line arguments
PUSH=false
NO_CACHE=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --push)
            PUSH=true
            shift
            ;;
        --no-cache)
            NO_CACHE=true
            shift
            ;;
        --tag)
            IMAGE_TAG="$2"
            shift 2
            ;;
        --name)
            IMAGE_NAME="$2"
            shift 2
            ;;
        --platform)
            PLATFORM="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --push              Push image to registry after build"
            echo "  --no-cache          Build without using cache"
            echo "  --tag TAG           Image tag (default: v<package-version> from pyproject.toml)"
            echo "  --name NAME         Image name (default: hl7validator)"
            echo "  --platform PLATFORM Target platform (default: linux/amd64)"
            echo "  --verbose, -v       Verbose output"
            echo "  --help, -h          Show this help message"
            echo ""
            echo "Environment variables:"
            echo "  IMAGE_NAME          Override default image name"
            echo "  IMAGE_TAG           Override default image tag"
            echo "  PLATFORM            Override default platform"
            echo ""
            echo "Examples:"
            echo "  $0                                    # Build with package version tag (e.g., v1.2.0)"
            echo "  $0 --tag latest                       # Build with 'latest' tag"
            echo "  $0 --tag v1.0.0                       # Build with specific tag"
            echo "  $0 --no-cache --push                  # Clean build and push"
            echo "  $0 --platform linux/arm64             # Build for ARM64"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Print header
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}HL7 V2 Validator - Docker Build${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Display configuration
echo -e "${GREEN}Configuration:${NC}"
echo "  Package Version: $PACKAGE_VERSION"
echo "  Image Name:      $IMAGE_NAME"
echo "  Image Tag:       $IMAGE_TAG"
echo "  Full Image:      $IMAGE_NAME:$IMAGE_TAG"
echo "  Platform:        $PLATFORM"
echo "  Dockerfile:      $DOCKERFILE_PATH"
echo "  Build Context:   $BUILD_CONTEXT"
echo "  No Cache:        $NO_CACHE"
echo "  Push:            $PUSH"
echo ""

# Check prerequisites
echo -e "${GREEN}Checking prerequisites...${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    exit 1
fi

# Check Docker daemon is running
if ! docker info &> /dev/null; then
    echo -e "${RED}Error: Docker daemon is not running${NC}"
    exit 1
fi

# Check if Dockerfile exists
if [ ! -f "$DOCKERFILE_PATH" ]; then
    echo -e "${RED}Error: Dockerfile not found at $DOCKERFILE_PATH${NC}"
    exit 1
fi

# Check if we're in the correct directory
if [ ! -f "../requirements.txt" ]; then
    echo -e "${RED}Error: requirements.txt not found. Are you in the docker directory?${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites met${NC}"
echo ""

# Compile translations before building
echo -e "${GREEN}Compiling translations...${NC}"
if command -v pybabel &> /dev/null; then
    (cd "$PROJECT_ROOT" && pybabel compile -d hl7validator/translations 2>/dev/null) || true
    echo -e "${GREEN}✓ Translations compiled${NC}"
else
    echo -e "${YELLOW}⚠ pybabel not found, skipping translation compilation${NC}"
    echo -e "${YELLOW}  Translations should be pre-compiled in the repository${NC}"
fi
echo ""

# Build wheel package
echo -e "${GREEN}Building wheel package...${NC}"
if command -v python3 &> /dev/null; then
    # Clean previous builds
    rm -rf "$PROJECT_ROOT/dist" "$PROJECT_ROOT/build" "$PROJECT_ROOT"/*.egg-info

    # Build the wheel
    (cd "$PROJECT_ROOT" && python3 -m pip install --user --upgrade build 2>/dev/null || true)
    (cd "$PROJECT_ROOT" && python3 -m build --wheel 2>&1)

    if [ -d "$PROJECT_ROOT/dist" ] && [ -n "$(ls -A $PROJECT_ROOT/dist/*.whl 2>/dev/null)" ]; then
        echo -e "${GREEN}✓ Wheel package built successfully${NC}"
        echo -e "${GREEN}  Package: $(ls $PROJECT_ROOT/dist/*.whl)${NC}"
    else
        echo -e "${RED}✗ Wheel build failed${NC}"
        exit 1
    fi
else
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi
echo ""

# Build Docker image
echo -e "${GREEN}Building Docker image...${NC}"
echo ""

BUILD_ARGS=()
BUILD_ARGS+=(--file "$DOCKERFILE_PATH")
BUILD_ARGS+=(--tag "$IMAGE_NAME:$IMAGE_TAG")
BUILD_ARGS+=(--platform "$PLATFORM")

if [ "$NO_CACHE" = true ]; then
    BUILD_ARGS+=(--no-cache)
fi

if [ "$VERBOSE" = true ]; then
    BUILD_ARGS+=(--progress=plain)
fi

# Add build metadata
BUILD_ARGS+=(--label "org.opencontainers.image.created=$(date -u +'%Y-%m-%dT%H:%M:%SZ')")
BUILD_ARGS+=(--label "org.opencontainers.image.version=$IMAGE_TAG")
BUILD_ARGS+=(--label "org.opencontainers.image.title=HL7 V2 Validator")
BUILD_ARGS+=(--label "org.opencontainers.image.description=HL7 Version 2 Message Validator and Converter")

# Execute build
if docker build "${BUILD_ARGS[@]}" "$BUILD_CONTEXT"; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ Build successful!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${GREEN}Image built: $IMAGE_NAME:$IMAGE_TAG${NC}"
else
    echo ""
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}✗ Build failed!${NC}"
    echo -e "${RED}========================================${NC}"
    exit 1
fi

# Show image details
echo ""
echo -e "${GREEN}Image details:${NC}"
docker images $IMAGE_NAME:$IMAGE_TAG

# Push to registry if requested
if [ "$PUSH" = true ]; then
    echo ""
    echo -e "${GREEN}Pushing image to registry...${NC}"
    if docker push $IMAGE_NAME:$IMAGE_TAG; then
        echo -e "${GREEN}✓ Push successful${NC}"
    else
        echo -e "${RED}✗ Push failed${NC}"
        exit 1
    fi
fi

# Display next steps
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Next steps:${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Run the container:"
echo "  docker run -p 80:80 $IMAGE_NAME:$IMAGE_TAG"
echo ""
echo "Run with custom port:"
echo "  docker run -p 8080:80 $IMAGE_NAME:$IMAGE_TAG"
echo ""
echo "Run with environment variables:"
echo "  docker run -p 80:80 -e SECRET_KEY=your-secret-key $IMAGE_NAME:$IMAGE_TAG"
echo ""
echo "Run in background:"
echo "  docker run -d -p 80:80 --name hl7validator $IMAGE_NAME:$IMAGE_TAG"
echo ""
echo "View logs:"
echo "  docker logs hl7validator"
echo ""
echo "Stop container:"
echo "  docker stop hl7validator"
echo ""
