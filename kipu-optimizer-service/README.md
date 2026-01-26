# planqk-starter-python

This is the PLANQK starter template for Python projects.
With only a few more steps, your quantum code is ready to be deployed as a PLANQK Service!

## Project Structure

Your code must be structured in a (not too) specific way.
The template provides a basic structure for your project:

```
.
├── .dockerignore
├── .gitignore
├── .planqkignore
├── .python-version
├── Dockerfile
├── pyproject.toml
├── README.md
├── requirements.txt
├── requirements-dev.txt
├── .devcontainer
│   └── ...
├── input
│   └── ...
├── notebooks
│   └── ...
└── src
    ├── __init__.py
    ├── __main__.py
    └── program.py
```

Your main entry point is the `program.py` file, which contains the `run()` method.
In [Extending the Starter Template](#extending-the-starter-template), you will find more information on how to extend the project.

## Run the Starter Template

### Set up the Environment

We recommend creating a dedicated Python environment to install and track all required packages from the start.
You may use the `requirements.txt` file to create a virtual environment with the tooling of your choice.
In the following, we use [`uv`](https://github.com/astral-sh/uv) to create a new virtual environment and install the required packages:

```bash
uv venv
uv sync

source .venv/bin/activate
```

You can use the following command to update the dependencies and the `uv.lock` file:

```bash
uv sync -U
```

If you are using `uv`, you have to update the requirements files after installing new packages:

```bash
uv export --format requirements-txt --no-dev --no-emit-project > requirements.txt
uv export --format requirements-txt --only-dev --no-emit-project > requirements-dev.txt
```

### Run the code

You can run the code by executing the following command:

```bash
python -m src
```

By this, the `src` folder is executed as a Python module and the `__main__.py` is executed.
The `__main__.py` is prepared to read the input data from the `input` directory and to call the `run()` method of `program.py`.

**This is helpful for local testing.**
Locally, you can test your code with a JSON-conform input that gets imported within the `__main__`-method.
You can use the files in the `input` folder to provide the required input data for your service.
You may adjust the `__main__`-method, for example, to load a different set of input from the `input` folder or to execute the
`run()` method with some static input.

**However, when bundling the code and deploying it to PLANQK, the runtime will call the**
**`run()` method directly with the input data provided via the Service API.**

Next, you learn how to extend the project and how you can work with input from the Service API as well as how to produce output.

## Extending the Starter Template

From the start, you should be able to run `python -m src` from within the project folder.
To extend the project, the most important method is the `run()` method inside `program.py`.

In the `run()` method you can define parameters that represent the user input through the Service API.
PLANQK ensures that the input provided via the Service API, e.g., in the form of
`{ "data": { ... }, "params": { ... } }`, is provided to your code at runtime and mapped to the parameters of the `run()` method, e.g.,
`data: Dict[str, Any]` and `params: Dict[str, Any]`.

You may use any Python type, e.g., dictionaries, lists, or simple types, to define what your Service API expects as JSON request body.
Further, you can use Pydantic models to define any complex input structure, which would also cover the validation of the input data.

> In-Depth: Input
>
> PLANQK ensures that the input provided via the Service API in the form of
> `{ "data": <data>, "params": <params> }` is mounted to the container at runtime.
> For example, given the input `{ "data": { "values": [1, 2, 3] }, "params": { "round_up": true } }`, the runtime creates the following files:
>
> - `data.json` with the content `{ "values": [1, 2, 3] }`
> - `params.json` with the content `{ "round_up": true }`
>
> These files are mounted into `/var/runtime/input` of the running container.
>
> The input for a service must always be a valid JSON object.

If you have written packages by yourself, which are required for your service, you can simply put them into separate Python packages within the
`src` folder.
Any required Python package (like `numpy`, `pandas`, ...) must be mentioned within, you guessed it, the `requirements.txt` file.
Once you have installed your dependencies to local virtual environment, you can import these packages within any Python file needed.

For output, we recommend to return a type or object that is JSON-serializable, for example, a dictionary or a Pydantic model.
PLANQK tries to serialize the return value of the `run()` method either to JSON or to a string.
It is then written to an `output.[json|txt]` file in the `output` directory.

The content of the `output.json` file will be returned as the HTTP response of the result endpoint of the Service API.

> In-Depth: Output
>
> PLANQK treats any file written to `/var/runtime/output` as the output of the service.
> Output that should be returned as a Service API response of the result endpoint must be written to the file `output.json`.
> Any other file written to `/var/runtime/output` can later be downloaded by the user.
> Respective links are provided in the Service API response of the result endpoint, according to the [HAL specification](https://stateless.group/hal_specification.html).
> For example, if you write a file `result.txt` to `/var/runtime/output`, the result response will contain the following link to download the file:
> `https://<service-endpoint>/<service-execution-id>/result/result.txt`.
>
> We recommend to only use additional files for large outputs that should be downloaded by the user.

> **IMPORTANT:**
> Do not rename either the `src` folder, the `program.py` package, as well as the `run()`-method inside `program.py`.
> These are fixed entry points for the service.
> Changing their names will result in a malfunctioning service.

## Run the Project using Docker

You may utilize Docker to run your code locally and test your current implementation.
In general, by following the next steps you replicate the steps done by PLANQK, which is a way to verify your service in an early stage.

Build the Docker image:

```bash
docker build --pull -t planqk-starter-python .
```

You can use the `input` directory to provide respective input files for testing.
Remember to provide input files according to the parameters of your `run()` method.
For example, if you expect a `data: Dict[str, Any]` parameter, you should test with the file `data.json`.

The return value of the `run()` method must be JSON-serializable object or type.
For example, a dictionary, a string, or a Pydantic model.
Depending on the type, the output is written to the `output.json` or `output.txt` file.
Further, any other file written to `/var/runtime/output` is treated as an additional output file that can be downloaded by the user.

By using the command below, all possible outputs will be available in the `out` directory after the container has finished running.

Start the Docker container:

```bash
PROJECT_ROOT=(`pwd`)
docker run -it \
  -e LOG_LEVEL=DEBUG \
  -e PLANQK_PERSONAL_ACCESS_TOKEN=plqk_LknW8yE... \
  -v $PROJECT_ROOT/input:/var/runtime/input \
  -v $PROJECT_ROOT/out:/var/runtime/output \
  planqk-starter-python
```

> **HINT**:
> For GitBash users on Windows, replace
> ```bash
> PROJECT_ROOT=(`pwd`)
> ```
> with
> ```bash
> PROJECT_ROOT=(/`pwd`)
> ```
> For Windows command-prompt users, you can define the volume mounts using `-v %cd%/input:/var/runtime/input` and `-v %cd%/out:/var/runtime/output`.

## Add Additional Dependencies

Although this template provides a `pyproject.toml` file to manage dependencies, PLANQK expects a
`requirements.txt` file in the root directory of your project.
This file should contain all required Python packages for your project.
The runtime installs these packages in a virtual environment when containerizing your project.

You can either add additional dependencies required at runtime by adding them to the `requirements.txt` file, or you can use tools to generate the
`requirements.txt` file based on the dependencies defined by the `pyproject.toml`.
For example, you can use `uv` to generate the `requirements.txt` file:

```bash
uv export --format requirements-txt --no-dev --no-emit-project > requirements.txt
```

## Keep your 'Ignore' Files Updated

Make sure to keep your `.gitignore`, `.dockerignore`, and `.planqkignore` files updated:

- `.gitignore` should contain files and directories that should not be tracked by Git.
- `.dockerignore` should contain files and directories that should be excluded from the Docker build context.
- `.planqkignore` should contain files and directories that should be excluded from the PLANQK ZIP file when using `planqk compress`.

## Describe your API using OpenAPI Specification v3.0

When your project is deployed to PLANQK, a published service exposes an API to asynchronously execute it.
A proper API description will help users of your service to understand how to use it.
It is the technical interface of your API product and describes the input and output data that is required to execute the service

Create a `openapi.yaml` file in the root directory of your project to describe your API using the OpenAPI Specification v3.0.
Run `planqk openapi` or download PLANQK's [template](https://docs.planqk.de/files/openapi-planqk-service.yaml) and use it as a starting point.

More information can be found in the [PLANQK documentation](https://docs.planqk.de/services/managed/openapi.html).

## Next Steps

Use `planqk serve` to run your project locally and expose it through a local web server, similarly to how PLANQK would run your code.
The local web server exposes the same HTTP endpoints to start a service execution, to check the status of running executions, to cancel executions, and to retrieve execution results.

Use `planqk up` to deploy your service to the PLANQK Platform.
Next, you may use `planqk run` to execute your service.
For more information, see the [PLANQK documentation](https://docs.planqk.de/quickstart.html).

However, you can also create a PLANQK Service manually via the PLANQK UI at <https://platform.planqk.de>.
To do so, you can use `planqk compress` to create a ZIP file that you can upload to the platform.

As soon as the service is ready to use, you will be able to run PLANQK Jobs to execute your service.
Further, you may publish it for internal use or into the PLANQK Marketplace to share it with other users.
