import json
import os
import re

from pyngrok import ngrok
from github import Github, InputFileContent


CONFIG_FILE = 'config.json'
GIST_FILE = 'static-pi-ip.md'
BASE_CONTENT = """# Static Pi IP
[What is this?](https://github.com/Parsa2820/static-pi-ip)
"""


def generate_content(url, host_user):
    url_pattern = re.compile(r'tcp:\/\/(?P<addr>[0-9a-z.]+):(?P<port>[0-9]+)')
    match = url_pattern.match(url)
    return f"{BASE_CONTENT}\n```\nssh {host_user}@{match.group('addr')} -p {match.group('port')}\n```"


def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_dir, CONFIG_FILE)) as f:
        config = json.load(f)
    ngrok.set_auth_token(config['ngroktoken'])
    tunnel = ngrok.connect(22, 'http')
    github = Github(config['githubtoken'])
    gist = github.get_gist(tunnel.public_url, config['githubgistid'])
    content = InputFileContent(generate_content(host_user=config['hostuser']))
    gist.edit(files={GIST_FILE: content})


if __name__ == '__main__':
    main()
