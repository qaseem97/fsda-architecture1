# FSDA Multi-Language Gateway — Architecture B (Server)

Access the MATLAB **FSDA** toolbox from **Python, R, and Julia** through a single local HTTP server. No embedded Python interpreter inside R or Julia, no per-language MATLAB binding — every client just sends an HTTP request.

One local **FastAPI** server owns the one MATLAB Engine session and exposes a single generic route. The same MATLAB-side dispatcher (`FSDAEngine.m`) used in Architecture A is reused unchanged here.

```
Python client   ┐
R client         ├──► HTTP (localhost:8000) ──► FastAPI server ──► fsda_gateway.py ──► MATLAB Engine ──► FSDAEngine.m
Julia client    ┘
```

## Prerequisites

- MATLAB, with the **FSDA toolbox** installed via Add-On Manager
- Python 3.12
- R, with `httr`, `jsonlite`
- Julia, with `HTTP.jl`, `JSON.jl`

## Folder Structure

```
fsda-architecture1/
├── venv/                                  (created by setup, not committed)
├── src/
│   ├── gateways/
│   │   ├── fsda_gateway.py                Python gateway class (FSDA)
│   │   └── matlab_engine/
│   │       └── FSDAEngine.m               Generic MATLAB dispatcher (same as Architecture A)
│   └── server/
│       └── server.py                      FastAPI app — generic /call/{function_name} route
├── clients/
│   ├── python/
│   │   ├── fsda_client.py                 Generic Python client (__getattr__ dispatch)
│   │   └── test_client.py                 Run: python clients/python/test_client.py
│   ├── r/
│   │   ├── fsda_client.R                  Generic R client (httr)
│   │   └── test_client.R                  Run: Rscript clients/r/test_client.R
│   └── julia/
│       ├── fsda_client.jl                 Generic Julia client (HTTP.jl)
│       └── test_client.jl                 Run: julia clients/julia/test_client.jl
├── config.yaml
├── environment.yml
└── requirements.txt
```

> **Run every command from the project root** unless noted otherwise — paths inside the code are root-relative.

## Setup

### 1. Check your MATLAB version

```matlab
version
```

Note the release (e.g. `R2025b` → short version `25.2`). You'll need this to install a matching `matlabengine`.

### 2. Create the Python virtual environment

```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Python dependencies — version-matched to MATLAB

```cmd
venv\Scripts\python.exe -m pip install --upgrade pip
venv\Scripts\python.exe -m pip install matlabengine==25.2.* numpy pandas fastapi uvicorn
```

Replace `25.2` with your own MATLAB's short version number.

Confirm:

```cmd
venv\Scripts\python.exe -c "import matlab.engine; import fastapi; print('ALL OK')"
```

### 4. Install R packages

```r
install.packages(c("httr", "jsonlite"))
```

### 5. Install Julia packages

```julia
using Pkg
Pkg.add(["HTTP", "JSON"])
```

## Start the Server

From the project root, with `venv` activated:

```cmd
uvicorn src.server.server:app --port 8000
```

Wait for `Uvicorn running on http://127.0.0.1:8000` — this also starts the one MATLAB Engine session the server owns for its entire lifetime. Leave this terminal running.

## Run the Clients

In separate terminals, with the server still running:

```cmd
cd clients\python
python test_client.py
```

```cmd
cd clients\r
Rscript test_client.R
```

```cmd
cd clients\julia
julia test_client.jl
```

Each should print the same result for the `zscoreFS` test:

```
[[-0.674, -0.674, -0.674], [0.0, 0.0, 0.0], [0.674, 0.674, 0.674]]
```

## How It Works

- **`FSDAEngine.m`** — identical to Architecture A. A generic MATLAB dispatcher (`execute(funcName, varargin)`) that resolves any FSDA function by name via `str2func`.
- **`fsda_gateway.py`** — a Python class (`FSDA`) that starts **one** MATLAB Engine session when the server boots, and reuses it for every request via `feval('execute', ...)`.
- **`server.py`** — a FastAPI app with a single generic route, `POST /call/{function_name}`. It converts JSON arguments to `matlab.double`, calls the gateway, and serializes the result back to JSON (including MATLAB doubles, pandas DataFrames, and NaN values via a `make_json_safe()` helper).
- **Clients** — thin, generic wrappers in each language. None of them know anything about MATLAB; they only know the server's URL and send a function name + arguments as JSON.

## How It Differs From Architecture A

| | Architecture A (Embedded) | Architecture B (Server, this repo) |
|---|---|---|
| R / Julia dependency | `reticulate` / `PyCall` (embed Python) | `httr` / `HTTP.jl` (plain HTTP) |
| MATLAB session ownership | Shared session, or one per client | One session, owned solely by the server |
| Extra moving part | None | The server process must be running |
| Transport | In-process function calls | HTTP + JSON |

## Troubleshooting

| Problem | Fix |
|---|---|
| `matlabengine` build fails with a version mismatch | Re-check `version` in MATLAB and install the exact matching `matlabengine==<version>.*` |
| Server hangs on startup | MATLAB Engine can take 10–20 seconds to start — this is normal, wait for the Uvicorn line |
| `Connection refused` from a client | The server isn't running, or is on a different port — check the terminal running `uvicorn` |
| `NaN` or complex struct fields cause a 500 error | Extend `make_json_safe()` in `server.py` to handle the new MATLAB return type |
| Port 8000 already in use | Run with a different port: `uvicorn src.server.server:app --port 8001`, and update `config.yaml` / clients to match |
