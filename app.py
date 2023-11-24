from log_component import LogComponent


if __name__ == "__main__":
    logger = LogComponent()

    logger.info("Hello World")
    logger.error("Hello World")
    logger.debug("Hello World")
    logger.warning("Hello World")
    logger.stop(wait=True)