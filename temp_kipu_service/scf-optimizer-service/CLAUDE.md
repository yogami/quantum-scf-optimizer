# CLAUDE.md
This file provides guidance to Claude Code (claude.ai/code) how to develop and deploy Managed Services on the Kipu Quantum Hub (formerly PLANQK platform).
It includes instructions for development, testing, deployment, and architecture overview.
More details about Managed Services can be found in the [Kipu Quantum Hub documentation](https://docs.hub.kipu-quantum.com/services/managed/introduction.html).

## Development Commands

### Environment Setup

Use `uv` for dependency management:

```bash
# Create virtual environment and install dependencies
uv venv
uv sync

# Activate the virtual environment
source .venv/bin/activate

# Update dependencies and lock file
uv sync -U

# Update requirements.txt after installing new packages
uv export --format requirements-txt --no-dev --no-emit-project > requirements.txt
uv export --format requirements-txt --only-dev --no-emit-project > requirements-dev.txt
```

### Using the PLANQK CLI
The PLANQK CLI lets you interact with the Kipu Quantum Hub directly from your terminal.
Always use the PLANQK CLI to interact with the PLANQK platform and test the service locally.

```bash
# Use this command to see available PLANQK CLI commands
planqk help

# Use this for verifying your code works.
# The command runs your project in a containerized environment and expose it through a local web server, similarly to how Kipu Quantum Hub would run your code. 
# The local web server exposes the same HTTP endpoints to start a service execution, to check the status of running executions, to cancel executions, and to retrieve execution results.
planqk serve

# Deploy to PLANQK platform
planqk up

# Execute deployed service
planqk run
```

## Architecture

### PLANQK Service Pattern

This project follows PLANQK's standardized service architecture:

1. **Entry Point**: `src/program.py` contains the `run()` function - the main entry point called by PLANQK runtime
2. **Input Handling**: PLANQK mounts JSON input files to `/var/runtime/input/` at runtime:
    - `data.json` - contains the `data` parameter
    - `params.json` - contains the `params` parameter
3. **Output Handling**: Service writes output to `/var/runtime/output/`:
    - `output.json` - returned as HTTP response from the Service API
    - Additional files (e.g., `hello.txt`, `hello.jpg`) are made available as downloadable links via HAL specification
4. **planqk.json**: The `planqk.json` file contains your service configuration and is used by the PLANQK CLI to deploy and run your service.
   It will be generated automatically by the PLANQK CLI and must be located in the root folder of your project.

Here is an example containing all supported fields:

``` json
{
  "name": "my-service",
  "descriptionFile": "README.md",
  "resources": {
    "cpu": 2,
    "memory": 4,
    "gpu": {
      "type": "NVIDIA_TESLA_T4",
      "count": 1
    }
  },
  "runtime": "PYTHON_TEMPLATE",
  "serviceId": "99487f0b-21f0-4256-8335-5179d416dbb4"
}
```

- **`name`**: The name of your service (required).
- **`descriptionFile`**: The name of a markdown file used as the description for your service. The file must be in the root folder of your project.
- **`resources`**: The resource configuration of your service (required).
    - **`cpu`**: The number of virtual CPU cores to allocate (required).
    - **`memory`**: The amount of memory in GB to allocate (required).
    - **`gpu`**: The GPU configuration of your service.
        - **`type`**: The type of GPU to allocate (`NVIDIA_TESLA_T4` or `NVIDIA_TESLA_V100`).
        - **`count`**: The number of GPUs to allocate.
- **`runtime`**: The runtime to use for your service (required). Use `PYTHON_TEMPLATE` for Python-based quantum services or `DOCKER` for custom docker images.
- **`serviceId`**: References a deployed service. Automatically added after a successful deployment (`planqk up`).


### Code Structure
- `src/program.py`: Contains the `run(data, params)` function which is the service entry point. Uses Pydantic models (`InputData`, `InputParams`, `CalculationResult`) to define input/output schemas
- `src/__main__.py`: Local testing wrapper that sets up input/output directories and calls `run()` via `planqk.commons.runtime.main.main()`
- `input/`: Test input files (`data.json`, `params.json`) for local development
- `openapi.yaml`: OpenAPI 3.1 specification describing the service API

### Key Constraints

**DO NOT rename these fixed entry points** (PLANQK runtime depends on them):
- The `src/` folder
- The `program.py` file
- The `run()` function inside `program.py`

### Input/Output Conventions

- Input parameters use Pydantic models for validation and schema definition
- Return values must be JSON-serializable (dict, string, Pydantic model, etc.)
- Use `planqk.commons.runtime.output.write_string_output()` for text files
- Use `planqk.commons.runtime.output.write_binary_output()` for binary files
- All output files written to the output directory become downloadable via the Service API

### Quantum Backend Integration

- Uses `planqk.qiskit.PlanqkQuantumProvider` to access quantum backends
- Authentication via `PLANQK_PERSONAL_ACCESS_TOKEN` environment variable or `planqk login`
- Available backends listed at https://platform.planqk.de/quantum-backends
- Example uses `azure.ionq.simulator` backend

### Always use the Service SDK to interact with services on the Kipu Marketplace
To interact with services from the Kipu Marketplace, always use the `planqk-service-sdk` package.
To subscribe to a service you need an application with consumer key and consumer secret.
You can create an application or get the credentials from an existin one using the `kipu-quantum-hub` MCP.
Once you have the credentials you can create a client and subscribe to services as shown below:

```python
from planqk.service.client import PlanqkServiceClient

# Create a client instance
client = PlanqkServiceClient(
    service_endpoint="https://<your_service_endpoint_url>",
    consumer_key="your_consumer_key",
    consumer_secret="your_consumer_secret"
)

# Prepare your input data and parameters
data = {"values": [1, 2, 3, 4, 5]}
params = {"algorithm": "quantum_fourier_transform", "shots": 1000}

# Start a service execution
execution = client.run(request={"data": data, "params": params})

# Wait for completion and get results
execution.wait_for_final_state()
result = execution.result()

print(f"Execution finished with status: {execution.status}")
print(f"Result: {result}")
```

For more examples use the get_code_documentation() tool of the `kipu-quantum-hub` MCP.

## Important Files

- `requirements.txt`: Runtime dependencies installed by PLANQK (must be kept in sync with `pyproject.toml`)
- `.planqkignore`: Files excluded from PLANQK deployment ZIP
- `planqk.json`: PLANQK service configuration (name, resources, runtime)
- `.python-version`: Specifies Python 3.11+ requirement

## Deployment Workflow

1. Test locally: `python -m src`
2. Test with PLANQK runtime: `planqk serve`
3. Deploy: `planqk up`
5. Once deployed, service exposes asynchronous HTTP API for execution, status checking, and result retrieval
