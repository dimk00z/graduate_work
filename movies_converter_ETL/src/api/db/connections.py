import sys
import traceback

import backoff
from db.postgres.connection import close_postgres, init_postgres
from loguru import logger


def backoff_handler(details):
    _, _, traceback_ = sys.exc_info()
    logger.debug(
        "backoff {wait:0.1f}s after {tries} tries "
        "calling function {target} with args {args} and kwargs {kwargs}".format(
            **details
        )
    )
    traceback.print_tb(traceback_)


@backoff.on_exception(
    wait_gen=backoff.expo,
    on_backoff=backoff_handler,
    max_tries=3,
    max_time=60,
    exception=Exception,
)
async def init_connections():
    await init_postgres()
    logger.success("Connected! :)")


async def close_connections():
    await close_postgres()
