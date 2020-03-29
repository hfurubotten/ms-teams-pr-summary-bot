# MS Team Pull Request Summary Bot

Highly experimental and hacky way of sending a summary list of pull requests, that's ready for review, to a MS Teams channel at a given time.

[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

## Setup

First of all you need a Azure Function to run this "bot" in, and then configure it with a PAT (Personal Access Token) and a web hook url to MS Teams.

Setup Azure Function:

1. [Create a Azure function][create-func] with storage account. _Consumption plan is recommended_
2. [Create a Key Vault][create-kv] to store the secrets needed by the app.
3. [Generate a Github PAT][github-pat] (Personal Access Token) with the needed access scopes listed below.
4. [Store your PAT][kv-secret] in your new Azure Key Vault as a secret.
5. [Add a Incoming Web-hook][create-teams-hook] in the MS Teams channel that should receive the summary messages, and copy the web-hook url.
6. Store your web-hook url in your Azure Key Vault as a secret. Follow the steps in the link above.
7. [Turn on Managed Service Identity(MSI)][func-msi] on your Azure function.
8. [Give your Azure Function MSI access][kv-access] to your Azure Key Vault with at least `secret:get` permission.
9. Configure the organization or username to search for pull requests for.
10. [Upload this Azure Function][publish-func] to your new Azure Function.

## Available configuration

| Configuration Name | Required | Description                                                             |
| ------------------ | -------- | ----------------------------------------------------------------------- |
| `GITHUB_PAT`       | yes      | Github Personal Access Token                                            |
| `GITHUB_ORG`       | yes      | Username or organization "login" name to search for pull requests under |
| `TEAMS_HOOK_URL`   | yes      | Incoming Web-hook url to MS Teams                                       |

## Github Scopes

The personal access token to Github needs the following permissions:

- `repo` - needed to find pull requests. Sadly, can't be restricted further down if pull requests should be found.
- `read:org` - needed when the bot should find pull requests within an organization. If used only with your personal account it's not needed.

> Note: If your organization has SSO required, remember to enable SSO for your PAT.

---

[create-func]: https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-azure-function#create-a-function-app
[create-kv]: https://docs.microsoft.com/en-us/azure/key-vault/quick-create-portal#create-a-vault
[github-pat]: https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line
[kv-secret]: https://docs.microsoft.com/en-us/azure/key-vault/quick-create-portal#add-a-secret-to-key-vault
[create-teams-hook]: https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook#add-an-incoming-webhook-to-a-teams-channel
[func-msi]: https://docs.microsoft.com/en-us/azure/app-service/overview-managed-identity?tabs=dotnet#add-a-system-assigned-identity
[kv-access]: https://docs.microsoft.com/en-us/azure/key-vault/managed-identity
[publish-func]: https://docs.microsoft.com/en-us/azure/key-vault/managed-identity
[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg
[buymeacoffee]: https://www.buymeacoffee.com/heine
