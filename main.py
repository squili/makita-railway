from github import Github
from jinja2 import Environment, Template
import os
import requests
import signal
import stat
import subprocess

gh = Github()

latest_release = gh.get_repo('squili/makita').get_latest_release()

print(f'[makita-railway] Makita version {latest_release.tag_name[1:]}')

download_url = next(filter(lambda asset: asset.name == 'makita', latest_release.get_assets())).browser_download_url

print(f'[makita-railway] Downloading {download_url}...')

r = requests.get(download_url, stream=True)
r.raise_for_status()

with open('makita', 'wb') as f:
    for block in r.iter_content(chunk_size=None):
        f.write(block)

print('[makita-railway] Configuring makita...')

os.chmod('makita', stat.S_IEXEC)

with open('config.jinja') as source, open('config.ron', 'w') as target:
    target.write(Environment().from_string(source.read()).render(
        token=os.environ['TOKEN'],
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['CLIENT_SECRET'],
        database_url=os.environ['DATABASE_URL'],
        host_addr=os.environ['HOST_ADDR'],
        owner_id=os.environ['OWNER_ID'],
        manager_guild=os.environ['MANAGER_GUILD'],
        github_webhook_secret=os.environ['GITHUB_WEBHOOK_SECRET'],
    ))

print(open('config.ron').read())

print('[makita-railway] Starting makita...')

child = subprocess.Popen(['./makita', 'run'], env=os.environ)
signal.signal(signal.SIGINT, lambda: child.kill())
child.wait()
