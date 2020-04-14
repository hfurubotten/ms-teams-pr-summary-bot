import logging
import os

import aiohttp
import pendulum

import __app__.shared.const as c

_LOGGER = logging.getLogger(__name__)


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
    msg = f"There are currently {len(nodes)} pull requests open.\n\n"
    for node in nodes:
        if bool(node["isDraft"]) or bool(node["closed"]):
            continue
        publishedAt = pendulum.parse(node["publishedAt"])
        duration = pendulum.now() - publishedAt
        msg += c.TEAMS_PRS_MESSAGE_FORMAT.format(
            node["repository"]["nameWithOwner"],
            node["title"],
            node["permalink"],
            node["number"],
            node["author"]["login"],
            " ".join(duration.in_words().split()[0:4]),
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
