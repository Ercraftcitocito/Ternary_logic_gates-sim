import tkinter as tk
from tkinter import simpledialog

# -------- LÓGICA TERNARIA --------


def ternary_not(a):
    return -a


def ternary_min(a, b):
    return min(a, b)


def ternary_max(a, b):
    return max(a, b)


COLORS = {-1: "#d9534f", 0: "#888888", 1: "#5cb85c"}

# -------- NODOS --------


class Gate:
    def __init__(self, app, x, y, gate_type):
        self.app = app
        self.x = x
        self.y = y
        self.gate_type = gate_type
        self.value = 0

        # determine number of inputs (NOT -> 1, others -> 2)
        self.inputs_count = 1 if gate_type == "NOT" else 2
        self.input_wires = [None] * self.inputs_count

        self.rect = app.canvas.create_rectangle(x, y, x + 90, y + 50, fill="#f5f5f5")
        self.text = app.canvas.create_text(x + 45, y + 25, text=gate_type)

        # draw input ports on the left
        self.input_ports = []
        for i in range(self.inputs_count):
            py = y + int((i + 1) * (50 / (self.inputs_count + 1)))
            port = app.canvas.create_oval(x - 6, py - 6, x + 6, py + 6, fill="#ffffff", outline="#000000")
            self.input_ports.append(port)

        # output port on the right
        self.output_port = app.canvas.create_oval(x + 90 - 6, y + 25 - 6, x + 90 + 6, y + 25 + 6, fill="#ffffff", outline="#000000")

        self.items = [self.rect, self.text] + self.input_ports + [self.output_port]

    def get_output_point(self):
        return (self.x + 90, self.y + 25)

    def get_input_point(self, idx):
        py = self.y + int((idx + 1) * (50 / (self.inputs_count + 1)))
        return (self.x, py)


class InputNode:
    def __init__(self, app, x, y, name):
        self.app = app
        self.x = x
        self.y = y
        self.name = name
        self.value = 0

        self.rect = app.canvas.create_rectangle(
            x, y, x + 90, y + 50, fill=COLORS[self.value]
        )
        self.text = app.canvas.create_text(x + 45, y + 25, text=f"{name}\n0")

        # output port on right
        self.output_port = app.canvas.create_oval(x + 90 - 6, y + 25 - 6, x + 90 + 6, y + 25 + 6, fill="#ffffff", outline="#000000")

        self.items = [self.rect, self.text, self.output_port]

    def get_output_point(self):
        return (self.x + 90, self.y + 25)


class OutputNode:
    def __init__(self, app, x, y, name):
        self.app = app
        self.x = x
        self.y = y
        self.name = name
        self.value = 0

        self.rect = app.canvas.create_rectangle(
            x, y, x + 90, y + 50, fill=COLORS[self.value]
        )
        self.text = app.canvas.create_text(x + 45, y + 25, text=f"{name}\n0")

        # single input port on left
        self.input_wires = [None]
        self.input_port = app.canvas.create_oval(x - 6, y + 25 - 6, x + 6, y + 25 + 6, fill="#ffffff", outline="#000000")

        self.items = [self.rect, self.text, self.input_port]

    def get_input_point(self, idx=0):
        return (self.x, self.y + 25)


# -------- APP --------


