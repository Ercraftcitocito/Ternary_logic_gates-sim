# 🚀 Quick Start Guide

## For Linux Users

1. **Open Terminal** and navigate to the project:
   ```bash
   cd Ternary_logic_gates-sim
   ```

2. **Start the server**:
   ```bash
   ./start-server.sh
   ```
   Or manually:
   ```bash
   python3 -m http.server 8000
   ```

3. **Open your browser** to: `http://localhost:8000`

## For Windows Users

1. **Open Command Prompt** and navigate to the project:
   ```cmd
   cd Ternary_logic_gates-sim
   ```

2. **Start the server** by double-clicking `start-server.bat`
   Or run manually:
   ```cmd
   python -m http.server 8000
   ```

3. **Open your browser** to: `http://localhost:8000`

## Alternative: Direct File Opening

Simply **double-click** `index.html` to open it directly in your default browser without needing a server.

## First Steps

1. **Add some gates**: Click "Add NOT Gate", "Add MAX Gate", or "Add MIN Gate"
2. **Check inputs/outputs**: You'll see 2 inputs and 1 output by default
3. **Draw connections**: Click and drag from an input/gate to create connections
4. **Adjust values**: Use the sliders on the right sidebar to change input values
5. **Watch real-time evaluation**: Outputs update instantly

## Common Issues

**"Port 8000 already in use?"**
```bash
python3 -m http.server 8001  # Use port 8001 instead
```

**"Python not found?"**
- Install from: https://www.python.org/downloads/
- Or use Node.js: `npm install && npm run serve`

**"Gates not responding?"**
- Press F12 to open developer console for error messages
- Refresh the page (Ctrl+R)
- Clear browser cache

## Testing

Verify everything works with:
```bash
node test.js
```

---

**Happy designing! 🎛️**
