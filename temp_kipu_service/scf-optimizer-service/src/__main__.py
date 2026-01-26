import os

from planqk.commons.constants import OUTPUT_DIRECTORY_ENV, INPUT_DIRECTORY_ENV, ENTRYPOINT_ENV, DATAPOOL_DIRECTORY_ENV
from planqk.commons.logging import init_logging
from planqk.commons.runtime.main import main

init_logging()

# Determine entrypoint, use from environment or set to "src.program:run" for local testing
entrypoint = os.environ.get(ENTRYPOINT_ENV, "src.program:run")

# Set input and output directories, use from environment or set to "./input" and "./out" for local testing
input_directory = os.environ.get(INPUT_DIRECTORY_ENV, "./input")
datapool_directory = os.environ.get(DATAPOOL_DIRECTORY_ENV, "./input")
os.makedirs(input_directory, exist_ok=True)
output_directory = os.environ.get(OUTPUT_DIRECTORY_ENV, "./out")
os.makedirs(output_directory, exist_ok=True)

# Overwrite environment variables, so that they are used by main()
os.environ[ENTRYPOINT_ENV] = entrypoint
os.environ[INPUT_DIRECTORY_ENV] = input_directory
os.environ[DATAPOOL_DIRECTORY_ENV] = datapool_directory
os.environ[OUTPUT_DIRECTORY_ENV] = output_directory

rc = main()

exit(rc)
