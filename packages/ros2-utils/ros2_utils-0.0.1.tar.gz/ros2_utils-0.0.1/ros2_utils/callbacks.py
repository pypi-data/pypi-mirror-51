import rclpy


def log_level(msg, node):
    '''
    '''
    logger = node.get_logger()
    try:
        new_log_level = getattr(rclpy.logging.LoggingSeverity, msg.data)
        if new_log_level == logger.get_effective_level():
            logger.info(f'New log level {new_log_level} is the same as current. Not setting.')
        else:
            logger.set_level(getattr(rclpy.logging.LoggingSeverity, msg.data))
            logger.info(f'Set new log level {new_log_level}.')
    except AttributeError as e:
        logger.error(f'Failed to set new log level {msg.data}. Exception: {e}')
