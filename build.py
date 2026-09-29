#!/usr/bin/env python3
"""Build offline, single-file editor and game. Python standard library only."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'src'
DIST = ROOT / 'dist'
DIST.mkdir(exist_ok=True)
read = lambda name: (SRC / name).read_text(encoding='utf-8')
core, runtime, css = read('core.js'), read('runtime.js'), read('runtime.css')
bundle = json.dumps(dict(core=core,runtime=runtime,css=css),ensure_ascii=False).replace('<','\\u003c')
html = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><meta name="description" content="Moonlit Studio 离线 Galgame 编辑器"><title>Moonlit Studio · Galgame 编辑器</title><style>'''+css+read('editor.css')+'''</style></head><body><div id="app"></div><dialog id="editor-modal" aria-label="编辑器对话框"></dialog><div id="player-host" hidden></div><div id="toasts" role="status" aria-live="polite"></div><script>'''+core+'\n'+runtime+'\n'+read('storage.js')+'\nwindow.GAL_BUNDLE='+bundle+';\n'+read('editor.js')+'''</script></body></html>'''
(DIST / 'Moonlit-Studio.html').write_text(html,encoding='utf-8')
print(f'Built {DIST / "Moonlit-Studio.html"} ({len(html.encode()):,} bytes)')
# Release example: all assets and code are embedded, just like an editor export.
from html import escape
example = ROOT / 'examples' / 'rain-before-dawn.galproject.json'
if example.exists():
    p = json.loads(example.read_text(encoding='utf-8'))
    data = json.dumps(p,ensure_ascii=False).replace('<','\\u003c')
    game = '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(p['title'])+'</title><style>'+css+'</style></head><body><main id="game" class="standalone-game"></main><script type="application/json" id="project-data">'+data+'</script><script>'+core+'\n'+runtime+'\nnew GalRuntime.Player(document.getElementById("game"),JSON.parse(document.getElementById("project-data").textContent));</script></body></html>'
    (DIST / 'Rain-Before-Dawn.html').write_text(game,encoding='utf-8')
diag = '''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Moonlit 启动自检</title><style>body{max-width:850px;margin:45px auto;padding:0 24px;background:#142030;color:#ccd9e8;font:16px/1.8 "Microsoft YaHei",sans-serif}h1{font-size:30px;color:#d3b787}p{color:#93abc6}ul{list-style:none;padding:0}li{padding:14px 18px;margin:10px 0;border:1px solid #344c66;border-radius:6px}.pass{background:#22383c}.fail{background:#4a2e39;color:#ffd0d0}button,a{padding:10px 18px;background:#d3b787;color:#142030;border:0;border-radius:5px;cursor:pointer;text-decoration:none;font:inherit;display:inline-block;margin:5px}</style><h1>Moonlit Studio · 启动自检</h1><p>在你的电脑上检查离线引擎、项目保存和浏览器格式支持。此页不会读取或修改已有项目。</p><h2 id="summary">正在检查…</h2><ul id="checks"></ul><button id="tone">播放测试提示音</button><a href="Moonlit-Studio.html">打开编辑器</a><script>'''+core+'\n'+read('diagnostics.js')+'</script></html>'
(DIST / 'Diagnostics.html').write_text(diag,encoding='utf-8')
print('Built offline example and diagnostics.')
