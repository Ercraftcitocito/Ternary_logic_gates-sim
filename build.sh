#!/bin/bash
# Build script for Ternary Logic Gate Simulator

set -e

echo "╔════════════════════════════════════╗"
echo "║  Ternary Logic Gate Simulator      ║"
echo "║  Cross-Platform Build Script       ║"
echo "╚════════════════════════════════════╝"
echo ""

# Check if Rust is installed
if ! command -v cargo &> /dev/null; then
    echo "❌ Rust is not installed"
    echo "Please install Rust from https://www.rust-lang.org/tools/install"
    exit 1
fi

echo "✓ Rust found: $(rustc --version)"
echo ""

# Clean previous builds
if [ "$1" = "clean" ]; then
    echo "🧹 Cleaning previous builds..."
    cargo clean
    echo "✓ Clean complete"
    echo ""
fi

# Run tests
if [ "$1" != "no-test" ]; then
    echo "🧪 Running tests..."
    cargo test --lib
    echo "✓ Tests passed"
    echo ""
fi

# Build
echo "🔨 Building release binary..."
cargo build --release

echo ""
echo "╔════════════════════════════════════╗"
echo "║  Build Successful!                 ║"
echo "╚════════════════════════════════════╝"
echo ""

# Determine binary name
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    BIN="target/release/ternary-logic-sim.exe"
else
    BIN="target/release/ternary-logic-sim"
fi

echo "Binary location: $BIN"
echo ""
echo "To run the simulator:"
echo "  cargo run --release"
echo "  or"
echo "  $BIN"
echo ""

# Ask if user wants to run
read -p "Run simulator now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    cargo run --release
fi
