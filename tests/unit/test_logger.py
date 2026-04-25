# tests/unit/test_logger.py
import os
import sys
import logging
import pytest
from ds_e2e_project import logger  # import from your src package 


class TestLoggingSetup:

    def test_log_directory_is_created(self):
        assert os.path.isdir("logs")

    def test_log_file_is_created(self):
        assert os.path.isfile("logs/logging.log")

    def test_logger_name(self):
        assert logger.name == "ds_e2e_project_logger"

    def test_root_logger_level_is_info(self):
        assert logging.getLogger().level == logging.INFO

    def test_file_handler_exists(self):
        types = [type(h) for h in logging.getLogger().handlers]
        assert logging.FileHandler in types

    def test_stream_handler_points_to_stdout(self):
        stream_handlers = [
            h for h in logging.getLogger().handlers
            if type(h) is logging.StreamHandler
        ]
        assert stream_handlers[0].stream == sys.stdout

    def test_info_message_written_to_file(self):
        # record file size before writing
        log_path = "logs/logging.log"
        before = os.path.getsize(log_path) if os.path.exists(log_path) else 0

        logger.info("sentinel_test_message")
        for h in logging.getLogger().handlers:
            h.flush()

        with open(log_path) as f:
            f.seek(before)           # ← only read what was written in this test
            new_content = f.read()

        assert "sentinel_test_message" in new_content

    def test_debug_message_not_written(self):
        logger.debug("should_not_appear")
        with open("logs/logging.log") as f:
            assert "should_not_appear" not in f.read()