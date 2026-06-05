# Ternary Logic Gate Simulator

A cross-platform simulator for symmetric ternary logic gates using values: **-1, 0, 1**

## Features

- **Ternary Logic Gates** supporting symmetric values (-1, 0, 1)
  - **AND**: Minimum of inputs
  - **OR**: Maximum of inputs
  - **XOR**: Sum modulo 3, mapped to {-1, 0, 1}
  - **NOT**: Negates the input
  - **MIN**: Returns the minimum value
  - **MAX**: Returns the maximum value
  - **SUM**: Sums inputs, clamped to {-1, 0, 1}

- **Circuit Building**: Add multiple gates sequentially
- **Simulation**: Set input values and evaluate the circuit
- **Cross-Platform**: Runs on Windows, Linux, and macOS (CLI)

## Building

### Requirements
- Rust 1.70+
- Cargo

### Compile

```bash
cargo build --release
```

The compiled binary will be at:
- `target/release/ternary-logic-sim` (Linux/macOS)
- `target/release/ternary-logic-sim.exe` (Windows)

## Running

```bash
cargo run --release
```

Or execute the binary directly:

```bash
./target/release/ternary-logic-sim
```

## Usage

The simulator provides an interactive CLI menu:

1. **Add Gate**: Choose a gate type and add it to the circuit
2. **Simulate**: Set input values (A, B, C) and evaluate
3. **View Circuit**: Display current circuit configuration
4. **Clear Circuit**: Reset and start over
5. **Exit**: Quit the program

### Example Session

```
1) Add gate
  - Select AND gate
  
2) Add gate
  - Select OR gate
  
3) Simulate
  - Input A: 1
  - Input B: 0
  - Input C: -1
  - Outputs are displayed
  
4) View circuit
  - Shows all gates in the circuit
```

## Gate Definitions

For inputs **x, y, z** with values in **{-1, 0, 1}**:

| Gate | Operation | Example |
|------|-----------|---------|
| AND  | min(x, y) | AND(1, -1) = -1 |
| OR   | max(x, y) | OR(1, -1) = 1 |
| XOR  | sum mod 3 | XOR(1, 1) = -1 |
| NOT  | -x | NOT(1) = -1 |
| MIN  | minimum | MIN(1, 0, -1) = -1 |
| MAX  | maximum | MAX(1, 0, -1) = 1 |
| SUM  | clamp(sum) | SUM(1, 1) = 1, SUM(1, 1, 1) = 1 |

## Project Structure

```
Ternary_logic_gates-sim/
├── src/
│   ├── lib.rs          # Gate logic and circuit implementation
│   └── main.rs         # CLI interface
├── Cargo.toml          # Project manifest
└── README.md           # This file
```

## Ternary Logic

This project implements symmetric ternary logic (also known as balanced ternary):
- **-1**: False/Low/Negative
- **0**: Unknown/Neutral/Zero
- **1**: True/High/Positive

## Requirements

- **Rust**: 1.70 or later
- **Cargo**: Latest version

No external GUI dependencies for the CLI version.

## License

MIT License

## Author

Copilot Code Assistant
