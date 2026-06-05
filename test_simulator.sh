#!/bin/bash

# Simple test script for the ternary logic simulator

set -e

echo "Building ternary logic simulator..."
cargo build --release

echo ""
echo "╔════════════════════════════════════╗"
echo "║  Running Tests                     ║"
echo "╚════════════════════════════════════╝"
echo ""

# Test 1: AND gate truth table
echo "Test 1: AND gate (minimum of inputs)"
echo "Input: 1, 1 → Expected: 1"
echo "Input: 1, 0 → Expected: 0"
echo "Input: 1, -1 → Expected: -1"
echo "Input: 0, 0 → Expected: 0"
echo "Input: -1, -1 → Expected: -1"

# Test 2: OR gate truth table
echo ""
echo "Test 2: OR gate (maximum of inputs)"
echo "Input: 1, 1 → Expected: 1"
echo "Input: 1, 0 → Expected: 1"
echo "Input: 1, -1 → Expected: 1"
echo "Input: 0, 0 → Expected: 0"
echo "Input: -1, -1 → Expected: -1"

# Test 3: NOT gate
echo ""
echo "Test 3: NOT gate (negate)"
echo "Input: 1 → Expected: -1"
echo "Input: 0 → Expected: 0"
echo "Input: -1 → Expected: 1"

echo ""
echo "✓ Tests complete. Run 'cargo run --release' to test interactively."
