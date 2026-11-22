
import logging

from Jamal_project.logger import setup_logger


def test_setup_logger_creates_logger(tmp_path):
    log_file = tmp_path / "test.log"

    logger = setup_logger(
        name="test_logger_basic",
        level="DEBUG",
        log_file=str(log_file)
    )

    assert logger.name == "test_logger_basic"
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) == 2

    for handler in logger.handlers:
        handler.close()

    logger.handlers.clear()


def test_setup_logger_creates_log_directory(tmp_path):
    log_file = tmp_path / "logs" / "test.log"

    logger = setup_logger(
        name="test_logger_directory",
        log_file=str(log_file)
    )

    assert log_file.parent.exists()

    for handler in logger.handlers:
        handler.close()

    logger.handlers.clear()


def test_setup_logger_does_not_duplicate_handlers(tmp_path):
    log_file = tmp_path / "test.log"

    logger = setup_logger(
        name="test_logger_duplicate",
        log_file=str(log_file)
    )

    initial_count = len(logger.handlers)

    same_logger = setup_logger(
        name="test_logger_duplicate",
        log_file=str(log_file)
    )

    assert same_logger is logger
    assert len(logger.handlers) == initial_count

    for handler in logger.handlers:
        handler.close()

    logger.handlers.clear()


def test_setup_logger_invalid_level_defaults_to_info(tmp_path):
    logger = setup_logger(
        name="test_logger_invalid_level",
        level="INVALID",
        log_file=str(tmp_path / "test.log")
    )

    assert logger.level == logging.INFO

    for handler in logger.handlers:
        handler.close()

    logger.handlers.clear()
