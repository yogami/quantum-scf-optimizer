import base64
import logging
import time
from typing import Dict, Any

from loguru import logger
from planqk.commons.runtime.output import write_string_output, write_binary_output
from planqk.qiskit import PlanqkQuantumProvider
from pydantic import BaseModel, Field
from qiskit import QuantumCircuit, transpile

from .planqk_sample_image import image_data_base64


# Pydantic model to express what kind of input data is expected. The model, together with the parameter name of the
# run() function, defines that the input of the Service API is expected to be `{ "data": { "n_coin_tosses": 2 } }`.
class InputData(BaseModel):
    n_coin_tosses: int = Field(default=2)


# Pydantic model to express what kind of input params are expected. The model, together with the parameter name of the
# run() function, defines that the input of the Service API is expected to be `{ "params": { "shots": 100 } }`.
class InputParams(BaseModel):
    shots: int = Field(default=100)


# Pydantic model to define how the output data will look like. The respective return value will be returned by the
# service's HTTP API and looks like `{ "counts": { "0000": 6, "0001": 9, ... }, "elapsed_time": 8.725992918014526 }`.
class CalculationResult(BaseModel):
    counts: Dict[str, Any]
    elapsed_time: float


def run(data: InputData, params: InputParams) -> CalculationResult:
    """
    Coin Toss: Here we build a circuit (quantum algorithm) that performs n coin tosses on a
    Quantum Computer. Instead of heads and tails, we work with 0s and 1s: there are 2^n possible
    outcomes, and each time (number of shots) we measure the quantum state, we observe one of
    these outcomes.
    """
    circuit = QuantumCircuit(data.n_coin_tosses)
    for i in range(data.n_coin_tosses):
        circuit.h(i)
    circuit.measure_all()

    # If you deploy the project to PLANQK, you can just create a default instance of the
    # PlanqkQuantumProvider. For local testing, you may use the PLANQK CLI and log in with
    # "planqk login" or set the environment variable PLANQK_PERSONAL_ACCESS_TOKEN.
    # Alternatively, you can pass the access token as an argument to the constructor:
    # provider = PlanqkQuantumProvider(access_token="YOUR_PERSONAL_ACCESS_TOKEN_HERE")
    provider = PlanqkQuantumProvider()

    # Select a quantum backend suitable for the task. All PLANQK supported quantum backends are
    # listed at https://platform.planqk.de/quantum-backends.
    backend = provider.get_backend("azure.ionq.simulator")

    start_time = time.time()

    # Transpile the circuit and run it on the selected backend
    circuit = transpile(circuit, backend)
    job = backend.run(circuit, shots=params.shots)
    counts = job.result().get_counts()

    elapsed_time = time.time() - start_time

    # Print the counts to the console
    print(counts)
    # You may use a loguru logger to log messages instead of print()
    logger.debug(f"Job result: {counts}")
    # Alternatively, you may use Python's built-in logging module to log messages
    logging.debug(f"Elapsed time: {elapsed_time}")

    # We have to cast the values in the job's counts dictionary to integers to ensure that it can be serialized to JSON.
    counts = {str(k): int(v) for k, v in counts.items()}

    # Return the result, which will be available through the result endpoint of the Service API.
    return_value = CalculationResult(counts=counts, elapsed_time=elapsed_time)

    # You may output additional data by writing files to the output directory. You can write any form of text file:
    write_string_output("hello.txt", "Hello World!")
    # ... or binary files:
    image_data = base64.b64decode(image_data_base64)
    write_binary_output("hello.jpg", image_data)

    return return_value
