# LogComponent

## Overview

`LogComponent` is a simple logging module designed for asynchronous writing of log messages to files. It provides a straightforward interface for writing log entries of different levels (INFO, WARNING, ERROR, DEBUG) to timestamped log files.

## Features

- **Asynchronous Writing:** Log entries are written asynchronously, allowing the calling application to continue its work without waiting for log files to be written.

- **Timestamped Log Files:** Log entries are written to files with filenames based on the current date, allowing for easy organization and retrieval of logs.

- **Graceful Shutdown:** The component can be stopped in two ways:
  - Immediate Stop: Stop the component right away, even if there are outstanding log entries.
  - Wait for Finish: Stop the component after finishing writing outstanding log entries.

## Usage

1. **Initialization:**

   ```python
   from log_component import LogComponent

   logger = LogComponent(log_file_format="log_%Y%m%d.log", log_directory="logs")

2. **Writing Log Entries::**
    ```python
    logger.info("This is an information message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.debug("This is a debug message.")

2. **Writing Log Entries::**
- Immediate Stop
    ```python
    logger.stop(wait=False)

- Wait for Finish:
    ```python
    logger.stop(wait=True)


# Unit Tests

**Unit tests are included to validate the following:**

- A call to write results in writing something.
- New log files are created if midnight is crossed.
- The stop behavior works as described (both immediate and waiting for finish).
