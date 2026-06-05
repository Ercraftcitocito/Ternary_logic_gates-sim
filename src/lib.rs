use std::collections::HashMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum TernaryValue {
    Negative = -1,
    Zero = 0,
    Positive = 1,
}

impl TernaryValue {
    pub fn from_i32(value: i32) -> Self {
        match value {
            -1 => TernaryValue::Negative,
            0 => TernaryValue::Zero,
            1 => TernaryValue::Positive,
            _ => panic!("Invalid ternary value: {}", value),
        }
    }

    pub fn to_i32(self) -> i32 {
        self as i32
    }

    pub fn as_str(self) -> &'static str {
        match self {
            TernaryValue::Negative => "-1",
            TernaryValue::Zero => "0",
            TernaryValue::Positive => "1",
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum GateType {
    And,
    Or,
    Xor,
    Not,
    Min,
    Max,
    Sum,
}

impl GateType {
    pub fn as_str(self) -> &'static str {
        match self {
            GateType::And => "AND",
            GateType::Or => "OR",
            GateType::Xor => "XOR",
            GateType::Not => "NOT",
            GateType::Min => "MIN",
            GateType::Max => "MAX",
            GateType::Sum => "SUM",
        }
    }
}

pub struct Gate {
    pub id: usize,
    pub gate_type: GateType,
    pub inputs: Vec<usize>,
    pub output: TernaryValue,
}

pub fn apply_gate(gate_type: GateType, inputs: &[TernaryValue]) -> TernaryValue {
    match gate_type {
        GateType::And => and_gate(inputs),
        GateType::Or => or_gate(inputs),
        GateType::Xor => xor_gate(inputs),
        GateType::Not => not_gate(inputs),
        GateType::Min => min_gate(inputs),
        GateType::Max => max_gate(inputs),
        GateType::Sum => sum_gate(inputs),
    }
}

// Ternary AND: min(inputs)
fn and_gate(inputs: &[TernaryValue]) -> TernaryValue {
    min_gate(inputs)
}

// Ternary OR: max(inputs)
fn or_gate(inputs: &[TernaryValue]) -> TernaryValue {
    max_gate(inputs)
}

// Ternary XOR: sum mod 3, then map to {-1, 0, 1}
fn xor_gate(inputs: &[TernaryValue]) -> TernaryValue {
    if inputs.is_empty() {
        return TernaryValue::Zero;
    }
    
    let sum: i32 = inputs.iter().map(|v| v.to_i32()).sum();
    let result = ((sum % 3) + 3) % 3; // Normalize to 0-2
    
    match result {
        0 => TernaryValue::Zero,
        1 => TernaryValue::Positive,
        2 => TernaryValue::Negative,
        _ => TernaryValue::Zero,
    }
}

// Ternary NOT: negate the input
fn not_gate(inputs: &[TernaryValue]) -> TernaryValue {
    if inputs.is_empty() {
        return TernaryValue::Zero;
    }
    TernaryValue::from_i32(-inputs[0].to_i32())
}

// MIN gate
fn min_gate(inputs: &[TernaryValue]) -> TernaryValue {
    if inputs.is_empty() {
        return TernaryValue::Zero;
    }
    inputs
        .iter()
        .min_by_key(|v| v.to_i32())
        .copied()
        .unwrap_or(TernaryValue::Zero)
}

// MAX gate
fn max_gate(inputs: &[TernaryValue]) -> TernaryValue {
    if inputs.is_empty() {
        return TernaryValue::Zero;
    }
    inputs
        .iter()
        .max_by_key(|v| v.to_i32())
        .copied()
        .unwrap_or(TernaryValue::Zero)
}

// SUM gate: sum all inputs, clamp to {-1, 0, 1}
fn sum_gate(inputs: &[TernaryValue]) -> TernaryValue {
    if inputs.is_empty() {
        return TernaryValue::Zero;
    }
    
    let sum: i32 = inputs.iter().map(|v| v.to_i32()).sum();
    if sum > 1 {
        TernaryValue::Positive
    } else if sum < -1 {
        TernaryValue::Negative
    } else {
        TernaryValue::from_i32(sum)
    }
}

pub struct Circuit {
    pub gates: HashMap<usize, Gate>,
    pub inputs: Vec<TernaryValue>,
    pub outputs: Vec<usize>,
    next_id: usize,
}

impl Circuit {
    pub fn new() -> Self {
        Circuit {
            gates: HashMap::new(),
            inputs: vec![],
            outputs: vec![],
            next_id: 0,
        }
    }

