import subprocess


gh_cli = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
p = subprocess.run(gh_cli, capture_output=True)
tag = p.stdout.decode().strip()


gh_cli = ['git', 'rev-list', '--abbrev-commit', '--tags', '--skip=1', '--max-count=1']
rev = subprocess.run(gh_cli, capture_output=True).stdout.decode().strip()

tag_gh_cli = ['git', 'describe', '--abbrev=0', '--tags', f'{rev}']
p = subprocess.run(tag_gh_cli, capture_output=True)
prev_tag = p.stdout.decode().strip()


print(prev_tag, tag)