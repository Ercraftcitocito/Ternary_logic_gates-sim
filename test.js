/**
 * Test Suite for Ternary Logic Gates
 */

// Node.js setup
if (typeof require !== 'undefined') {
  var { TernaryGate, TernaryCircuit } = require('./src/logic.js');
}

function assert(condition, message) {
  if (!condition) {
    console.error('❌ FAILED:', message);
    process.exit(1);
  } else {
    console.log('✓ PASSED:', message);
  }
}

function testNOTGate() {
  console.log('\n=== Testing NOT Gate ===');
  const gate = new TernaryGate('NOT', 'test_not');

  // NOT(-1) = 1
  gate.clearInputs();
  gate.addInput(-1);
  assert(gate.compute() === 1, 'NOT(-1) should equal 1');

  // NOT(0) = 0
  gate.clearInputs();
  gate.addInput(0);
  assert(gate.compute() === 0, 'NOT(0) should equal 0');

  // NOT(1) = -1
  gate.clearInputs();
  gate.addInput(1);
  assert(gate.compute() === -1, 'NOT(1) should equal -1');
}

function testMAXGate() {
  console.log('\n=== Testing MAX Gate ===');
  const gate = new TernaryGate('MAX', 'test_max');

  // MAX(-1, -1) = -1
  gate.clearInputs();
  gate.addInput(-1);
  gate.addInput(-1);
  assert(gate.compute() === -1, 'MAX(-1, -1) should equal -1');

  // MAX(-1, 0) = 0
  gate.clearInputs();
  gate.addInput(-1);
  gate.addInput(0);
  assert(gate.compute() === 0, 'MAX(-1, 0) should equal 0');

  // MAX(-1, 1) = 1
  gate.clearInputs();
  gate.addInput(-1);
  gate.addInput(1);
  assert(gate.compute() === 1, 'MAX(-1, 1) should equal 1');

  // MAX(0, 1) = 1
  gate.clearInputs();
  gate.addInput(0);
  gate.addInput(1);
  assert(gate.compute() === 1, 'MAX(0, 1) should equal 1');

  // MAX with three inputs
  gate.clearInputs();
  gate.addInput(-1);
  gate.addInput(0);
  gate.addInput(1);
  assert(gate.compute() === 1, 'MAX(-1, 0, 1) should equal 1');
}

function testMINGate() {
  console.log('\n=== Testing MIN Gate ===');
  const gate = new TernaryGate('MIN', 'test_min');

  // MIN(-1, -1) = -1
  gate.clearInputs();
  gate.addInput(-1);
  gate.addInput(-1);
  assert(gate.compute() === -1, 'MIN(-1, -1) should equal -1');

  // MIN(-1, 0) = -1
  gate.clearInputs();
  gate.addInput(-1);
  gate.addInput(0);
  assert(gate.compute() === -1, 'MIN(-1, 0) should equal -1');

  // MIN(0, 1) = 0
  gate.clearInputs();
  gate.addInput(0);
  gate.addInput(1);
  assert(gate.compute() === 0, 'MIN(0, 1) should equal 0');

  // MIN(1, 1) = 1
  gate.clearInputs();
  gate.addInput(1);
  gate.addInput(1);
  assert(gate.compute() === 1, 'MIN(1, 1) should equal 1');

  // MIN with three inputs
  gate.clearInputs();
  gate.addInput(-1);
  gate.addInput(0);
  gate.addInput(1);
  assert(gate.compute() === -1, 'MIN(-1, 0, 1) should equal -1');
}

function testCircuitIntegration() {
  console.log('\n=== Testing Circuit Integration ===');
  const circuit = new TernaryCircuit();

  // Create a simple circuit: input -> NOT gate -> output
  const input1 = circuit.addInput(1);
  const not_gate = circuit.addGate('NOT');
  const output1 = circuit.addOutput();

  circuit.connect(
    { type: 'input', id: input1 },
    { gateId: not_gate.id }
  );

  circuit.connect(
    { gateId: not_gate.id },
    { id: output1 }
  );

  circuit.evaluate();

  assert(circuit.getState().outputs[0].value === -1, 'NOT circuit: input 1 -> NOT -> output should be -1');

  // Test with different input
  circuit.setInputValue(input1, -1);
  circuit.evaluate();
  assert(circuit.getState().outputs[0].value === 1, 'NOT circuit: input -1 -> NOT -> output should be 1');
}

function testComplexCircuit() {
  console.log('\n=== Testing Complex Circuit ===');
  const circuit = new TernaryCircuit();

  // Create: input1 and input2 -> MAX gate -> output
  const input1 = circuit.addInput(1);
  const input2 = circuit.addInput(0);
  const max_gate = circuit.addGate('MAX');
  const output1 = circuit.addOutput();

  circuit.connect({ type: 'input', id: input1 }, { gateId: max_gate.id });
  circuit.connect({ type: 'input', id: input2 }, { gateId: max_gate.id });
  circuit.connect({ gateId: max_gate.id }, { id: output1 });

  circuit.evaluate();
  assert(circuit.getState().outputs[0].value === 1, 'MAX(1, 0) should equal 1');

  // Test MIN gate
  const min_gate = circuit.addGate('MIN');
  const output2 = circuit.addOutput();

  circuit.connect({ type: 'input', id: input1 }, { gateId: min_gate.id });
  circuit.connect({ type: 'input', id: input2 }, { gateId: min_gate.id });
  circuit.connect({ gateId: min_gate.id }, { id: output2 });

  circuit.evaluate();
  assert(circuit.getState().outputs[1].value === 0, 'MIN(1, 0) should equal 0');
}

function testInputValueClamping() {
  console.log('\n=== Testing Input Value Clamping ===');
  const circuit = new TernaryCircuit();
  const input1 = circuit.addInput(0);

  // Try to set value outside range
  circuit.setInputValue(input1, 5);
  assert(circuit.inputs[0].value === 1, 'Input value > 1 should be clamped to 1');

  circuit.setInputValue(input1, -5);
  assert(circuit.inputs[0].value === -1, 'Input value < -1 should be clamped to -1');

  circuit.setInputValue(input1, 0);
  assert(circuit.inputs[0].value === 0, 'Input value 0 should stay 0');
}

function runAllTests() {
  console.log('🧪 Ternary Logic Gates Test Suite');
  console.log('==================================');

  try {
    testNOTGate();
    testMAXGate();
    testMINGate();
    testCircuitIntegration();
    testComplexCircuit();
    testInputValueClamping();

    console.log('\n✅ All tests passed!');
  } catch (error) {
    console.error('\n❌ Test suite error:', error);
    process.exit(1);
  }
}

// Run tests if in Node.js
if (typeof require !== 'undefined') {
  runAllTests();
}
