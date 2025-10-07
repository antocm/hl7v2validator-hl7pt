@echo off
REM HL7 V2 Validator - Docker Build Script (Windows)
REM This script builds the Docker container for the HL7 V2 Validator application

setlocal enabledelayedexpansion

REM Extract version from pyproject.toml
for /f "tokens=2 delims==" %%a in ('findstr /r "^version" ..\pyproject.toml') do (
    set PACKAGE_VERSION=%%a
)
REM Remove quotes and spaces
set PACKAGE_VERSION=%PACKAGE_VERSION:"=%
set PACKAGE_VERSION=%PACKAGE_VERSION: =%

REM Configuration
set IMAGE_NAME=hl7validator
set IMAGE_TAG=v%PACKAGE_VERSION%
set DOCKERFILE_PATH=docker/Dockerfile
set BUILD_CONTEXT=..
set PLATFORM=linux/amd64
set PUSH=false
set NO_CACHE=false
set VERBOSE=false

REM Parse command line arguments
:parse_args
if "%~1"=="" goto end_parse
if /i "%~1"=="--push" (
    set PUSH=true
    shift
    goto parse_args
)
if /i "%~1"=="--no-cache" (
    set NO_CACHE=true
    shift
    goto parse_args
)
if /i "%~1"=="--tag" (
    set IMAGE_TAG=%~2
    shift
    shift
    goto parse_args
)
if /i "%~1"=="--name" (
    set IMAGE_NAME=%~2
    shift
    shift
    goto parse_args
)
if /i "%~1"=="--platform" (
    set PLATFORM=%~2
    shift
    shift
    goto parse_args
)
if /i "%~1"=="--verbose" (
    set VERBOSE=true
    shift
    goto parse_args
)
if /i "%~1"=="-v" (
    set VERBOSE=true
    shift
    goto parse_args
)
if /i "%~1"=="--help" goto show_help
if /i "%~1"=="-h" goto show_help
echo Unknown option: %~1
echo Use --help for usage information
exit /b 1

:show_help
echo Usage: %~nx0 [OPTIONS]
echo.
echo Options:
echo   --push              Push image to registry after build
echo   --no-cache          Build without using cache
echo   --tag TAG           Image tag (default: v^<package-version^> from pyproject.toml^)
echo   --name NAME         Image name (default: hl7validator^)
echo   --platform PLATFORM Target platform (default: linux/amd64^)
echo   --verbose, -v       Verbose output
echo   --help, -h          Show this help message
echo.
echo Examples:
echo   %~nx0                                    # Build with package version tag (e.g., v1.2.0^)
echo   %~nx0 --tag latest                       # Build with 'latest' tag
echo   %~nx0 --tag v1.0.0                       # Build with specific tag
echo   %~nx0 --no-cache --push                  # Clean build and push
echo   %~nx0 --platform linux/arm64             # Build for ARM64
exit /b 0

:end_parse

REM Print header
echo ========================================
echo HL7 V2 Validator - Docker Build
echo ========================================
echo.

REM Display configuration
echo Configuration:
echo   Package Version: %PACKAGE_VERSION%
echo   Image Name:      %IMAGE_NAME%
echo   Image Tag:       %IMAGE_TAG%
echo   Full Image:      %IMAGE_NAME%:%IMAGE_TAG%
echo   Platform:        %PLATFORM%
echo   Dockerfile:      %DOCKERFILE_PATH%
echo   Build Context:   %BUILD_CONTEXT%
echo   No Cache:        %NO_CACHE%
echo   Push:            %PUSH%
echo.

REM Check prerequisites
echo Checking prerequisites...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not installed
    exit /b 1
)

REM Check Docker daemon is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker daemon is not running
    exit /b 1
)

REM Check if Dockerfile exists
if not exist "%DOCKERFILE_PATH%" (
    echo Error: Dockerfile not found at %DOCKERFILE_PATH%
    exit /b 1
)

