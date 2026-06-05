import tkinter as tk
from tkinter import simpledialog

# -------- LÓGICA TERNARIA --------


def ternary_not(a):
    return -a


def ternary_min(a, b):
    return min(a, b)


def ternary_max(a, b):
    return max(a, b)


COLORS = {-1: "#ff6b6b", 0: "#9aa0a6", 1: "#6fdc99"}

# -------- NODOS --------


class Gate:
    def __init__(self, app, x, y, gate_type, hidden=False):
        self.app = app
        self.x = x
        self.y = y
        self.gate_type = gate_type
        self.value = 0
        self.hidden = hidden
        self.app = app
        self.x = x
        self.y = y
        self.gate_type = gate_type
        self.value = 0

        # determine number of inputs (NOT -> 1, others -> 2)
        self.inputs_count = 1 if gate_type == "NOT" else 2
        self.input_wires = [None] * self.inputs_count

        self.rect = app.canvas.create_rectangle(x, y, x + 90, y + 50, fill="#eef6ff", outline="#1e40af", width=2)
        self.text = app.canvas.create_text(x + 45, y + 25, text=gate_type, font=("Helvetica", 10, "bold"), fill="#0f172a")

        # draw input ports on the left
        self.input_ports = []
        for i in range(self.inputs_count):
            py = y + int((i + 1) * (50 / (self.inputs_count + 1)))
            if not hidden:
                port = app.canvas.create_oval(x - 6, py - 6, x + 6, py + 6, fill="#f8fafc", outline="#1e293b")
            else:
                port = None
            self.input_ports.append(port)

        # output port on the right
        if not hidden:
            self.output_port = app.canvas.create_oval(x + 90 - 6, y + 25 - 6, x + 90 + 6, y + 25 + 6, fill="#f8fafc", outline="#1e293b")
        else:
            self.output_port = None

        # collect visible items
        self.items = [self.rect, self.text] + [p for p in self.input_ports if p is not None] + ([self.output_port] if self.output_port is not None else [])

        # register ports with app for hit-testing
        for i, port in enumerate(self.input_ports):
            if port is not None:
                app.register_port(port, self, 'input', i, mapped_node=None)
        if self.output_port is not None:
            app.register_port(self.output_port, self, 'output', 0, mapped_node=self)


    def get_output_point(self):
        return (self.x + 90, self.y + 25)

    def get_input_point(self, idx):
        py = self.y + int((idx + 1) * (50 / (self.inputs_count + 1)))
        return (self.x, py)


class InputNode:
    def __init__(self, app, x, y, name, hidden=False):
        self.app = app
        self.x = x
        self.y = y
        self.name = name
        self.value = 0
        self.hidden = hidden

        if not hidden:
            self.rect = app.canvas.create_rectangle(
                x, y, x + 90, y + 50, fill=COLORS[self.value], outline="#0f172a", width=2
            )
            self.text = app.canvas.create_text(x + 45, y + 25, text=f"{name}\n0", font=("Helvetica", 10), fill="#0f172a")
            # output port on right
            self.output_port = app.canvas.create_oval(x + 90 - 6, y + 25 - 6, x + 90 + 6, y + 25 + 6, fill="#f8fafc", outline="#1e293b")
            self.items = [self.rect, self.text, self.output_port]
            app.register_port(self.output_port, self, 'output', 0, mapped_node=self)
        else:
            self.rect = None
            self.text = None
            self.output_port = None
            self.items = []

    def get_output_point(self, idx=0):
        return (self.x + 90, self.y + 25)


class OutputNode:
    def __init__(self, app, x, y, name, hidden=False):
        self.app = app
        self.x = x
        self.y = y
        self.name = name
        self.value = 0
        self.hidden = hidden

        if not hidden:
            self.rect = app.canvas.create_rectangle(
                x, y, x + 90, y + 50, fill=COLORS[self.value], outline="#0f172a", width=2
            )
            self.text = app.canvas.create_text(x + 45, y + 25, text=f"{name}\n0", font=("Helvetica", 10), fill="#0f172a")
            # single input port on left
            self.input_wires = [None]
            self.input_port = app.canvas.create_oval(x - 6, y + 25 - 6, x + 6, y + 25 + 6, fill="#f8fafc", outline="#1e293b")
            self.items = [self.rect, self.text, self.input_port]
            app.register_port(self.input_port, self, 'input', 0, mapped_node=self)
        else:
            self.rect = None
            self.text = None
            self.input_wires = [None]
            self.input_port = None
            self.items = []

    def get_input_point(self, idx=0):
        return (self.x, self.y + 25)


