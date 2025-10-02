@echo off
REM HL7 V2 Validator - Local Development Run Script (Windows)
REM This script sets up and runs the Flask application for local development

setlocal enabledelayedexpansion

REM Configuration
set VENV_DIR=.venv
set PYTHON_CMD=python
set HOST=127.0.0.1
set PORT=5000
set DEBUG=true
set SKIP_INSTALL=false
set USE_GUNICORN=false

REM Parse command line arguments
:parse_args
if "%~1"=="" goto end_parse
if /i "%~1"=="--skip-install" (
    set SKIP_INSTALL=true
    shift
    goto parse_args
)
if /i "%~1"=="--gunicorn" (
    set USE_GUNICORN=true
    shift
    goto parse_args
)
if /i "%~1"=="--port" (
    set PORT=%~2
    shift
    shift
    goto parse_args
)
if /i "%~1"=="--host" (
    set HOST=%~2
    shift
    shift
    goto parse_args
)
if /i "%~1"=="--prod" (
    set DEBUG=false
    set USE_GUNICORN=true
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
echo   --skip-install      Skip dependency installation
echo   --gunicorn          Use gunicorn instead of Flask dev server
echo   --port PORT         Port to run on (default: 5000^)
echo   --host HOST         Host to bind to (default: 127.0.0.1^)
echo   --prod              Production mode (debug off, use gunicorn^)
echo   --help, -h          Show this help message
echo.
echo Environment variables:
echo   VENV_DIR            Virtual environment directory (default: .venv^)
echo   PYTHON_CMD          Python command (default: python^)
echo   HOST                Host to bind (default: 127.0.0.1^)
echo   PORT                Port to use (default: 5000^)
echo   DEBUG               Enable debug mode (default: true^)
echo   SECRET_KEY          Flask secret key (generated if not set^)
echo.
echo Examples:
echo   %~nx0                          # Development mode
echo   %~nx0 --port 8000              # Run on port 8000
echo   %~nx0 --gunicorn               # Use gunicorn
echo   %~nx0 --prod                   # Production mode
exit /b 0

:end_parse

REM Print header
echo ========================================
echo HL7 V2 Validator - Local Setup
echo ========================================
echo.

REM Check prerequisites
echo Checking prerequisites...

REM Check if Python is installed
%PYTHON_CMD% --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('%PYTHON_CMD% --version 2^>^&1') do set PYTHON_VERSION=%%i
echo   Python version: %PYTHON_VERSION%

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo Error: requirements.txt not found
    echo Are you in the project root directory?
    exit /b 1
)

echo [OK] Prerequisites met
echo.

REM Setup virtual environment
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv %VENV_DIR%
    echo [OK] Virtual environment created
) else (
    echo [WARNING] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call %VENV_DIR%\Scripts\activate.bat

REM Install dependencies
if "%SKIP_INSTALL%"=="false" (
    echo Installing dependencies...
    python -m pip install --upgrade pip -q
    pip install -r requirements.txt -q
    echo [OK] Dependencies installed
) else (
    echo [WARNING] Skipping dependency installation
)
echo.

REM Compile translations
echo Compiling translations...
where pybabel >nul 2>&1
if not errorlevel 1 (
    pybabel compile -d hl7validator/translations >nul 2>&1
    echo [OK] Translations compiled
) else (
    echo [WARNING] pybabel not found, skipping translation compilation
)
echo.

REM Set environment variables
set FLASK_APP=run.py
set FLASK_DEBUG=%DEBUG%

if "%SECRET_KEY%"=="" (
    set SECRET_KEY=dev-secret-key-%RANDOM%%RANDOM%
    echo [WARNING] Using generated SECRET_KEY for development
    echo           For production, set SECRET_KEY environment variable
) else (
    echo [OK] Using provided SECRET_KEY
)
echo.

REM Display configuration
echo Configuration:
echo   Host:        %HOST%
echo   Port:        %PORT%
echo   Debug:       %DEBUG%
if "%USE_GUNICORN%"=="true" (
    echo   Server:      Gunicorn
) else (
    echo   Server:      Flask Dev Server
)
echo   Venv:        %VENV_DIR%
echo.

REM Run application
echo ========================================
echo Starting Application
echo ========================================
echo.

if "%USE_GUNICORN%"=="true" (
    echo Using Gunicorn...
    echo.
    gunicorn run:app ^
        --bind %HOST%:%PORT% ^
        --workers 2 ^
        --threads 2 ^
        --access-logfile - ^
        --error-logfile - ^
        --log-level info ^
        --reload
) else (
    echo Using Flask development server...
    echo.
    echo Application will be available at:
    echo   http://%HOST%:%PORT%
    echo.
    echo Press CTRL+C to stop
    echo.
    flask run --host=%HOST% --port=%PORT%
)

endlocal