    pub fn set_inputs(&mut self, inputs: Vec<TernaryValue>) {
        self.inputs = inputs;
    }

    pub fn add_gate(&mut self, gate_type: GateType, input_ids: Vec<usize>) -> usize {
        let id = self.next_id;
        self.next_id += 1;

        let gate = Gate {
            id,
            gate_type,
            inputs: input_ids,
            output: TernaryValue::Zero,
        };

        self.gates.insert(id, gate);
        id
    }

    pub fn set_output(&mut self, gate_id: usize) {
        if !self.outputs.contains(&gate_id) {
            self.outputs.push(gate_id);
        }
    }

    pub fn evaluate(&mut self) -> Vec<TernaryValue> {
        let mut cache: HashMap<usize, TernaryValue> = HashMap::new();

        // Load input values into cache
        for (i, &value) in self.inputs.iter().enumerate() {
            cache.insert(usize::MAX - i - 1, value); // Use negative indices for inputs
        }

        // Evaluate all gates
        for &gate_id in self.gates.keys() {
            self.evaluate_gate(gate_id, &mut cache);
        }

        // Collect output values
        self.outputs
            .iter()
            .map(|&gate_id| cache.get(&gate_id).copied().unwrap_or(TernaryValue::Zero))
            .collect()
    }

    fn evaluate_gate(
        &self,
        gate_id: usize,
        cache: &mut HashMap<usize, TernaryValue>,
    ) -> TernaryValue {
        if let Some(&cached) = cache.get(&gate_id) {
            return cached;
        }

        let gate = &self.gates[&gate_id];
        let mut input_values = Vec::new();

        for &input_id in &gate.inputs {
            if input_id >= usize::MAX - self.inputs.len() {
                // It's an input
                let idx = usize::MAX - input_id - 1;
                if idx < self.inputs.len() {
                    input_values.push(self.inputs[idx]);
                }
            } else if let Some(&value) = cache.get(&input_id) {
                input_values.push(value);
            } else {
                let value = self.evaluate_gate(input_id, cache);
                input_values.push(value);
            }
        }

        let output = apply_gate(gate.gate_type, &input_values);
        cache.insert(gate_id, output);
        output
    }

    pub fn get_gate_output(&self, gate_id: usize) -> Option<TernaryValue> {
        self.gates.get(&gate_id).map(|g| g.output)
    }

    pub fn get_gate(&self, gate_id: usize) -> Option<&Gate> {
        self.gates.get(&gate_id)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_and_gate() {
        assert_eq!(
            and_gate(&[TernaryValue::Positive, TernaryValue::Positive]),
            TernaryValue::Positive
        );
        assert_eq!(
            and_gate(&[TernaryValue::Positive, TernaryValue::Zero]),
            TernaryValue::Zero
        );
        assert_eq!(
            and_gate(&[TernaryValue::Positive, TernaryValue::Negative]),
            TernaryValue::Negative
        );
    }

    #[test]
    fn test_or_gate() {
        assert_eq!(
            or_gate(&[TernaryValue::Negative, TernaryValue::Negative]),
            TernaryValue::Negative
        );
        assert_eq!(
            or_gate(&[TernaryValue::Negative, TernaryValue::Zero]),
            TernaryValue::Zero
        );
        assert_eq!(
            or_gate(&[TernaryValue::Negative, TernaryValue::Positive]),
            TernaryValue::Positive
        );
    }

    #[test]
    fn test_not_gate() {
        assert_eq!(
            not_gate(&[TernaryValue::Positive]),
            TernaryValue::Negative
        );
        assert_eq!(not_gate(&[TernaryValue::Zero]), TernaryValue::Zero);
        assert_eq!(
            not_gate(&[TernaryValue::Negative]),
            TernaryValue::Positive
        );
    }

    #[test]
    fn test_circuit() {
        let mut circuit = Circuit::new();
        circuit.set_inputs(vec![TernaryValue::Positive, TernaryValue::Positive]);

        let gate1 = circuit.add_gate(GateType::And, vec![usize::MAX - 1, usize::MAX - 2]);
        circuit.set_output(gate1);

        let outputs = circuit.evaluate();
        assert_eq!(outputs[0], TernaryValue::Positive);
    }
}
