GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"
GRAPHQL_QUERY = """
query($queryString: String!){
  search(first: 50, type: ISSUE, query: $queryString) {
    nodes {
      ... on PullRequest {
        author {
          login
        }
        title
        permalink
        isDraft
        closed
        number
        updatedAt
        repository {
          nameWithOwner
        }
      }
    }
  }
}
"""
SEARCH_QUERY_FORMAT = "is:open is:pr archived:false user:{}"

TEAMS_PRS_MESSAGE_FORMAT = (
    """**\\[{}\\] [{}]({})**\r\n\r\n\\#{} created by @{}\r\n\r\n--------- \r\n\r\n"""
)
TEAMS_MESSAGE_TITLE_FORMAT = "Pull request reviews in {}"
