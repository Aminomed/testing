import re

html_keys = set()
with open(r'c:\GIT\Test\website\index.html', 'r', encoding='utf-8') as f:
    html = f.read()
    for m in re.finditer(r'data-i18n(-placeholder)?="([^"]+)"', html):
        html_keys.add(m.group(2))

with open(r'c:\GIT\Test\website\script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

de_keys = set()
curr = None
for line in lines:
    stripped = line.strip()
    if stripped.startswith('de: {'):
        curr = 'de'
        continue
    elif stripped.startswith('en: {'):
        curr = 'en'
        continue
    elif stripped.startswith('};') and curr:
        curr = None
        continue

    m = re.match(r'^([a-zA-Z0-9_]+)\s*:\s*["]', stripped)
    if m and curr == 'de':
        de_keys.add(m.group(1))

print("HTML keys missing from JS dict:", html_keys - de_keys)
print("JS keys unused in HTML:", de_keys - html_keys)
