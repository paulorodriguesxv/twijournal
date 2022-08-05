import logging

from decouple import config
from logging import Logger

class DefaultConfig():
    PORT = config("PORT", 8000)
    LOG_LEVEL = logging.INFO
    MAX_POSTS_PER_PAGE = config("MAX_POSTS_PER_PAGE", cast=int, default=5)
    POST_URI = config("POST_URI", "http://localhost:8000/posts/")
    FEED_URI = config("FEED_URI", "http://localhost:8000/feeds/")
    USER_MAX_POST_PER_DAY = config("USER_MAX_POST_PER_DAY", cast=int, default=5)
    MAX_FEED_POSTS_PER_PAGE = config("MAX_FEED_POSTS_PER_PAGE", cast=int, default=10)

    @staticmethod
    def init_logging() -> Logger:
        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                            level=DefaultConfig.LOG_LEVEL)
        
        logger = logging.getLogger()
        logger.setLevel(DefaultConfig.LOG_LEVEL)        

        return logger