# -------- APP --------


class Simulator:
    def __init__(self, root):

        self.root = root
        root.title("Simulador Lógico Ternario")

        self.canvas = tk.Canvas(root, bg="#f8fafc", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.bottom = tk.Frame(root)
        self.bottom.pack(fill="x", side="bottom")

        self.library = ["NOT", "MIN", "MAX"]

        self.nodes = []
        # connections: list of (src, dst, dst_idx)
        self.connections = []
        # map canvas wire id -> (src, dst, dst_idx)
        self.wire_items = {}

        self.port_map = {}  # canvas item id -> (owner, type, idx, mapped_node)
        self.templates = {}  # saved gates

        self.drag_node = None
        self.drag_dx = 0
        self.drag_dy = 0

        self.selected_node = None

        self.connect_source = None
        self.temp_line = None

        tk.Button(self.bottom, text="Entrada", command=self.add_input, bg="#2563eb", fg="white", activebackground="#1e40af", relief="flat", padx=8).pack(side="left")

        tk.Button(self.bottom, text="Salida", command=self.add_output, bg="#2563eb", fg="white", activebackground="#1e40af", relief="flat", padx=8).pack(side="left")

        tk.Button(self.bottom, text="Guardar puerta", command=self.save_gate, bg="#2563eb", fg="white", activebackground="#1e40af", relief="flat", padx=8).pack(
            side="left"
        )

        self.libframe = tk.Frame(self.bottom)
        self.libframe.pack(side="left", padx=20)

        self.refresh_library()

        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.release)
        # right-click: start/drag/end connection
        self.canvas.bind("<Button-3>", self.start_connect)
        self.canvas.bind("<B3-Motion>", self.connect_drag)
        self.canvas.bind("<ButtonRelease-3>", self.end_connect)
        self.canvas.bind("<Double-Button-1>", self.double_click)
        # delete selected node with Delete key
        root.bind('<Delete>', self.delete_selected)


    def register_port(self, item_id, owner, ptype, idx, mapped_node=None):
        # item_id: canvas id of port oval
        self.port_map[item_id] = (owner, ptype, idx, mapped_node)

    def delete_selected(self, event=None):
        if not self.selected_node:
            return
        node = self.selected_node
        # remove related connections
        to_remove = []
        for c in list(self.connections):
            src, dst, idx = c
            if src == node or dst == node:
                to_remove.append(c)
        for c in to_remove:
            try:
                self.connections.remove(c)
            except Exception:
                pass
        # delete canvas items
        for it in getattr(node, 'items', []):
            if it:
                try:
                    self.canvas.delete(it)
                except Exception:
                    pass
                # also clear port_map entries
                if it in self.port_map:
                    try:
                        del self.port_map[it]
                    except Exception:
                        pass
        # if composite, delete its internal nodes as well
        if hasattr(node, 'internal_nodes'):
            for n in list(node.internal_nodes):
                if n in self.nodes:
                    try:
                        for it in getattr(n, 'items', []):
                            if it:
                                self.canvas.delete(it)
                    except Exception:
                        pass
                    try:
                        self.nodes.remove(n)
                    except Exception:
                        pass
        try:
            self.nodes.remove(node)
        except Exception:
            pass
        self.selected_node = None
        self.redraw_connections()

    def refresh_library(self):
        for w in self.libframe.winfo_children():
            w.destroy()

        for gate in self.library:
            tk.Button(
                self.libframe, text=gate, command=lambda g=gate: self.add_gate(g), bg="#e2e8f0", relief="flat", padx=6, pady=2
            ).pack(side="left", padx=4)
        # show saved templates
        for name in self.templates.keys():
            tk.Button(self.libframe, text=name, command=lambda n=name: self.add_gate(n), bg="#fde68a", relief="flat", padx=6, pady=2).pack(side="left", padx=4)

    def add_gate(self, gate):
        # if gate is a saved template, instantiate composite
        if gate in self.templates:
            self.instantiate_template(gate, 250, 100)
            return
        self.nodes.append(Gate(self, 250, 100, gate))

    def add_input(self):
        n = len([x for x in self.nodes if isinstance(x, InputNode)])
        self.nodes.append(InputNode(self, 20, 50 + n * 80, f"IN{n + 1}"))

    def add_output(self):
        n = len([x for x in self.nodes if isinstance(x, OutputNode)])
        self.nodes.append(OutputNode(self, 850, 50 + n * 80, f"OUT{n + 1}"))

    def node_at(self, x, y):
        # returns (node, hit) where hit is dict with type: 'body'/'input'/'output' and index
        item = self.canvas.find_closest(x, y)
        if not item:
            return None, None
        iid = item[0]

        # check if clicked on a registered port
        if iid in self.port_map:
            owner, ptype, idx, mapped = self.port_map[iid]
            return owner, {'type': ptype, 'index': idx, 'item': iid, 'mapped': mapped}

        # fallback: find node by item membership
        for node in self.nodes:
            if getattr(node, 'items', None) and iid in node.items:
                return node, {'type': 'body', 'index': None, 'item': iid}

        return None, None

    def left_click(self, event):
        node, hit = self.node_at(event.x, event.y)

        if node:
            # select and start dragging
            self.selected_node = node
            # visual highlight
            try:
                for n in self.nodes:
                    if hasattr(n, 'rect') and n.rect:
                        self.canvas.itemconfig(n.rect, width=2)
                if hasattr(node, 'rect') and node.rect:
                    self.canvas.itemconfig(node.rect, width=4)
            except Exception:
                pass

            self.drag_node = node
            self.drag_dx = event.x - node.x
            self.drag_dy = event.y - node.y

    def drag(self, event):

        if not self.drag_node:
            return

        n = self.drag_node

        n.x = event.x - self.drag_dx
        n.y = event.y - self.drag_dy

        self.canvas.coords(n.rect, n.x, n.y, n.x + 90, n.y + 50)
        self.canvas.coords(n.text, n.x + 45, n.y + 25)

        # update any ports to move with the node
        if isinstance(n, Gate):
            for i, port_id in enumerate(n.input_ports):
                py = n.y + int((i + 1) * (50 / (n.inputs_count + 1)))
                try:
                    self.canvas.coords(port_id, n.x - 6, py - 6, n.x + 6, py + 6)
                except Exception:
                    pass
            try:
                self.canvas.coords(n.output_port, n.x + 90 - 6, n.y + 25 - 6, n.x + 90 + 6, n.y + 25 + 6)
            except Exception:
                pass
        elif isinstance(n, InputNode):
            try:
                self.canvas.coords(n.output_port, n.x + 90 - 6, n.y + 25 - 6, n.x + 90 + 6, n.y + 25 + 6)
            except Exception:
                pass
        elif isinstance(n, OutputNode):
            try:
                self.canvas.coords(n.input_port, n.x - 6, n.y + 25 - 6, n.x + 6, n.y + 25 + 6)
            except Exception:
                pass

        self.redraw_connections()

    def release(self, event):
        self.drag_node = None

    def find_nearest_input_port(self, x, y, exclude_node=None, max_dist=120):
        best = None
        best_node = None
        best_idx = None
        best_px = None
        best_py = None
        maxd2 = max_dist * max_dist
        for node in self.nodes:
            # skip nodes that are the excluded one
            if node == exclude_node:
                continue
            if isinstance(node, Gate):
                for i in range(node.inputs_count):
                    px, py = node.get_input_point(i)
                    d2 = (px - x) ** 2 + (py - y) ** 2
                    # only consider free slots
                    if node.input_wires[i] is not None:
                        continue
                    if d2 <= maxd2 and (best is None or d2 < best):
                        best = d2
                        best_node = node
                        best_idx = i
                        best_px = px
                        best_py = py
            elif isinstance(node, OutputNode):
                px, py = node.get_input_point(0)
                d2 = (px - x) ** 2 + (py - y) ** 2
                if node.input_wires and node.input_wires[0] is not None:
                    continue
                if d2 <= maxd2 and (best is None or d2 < best):
                    best = d2
                    best_node = node
                    best_idx = 0
                    best_px = px
                    best_py = py
        return best_node, best_idx, best_px, best_py

    def start_connect(self, event):
        # if clicked on an existing wire -> delete it
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            iid = item[0]
            if iid in self.wire_items:
                src, dst, idx = self.wire_items[iid]
                # remove connection
                if (src, dst, idx) in self.connections:
                    self.connections.remove((src, dst, idx))
                try:
                    # if dst is an internal input node created by composite
                    dst.input_wires[idx] = None
                except Exception:
                    pass
                self.redraw_connections()
                self.evaluate()
                return

        node, hit = self.node_at(event.x, event.y)
        if node is None:
            return

        # if clicked on an output port, start from the mapped node
        start_node = node
        sx = event.x
        sy = event.y
        if hit and hit.get('type') == 'output':
            mapped = hit.get('mapped')
            if mapped is not None:
                start_node = mapped
            # get precise port center
            coords = self.canvas.coords(hit.get('item'))
            if coords:
                sx = (coords[0] + coords[2]) / 2
                sy = (coords[1] + coords[3]) / 2
        else:
            # nodes without output cannot start a connection
            if not hasattr(node, 'get_output_point'):
                return
            sx, sy = node.get_output_point()

        self.connect_source = start_node
        # create temporary line that follows cursor
        self.temp_line = self.canvas.create_line(sx, sy, event.x, event.y, width=3, dash=(4, 2), fill="#334155", tags="temp")

    def connect_drag(self, event):
        if not self.temp_line:
            return
        # try to snap to nearest input port
        dst_node, dst_idx, px, py = self.find_nearest_input_port(event.x, event.y, exclude_node=self.connect_source, max_dist=100)
        coords = self.canvas.coords(self.temp_line)
        sx, sy = coords[0], coords[1]
        if dst_node is not None and px is not None:
            ex, ey = px, py
        else:
            ex, ey = event.x, event.y
        self.canvas.coords(self.temp_line, sx, sy, ex, ey)

    def end_connect(self, event):
        if not self.connect_source:
            # cleanup any temp line
            if self.temp_line:
                self.canvas.delete(self.temp_line)
                self.temp_line = None
            return

        src = self.connect_source
        # snap to nearest input port within a larger radius
        dst_node, dst_idx, px, py = self.find_nearest_input_port(event.x, event.y, exclude_node=src, max_dist=160)

        if dst_node is None:
            # no suitable port nearby -> cancel
            if self.temp_line:
                self.canvas.delete(self.temp_line)
                self.temp_line = None
            self.connect_source = None
            return

        dst = dst_node

        # prevent connecting to input nodes or to self
        if isinstance(dst, InputNode) or dst == src:
            if self.temp_line:
                self.canvas.delete(self.temp_line)
                self.temp_line = None
            self.connect_source = None
            return

        # If dst is a composite-like object that exposes internal_inputs, map connection to internal node
        if hasattr(dst, 'internal_inputs'):
            internal = dst.internal_inputs[dst_idx]
            # check free
            if internal.input_wires[0] is not None:
                if self.temp_line:
                    self.canvas.delete(self.temp_line)
                    self.temp_line = None
                self.connect_source = None
                return
            # create connection to internal node instead
            self.connections.append((src, internal, 0))
            try:
                internal.input_wires[0] = src
            except Exception:
                pass
        else:
            # check slot free (redundant because find_nearest_input_port checked, but keep safety)
            if getattr(dst, "input_wires", [None])[dst_idx] is not None:
                if self.temp_line:
                    self.canvas.delete(self.temp_line)
                    self.temp_line = None
                self.connect_source = None
                return

            # create connection
            self.connections.append((src, dst, dst_idx))
            try:
                dst.input_wires[dst_idx] = src
            except Exception:
                pass

        # cleanup temp line
        if self.temp_line:
            self.canvas.delete(self.temp_line)
            self.temp_line = None

        self.connect_source = None
        self.redraw_connections()
        self.evaluate()

    def redraw_connections(self):

        # remove previous wires
        for iid in list(self.wire_items.keys()):
            try:
                self.canvas.delete(iid)
            except Exception:
                pass
        self.wire_items.clear()

        for src, dst, dst_idx in self.connections:
            color = COLORS.get(getattr(src, "value", 0), "#888")

            # compute src and dst points
            if hasattr(src, "get_output_point"):
                sx, sy = src.get_output_point()
            else:
                sx, sy = src.x + 90, src.y + 25

            if hasattr(dst, 'get_input_point'):
                dx, dy = dst.get_input_point(dst_idx)
            else:
                dx, dy = dst.x, dst.y + 25

            # draw a subtle shadow as background
            self.canvas.create_line(sx+1, sy+1, dx+1, dy+1, width=6, fill="#cbd5e1", tags="wire_ghost", smooth=True)
            iid = self.canvas.create_line(sx, sy, dx, dy, width=4, fill=color, tags="wire", arrow=tk.LAST, smooth=True)
            self.wire_items[iid] = (src, dst, dst_idx)

    def double_click(self, event):

        node, hit = self.node_at(event.x, event.y)

        if isinstance(node, InputNode):
            values = [-1, 0, 1]

            idx = values.index(node.value)
            node.value = values[(idx + 1) % 3]

            if node.rect:
                self.canvas.itemconfig(node.rect, fill=COLORS[node.value])

            if node.text:
                self.canvas.itemconfig(node.text, text=f"{node.name}\n{node.value}")

            self.evaluate()

    def incoming(self, target):
        # return list of source nodes connected to target in input order
        if isinstance(target, Gate):
            return [s for s in target.input_wires if s is not None]
        if isinstance(target, OutputNode):
            return [target.input_wires[0]] if target.input_wires and target.input_wires[0] is not None else []
        # composite internal input nodes will be handled as normal nodes (they have input_wires)

        # fallback: scan connections
        result = []
        for src, dst, idx in self.connections:
            if dst == target:
                result.append(src)
        return result

    def evaluate(self):

        for _ in range(10):
            for node in list(self.nodes):
                if isinstance(node, Gate):
                    ins = self.incoming(node)
                    vals = [x.value for x in ins]

                    if node.gate_type == "NOT" and len(vals) >= 1:
                        node.value = ternary_not(vals[0])

                    elif node.gate_type == "MIN" and len(vals) >= 2:
                        node.value = ternary_min(vals[0], vals[1])

                    elif node.gate_type == "MAX" and len(vals) >= 2:
                        node.value = ternary_max(vals[0], vals[1])

                    # update gate visual to reflect value
                    try:
                        if not getattr(node, 'hidden', False) and node.rect:
                            self.canvas.itemconfig(node.rect, fill=COLORS[node.value])
                    except Exception:
                        pass

                elif isinstance(node, OutputNode):
                    ins = self.incoming(node)

                    if ins:
                        node.value = ins[0].value

                        if not getattr(node, 'hidden', False) and node.rect:
                            self.canvas.itemconfig(node.rect, fill=COLORS[node.value])

                        if node.text:
                            self.canvas.itemconfig(
                                node.text, text=f"{node.name}\n{node.value}"
                            )

        self.redraw_connections()

    def instantiate_template(self, name, x, y):
        tpl = self.templates.get(name)
        if not tpl:
            return
        specs = tpl['nodes']
        conns = tpl['conns']

        # create composite visual container
        inputs = sum(1 for s in specs if s['type'] == 'Input')
        outputs = sum(1 for s in specs if s['type'] == 'Output')

        comp = Composite(self, x, y, name, inputs, outputs)
        self.nodes.append(comp)

        # create internal nodes (hidden) and map index
        created = []
        for s in specs:
            sx = x + s.get('x', 0)
            sy = y + s.get('y', 0)
            if s['type'] == 'Gate':
                n = Gate(self, sx, sy, s.get('gate_type', 'G'), hidden=True)
            elif s['type'] == 'Input':
                n = InputNode(self, sx, sy, s.get('name', 'IN'), hidden=True)
            elif s['type'] == 'Output':
                n = OutputNode(self, sx, sy, s.get('name', 'OUT'), hidden=True)
            else:
                n = Gate(self, sx, sy, 'G', hidden=True)
            self.nodes.append(n)
            created.append(n)

        # create connections among internal nodes
        for c in conns:
            si = c['src']
            di = c['dst']
            idx = c['idx']
            if 0 <= si < len(created) and 0 <= di < len(created):
                src = created[si]
                dst = created[di]
                # if dst is an OutputNode, use its input index 0
                if isinstance(dst, OutputNode):
                    self.connections.append((src, dst, 0))
                    try:
                        dst.input_wires[0] = src
                    except Exception:
                        pass
                elif isinstance(dst, Gate):
                    self.connections.append((src, dst, idx))
                    try:
                        dst.input_wires[idx] = src
                    except Exception:
                        pass

        # map composite external ports to internal nodes
        int_inputs = [n for n in created if isinstance(n, InputNode)]
        int_outputs = [n for n in created if isinstance(n, OutputNode)]
        comp.internal_inputs = int_inputs
        comp.internal_outputs = int_outputs

        # register composite ports to map to internal nodes
        for i, pid in enumerate(comp.input_ports):
            if pid is not None:
                # map input port to internal input node
                mapped = None
                if i < len(int_inputs):
                    mapped = int_inputs[i]
                self.register_port(pid, comp, 'input', i, mapped_node=mapped)
        for i, pid in enumerate(comp.output_ports):
            if pid is not None:
                mapped = None
                if i < len(int_outputs):
                    mapped = int_outputs[i]
                self.register_port(pid, comp, 'output', i, mapped_node=mapped)

        # done

    def save_gate(self):
        name = simpledialog.askstring("Nueva puerta", "Nombre:")
        if not name:
            return

        # serialize current workspace nodes and connections
        # determine bounding box
        if not self.nodes:
            return

        xs = [n.x for n in self.nodes]
        ys = [n.y for n in self.nodes]
        minx, miny = min(xs), min(ys)

        node_index = {n: i for i, n in enumerate(self.nodes)}
        specs = []
        for n in self.nodes:
            if isinstance(n, Gate):
                specs.append({'type': 'Gate', 'gate_type': n.gate_type, 'x': n.x - minx, 'y': n.y - miny, 'inputs_count': n.inputs_count})
            elif isinstance(n, InputNode):
                specs.append({'type': 'Input', 'name': n.name, 'x': n.x - minx, 'y': n.y - miny})
            elif isinstance(n, OutputNode):
                specs.append({'type': 'Output', 'name': n.name, 'x': n.x - minx, 'y': n.y - miny})
            else:
                specs.append({'type': 'Unknown'})

        conns = []
        for src, dst, idx in self.connections:
            conns.append({'src': node_index.get(src, -1), 'dst': node_index.get(dst, -1), 'idx': idx})

        self.templates[name] = {'nodes': specs, 'conns': conns}

        # add to library buttons
        if name not in self.library:
            self.library.append(name)
        self.refresh_library()

        # reset workspace: clear all items and start fresh with 1 input and 1 output
        # delete canvas items
        for n in self.nodes:
            for it in getattr(n, 'items', []):
                if it:
                    try:
                        self.canvas.delete(it)
                    except Exception:
                        pass
        for iid in list(self.wire_items.keys()):
            try:
                self.canvas.delete(iid)
            except Exception:
                pass
        self.nodes = []
        self.connections = []
        self.wire_items = {}
        self.port_map = {}

        # new workspace baseline: one input and one output
        self.add_input()
        self.add_output()

        # ensure library updated
        self.refresh_library()


