# PythonGRpcClient

Python gRPC client library for automating measurements with the **Sparrow HD-MEA application**.

---

## Change History

### Sparrow App v4.10.2

**New functions**
- `bool WriteChipID(string chipID)`
- `string ReadChipID()`
- `bool CloseConfiguration(int id)`
- `bool ExportMeasurementData(string fullFilename)`

**Changed functions**
- `bool SetPixelMode(int pixelNr, int modeId)`
- `bool SetPixelModeWell(int wellNR, int modeId)`
- `bool SetPixelModeRow(int wellNr, int rowNr, int modeId)`
- `bool SetPixelModeColumn(int wellNr, int columnNr, int modeId)`
- `bool SetPixelModeRange(int pixelNrFrom, int pixelNrTo, int modeId)`

---

## Files

| File | Description |
|---|---|
| `contracts.proto` | gRPC service and message definitions |
| `contracts_pb2.py` | Auto-generated gRPC message classes |
| `contracts_pb2_grpc.py` | Auto-generated gRPC stub classes |
| `SparrowRpcService.py` | Client-side API — **use this in your own scripts** |
| `SparrowRpcService_demo*.py` | Usage examples (demo1–demo9) |
| `SparrowRpcService_test_*.py` | Automated test scripts |
| `scriptDemo.py` | Minimal getting-started script |
| `testing.ipynb` | Interactive Jupyter notebook for manual testing |
| `html/SparrowRpcService.html` | Auto-generated API reference (pdoc3) |

---

## Setup

### 1. Install Python

Download and install **Python 3.10.6** from [python.org](https://www.python.org/downloads/).

### 2. Install gRPC tools

```bash
pip install grpcio-tools
```

Quick-start reference: <https://grpc.io/docs/languages/python/quickstart/>

### 3. Install documentation generator (optional)

```bash
pip install pdoc3
```

### 4. IDE setup

**Visual Studio Code**
- Install the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- Install the `vscode-proto3` extension for `.proto` syntax highlighting
- Install the `python docstrings` extension

**Visual Studio**
- Run the Visual Studio Installer → **Modify** → **Workloads** tab → select **Python development** (deselect any specific Python version if you want to manage it yourself) → **Modify**

---

## Using the Client

Import `SparrowRpcService` in your script and call the available methods:

```python
from SparrowRpcService import SparrowRpcService

sparrow = SparrowRpcService()
chip_id = sparrow.ReadChipID()
print(f"Connected to chip: {chip_id}")
```

See the `SparrowRpcService_demo*.py` files for more complete examples covering configuration creation, acquisition control, stimulation, and data export.

---

## Extending the gRPC Interface

### Python side (client)

1. Edit `contracts.proto` to add or modify service methods and message types.

2. Regenerate the Python gRPC bindings:
   ```bash
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. contracts.proto
   ```
   This overwrites `contracts_pb2.py` and `contracts_pb2_grpc.py`.

3. Update `SparrowRpcService.py` to expose the new or changed methods.

4. Regenerate the HTML documentation:
   ```bash
   pdoc --html --force ./SparrowRpcService.py
   ```

### C# side (server)

1. Edit `contracts.proto` inside the `Tools → RpcServiceGenerateProtoFiles` Visual Studio project.

2. Build the `RpcServiceGenerateProtoFiles` project. Generated server code is automatically copied to:
   - `Imec.Informed.Application\ScriptingRpc`
   - `Sandbox\TestRpcService`

3. Implement changes in the server project (`Imec.Informed.Application`):
   - `IGRpcServiceHandler.cs` — interface definition
   - `ScriptingRpcService.cs` — translates gRPC calls to interface methods
   - `MainWindow.xaml.cs` — concrete implementation of all server functions
