# Quick Start Guide

Get up and running with the Ternary Logic Gate Simulator in 5 minutes!

## 1. Install Rust (if not already installed)

**Windows**: Download from https://www.rust-lang.org/tools/install

**Linux/macOS**: 
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## 2. Clone and Build

```bash
cd Ternary_logic_gates-sim
cargo build --release
```

## 3. Run the Simulator

```bash
cargo run --release
```

## 4. Try Your First Circuit

```
Menu appears → Select: 1 (Add gate)
             → Choose: 1 (AND)
             → Select: 2 (Simulate)
             → Enter A: 1
             → Enter B: 1  
             → Enter C: 0
             → Result: Output 1: 0 (because first gate outputs 0)
```

## What Just Happened?

- ✓ Added an AND gate to your circuit
- ✓ Simulated with inputs A=1, B=1, C=0
- ✓ AND(1, 1) = 1 (minimum of inputs)

## Next Steps

Try these:

1. **Add More Gates**:
   - Add an OR gate (option 1 → 2)
   - Now you have 2 gates processing independently

2. **Try Different Values**:
   - Use -1, 0, 1 for inputs
   - See how each gate responds

3. **Experiment with Gate Types**:
   - AND: minimum
   - OR: maximum
   - XOR: sum mod 3
   - NOT: negate value
   - MIN/MAX: explicit operations
   - SUM: sum clamped to range

## Understanding Output

After simulation, you see:
```
┌─ Results ──────────────────────┐
│ Input:  A=X  B=Y  C=Z       │
├────────────────────────────────┤
│ Output 1: result                │
│ Output 2: result                │
│ ...
└────────────────────────────────┘
```

- Each output represents one gate you added
- Gates operate independently on the same inputs
- Output values are always in {-1, 0, 1}

## Common Commands

| Menu Option | Action |
|------------|--------|
| 1 | Add a new gate |
| 2 | Simulate circuit |
| 3 | View circuit status |
| 4 | Clear all gates |
| 5 | Exit program |

## Gate Reference

| Gate | Operation | Example |
|------|-----------|---------|
| AND | min(A, B) | AND(1, -1) = -1 |
| OR | max(A, B) | OR(1, -1) = 1 |
| XOR | sum mod 3 | XOR(1, 1) = -1 |
| NOT | -A | NOT(1) = -1 |
| MIN | minimum | MIN(1, 0, -1) = -1 |
| MAX | maximum | MAX(1, 0, -1) = 1 |
| SUM | clamp(sum) | SUM(1, 1) = 1 |

## Truth Table Quick Reference

### AND (minimum)
```
1 AND 1 = 1    1 AND 0 = 0    1 AND -1 = -1
0 AND 0 = 0    0 AND -1 = -1  -1 AND -1 = -1
```

### OR (maximum)
```
1 OR 1 = 1     1 OR 0 = 1     1 OR -1 = 1
0 OR 0 = 0     0 OR -1 = 0    -1 OR -1 = -1
```

### NOT
```
NOT(1) = -1    NOT(0) = 0     NOT(-1) = 1
```

## Tips & Tricks

1. **Start Simple**: Add one gate, test it with known values
2. **Use Menu 3**: View what gates you've added before simulating
3. **Input Values**: Always use -1, 0, or 1 (other values become 0)
4. **Clear Often**: Use option 4 to start fresh with new circuits
5. **Experiment**: Try all gate combinations!

## Troubleshooting

**Program won't start?**
- Ensure Rust is installed: `rustc --version`
- Make sure you're in the project directory

**Build fails?**
- Update Rust: `rustup update`
- Clean and rebuild: `cargo clean && cargo build --release`

**Unexpected output?**
- Check that inputs are exactly -1, 0, or 1
- Review the gate type (use menu 3 to confirm)

## Learn More

- **EXAMPLES.md**: Detailed usage examples
- **BUILDING.md**: Building on different platforms
- **TERNARY_LOGIC.md**: Theory behind ternary logic
- **README.md**: Full feature documentation

## Advanced: Building Complex Circuits

1. Plan your circuit on paper
2. Add gates one by one in order
3. Test after each addition
4. Use the same inputs for all gates
5. Each gate operates independently

Example: To create multiple outputs:
```
Gate 1: AND(A, B)
Gate 2: OR(A, C)
Gate 3: XOR(B, C)
Result: 3 independent outputs
```

Ready to dive deeper? Check out the full documentation files!

---

**Happy Computing with Ternary Logic!** 🚀