class Simulator:
    def __init__(self, root):

        self.root = root
        root.title("Simulador Lógico Ternario")

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.bottom = tk.Frame(root)
        self.bottom.pack(fill="x", side="bottom")

        self.library = ["NOT", "MIN", "MAX"]

        self.nodes = []
        # connections: list of (src, dst, dst_idx)
        self.connections = []
        # map canvas wire id -> (src, dst, dst_idx)
        self.wire_items = {}

        self.drag_node = None
        self.drag_dx = 0
        self.drag_dy = 0

        self.connect_source = None
        self.temp_line = None

        tk.Button(self.bottom, text="Entrada", command=self.add_input).pack(side="left")

        tk.Button(self.bottom, text="Salida", command=self.add_output).pack(side="left")

        tk.Button(self.bottom, text="Guardar puerta", command=self.save_gate).pack(
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

    def refresh_library(self):
        for w in self.libframe.winfo_children():
            w.destroy()

        for gate in self.library:
            tk.Button(
                self.libframe, text=gate, command=lambda g=gate: self.add_gate(g)
            ).pack(side="left")

    def add_gate(self, gate):
        self.nodes.append(Gate(self, 250, 100, gate))

    def add_input(self):
        n = len([x for x in self.nodes if isinstance(x, InputNode)])
        self.nodes.append(InputNode(self, 20, 50 + n * 80, f"IN{n + 1}"))

    def add_output(self):
        n = len([x for x in self.nodes if isinstance(x, OutputNode)])
        self.nodes.append(OutputNode(self, 850, 50 + n * 80, f"OUT{n + 1}"))

    def node_at(self, x, y):
        item = self.canvas.find_closest(x, y)
        if not item:
            return None

        item = item[0]

        for node in self.nodes:
            if item in node.items:
                return node
        return None

    def left_click(self, event):
        node = self.node_at(event.x, event.y)

        if node:
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
                    dst.input_wires[idx] = None
                except Exception:
                    pass
                self.redraw_connections()
                self.evaluate()
                return

        node = self.node_at(event.x, event.y)
        if node is None:
            return

        # start a new connection from node
        self.connect_source = node
        sx, sy = None, None
        if hasattr(node, "get_output_point"):
            sx, sy = node.get_output_point()
        else:
            # nodes without output cannot start a connection
            self.connect_source = None
            return

        # create temporary line that follows cursor
        self.temp_line = self.canvas.create_line(sx, sy, event.x, event.y, width=2, dash=(4, 2), fill="#000", tags="temp")

    def connect_drag(self, event):
        if self.temp_line:
            coords = self.canvas.coords(self.temp_line)
            # update end point
            self.canvas.coords(self.temp_line, coords[0], coords[1], event.x, event.y)

    def end_connect(self, event):
        if not self.connect_source:
            # cleanup any temp line
            if self.temp_line:
                self.canvas.delete(self.temp_line)
                self.temp_line = None
            return

        dst = self.node_at(event.x, event.y)
        src = self.connect_source

        # cannot connect to self or to input nodes
        if dst is None or dst == src or isinstance(dst, InputNode):
            if self.temp_line:
                self.canvas.delete(self.temp_line)
                self.temp_line = None
            self.connect_source = None
            return

        # determine destination input index
        dst_idx = 0
        if isinstance(dst, Gate):
            # choose nearest input port
            best = None
            best_i = 0
            for i in range(dst.inputs_count):
                px, py = dst.get_input_point(i)
                d = (px - event.x) ** 2 + (py - event.y) ** 2
                if best is None or d < best:
                    best = d
                    best_i = i
            dst_idx = best_i
        elif isinstance(dst, OutputNode):
            dst_idx = 0

        # check slot free
        if getattr(dst, "input_wires", [None])[dst_idx] is not None:
            # slot occupied
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

            if isinstance(dst, Gate):
                dx, dy = dst.get_input_point(dst_idx)
            elif isinstance(dst, OutputNode):
                dx, dy = dst.get_input_point(dst_idx)
            else:
                dx, dy = dst.x, dst.y + 25

            iid = self.canvas.create_line(sx, sy, dx, dy, width=3, fill=color, tags="wire", arrow=tk.LAST)
            self.wire_items[iid] = (src, dst, dst_idx)

    def double_click(self, event):

        node = self.node_at(event.x, event.y)

        if isinstance(node, InputNode):
            values = [-1, 0, 1]

            idx = values.index(node.value)
            node.value = values[(idx + 1) % 3]

            self.canvas.itemconfig(node.rect, fill=COLORS[node.value])

            self.canvas.itemconfig(node.text, text=f"{node.name}\n{node.value}")

            self.evaluate()

    def incoming(self, target):
        # return list of source nodes connected to target in input order
        if isinstance(target, Gate):
            return [s for s in target.input_wires if s is not None]
        if isinstance(target, OutputNode):
            return [target.input_wires[0]] if target.input_wires and target.input_wires[0] is not None else []

        # fallback: scan connections
        result = []
        for src, dst, idx in self.connections:
            if dst == target:
                result.append(src)
        return result

    def evaluate(self):

        for _ in range(10):
            for node in self.nodes:
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
                        self.canvas.itemconfig(node.rect, fill=COLORS[node.value])
                    except Exception:
                        pass

                elif isinstance(node, OutputNode):
                    ins = self.incoming(node)

                    if ins:
                        node.value = ins[0].value

                        self.canvas.itemconfig(node.rect, fill=COLORS[node.value])

                        self.canvas.itemconfig(
                            node.text, text=f"{node.name}\n{node.value}"
                        )

        self.redraw_connections()

    def save_gate(self):

        name = simpledialog.askstring("Nueva puerta", "Nombre:")

        if not name:
            return

        self.library.append(name)
        self.refresh_library()


root = tk.Tk()
root.geometry("1200x800")
Simulator(root)
root.mainloop()
