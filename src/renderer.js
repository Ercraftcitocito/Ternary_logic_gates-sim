/**
 * Canvas-based UI for Ternary Logic Gate Simulator
 */

class CanvasRenderer {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.circuit = null;
    this.scale = 1;
    this.offsetX = 0;
    this.offsetY = 0;

    // UI State
    this.selectedElement = null;
    this.draggingElement = null;
    this.drawingConnection = null;
    this.hoveredElement = null;

    // Layout
    this.inputRadius = 8;
    this.outputRadius = 8;
    this.gateWidth = 50;
    this.gateHeight = 50;
    this.inputX = 50;
    this.outputX = 0;
    this.verticalSpacing = 80;

    // Colors
    this.colors = {
      bg: '#1e1e1e',
      grid: '#333333',
      wire: '#ff0000',
      wireActive: '#00ff00',
      input: '#ff0000',
      output: '#00ff00',
      gate: {
        NOT: '#9c27b0',
        MAX: '#2196f3',
        MIN: '#4caf50'
      },
      text: '#ffffff',
      selected: '#ffff00'
    };

    this.setupEventListeners();
  }

  setCircuit(circuit) {
    this.circuit = circuit;
    this.recalculateLayout();
  }

  recalculateLayout() {
    if (!this.circuit) return;

    const inputCount = this.circuit.inputs.length;
    const outputCount = this.circuit.outputs.length;

    // Position inputs on the left
    this.circuit.inputs.forEach((input, idx) => {
      input.x = this.inputX;
      input.y = 100 + idx * this.verticalSpacing;
    });

    // Position outputs on the right
    this.outputX = this.canvas.width - 50;
    this.circuit.outputs.forEach((output, idx) => {
      output.x = this.outputX;
      output.y = 100 + idx * this.verticalSpacing;
    });

    // Position gates in middle (user can move them)
    this.circuit.gates.forEach((gate, idx) => {
      if (gate.x === 0 && gate.y === 0) {
        gate.x = this.canvas.width / 2 + (idx % 3) * 100;
        gate.y = 100 + Math.floor(idx / 3) * this.verticalSpacing;
      }
    });
  }

  setupEventListeners() {
    this.canvas.addEventListener('mousedown', e => this.onMouseDown(e));
    this.canvas.addEventListener('mousemove', e => this.onMouseMove(e));
    this.canvas.addEventListener('mouseup', e => this.onMouseUp(e));
    this.canvas.addEventListener('contextmenu', e => {
      e.preventDefault();
      this.onRightClick(e);
    });
  }

  render() {
    // Clear canvas
    this.ctx.fillStyle = this.colors.bg;
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // Draw grid
    this.drawGrid();

    if (!this.circuit) return;

    // Draw wires first (so they appear behind gates)
    this.drawConnections();

    // Draw inputs
    this.circuit.inputs.forEach(input => this.drawInput(input));

    // Draw gates
    this.circuit.gates.forEach(gate => this.drawGate(gate));

    // Draw outputs
    this.circuit.outputs.forEach(output => this.drawOutput(output));

    // Draw connection being drawn
    if (this.drawingConnection) {
      this.drawTempConnection();
    }
  }

  drawGrid() {
    this.ctx.strokeStyle = this.colors.grid;
    this.ctx.lineWidth = 0.5;
    const gridSize = 20;

    for (let x = 0; x < this.canvas.width; x += gridSize) {
      this.ctx.beginPath();
      this.ctx.moveTo(x, 0);
      this.ctx.lineTo(x, this.canvas.height);
      this.ctx.stroke();
    }

    for (let y = 0; y < this.canvas.height; y += gridSize) {
      this.ctx.beginPath();
      this.ctx.moveTo(0, y);
      this.ctx.lineTo(this.canvas.width, y);
      this.ctx.stroke();
    }
  }

  drawConnections() {
    this.circuit.connections.forEach((conn, idx) => {
      const fromPoint = this.getConnectionPoint(conn.from);
      const toPoint = this.getConnectionPoint(conn.to);

      if (fromPoint && toPoint) {
        this.ctx.strokeStyle = this.colors.wire;
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.moveTo(fromPoint.x, fromPoint.y);

        // Draw bezier curve
        const midX = (fromPoint.x + toPoint.x) / 2;
        this.ctx.bezierCurveTo(midX, fromPoint.y, midX, toPoint.y, toPoint.x, toPoint.y);
        this.ctx.stroke();
      }
    });
  }

  drawTempConnection() {
    const { from, currentPos } = this.drawingConnection;
    const fromPoint = this.getConnectionPoint(from);

    if (fromPoint) {
      this.ctx.strokeStyle = this.colors.wireActive;
      this.ctx.lineWidth = 2;
      this.ctx.setLineDash([5, 5]);
      this.ctx.beginPath();
      this.ctx.moveTo(fromPoint.x, fromPoint.y);
      this.ctx.lineTo(currentPos.x, currentPos.y);
      this.ctx.stroke();
      this.ctx.setLineDash([]);
    }
  }

  getConnectionPoint(ref) {
    if (ref.type === 'input') {
      const input = this.circuit.inputs.find(i => i.id === ref.id);
      return input ? { x: input.x + this.inputRadius, y: input.y } : null;
    } else if (ref.type === 'output' || this.circuit.outputs.find(o => o.id === ref.id)) {
      const output = this.circuit.outputs.find(o => o.id === ref.id);
      return output ? { x: output.x - this.outputRadius, y: output.y } : null;
    } else if (ref.gateId) {
      const gate = this.circuit.gates.find(g => g.id === ref.gateId);
      if (gate) {
        return { x: gate.x + this.gateWidth / 2, y: gate.y + this.gateHeight / 2 };
      }
    }
    return null;
  }

  drawInput(input) {
    const isSelected = this.selectedElement?.id === input.id && this.selectedElement?.type === 'input';
    const isHovered = this.hoveredElement?.id === input.id && this.hoveredElement?.type === 'input';

    this.ctx.fillStyle = isSelected ? this.colors.selected : this.colors.input;
    this.ctx.beginPath();
    this.ctx.arc(input.x, input.y, this.inputRadius, 0, Math.PI * 2);
    this.ctx.fill();

    if (isHovered) {
      this.ctx.strokeStyle = this.colors.selected;
      this.ctx.lineWidth = 2;
      this.ctx.stroke();
    }

    // Draw value label
    this.ctx.fillStyle = this.colors.text;
    this.ctx.font = '12px Arial';
    this.ctx.textAlign = 'right';
    this.ctx.fillText(input.value, input.x - 20, input.y + 4);
    this.ctx.textAlign = 'left';
    this.ctx.fillText('IN', input.x + 15, input.y + 4);
  }

  drawGate(gate) {
    const isSelected = this.selectedElement?.id === gate.id && this.selectedElement?.type === 'gate';
    const isHovered = this.hoveredElement?.id === gate.id && this.hoveredElement?.type === 'gate';

    const gateColor = this.colors.gate[gate.type] || '#999999';
    this.ctx.fillStyle = isSelected ? this.colors.selected : gateColor;
    this.ctx.fillRect(gate.x - this.gateWidth / 2, gate.y - this.gateHeight / 2, this.gateWidth, this.gateHeight);

    if (isHovered) {
      this.ctx.strokeStyle = this.colors.selected;
      this.ctx.lineWidth = 2;
      this.ctx.strokeRect(gate.x - this.gateWidth / 2, gate.y - this.gateHeight / 2, this.gateWidth, this.gateHeight);
    }

    // Draw gate label
    this.ctx.fillStyle = '#000000';
    this.ctx.font = 'bold 10px Arial';
    this.ctx.textAlign = 'center';
    this.ctx.textBaseline = 'middle';
    this.ctx.fillText(gate.type, gate.x, gate.y - 5);

    // Draw output value
    this.ctx.fillStyle = this.colors.text;
    this.ctx.font = '10px Arial';
    this.ctx.fillText(gate.output, gate.x, gate.y + 8);
  }

  drawOutput(output) {
    const isSelected = this.selectedElement?.id === output.id && this.selectedElement?.type === 'output';
    const isHovered = this.hoveredElement?.id === output.id && this.hoveredElement?.type === 'output';

    this.ctx.fillStyle = isSelected ? this.colors.selected : this.colors.output;
    this.ctx.beginPath();
    this.ctx.arc(output.x, output.y, this.outputRadius, 0, Math.PI * 2);
    this.ctx.fill();

    if (isHovered) {
      this.ctx.strokeStyle = this.colors.selected;
      this.ctx.lineWidth = 2;
      this.ctx.stroke();
    }

    // Draw value label
    this.ctx.fillStyle = this.colors.text;
    this.ctx.font = '12px Arial';
    this.ctx.textAlign = 'right';
    this.ctx.fillText(output.value, output.x - 20, output.y + 4);
    this.ctx.textAlign = 'left';
    this.ctx.fillText('OUT', output.x + 15, output.y + 4);
  }

  onMouseDown(e) {
    const pos = this.getMousePos(e);
    const element = this.getElementAt(pos);

    if (element) {
      this.selectedElement = element;
      this.draggingElement = element;

      if (element.type === 'input' || element.type === 'output' || element.type === 'gate') {
        this.drawingConnection = { from: element, currentPos: pos };
      }
    }

    this.render();
  }

  onMouseMove(e) {
    const pos = this.getMousePos(e);
    this.hoveredElement = this.getElementAt(pos);

    if (this.draggingElement && this.draggingElement.type === 'gate') {
      this.draggingElement.x = pos.x;
      this.draggingElement.y = pos.y;
    }

    if (this.drawingConnection) {
      this.drawingConnection.currentPos = pos;
    }

    this.render();
  }

  onMouseUp(e) {
    const pos = this.getMousePos(e);
    const element = this.getElementAt(pos);

    if (this.drawingConnection) {
      if (element && this.canConnect(this.drawingConnection.from, element)) {
        this.circuit.connect(
          this.getConnectionRef(this.drawingConnection.from),
          this.getConnectionRef(element)
        );
      }
      this.drawingConnection = null;
    }

    this.draggingElement = null;
    this.circuit.evaluate();
    this.render();
  }

  onRightClick(e) {
    const pos = this.getMousePos(e);
    const element = this.getElementAt(pos);

    if (element && element.type === 'gate') {
      this.circuit.removeGate(element.id);
      this.selectedElement = null;
    }

    this.render();
  }

  getMousePos(e) {
    const rect = this.canvas.getBoundingClientRect();
    return {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    };
  }

  getElementAt(pos) {
    // Check inputs
    for (const input of this.circuit.inputs) {
      if (this.distance(pos, input) <= this.inputRadius) {
        return { ...input, type: 'input' };
      }
    }

    // Check outputs
    for (const output of this.circuit.outputs) {
      if (this.distance(pos, output) <= this.outputRadius) {
        return { ...output, type: 'output' };
      }
    }

    // Check gates
    for (const gate of this.circuit.gates) {
      if (
        pos.x >= gate.x - this.gateWidth / 2 &&
        pos.x <= gate.x + this.gateWidth / 2 &&
        pos.y >= gate.y - this.gateHeight / 2 &&
        pos.y <= gate.y + this.gateHeight / 2
      ) {
        return { ...gate, type: 'gate' };
      }
    }

    return null;
  }

  distance(p1, p2) {
    return Math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2);
  }

  canConnect(from, to) {
    // Can't connect to same element
    if (from.id === to.id) return false;
    // Can't connect output to input (wrong direction)
    if (from.type === 'output' && to.type === 'input') return false;
    // Can't connect output to output
    if (from.type === 'output' && to.type === 'output') return false;
    return true;
  }

  getConnectionRef(element) {
    if (element.type === 'input') {
      return { type: 'input', id: element.id };
    } else if (element.type === 'output') {
      return { id: element.id };
    } else if (element.type === 'gate') {
      return { gateId: element.id };
    }
  }
}
