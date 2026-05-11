# Learning on MEA

A Python application for running an uninstructed learning experiment on neuronal cultures grown on a High-Density Multi-Electrode Array (HD-MEA), based on the protocol described in *Shahaf & Marom (2001)*.

---

## Background

The experiment tests whether a neuronal network can be conditioned to respond to a stimulation electrode it initially ignores. A response-to-stimulus ratio (R/S) is used as the learning criterion: the network is considered to have learned when R/S drops below a defined threshold within a time window following each stimulation.

---

## Experiment Outline

1. Record spontaneous activity across the full chip to establish a **pre-learning baseline**.
2. Run a stimulation scan across electrodes to identify a suitable **target electrode** (R/S < 1).
3. Run the **learning paradigm**: stimulate the target electrode repeatedly until the criterion R/S ≥ threshold is met within a sliding 10-trial window, or until 30 iterations are completed.
4. After the learning phase, record spontaneous activity again to evaluate **learning-induced network changes**.
5. Optionally repeat the protocol on another active area.

---

## Project Structure

```
learning_protocol/
├── main.py                  # Entry point — initializes the GUI and starts the Tkinter event loop
├── GUIs.py                  # ExperimentGUI class — full Tkinter-based control panel
├── Experiment_control.py    # ExperimentControl class — orchestrates the acquisition and stimulation protocol
├── Calculations_functions.py# Signal analysis: threshold crossing detection
├── SimulatedTrace.py        # Simulated neural trace generators for offline testing
├── SparrowRpcService.py     # gRPC client API for the Sparrow HD-MEA application
├── electrode_select_GUI.py  # 16×16 grid GUI for selecting stimulation electrodes
├── Check_stim_GUI.py        # PyQt stimulation checker GUI
├── Sparrow_com.py           # Low-level Sparrow communication helpers
├── Baseline_cfg.yaml        # Configuration for baseline (no-stimulation) recordings
├── Recording_cfg.yaml       # Configuration for stimulation recordings and analysis
└── PythonGRpcClient/        # Standalone gRPC client library and demos (see its own README)
```

---

## Requirements

- Python 3.10+
- `grpcio` and `grpcio-tools`
- `numpy`, `pandas`
- `matplotlib`
- `PyYAML`
- `tkinter` (included with standard Python on Windows/macOS)
- A running instance of the **Sparrow HD-MEA application** (for live acquisition)

Install Python dependencies:

```bash
pip install grpcio grpcio-tools numpy pandas matplotlib pyyaml
```

---

## Quick Start

1. Set the default data path in the Sparrow application to your intended **streaming path** (fast, local SSD).
2. Launch the GUI:
   ```bash
   python main.py
   ```
3. In the GUI:
   - Click **Load Storage Path** — this sets the slow-storage destination and copies the YAML config files there.
   - Click **Load Stream Path** — this sets the fast-streaming destination.
   - Optionally click **Open Configurations** to review or edit the copied YAML files before the run.
   - Click **Choose stimulation electrode(s)** to select electrodes on the 16×16 grid.
   - Adjust experiment parameters (well number, max time, rest time, criterion, stimulation rate, experiment type).
   - Click **Start Experiment**.

---

## Configuration Files

### `Baseline_cfg.yaml`
Controls the full-chip spontaneous-activity recording (no stimulation).

| Key | Description |
|---|---|
| `main_cfg.config_name` | Name of the Sparrow configuration |
| `main_cfg.map_number` | Electrode map to use |
| `main_cfg.Stim` | Must be `False` for baseline |
| `Rec_cfg.rec_length_map` | Recording duration in seconds |
| `Rec_cfg.Gain` | Recording amplifier gain |

### `Recording_cfg.yaml`
Controls the stimulation recording and the analysis window.

| Key | Description |
|---|---|
| `main_cfg.map_number` | Electrode map to use |
| `main_cfg.Stim` | Must be `True` for stimulation runs |
| `Rec_cfg.rec_length_map` | Recording duration per map in seconds |
| `stim_cfg.time_before` | Pre-stimulus padding (s) |
| `stim_cfg.time_after` | Post-stimulus recording window (s) |
| `stim_cfg.stimulation_length` | Stimulus pulse duration (s) |
| `stim_cfg.stim_amp` | Stimulus amplitude (mV) |
| `time_window_settings.start_time` | Start of the response analysis window relative to stimulus onset (s) |
| `time_window_settings.end_time` | End of the response analysis window (s) |
| `calculations.threshold_scaling` | RMS multiplier used to define the spike-detection threshold |

---

## Key Components

### `GUIs.py` — `ExperimentGUI`
The main control panel. Handles all user interaction, directory creation, thread management, real-time logging, and live plotting. On start, it:
- Creates timestamped experiment directories under the streaming and storage paths.
- Spawns the experiment thread (`run_experiment`) and a clock-update thread.
- Polls a `log_queue` and a `plot_queue` every 100 ms to update the GUI safely from background threads.

### `Experiment_control.py` — `ExperimentControl`
Orchestrates the three-phase protocol:
- `run_basleine` — runs a timed baseline acquisition, checking for a stop signal every second.
- `run_preExperiment_stimulation` — scans electrodes to produce a pre-experiment stimulation trace.
- `run_Experiment_stimulation` — iterates up to 30 learning trials, evaluating the R/S criterion with a 10-trial sliding window.

> **Note:** gRPC calls to the Sparrow application are currently stubbed out with `#FIXME` comments. The experiment runs in simulation mode using `SimulatedTrace.py`.

### `Calculations_functions.py`
- `check_crossing(file_path, vector)` — reads thresholding parameters from a YAML file and returns `True` if the signal crosses the RMS-scaled threshold within the configured analysis window (sampled at 30 kHz).

### `SimulatedTrace.py`
Generates synthetic neural traces for offline development and testing:
- `generate_random_vector` — uniform noise baseline.
- `insert_peaks` — adds simulated spike peaks with learning-dependent probability (more consistent responses at higher iteration counts).
- `Single_electrode(iteration_number, rep_num)` — convenience wrapper used during experiment simulation.

### `SparrowRpcService.py`
A gRPC client wrapping the Sparrow HD-MEA application's RPC interface. Exposes Python methods for chip configuration, acquisition control, stimulation, data export, and impedance spectroscopy. See `PythonGRpcClient/README.md` for setup details.

### `electrode_select_GUI.py` — `GridSelector`
A 16×16 Tkinter grid that lets the user toggle individual electrodes or entire rows/columns before confirming a selection. The confirmed list is passed back to the GUI via a callback.

---

## Output Files

Each experiment run creates a timestamped directory (`<ChipID>_<DDMMYYYY>_well<N>`) under both the streaming and storage paths, containing:

| File | Description |
|---|---|
| `exp_parameters.txt` | All GUI parameter values at experiment completion |
| `log.txt` | Full text log of the experiment session |
| `Baseline_cfg.yaml` | Copy of the baseline config used |
| `Recording_cfg.yaml` | Copy of the recording/stimulation config used |

---

## Protocol Reference

A detailed LaTeX write-up of the experimental protocol is available in [`Protocol pdf/Protocol.tex`](Protocol%20pdf/Protocol.tex) (PDF: [`Protocol pdf/Protocol.pdf`](Protocol%20pdf/Protocol.pdf)).

---

## References

Shahaf, G., & Marom, S. (2001). Learning in networks of cortical neurons. *Journal of Neuroscience*, 21(22), 8782–8788.
