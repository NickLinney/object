from pathlib import Path
import json

root = Path(__file__).parents[1]
required = ['packet.manifest.json', 'abstract-specification.md', 'implementation-abstract.md', 'contract.md', 'catalog/source-register.json', 'schemas/package.manifest.schema.json', 'validation/README.md']
missing = [p for p in required if not (root / p).exists()]
if missing:
    raise SystemExit('missing required template roles: ' + ', '.join(missing))
for p in root.rglob('*.json'):
    json.loads(p.read_text())
print('PASS: abstract Object package template')
