# Symmetric Ternary Logic (-1, 0, 1)

## Overview

Ternary logic operates with three states instead of the traditional two (binary).
This implementation uses **symmetric ternary** or **balanced ternary**:

| Value | Representation | Meaning |
|-------|----------------|---------|
| **1** | TRUE | Positive, Yes, High |
| **0** | UNKNOWN | Neutral, Uncertain, Zero |
| **-1** | FALSE | Negative, No, Low |

## Advantages of Ternary Logic

1. **Three States**: Can represent unknown/undefined states explicitly
2. **Symmetric**: The negative and positive values are treated equally
3. **Natural for Some Problems**: Some systems naturally have three states
4. **Reduced Circuits**: Some operations require fewer gates than binary

## Gate Implementations

### AND (Minimum)
The ternary AND gate returns the minimum of its inputs.

```
Mathematical: AND(x, y) = min(x, y)

Truth Table:
x  | y  | AND(x,y)
---|----|---------
 1 |  1 |    1
 1 |  0 |    0
 1 | -1 |   -1
 0 |  0 |    0
 0 | -1 |   -1
-1 | -1 |   -1
```

**Property**: AND is commutative and associative
- AND(x, y) = AND(y, x)
- AND(AND(x, y), z) = AND(x, AND(y, z))

### OR (Maximum)
The ternary OR gate returns the maximum of its inputs.

```
Mathematical: OR(x, y) = max(x, y)

Truth Table:
x  | y  | OR(x,y)
---|----|---------
 1 |  1 |    1
 1 |  0 |    1
 1 | -1 |    1
 0 |  0 |    0
 0 | -1 |    0
-1 | -1 |   -1
```

**Property**: OR is commutative and associative

### XOR (Sum Modulo 3)
The ternary XOR gate sums inputs and maps the result back to {-1, 0, 1}.

```
Mathematical: XOR(x, y) = [(x + y) mod 3] → {-1, 0, 1}

Mapping:
(x + y) mod 3 = 0  →  -1
(x + y) mod 3 = 1  →   1
(x + y) mod 3 = 2  →   0
(x + y) mod 3 = 3  →   0

Examples:
XOR(1, 1) = (2 mod 3) = 2 → 0
XOR(1, 0) = (1 mod 3) = 1 → 1
XOR(-1, -1) = (-2 mod 3) = 1 → 1
XOR(1, -1) = (0 mod 3) = 0 → -1
```

### NOT (Negation)
The ternary NOT gate negates the input.

```
Mathematical: NOT(x) = -x

Truth Table:
x  | NOT(x)
---|---------
 1 |   -1
 0 |    0
-1 |    1
```

**Property**: Double negation returns original
- NOT(NOT(x)) = x

### MIN (Minimum)
Returns the minimum value among all inputs.

```
Mathematical: MIN(x, y, z, ...) = smallest value

Examples:
MIN(1, 0, -1) = -1
MIN(1, 1, 1) = 1
MIN(0, 0, 0) = 0
MIN(-1, -1, -1) = -1
```

### MAX (Maximum)
Returns the maximum value among all inputs.

```
Mathematical: MAX(x, y, z, ...) = largest value

Examples:
MAX(1, 0, -1) = 1
MAX(-1, -1, -1) = -1
MAX(0, 0, 0) = 0
MAX(1, 1, 1) = 1
```

### SUM (Summation with Clamping)
Sums all inputs and clamps the result to {-1, 0, 1}.

```
Mathematical: SUM(x, y, z, ...) = clamp(x + y + z + ..., -1, 1)

Where:
clamp(x, -1, 1) = 
  -1 if x < -1
   x if -1 ≤ x ≤ 1
   1 if x > 1

Examples:
SUM(1, 1) = 2 → clamped to 1
SUM(1, 1, 1) = 3 → clamped to 1
SUM(-1, -1) = -2 → clamped to -1
SUM(1, -1) = 0 → 0
```

## De Morgan's Laws in Ternary Logic

The classical De Morgan's laws hold with modified operations:

```
NOT(AND(x, y)) = OR(NOT(x), NOT(y))
NOT(OR(x, y)) = AND(NOT(x), NOT(y))
```

**Examples**:
- NOT(AND(1, 1)) = NOT(1) = -1
- OR(NOT(1), NOT(1)) = OR(-1, -1) = -1 ✓

- NOT(OR(1, -1)) = NOT(1) = -1
- AND(NOT(1), NOT(-1)) = AND(-1, 1) = -1 ✓

## Truth Values

In symmetric ternary logic:

| Context | -1 | 0 | 1 |
|---------|----|----|---|
| Logic | FALSE | UNKNOWN | TRUE |
| Voltage | Low | Mid | High |
| Sign | Negative | Zero | Positive |
| State | Off | Standby | On |
| Value | -1 | 0 | 1 |

## Applications

### 1. **Signal Processing**
- **-1**: Negative signal
- **0**: No signal
- **1**: Positive signal

### 2. **Voting Systems**
- **-1**: Vote No / Disagree
- **0**: Abstain / Neutral
- **1**: Vote Yes / Agree

### 3. **Sensor Fusion**
- **-1**: Below threshold
- **0**: At threshold / Uncertain
- **1**: Above threshold

### 4. **Confidence Levels**
- **-1**: Low confidence / Unreliable
- **0**: Medium confidence / Neutral
- **1**: High confidence / Reliable

## Comparison: Binary vs Ternary

| Aspect | Binary | Ternary |
|--------|--------|---------|
| States | 2 | 3 |
| Values | {0, 1} | {-1, 0, 1} |
| Unknown | Not represented | Explicit (0) |
| Symmetry | Asymmetric | Symmetric |
| Gates | AND, OR, NOT, XOR | AND, OR, NOT, XOR, MIN, MAX, SUM |
| Complexity | Lower | Moderate |
| Truth Tables | 2^n rows | 3^n rows |

## Mathematical Properties

### Closure
All ternary operations {AND, OR, NOT, XOR, MIN, MAX, SUM} are closed over {-1, 0, 1}.
Any combination produces a valid ternary value.

### Associativity
- AND(AND(x, y), z) = AND(x, AND(y, z))
- OR(OR(x, y), z) = OR(x, OR(y, z))
- XOR(XOR(x, y), z) = XOR(x, XOR(y, z))

### Commutativity
- AND(x, y) = AND(y, x)
- OR(x, y) = OR(y, x)
- XOR(x, y) = XOR(y, x)

### Identity Elements
- AND: 1 is the identity (AND(x, 1) = x)
- OR: -1 is the identity (OR(x, -1) = x)
- XOR: 0 is the identity (XOR(x, 0) = x)

## Design Considerations

1. **Handling Unknown**: The explicit 0 state can represent unknown/undefined inputs
2. **Error Detection**: Symmetric values make anomalies more obvious
3. **Signal Integrity**: Three levels can reduce noise sensitivity
4. **Gate Complexity**: Slightly more complex than binary, but not significantly

## References

- Balanced Ternary: https://en.wikipedia.org/wiki/Balanced_ternary
- Ternary Logic: https://en.wikipedia.org/wiki/Three-valued_logic
- SETUN Computer: First ternary computer built in 1958

## Further Reading

For more information on ternary logic and its applications, see:
- "Introduction to Ternary Logic" - Various academic papers
- Ternary computing historical research
- Multi-valued logic theory
