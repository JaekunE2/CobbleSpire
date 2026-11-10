"""src.html + _moves_ko.json + sprites/ + items/ ->
  cobblespire-proto.html (Artifact용, 스프라이트 내장)
  index.html            (로컬 서버용, 스프라이트 내장)
  ../docs/index.html    (GitHub Pages용, 스프라이트는 PokeAPI 저장소에서 런타임 로드 → 저장소에 그림 파일을 넣지 않음)
  _check.js             (node --check / 시뮬레이션용)
"""
import re, json, base64, pathlib
root = pathlib.Path(__file__).parent
s = (root / 'src.html').read_text(encoding='utf-8')
ko = (root / '_moves_ko.json').read_text(encoding='utf-8')
assert s.count('/*__MOVES_KO__*/{}') == 1
assert s.count('/*__SPRITES__*/{}') == 1
base = s.replace('/*__MOVES_KO__*/{}', ko)

# 1) 내장판: 스프라이트·아이템 아이콘을 data URI로 (CDN·외부 이미지는 Artifact에서 막히므로)
sprites = {}
for f in sorted((root / 'sprites').glob('*.gif')):
    sprites[f.stem] = 'data:image/gif;base64,' + base64.b64encode(f.read_bytes()).decode()
for f in sorted((root / 'items').glob('*.png')):
    sprites['i_' + f.stem] = 'data:image/png;base64,' + base64.b64encode(f.read_bytes()).decode()
out = base.replace('/*__SPRITES__*/{}', json.dumps(sprites, separators=(',', ':')))
(root / 'cobblespire-proto.html').write_text(out, encoding='utf-8')

head = ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n')
def page(html):
    i = html.index('<div class="wrap"')
    return head + html[:i] + '</head>\n<body>\n' + html[i:] + '\n</body>\n</html>\n'
(root / 'index.html').write_text(page(out), encoding='utf-8')

# 2) GitHub Pages판: 같은 키로 PokeAPI 원본 URL을 가리킨다 (저작권 자산을 저장소에 커밋하지 않음)
API = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/'
remote = {}
for f in sorted((root / 'sprites').glob('*.gif')):
    k = f.stem; dex = k[1:]
    remote[k] = API + 'pokemon/versions/generation-v/black-white/animated/' + ('back/' if k[0] == 'b' else '') + dex + '.gif'
for f in sorted((root / 'items').glob('*.png')):
    remote['i_' + f.stem] = API + 'items/' + f.stem + '.png'
web = base.replace('/*__SPRITES__*/{}', json.dumps(remote, separators=(',', ':')))
docs = root.parent / 'docs'
docs.mkdir(exist_ok=True)
(docs / 'index.html').write_text(page(web), encoding='utf-8')

# 3) 검사·시뮬레이션용 JS (연출 대기 없이 즉시 진행)
m = re.search(r'<script>(.*?)</script>', out, re.S)
js = m.group(1).replace('\nlet S={screen', '\nvar S={screen').replace('\nlet UID=1;', '\nvar UID=1;')
needle = 'const sleep=(ms)=>S.headless?Promise.resolve():new Promise(res=>setTimeout(res,ms));'
assert needle in js
js = js.replace(needle, 'var sleep=(ms)=>Promise.resolve();')
(root / '_check.js').write_text(js, encoding='utf-8')
print('built', len(out), 'bytes (embedded);', len(web), 'bytes (web); sprites', len(sprites))
