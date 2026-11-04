"""Generate individual current-model links and a latest-file index from the catalog."""
from pathlib import Path
import hashlib
import html
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'js/models.js').read_text()
catalog = json.loads(source[source.index('{'):].rstrip().rstrip(';'))
models = [(key, model) for key, model in catalog.items() if model['device'] != 'history']
# Put current screen products first, followed by the remaining current models.
order = ['AURA_SCREEN', 'NEXUS_SCREEN', 'AURA_DUO_SCREEN']
models.sort(key=lambda item: order.index(item[0]) if item[0] in order else len(order))
latest = ROOT / 'output/latest'
(latest / 'stl').mkdir(parents=True, exist_ok=True)
rows, links, manifest = [], [], []
for key, model in models:
    path = ROOT / model['path']
    assert path.is_file(), path
    name = model['name_en'].split(' · ')[0]
    version = model['stage'].split(' / ')[0]
    bed_down = path.stem.endswith('_BED_DOWN')
    filename = path.name if bed_down else re.sub(r'[^A-Za-z0-9]+', '_', name).strip('_') + '_' + version + '.stl'
    shutil.copy2(path, latest / 'stl' / filename)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest.append(dict(model=key, file=filename, source=model['path'], sha256=digest))
    zh = version + (' · 平底向下 · STL' if bed_down else ' · 單獨 STL')
    en = version + (' · Flat base down · STL' if bed_down else ' · Individual STL')
    links.append('            <a class="individual-stl" data-model-download="' + key + '" href="' + html.escape(model['path']) + '" download><span><strong>' + html.escape(name) + '</strong><small data-zh="' + zh + '" data-en="' + en + '">' + zh + '</small></span><span aria-hidden="true">↓</span></a>')
    rows.append('| ' + name + ' | ' + version + (' · bed down' if bed_down else '') + ' | [Download STL](../../' + model['path'] + ') |')
(latest / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
(latest / 'README.md').write_text('''# Latest individual STL models

Each link below opens one current STL file. A ZIP is not required.
The three SCREEN models use flat-base-down files. The other models retain
their existing orientations. Use 100% scale and review the slicer preview.

| Model | Current version | Individual file |
| --- | --- | --- |
''' + '\n'.join(rows) + '''

The files linked above live in the tracked canonical assets directories.
This index is tracked, so it is visible on GitHub as well as locally.

Locally, `output/latest/stl/` contains a flat copy of all 15 current models,
with file/source hashes in `manifest.json`. Generated copies, images and ZIPs
remain Git-ignored. Older versions are in `output/archive/`.

Refresh the links, index and flat local copies:

    .venv/bin/python scripts/sync-model-downloads.py
    python3 scripts/sync-site.py

Full build: .venv/bin/python scripts/build-latest-pack.py
''')
block = '''          <!-- BEGIN CURRENT INDIVIDUAL STLS -->
          <div class="individual-downloads">
            <h3 data-zh="最新版本 · 單獨 STL 下載" data-en="Latest versions · Individual STL downloads">最新版本 · 單獨 STL 下載</h3>
            <p data-zh="每個按鈕下載一個最新模型，毋須解壓縮。三款 SCREEN 已平底向下擺放。" data-en="Each button downloads one current model. No ZIP needed. All three SCREEN models use flat-base-down orientation.">每個按鈕下載一個最新模型，毋須解壓縮。三款 SCREEN 已平底向下擺放。</p>
            <div class="individual-stl-grid">
''' + '\n'.join(links) + '''
            </div>
          </div>
          <!-- END CURRENT INDIVIDUAL STLS -->'''
page = ROOT / 'index.html'
content = page.read_text()
if '<!-- BEGIN CURRENT INDIVIDUAL STLS -->' in content:
    content = re.sub(r'          <!-- BEGIN CURRENT INDIVIDUAL STLS -->.*?          <!-- END CURRENT INDIVIDUAL STLS -->', lambda _: block, content, flags=re.S)
else:
    content = content.replace('          <span class="micro">PROTOTYPE RESOURCES</span>', block + '\n          <span class="micro" data-zh="整套 ZIP、指南與舊版本" data-en="ZIP bundles, guides and earlier versions">整套 ZIP、指南與舊版本</span>')
page.write_text(content)
print(f'Updated {len(models)} individual links, tracked latest index and local STL copies.')
