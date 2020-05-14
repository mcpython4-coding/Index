import github
import json
import os
import sys

token = None
if os.path.exists("auth.json"):
    # you may want to create an token stored under auth.json as {"token": <the token str>} to make more accessing
    # better
    with open("auth.json") as f:
        token = json.load(f)["token"]

with open("core.json") as f:
    data = json.load(f)

git = github.Github(login_or_token=token).get_repo("mcpython4-coding/core")

if input("re-do commits: ").lower() in ("y", "j", "1"):
    commits = list(git.get_commits(sha="dev"))
    m = len(commits)

    data["versions"]["dev_unstable"].clear()

    for i, commit in enumerate(commits):
        h = commit.url.split("/")[-1]
        d = commit.raw_data
        t = {"name": "dev:{}".format(h), "url": "https://github.com/mcpython4-coding/core/archive/{}.zip".format(h),
             "main": "__main__.py", "change": d["commit"]["message"]}
        data["versions"]["dev_unstable"].append(t)
        print("commit '{}' found ({}/{})".format(d["commit"]["message"].split("\n")[0], i + 1, m))

if input("re-do releases: ").lower() in ("y", "j", "1"):
    data["versions"]["release"].clear()
    data["versions"]["release"].append(
        {"name": "active_stable", "url": "https://github.com/mcpython4-coding/core/archive/release.zip",
         "main": "__main__.py", "type": "snapshot", "release_name": "unstable",
         "modifications": [{"mode": "remove", "path": "mods/TestMod"}]})

    for release in git.get_releases():
        data["versions"]["release"].append({"name": release.title, "url": release.zipball_url, "main": "__main__.py",
                                            "type": "stable" if not release.prerelease else "pre-release",
                                            "release_name": release.title})
        print("found release '{}' released on {}".format(release.title, release.created_at))

with open("core.json", mode="w") as f:
    json.dump(data, f)
