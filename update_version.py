import re
from github import Github
import os

def update_version(file_path, new_version):
    with open(file_path, 'r') as file:
        content = file.read()

    updated_content = re.sub(r'version\s*=\s*\d+\.\d+\.\d+', f'version = {new_version}', content)

    with open(file_path, 'w') as file:
        file.write(updated_content)

if __name__ == "__main__":
    new_version = os.getenv('GITHUB_REF').split("/")[-1]
    setup_cfg_path = 'setup.cfg'  # Update with the actual path to your setup.cfg file

    update_version(setup_cfg_path, new_version)