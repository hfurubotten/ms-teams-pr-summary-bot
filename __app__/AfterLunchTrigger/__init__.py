import datetime
import logging
import os

import aiohttp
import azure.functions as func

import __app__.shared.const as c
from __app__.shared import fetch_prs, format_teams_msg, send_msg_to_teams

_LOGGER = logging.getLogger(__name__)


async def main(my_timer: func.TimerRequest) -> None:
    _LOGGER.info("Starting review-ready PR list collection.")
    async with aiohttp.ClientSession(raise_for_status=True) as client:
        nodes = await fetch_prs(client)
        _LOGGER.info("Fetched PR list. Starting format of message.")
        msg = format_teams_msg(nodes)
        _LOGGER.info("Sending message to Teams.")
        await send_msg_to_teams(client, msg)