# Composite node class near other classes

class Composite:
    def __init__(self, app, x, y, name, inputs, outputs):
        self.app = app
        self.x = x
        self.y = y
        self.name = name
        self.inputs_count = inputs
        self.outputs_count = outputs
        self.internal_inputs = []
        self.internal_outputs = []
        self.internal_nodes = []

        # visual container
        self.rect = app.canvas.create_rectangle(x, y, x + 140, y + max(60, inputs * 30, outputs * 30), fill="#f1f5f9", outline="#0f172a", width=2)
        self.text = app.canvas.create_text(x + 70, y + 15, text=name, font=("Helvetica", 10, "bold"), fill="#0f172a")

        # create input ports
        self.input_ports = []
        for i in range(inputs):
            py = y + int((i + 1) * (50 / (inputs + 1))) + 10
            pid = app.canvas.create_oval(x - 6, py - 6, x + 6, py + 6, fill="#f8fafc", outline="#1e293b")
            self.input_ports.append(pid)

        # create output ports
        self.output_ports = []
        for i in range(outputs):
            py = y + int((i + 1) * (50 / (outputs + 1))) + 10
            pid = app.canvas.create_oval(x + 140 - 6, py - 6, x + 140 + 6, py + 6, fill="#f8fafc", outline="#1e293b")
            self.output_ports.append(pid)

        self.items = [self.rect, self.text] + self.input_ports + self.output_ports

    def get_output_point(self, idx=0):
        py = self.y + int((idx + 1) * (50 / (self.outputs_count + 1))) + 10
        return (self.x + 140, py)

    def get_input_point(self, idx=0):
        py = self.y + int((idx + 1) * (50 / (self.inputs_count + 1))) + 10
        return (self.x, py)


root = tk.Tk()
root.geometry("1200x800")
Simulator(root)
root.mainloop()
