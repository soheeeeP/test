import re
import sys
import argparse
import subprocess
from pathlib import Path


def get_prev_tag():
    gh_cli = ['git', 'rev-list', '--abbrev-commit', '--tags', '--skip=1', '--max-count=1']
    rev = subprocess.run(gh_cli, capture_output=True).stdout.decode().strip()

    tag_gh_cli = ['git', 'describe', '--abbrev=0', '--tags', f'{rev}']
    p = subprocess.run(tag_gh_cli, capture_output=True)
    tag = p.stdout.decode().strip()
    return tag

def get_tag():
    gh_cli = ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
    p = subprocess.run(gh_cli, capture_output=True)
    tag = p.stdout.decode().strip()
    return tag

def get_repo_url():
    p = subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True)
    url = p.stdout.decode().strip()
    return url


def get_change_log_content(prev_tag, tag):
    p = subprocess.run(['git', 'log', '--oneline', '--format=" * %s"', f'{prev_tag}..{tag}~1'], capture_output=True)
    content = re.sub('"\n"', '\n', p.stdout.decode().strip()).strip('\"')
    return content


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--tag', '-t', type=str, default=False,
        help="Declare current tag."
    )
    args = parser.parse_args()
    if not args.tag:
        print("::error ::No version given from args.")
        sys.exit(1)

    repo_url = get_repo_url()
    m = re.match(r'^(https://)[a-zA-Z0-9-]+\.(com)+/[a-zA-Z-_.]+/[a-zA-Z-_]+', repo_url, re.S)

    prev_tag = get_prev_tag()
    tag = get_tag()
    output_path = Path('./CHANGELOG.md')
    output_text = get_change_log_content(prev_tag, tag)

    print(output_text)
    output_path.write_text(output_text)



if __name__ == '__main__':
    main()
