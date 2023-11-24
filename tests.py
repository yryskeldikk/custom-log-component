import unittest
from unittest.mock import patch
import time
from datetime import datetime, timedelta
from log_component import LogComponent


class TestLogger(unittest.TestCase):
    log_directory = "test_logs"

    def test_write_info(self):
        logger = LogComponent(log_directory=self.log_directory)
        logger.info("Test log message")
        logger.stop(wait=True)

        logs = self.get_logs_from_file()
        self.assertTrue(logs, "No logs found")
        self.assertTrue(
            "INFO: Test log message" in logs[-1], "Expected log message not found"
        )

    def test_write_error(self):
        logger = LogComponent(log_directory=self.log_directory)
        logger.error("Test log message")
        logger.stop(wait=True)

        logs = self.get_logs_from_file()
        self.assertTrue(logs, "No logs found")
        self.assertTrue(
            "ERROR: Test log message" in logs[-1], "Expected log message not found"
        )

    def test_write_debug(self):
        logger = LogComponent(log_directory=self.log_directory)
        logger.debug("Test log message")
        logger.stop(wait=True)

        logs = self.get_logs_from_file()
        self.assertTrue(logs, "No logs found")
        self.assertTrue(
            "DEBUG: Test log message" in logs[-1], "Expected log message not found"
        )

    def test_write_warning(self):
        logger = LogComponent(log_directory=self.log_directory)
        logger.warning("Test log message")
        logger.stop(wait=True)

        logs = self.get_logs_from_file()
        self.assertTrue(logs, "No logs found")
        self.assertTrue(
            "WARNING: Test log message" in logs[-1], "Expected log message not found"
        )

    @patch("log_component.log_component.datetime")
    def test_cross_midnight(self, mock_datetime):
        # Test that new files are created if midnight is crossed
        logger = LogComponent(log_directory=self.log_directory)
        custom_date = datetime(2022, 1, 1, 12, 0, 0)

        mock_datetime.now.return_value = custom_date
        logger.info("Log message after crossing midnight")
        logger.stop(wait=True)

        logs = self.get_logs_from_file(
            f"./{logger.log_directory}/{custom_date.strftime('log_%Y%m%d.log')}"
        )
        self.assertTrue(logs, "No logs found for the new day")
        self.assertTrue("INFO: Log message after crossing midnight" in logs[-1])

    def test_stop_behavior(self):
        # Test that stop behavior is working as described
        logger = LogComponent(log_directory=self.log_directory)

        logger.info("Log message 1")
        logger.info("Log message 2")
        logger.stop(wait=False)
        
        logger = LogComponent(log_directory=self.log_directory)
        logger.info("Log message 3")
        logger.stop(wait=True) 

        logs = self.get_logs_from_file()
        self.assertFalse(
            any("INFO: Log message 2" in log for log in logs), "Last log should be missing"
        )

        logs = self.get_logs_from_file()
        self.assertTrue(logs, "No logs found")
        self.assertTrue("INFO: Log message 3" in logs[-1], "Last log should be present")

    # Helper method to retrieve logs from the log file
    def get_logs_from_file(self, filename=None):
        if filename is None:
            filename = f"./test_logs/{datetime.now().strftime('log_%Y%m%d.log')}"
        with open(filename, "r") as file:
            return file.readlines()


if __name__ == "__main__":
    unittest.main()
