# Catalog Discovery Mode — Design & Integration Devlog

Date: 2026-07-04
Status: Design complete, implementation pending
Participants: Boss (synthesis), Frontend (design axis), Backend (catalog schema), Docs (integration map)

---

## 1. Decision: Interview에 Catalog Discovery 모드 통합

기존 Interview(Clarification Mode)에 **Catalog Discovery Mode**를 추가한다.
별도 제품이 아니라 Interview의 서브모드. 영어명 **Guided Solution Discovery**.

### 3-Mode Interview Structure

| Mode | When | What it does |
|---|---|---|
| **Clarification** (기존) | User already knows roughly what they want | Structure goals/constraints/success criteria |
| **Catalog Discovery** (신규) | User doesn't know the option space | Present ontology of choices FIRST, then ask |
| **Configurator** (신규) | After selections are made | Compile into PRD → feature list → MVP scope → PABCD plan |

### Entry heuristic
- User states a concrete feature/goal → Clarification
- User states a vague domain ("사주 앱 만들고 싶어") → Catalog Discovery
- Explicit user request → either mode

---

## 2. Design Axis — 제일 중요한 축

### 2.1 디자인을 초보에게 설명하는 방법

비유 기반 5가지 개념으로 풀어준다 (technical term을 쓰지 않음):

| Concept | Korean | Analogy |
|---|---|---|
| Visual Soul (Mood) | 분위기 | 카페 vs 유리 사무실 vs 럭셔리 쇼룸의 첫인상 |
| Information Space (Density) | 화면 밀도 | 미술관(여유) vs 조종석(빽빽) |
| Light & Shadow | 명암 대비 | 종이책(라이트) vs 네온사인(다크) |
| Form & Border | 모양 | 설계도(각진) vs 말랑한 젤리(둥근) |
| Typography Vibe | 글씨체 | 붓글씨(명조) vs 깔끔한 고딕 |

### 2.2 디자인 방향 잡는 방법론 — 4가지 비교 후 결론

| Approach | Strength | 초보 첫 단계로서 강/약 |
|---|---|---|
| **Product-Personality Selection** | 검증된 디자인 DNA를 패키지로 선택, 일관성 즉시 확보 | **★ 최강** — 브랜드 아이덴티티를 매개로 비디자이너도 쉽게 결정 |
| Reference-First (기존 제품 보여주기) | 직관적 시각화 | 약함 — 부가 기능까지 복사하려 하거나 선택 장애 유발 |
| Mood/Adjective→Token 매핑 | 감정어를 토큰으로 즉시 투영 | 약함 — "깔끔하게" 같은 형용사의 주관적 해석 편차 큼 |
| Progressive Design Read | 세밀한 다이얼 조율 | 약함 — 중간 수준 디자인 지식이 선행되어야 함 |

**결론: Product-Personality Selection이 Step 1.**
이후 순서: Mood/Adjective로 세부 감성 조율 → Reference-First로 컴포넌트 레이아웃 앵커 → Design Read로 프로덕션급 밀도/모션 확정.

### 2.3 Design Axis 카탈로그 엔트리 (6개)

| id | 한국어 라벨 | teach text | 예시 제품 | 토큰 분기 |
|---|---|---|---|---|
| `mood` | 분위기 | 서비스의 첫인상과 감성적 온도 결정 | Toss, Notion | 친근함 vs 세련됨 색상 스키마 |
| `lightness` | 밝기 | 배경색 톤으로 피로도/몰입감 좌우 | Notion, Linear | bg-white vs bg-gray-950 |
| `density` | 정보 밀도 | 한 화면의 정보량과 여백 간격 조절 | GitHub, Apple | D4-D8(빽빽) vs D1-D3(여유) |
| `shape` | 모서리 곡률 | 버튼/카드 둥글기로 친근 vs 단단함 | Toss, Vercel | rounded-2xl vs rounded-none |
| `typography` | 글꼴 스타일 | 서체로 신뢰도/가독성 결정 | Notion, Stripe | Pretendard vs Satoshi/Serif |
| `motion` | 인터랙션 감도 | 전환 시 움직임의 속도/탄성 | Arc, Apple | spring vs instant |

### 2.4 사주 앱 페르소나 샘플 질문 플로우 (4문)

