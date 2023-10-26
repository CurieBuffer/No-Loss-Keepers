import base64
import datetime
import json

import requests


def push_to_repo_branch(
    gitHubFileName, fileName, repo_slug, branch, user, email, token
):
    """
    Push file update to GitHub repo

    :param gitHubFileName: the name of the file in the repo
    :param fileName: the name of the file on the local branch
    :param repo_slug: the github repo slug, i.e. username/repo
    :param branch: the name of the branch to push the file to
    :param user: github username
    :param token: github user token
    :return None
    :raises Exception: if file with the specified name cannot be found in the repo
    """

    message = "Automated update " + str(datetime.datetime.now())
    path = "https://api.github.com/repos/%s/branches/%s" % (repo_slug, branch)
    r = requests.get(path, auth=(user, token))
    if not r.ok:
        print("Error when retrieving branch info from %s" % path)
        print("Reason: %s [%d]" % (r.text, r.status_code))
        raise
    rjson = r.json()
    treeurl = rjson["commit"]["commit"]["tree"]["url"]
    r2 = requests.get(treeurl, auth=(user, token))
    if not r2.ok:
        print("Error when retrieving commit tree from %s" % treeurl)
        print("Reason: %s [%d]" % (r2.text, r2.status_code))
        raise
    r2json = r2.json()
    sha = None

    for file in r2json["tree"]:
        # Found file, get the sha code
        if file["path"] == gitHubFileName:
            sha = file["sha"]

    # if sha is None after the for loop, we did not find the file name!
    if sha is None:
        print("Could not find " + gitHubFileName + " in repos 'tree' ")
        raise Exception

    with open(fileName, "rb") as data:
        # print(data.read())
        content = base64.b64encode(data.read()).decode("utf-8")

    # gathered all the data, now let's push
    inputdata = {}
    # inputdata["path"] = gitHubFileName
    inputdata["branch"] = branch
    inputdata["message"] = message
    inputdata["content"] = content
    inputdata["committer"] = {"name": user, "email": email}
    if sha:
        inputdata["sha"] = str(sha)

    # import requests

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    url = f"https://api.github.com/repos/{repo_slug}/contents/{gitHubFileName}"

    response = requests.put(
        url,
        headers=headers,
        data=json.dumps(inputdata),
    )
    print(response)
