@echo off
REM Build script for Ternary Logic Gate Simulator (Windows)

echo.
echo ╔════════════════════════════════════╗
echo ║  Ternary Logic Gate Simulator      ║
echo ║  Windows Build Script              ║
echo ╚════════════════════════════════════╝
echo.

REM Check if Rust is installed
where cargo >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Rust is not installed
    echo Please install Rust from https://www.rust-lang.org/tools/install
    pause
    exit /b 1
)

REM Get Rust version
for /f "tokens=*" %%i in ('rustc --version') do set RUST_VERSION=%%i
echo ✓ %RUST_VERSION%
echo.

REM Clean if requested
if "%1"=="clean" (
    echo 🧹 Cleaning previous builds...
    cargo clean
    if %errorlevel% neq 0 (
        echo ❌ Clean failed
        pause
        exit /b 1
    )
    echo ✓ Clean complete
    echo.
)

REM Run tests unless no-test flag
if not "%1"=="no-test" (
    echo 🧪 Running tests...
    cargo test --lib
    if %errorlevel% neq 0 (
        echo ❌ Tests failed
        pause
        exit /b 1
    )
    echo ✓ Tests passed
    echo.
)

REM Build
echo 🔨 Building release binary...
cargo build --release
if %errorlevel% neq 0 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════╗
echo ║  Build Successful!                 ║
echo ╚════════════════════════════════════╝
echo.

echo Binary location: target\release\ternary-logic-sim.exe
echo.
echo To run the simulator:
echo   cargo run --release
echo   or
echo   target\release\ternary-logic-sim.exe
echo.

set /p RUN="Run simulator now? (y/n) "
if /i "%RUN%"=="y" (
    cargo run --release
)

pause
