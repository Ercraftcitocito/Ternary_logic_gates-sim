# Building and Running the Ternary Logic Simulator

This guide provides instructions for building and running the simulator on Windows, Linux, and macOS.

## Prerequisites

All platforms require:
- **Rust**: Version 1.70 or later
- **Cargo**: Included with Rust

### Installing Rust

#### Windows
1. Download the installer from https://www.rust-lang.org/tools/install
2. Run the installer and follow the prompts
3. Restart your terminal/command prompt

#### Linux (Ubuntu/Debian)
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

#### Linux (Fedora/RHEL)
```bash
dnf install -y rust cargo
```

#### macOS
```bash
brew install rust
```

Or using Rustup:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## Building the Project

### Step 1: Clone or Navigate to Repository
```bash
cd Ternary_logic_gates-sim
```

### Step 2: Build Release Version
```bash
cargo build --release
```

This creates an optimized binary in `target/release/`.

### Step 3: Run the Simulator

#### Windows
```cmd
target\release\ternary-logic-sim.exe
```

#### Linux/macOS
```bash
./target/release/ternary-logic-sim
```

Alternatively, use `cargo`:
```bash
cargo run --release
```

## Alternative: Debug Build

For development or debugging:

```bash
cargo build
cargo run
```

This creates an unoptimized binary in `target/debug/`.
Debug builds compile faster but run slower.

## Running Tests

To verify everything works correctly:

```bash
cargo test --lib
```

You should see output like:
```
running 4 tests
test tests::test_and_gate ... ok
test tests::test_not_gate ... ok
test tests::test_circuit ... ok
test tests::test_or_gate ... ok

test result: ok. 4 passed; 0 failed
```

## Project Structure After Building

```
Ternary_logic_gates-sim/
├── target/
│   ├── release/
│   │   ├── ternary-logic-sim (Linux/macOS executable)
│   │   └── ternary-logic-sim.exe (Windows executable)
│   └── debug/
│       └── ternary-logic-sim (unoptimized)
├── src/
│   ├── lib.rs
│   └── main.rs
├── Cargo.toml
└── README.md
```

## Troubleshooting

### "Command not found: cargo"
- Ensure Rust is installed correctly
- Restart your terminal after installation
- Check that `~/.cargo/bin` is in your PATH

### Compilation errors
- Ensure Rust 1.70+ is installed: `rustc --version`
- Update Rust: `rustup update`
- Clean build: `cargo clean && cargo build --release`

### "No such file or directory"
- Verify you're in the correct directory
- Use absolute paths if needed

## Creating Executable Shortcuts

### Windows
Create a file `run-simulator.bat`:
```batch
@echo off
target\release\ternary-logic-sim.exe
pause
```

### Linux/macOS
Create a file `run-simulator.sh`:
```bash
#!/bin/bash
./target/release/ternary-logic-sim
```

Then make it executable:
```bash
chmod +x run-simulator.sh
./run-simulator.sh
```

## Performance

- **Release build** (recommended): ~1-2 MB executable, optimal performance
- **Debug build**: ~5-10 MB executable, slower execution

For regular use, always use release builds.

## Next Steps

After building:
1. Read [README.md](README.md) for features overview
2. Check [EXAMPLES.md](EXAMPLES.md) for usage examples
3. Run with `cargo run --release` and explore the interactive menu
