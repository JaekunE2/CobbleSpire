"""Showdown moves.js + Cobblemon ko_kr.json 을 읽어 카드 자동 변환 가능성을 집계한다.
사용: python -I card_census.py <moves.js> <ko_kr.json> [out.json]
"""
import json, re, sys, collections
moves_js, ko_path = sys.argv[1], sys.argv[2]
out = sys.argv[3] if len(sys.argv) > 3 else None
src = open(moves_js, encoding='utf-8').read()
ko = json.load(open(ko_path, encoding='utf-8'))

# 최상위 항목만 잘라낸다: "\n  name: {" ... "\n  }," (2칸 들여쓰기)
entries = re.findall(r'\n  ([a-z0-9]+): \{\n(.*?)\n  \},?', src, re.S)
def field(body, key, default=None):
    m = re.search(r'\n\s+%s: ([^\n]+?),?\n' % key, body)
    return m.group(1) if m else default
def flags(body):
    m = re.search(r'flags: \{([^}]*)\}', body, re.S)
    return set(re.findall(r'([a-z]+): 1', m.group(1))) if m else set()

cards = []
stats = collections.Counter()
for mid, body in entries:
    if 'isNonstandard' in body and 'isNonstandard: "Past"' not in body: 
        stats['skip_nonstandard'] += 1; continue   # CAP·LGPE·Gigantamax 등
    if 'isZ:' in body or 'isMax:' in body: stats['skip_z_max'] += 1; continue
    name_ko = ko.get(f'cobblemon.move.{mid}')
    desc_ko = ko.get(f'cobblemon.move.{mid}.desc')
    if not name_ko: stats['no_ko'] += 1; continue
    power = int(field(body, 'basePower', '0'))
    cat = field(body, 'category', '"Status"').strip('"')
    typ = field(body, 'type', '"Normal"').strip('"')
    pp = int(field(body, 'pp', '10'))
    prio = int(field(body, 'priority', '0'))
    acc = field(body, 'accuracy', '100')
    fl = flags(body)
    target = field(body, 'target', '"normal"').strip('"')
    special = []
    for key, tag in [('recoil', 'recoil'), ('drain', 'drain'), ('multihit', 'multihit'), ('ohko', 'ohko'),
                     ('boosts', 'boosts'), ('heal', 'heal'), ('sideCondition', 'side'), ('weather', 'weather'),
                     ('terrain', 'terrain'), ('volatileStatus', 'volatile'), ('status', 'status'),
                     ('selfdestruct', 'selfdestruct'), ('onTryHit', 'custom'), ('onHit', 'custom'),
                     ('basePowerCallback', 'custom'), ('damageCallback', 'custom'), ('onModifyMove', 'custom'),
                     ('condition:', 'custom'), ('self:', 'self'), ('secondary: {', 'secondary'), ('secondaries', 'secondary')]:
        if key in body: special.append(tag)
    if 'charge' in fl: special.append('charge')
    if 'recharge' in fl: special.append('recharge')
    if power == 0 and cat != 'Status': special.append('variable_power')
    # 코스트 초안: 위력 기준. 상태기는 1, 선공·반동은 보정
    if cat == 'Status': cost = 1
    elif power <= 45: cost = 0 if prio > 0 and power <= 40 else 1
    elif power <= 95: cost = 2 if prio <= 0 else 2
    else: cost = 3
    if 'recoil' in special and cost > 1: cost -= 1
    dmg = round(power * 0.15) if power else 0
    kind = 'attack' if cat != 'Status' else 'skill'
    tier = 'auto' if not any(s in ('custom', 'variable_power', 'ohko') for s in special) else 'manual'
    cards.append(dict(id=mid, name=name_ko, type=typ.lower(), category=cat.lower(), cost=cost, damage=dmg, power=power,
                      accuracy=acc, priority=prio, target=target, kind=kind, special=special, tier=tier, desc=desc_ko))
    stats['total'] += 1; stats['kind_' + kind] += 1; stats['tier_' + tier] += 1; stats['cost_%d' % cost] += 1
    for s in set(special): stats['special_' + s] += 1
print(json.dumps(stats, ensure_ascii=False, indent=1))
by_type = collections.Counter(c['type'] for c in cards)
print('by type', dict(by_type))
if out:
    json.dump(cards, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', out, len(cards))