REM Check if we're in the correct directory
if not exist "requirements.txt" (
    echo Error: requirements.txt not found. Are you in the project root?
    exit /b 1
)

echo [OK] All prerequisites met
echo.

REM Compile translations before building
echo Compiling translations...
where pybabel >nul 2>&1
if not errorlevel 1 (
    pybabel compile -d hl7validator/translations >nul 2>&1
    echo [OK] Translations compiled
) else (
    echo [WARNING] pybabel not found, skipping translation compilation
    echo           Translations should be pre-compiled in the repository
)
echo.

REM Build wheel package
echo Building wheel package...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    exit /b 1
)

REM Clean previous builds
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
for %%i in (*.egg-info) do if exist "%%i" rmdir /s /q "%%i"

REM Install build tool and build the wheel
python -m pip install --user --upgrade build >nul 2>&1
python -m build --wheel

if not exist "dist\*.whl" (
    echo [ERROR] Wheel build failed
    exit /b 1
)

for %%i in (dist\*.whl) do echo [OK] Wheel package built successfully: %%i
echo.

REM Build Docker image
echo Building Docker image...
echo.

set BUILD_ARGS=--file %DOCKERFILE_PATH%
set BUILD_ARGS=%BUILD_ARGS% --tag %IMAGE_NAME%:%IMAGE_TAG%
set BUILD_ARGS=%BUILD_ARGS% --platform %PLATFORM%

if "%NO_CACHE%"=="true" (
    set BUILD_ARGS=%BUILD_ARGS% --no-cache
)

if "%VERBOSE%"=="true" (
    set BUILD_ARGS=%BUILD_ARGS% --progress=plain
)

REM Add build metadata
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do (
    set BUILD_DATE=%%c-%%a-%%b
)
for /f "tokens=1-2 delims=: " %%a in ('time /t') do (
    set BUILD_TIME=%%a:%%b:00
)

set BUILD_ARGS=%BUILD_ARGS% --label org.opencontainers.image.created=%BUILD_DATE%T%BUILD_TIME%Z
set BUILD_ARGS=%BUILD_ARGS% --label org.opencontainers.image.version=%IMAGE_TAG%
set BUILD_ARGS=%BUILD_ARGS% --label org.opencontainers.image.title="HL7 V2 Validator"
set BUILD_ARGS=%BUILD_ARGS% --label org.opencontainers.image.description="HL7 Version 2 Message Validator and Converter"

REM Execute build
docker build %BUILD_ARGS% %BUILD_CONTEXT%
if errorlevel 1 (
    echo.
    echo ========================================
    echo [ERROR] Build failed!
    echo ========================================
    exit /b 1
)

echo.
echo ========================================
echo [OK] Build successful!
echo ========================================
echo.
echo Image built: %IMAGE_NAME%:%IMAGE_TAG%

REM Show image details
echo.
echo Image details:
docker images %IMAGE_NAME%:%IMAGE_TAG%

REM Push to registry if requested
if "%PUSH%"=="true" (
    echo.
    echo Pushing image to registry...
    docker push %IMAGE_NAME%:%IMAGE_TAG%
    if errorlevel 1 (
        echo [ERROR] Push failed
        exit /b 1
    )
    echo [OK] Push successful
)

REM Display next steps
echo.
echo ========================================
echo Next steps:
echo ========================================
echo.
echo Run the container:
echo   docker run -p 80:80 %IMAGE_NAME%:%IMAGE_TAG%
echo.
echo Run with custom port:
echo   docker run -p 8080:80 %IMAGE_NAME%:%IMAGE_TAG%
echo.
echo Run with environment variables:
echo   docker run -p 80:80 -e SECRET_KEY=your-secret-key %IMAGE_NAME%:%IMAGE_TAG%
echo.
echo Run in background:
echo   docker run -d -p 80:80 --name hl7validator %IMAGE_NAME%:%IMAGE_TAG%
echo.
echo View logs:
echo   docker logs hl7validator
echo.
echo Stop container:
echo   docker stop hl7validator
echo.

endlocal
