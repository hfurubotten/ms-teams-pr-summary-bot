import datetime
import logging
import os

import aiohttp
import azure.functions as func

import __app__.AfterLunchTrigger.const as c

_LOGGER = logging.getLogger(__name__)


async def main(mytimer: func.TimerRequest) -> None:
    _LOGGER.info("Starting-review ready PR list collection.")
    async with aiohttp.ClientSession(raise_for_status=True) as client:
        nodes = await fetch_prs(client)
        _LOGGER.info("Fetched PR list. Starting format of message.")
        msg = format_teams_msg(nodes)
        _LOGGER.info("Sending message to Teams.")
        await send_msg_to_teams(client, msg)


async def fetch_prs(client) -> dict:
    async with client.post(
        c.GITHUB_GRAPHQL_URL,
        headers={"Authorization": "Bearer {}".format(os.environ["GITHUB_PAT"])},
        json={
            "query": c.GRAPHQL_QUERY,
            "variables": {
                "queryString": c.SEARCH_QUERY_FORMAT.format(os.environ["GITHUB_ORG"])
            },
        },
    ) as resp:
        body = await resp.json()
        return body["data"]["search"]["nodes"]


def format_teams_msg(nodes) -> dict:
    msg = ""
    for node in nodes:
        if bool(node["isDraft"]) or bool(node["closed"]):
            continue
        msg += c.TEAMS_PRS_MESSAGE_FORMAT.format(
            node["repository"]["nameWithOwner"],
            node["title"],
            node["permalink"],
            node["number"],
            node["author"]["login"],
        )

    return {
        "@context": "https://schema.org/extensions",
        "@type": "MessageCard",
        "themeColor": "0072C6",
        "title": c.TEAMS_MESSAGE_TITLE_FORMAT.format(os.environ["GITHUB_ORG"]),
        "text": msg,
    }


async def send_msg_to_teams(client, msg) -> None:
    async with client.post(os.environ["TEAMS_HOOK_URL"], json=msg) as resp:
        _LOGGER.info(
            "Got status '%s' and message '%s' from teams.",
            resp.status,
            await resp.text(),
        )
