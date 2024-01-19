import re
version_text = open('versions.txt', 'r').read()
version_nb = re.findall(r'\d+', version_text)
__version__ = f'v{version_nb[0]}.{version_nb[1]}.{version_nb[2]}'
