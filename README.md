# CobbleSpire (가제)

코블버스(Cobblemon 1.7.3 / MC 1.21.1 Fabric) 위에서 돌아가는 슬레이 더 스파이어식 로그라이크 덱빌딩 모드. 아직 기획 단계이며, 규칙을 검증하기 위한 **웹 체험판**이 함께 있다.

**▶ 체험판 플레이: https://jaekune2.github.io/CobbleSpire/** (브라우저만 있으면 됨. 모바일도 가능)

- `docs/기획서-v0.1.md` : 게임·UI·기술 설계, 리소스 조사, 개발 단계, 멀티플레이 설계 초안(10절)
- `docs/index.html` : GitHub Pages용 체험판 (빌드 산출물)
- `tools/card_census.py` : Showdown `moves.js` + Cobblemon `ko_kr.json` → 카드 초안 집계·생성
- `data/cards_auto_draft.json` : 자동 변환 카드 821장 초안 (코스트·피해는 미조정)
- `data/cobbleverse-1.7.42-index.json` : 모드팩 구성(Modrinth mrpack 인덱스)

## 체험판에서 해 볼 수 있는 것

- 스타터 3종 → 관동 1번도로에서 회색체육관까지 8개 지역 루트 지도 → 관장 웅.
- 기술 카드 + 에너지 전투, 상태이상·날씨·랭크, 포획(파티 3마리), 진화, 지닌 도구·열매, 이벤트 16종, 포켓몬센터·상점·보물.
- 제목 화면에서 **파티 방식**(교체형 / 동시형), **상성 배율**(완화 / 원작), **인원**(혼자 / 2~4명 봇 동료)과 **멀티 방식**(투표형 / 분산형)을 바꿔 가며 비교할 수 있다.
- "자동 시연 보기"를 누르면 봇이 끝까지 플레이한다.

## proto/ — 체험판 소스

- 수정은 `proto/src.html`에서 하고 `python -I proto/_build.py`로 빌드한다. 산출물 3종:
  - `proto/cobblespire-proto.html`, `proto/index.html`: 스프라이트를 data URI로 내장한 로컬용 (저장소에는 넣지 않음)
  - `docs/index.html`: GitHub Pages용. 스프라이트는 PokeAPI 저장소에서 런타임에 불러온다.
- 그림: `proto/sprites/`(5세대 애니메이션 스프라이트, f=앞 b=뒤, 도감 번호)와 `proto/items/`(도구·열매·볼 아이콘)는 PokeAPI/sprites에서 받아 두는 로컬 자산이며 **저장소에 포함하지 않는다**(닌텐도 저작물). 없으면 타입 색 원으로 대체 표시된다.
- 검증: `node --check proto/_check.js`(문법), `node proto/_sim2.js`(혼자 150런 승률), `node proto/_sim3.js [런 수] [COOP 덮어쓰기 JSON]`(멀티 8조합 승률). 적 배율은 `src.html`의 `BAL`(혼자)·`COOP`(협동 인원당 증가율).
- 로컬 서버: `proto/serve.bat` (http://localhost:8765/). 실제 Chromium 점검(Playwright): `python proto/_pwdemo.py switch|field [초]`, `python proto/_pwmulti.py vote|split [인원] [switch|field] [초]`, `python proto/_pwtest.py`.

## 저작권 안내

비상업 팬 프로토타입입니다. 포켓몬 및 포켓몬 이름은 Nintendo / Creatures Inc. / GAME FREAK inc.의 상표·저작물이며, 이 저장소의 코드(MIT)만 자유롭게 쓸 수 있습니다. 스프라이트는 저장소에 포함되지 않습니다.