1. **분위기** — "사주를 보러 왔을 때 기분이 어때야 할까요? 신비로운 우주 탐험? 따뜻한 동네 점집? 아니면 정밀한 데이터 분석실?"
2. **밝기** — "사주 결과를 보는 화면을 밤하늘+별자리(다크) vs 한지+먹물(라이트) 중 어떤 느낌으로?"
3. **밀도** — "결과를 카드 스토리로 한 장씩 넘겨볼까요, 차트 대시보드로 한눈에 볼까요?"
4. **글꼴** — "해설 텍스트를 고풍스러운 명조체 vs 정밀한 고딕체 중 어느 방향?"

---

## 3. Catalog Schema (Backend 제안)

### 3.1 Entry schema (YAML)

```yaml
- id: "security.pii_protection"     # namespaced unique id
  axis: "security"                   # category group
  label:
    en: "Personal Data Protection"
    ko: "개인정보 보호"
  teach_text:
    en: "If your app collects names, birthdays, or locations..."
    ko: "앱이 이름, 생년월일, 위치 정보를 수집하면..."
  examples:
    en: "Health apps, fortune-telling apps..."
    ko: "건강 앱, 사주 앱..."
  implies: ["security.encryption_at_rest", "ops.data_retention"]
  conflicts: []
  risk_class: "high"    # low | medium | high
  cost_class: 2         # 1 | 2 | 3
  followup_questions: ["q_pii_scope"]
  auto_activate_rules: ["생년월일", "birth", "사주"]
```

### 3.2 Axis 목록 (6축)

| Axis | Scope |
|---|---|
| `design` | 분위기, 밀도, 밝기, 곡률, 글꼴, 모션 |
| `security` | 인증, 인가, 개인정보, 지적재산, trust boundary |
| `data` | 저장 타입, 캐싱, 잔류, 보존 정책 |
| `ops` | 관리자 리뷰, 승인 플로우, 스케줄 작업, 모니터링 |
| `feature` | 결제, 알림, 워크플로우, 파일 업로드, 채팅 |
| `cost` | 인프라 복잡도, 서포트 부담, 컴플라이언스 비용 |

### 3.3 Configurator 출력물

선택된 엔트리 + `implies[]` 체인 해소 → 다음 산출물 생성:
- PRD (기능 요구사항 + 비기능 요구사항)
- MVP cut rule (cost_class 기준 우선순위)
- Risk register (risk_class=high 엔트리 자동 등록)
- PABCD plan seed (work class + loop archetype 포함)

### 3.4 저장 위치

`skills/dev-pabcd/references/catalog-discovery.yaml` — agent-neutral copy rule(README.md) 준수.
i18n은 YAML 내 인라인 유지 (자기완결).

---

## 4. 다운스트림 적용 포인트

| Repo | Interview 현재 위치 | 통합 지점 | Effort | Risk |
|---|---|---|---|---|
| **cli-jaw** | `src/orchestrator/state-machine.ts` (I-state) + `src/prompt/templates/orchestration.md` | FSM I-state에 sub-mode 추가 + `discovery-catalog.json` 로딩 | M | M |
| **jawcode** | `packages/.../jwc/skills/jaw-interview/SKILL.md` + auto-research-greenfield.md | SKILL.md에 Phase 0.5 Discovery 모드 추가 + references/ 카탈로그 | M/L | M |
| **opencodex** | Interview 표면 없음 (API proxy + dashboard) | `gui/src/`에 대시보드 위자드 추가 + REST endpoint | S(GUI만) | L |

### 핵심 적응 원칙
1. 카탈로그는 pabcd_initiative가 canonical source → 다운스트림은 port (blind copy 금지)
2. cli-jaw: FSM sub-mode (`catalog_discovery` state in I)
3. jawcode: prompt 기반 (SKILL.md reference)
4. opencodex: GUI 위자드 (React)

---

## 5. Open Questions (미결)

1. **Conflict resolution**: 충돌하는 선택지 동시 선택 시 차단 vs 경고 + 진행?
2. **implies[] 시각화**: CLI 채팅 vs 브라우저 UI에서 의존관계를 어떻게 보여줄 것인가?
3. **도메인 특화 용어**: 사주 앱의 천간/지지/신살 같은 전문 용어 → 팝오버 툴팁 자동 포함?
4. **음양력 날짜 입력**: 사주 계산에 필수인 solar/lunar 듀얼 date picker 기본 포함 여부
5. **Asset guardrails**: 12지신 아이콘 등 도메인 에셋 소싱 시 AI-generated slop 방지 룰
6. **Loop archetype 자동 분류**: Configurator가 "better" 루프를 감지하면 explore-and-select 템플릿 자동 주입?
