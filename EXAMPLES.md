# Ternary Logic Simulator - Examples

## Example 1: Simple AND Operation

### Steps:
1. Start the program: `cargo run --release`
2. Add an AND gate (option 1, then select AND)
3. Simulate (option 2)
4. Enter inputs:
   - A: 1
   - B: 1
   - C: 1
5. Result: Output should be 1 (AND(1,1) = min(1,1) = 1)

### Truth Table for AND:
```
A  | B  | AND(A,B)
---|----|---------
 1 |  1 |    1
 1 |  0 |    0
 1 | -1 |   -1
 0 |  0 |    0
 0 | -1 |   -1
-1 | -1 |   -1
```

## Example 2: Multiple Gates in Series

### Circuit: (A AND B) OR C

1. Add AND gate
2. Add OR gate
3. Simulate with:
   - A: 1, B: 0, C: 1
4. Expected flow:
   - AND(1, 0) = 0
   - OR(0, 1) = 1
   - Result: 1

## Example 3: NOT Operations

1. Add NOT gate
2. Simulate with A: 1, B: 0, C: 0
3. Expected results:
   - NOT(1) = -1
   - NOT(0) = 0
   - NOT(0) = 0

## Truth Tables

### AND (min operation)
```
Inputs  | Output
--------|--------
1, 1    | 1
1, 0    | 0
1, -1   | -1
0, 0    | 0
0, -1   | -1
-1, -1  | -1
```

### OR (max operation)
```
Inputs  | Output
--------|--------
1, 1    | 1
1, 0    | 1
1, -1   | 1
0, 0    | 0
0, -1   | 0
-1, -1  | -1
```

### XOR (sum mod 3)
```
Inputs  | Output
--------|--------
1, 1    | -1
1, 0    | 1
1, -1   | 0
0, 0    | 0
0, -1   | -1
-1, -1  | 1
```

### NOT (negate)
```
Input | Output
------|--------
1     | -1
0     | 0
-1    | 1
```

## Example 4: Balanced Ternary Logic

In balanced ternary, -1 typically represents FALSE, 0 represents UNKNOWN,
and 1 represents TRUE.

### Example: Decision Making Circuit
```
If (sensor_A AND threshold) OR override:
  
1. Add AND gate
2. Add OR gate
3. Input sensor_A=1, threshold=1, override=-1
4. AND(1, 1) = 1
5. OR(1, -1) = 1 (System activates)
```

## Testing Different Operations

All gates can be tested with the same workflow:

1. Start program
2. Add a gate
3. Simulate with different input combinations
4. Observe outputs

### Quick Test Pattern:
```
Test with inputs: (1, 1, 1), (1, 0, 0), (0, 0, 0), (-1, -1, -1)
Compare outputs across different gate types
```

## Advanced: Circuit Composition

You can create complex circuits by adding multiple gates:

1. Gate 1 (e.g., AND) creates first output
2. Gate 2 (e.g., OR) creates second output
3. Gate 3 (e.g., XOR) creates third output
4. Etc.

Each gate operates independently on the same input set,
allowing you to build multi-output circuits.
