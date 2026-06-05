/**
 * Ternary Logic Gates
 * Symmetric ternary values: -1 (false), 0 (unknown/neutral), 1 (true)
 */

class TernaryGate {
  constructor(type, id) {
    this.type = type; // 'NOT', 'MAX', 'MIN'
    this.id = id;
    this.inputs = [];
    this.output = 0;
    this.x = 0;
    this.y = 0;
  }

  setPosition(x, y) {
    this.x = x;
    this.y = y;
  }

  addInput(value) {
    this.inputs.push(value);
  }

  clearInputs() {
    this.inputs = [];
  }

  compute() {
    switch (this.type) {
      case 'NOT':
        return this.computeNOT();
      case 'MAX':
        return this.computeMAX();
      case 'MIN':
        return this.computeMIN();
      default:
        return 0;
    }
  }

  computeNOT() {
    // NOT gate: inverts the single input
    // NOT(-1) = 1, NOT(0) = 0, NOT(1) = -1
    const input = this.inputs[0] !== undefined ? this.inputs[0] : 0;
    this.output = -input;
    return this.output;
  }

  computeMAX() {
    // MAX gate: returns the maximum input value
    // MAX(-1, 0) = 0, MAX(0, 1) = 1, MAX(-1, 1) = 1
    if (this.inputs.length === 0) {
      this.output = 0;
      return this.output;
    }
    this.output = Math.max(...this.inputs);
    return this.output;
  }

  computeMIN() {
    // MIN gate: returns the minimum input value
    // MIN(-1, 0) = -1, MIN(0, 1) = 0, MIN(-1, 1) = -1
    if (this.inputs.length === 0) {
      this.output = 0;
      return this.output;
    }
    this.output = Math.min(...this.inputs);
    return this.output;
  }

  getOutput() {
    return this.output;
  }
}

class TernaryCircuit {
  constructor() {
    this.gates = [];
    this.inputs = []; // {id, value}
    this.outputs = []; // {id, value, sourceGateId}
    this.connections = []; // {from: {gateId, outputIndex}, to: {gateId, inputIndex}}
    this.nextGateId = 1;
  }

  addGate(type) {
    const gate = new TernaryGate(type, `gate_${this.nextGateId++}`);
    this.gates.push(gate);
    return gate;
  }

  removeGate(gateId) {
    this.gates = this.gates.filter(g => g.id !== gateId);
    this.connections = this.connections.filter(
      c => c.from.gateId !== gateId && c.to.gateId !== gateId
    );
  }

  addInput(value = 0) {
    const id = `input_${this.inputs.length}`;
    this.inputs.push({ id, value });
    return id;
  }

  removeInput(inputId) {
    this.inputs = this.inputs.filter(i => i.id !== inputId);
    this.connections = this.connections.filter(
      c => c.from.id !== inputId && c.to.id !== inputId
    );
  }

  addOutput() {
    const id = `output_${this.outputs.length}`;
    this.outputs.push({ id, value: 0, sourceGateId: null });
    return id;
  }

  removeOutput(outputId) {
    this.outputs = this.outputs.filter(o => o.id !== outputId);
    this.connections = this.connections.filter(
      c => c.to.id !== outputId
    );
  }

  connect(from, to) {
    // from: {id: gateId or inputId, outputIndex: 0}
    // to: {id: gateId or outputId, inputIndex: 0}
    this.connections.push({ from, to });
  }

  disconnect(connectionIndex) {
    this.connections.splice(connectionIndex, 1);
  }

  setInputValue(inputId, value) {
    const input = this.inputs.find(i => i.id === inputId);
    if (input) {
      input.value = Math.max(-1, Math.min(1, value)); // Clamp to [-1, 1]
    }
  }

  evaluate() {
    // Clear all gate inputs
    this.gates.forEach(gate => gate.clearInputs());

    // Propagate inputs to gates
    for (const conn of this.connections) {
      if (conn.from.type === 'input') {
        const input = this.inputs.find(i => i.id === conn.from.id);
        const toGate = this.gates.find(g => g.id === conn.to.gateId);
        if (input && toGate) {
          toGate.addInput(input.value);
        }
      } else if (conn.from.gateId) {
        const fromGate = this.gates.find(g => g.id === conn.from.gateId);
        const toGate = this.gates.find(g => g.id === conn.to.gateId) || this.gates.find(g => g.id === conn.to.id);
        if (fromGate && toGate) {
          toGate.addInput(fromGate.getOutput());
        }
      }
    }

    // Compute all gates
    this.gates.forEach(gate => gate.compute());

    // Update outputs
    for (const output of this.outputs) {
      const conn = this.connections.find(c => c.to.id === output.id);
      if (conn && conn.from.gateId) {
        const gate = this.gates.find(g => g.id === conn.from.gateId);
        output.value = gate ? gate.getOutput() : 0;
        output.sourceGateId = conn.from.gateId;
      } else if (conn && conn.from.type === 'input') {
        const input = this.inputs.find(i => i.id === conn.from.id);
        output.value = input ? input.value : 0;
      } else {
        output.value = 0;
      }
    }
  }

  getGate(gateId) {
    return this.gates.find(g => g.id === gateId);
  }

  getState() {
    return {
      gates: this.gates.map(g => ({
        id: g.id,
        type: g.type,
        x: g.x,
        y: g.y,
        output: g.output
      })),
      inputs: this.inputs,
      outputs: this.outputs,
      connections: this.connections
    };
  }
}

// Export for use in browser and Node.js
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { TernaryGate, TernaryCircuit };
}
