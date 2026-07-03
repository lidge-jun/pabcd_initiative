# Phase 1 — Catalog data structure (design/UX-first)

## Part 1 — Plain explanation

We create ONE new data file: a versioned "menu" of app-building choices. Its first and most
important section is **Design/UX** (mood, brightness, density, shape, typography, motion),
followed by **domain** (what kind of app), and only THEN the technical sections
(features, data, security, ops, cost) — which point back to the design/domain answers so the
interview can ask them in a smart, derived order instead of a flat wall of questions.

## Part 2 — Diff-level precision

### NEW: `skills/dev-pabcd/references/catalog-discovery.yaml`

Structure:
```yaml
version: 1
last-verified: 2026-07-04
# Explicit stage ordering — design/UX LEADS. This is the load-bearing invariant.
axis_order:
  - {stage: 1, axis: design,   label_ko: "디자인/UX",   note: "asked FIRST — most important"}
  - {stage: 2, axis: domain,   label_ko: "앱 유형",      note: "what kind of app"}
  - {stage: 3, axis: feature,  label_ko: "기능",         derived: true}
  - {stage: 3, axis: data,     label_ko: "데이터",       derived: true}
  - {stage: 3, axis: security, label_ko: "보안/개인정보", derived: true}
  - {stage: 3, axis: ops,      label_ko: "운영/자동화",   derived: true}
  - {stage: 3, axis: cost,     label_ko: "비용/복잡도",   derived: true}

# Design methodology wiring (from dev-uiux-design). Step 1 = Product-Personality Selection.
design_methodology:
  primary: product_personality_selection
  ref: "skills/dev-uiux-design/SKILL.md"
  followups:
    - step: korean_request_translation  # dev-uiux-design §3 — map Korean adjectives to design tokens
    - step: reference_discovery         # dev-uiux-design §1 Step 6 — anchor with existing product visuals
    - step: design_read                 # dev-uiux-design §2 — full Design Read for production-ready dials

entries:
  # ---- STAGE 1: DESIGN (6 dials, leading) ----
  - id: design.mood
    axis: design
    stage: 1
    label: {ko: "분위기", en: "Mood"}
    teach_text: {ko: "앱을 열었을 때의 첫인상과 감성적 온도. 카페 vs 유리 사무실 vs 럭셔리 쇼룸.", en: "..."}
    examples: {ko: "Toss(친근), Stripe(세련)", en: "..."}
    token_hint: "personality/palette branch"
  - id: design.lightness
    axis: design
    stage: 1
    label: {ko: "밝기", en: "Lightness"}
    teach_text: {ko: "화면의 기본 배경색 톤. 종이책(라이트) vs 네온사인(다크).", en: "..."}
    examples: {ko: "Notion(라이트), Linear(다크)", en: "..."}
    token_hint: "bg-white/text-gray-900 vs bg-gray-950/text-gray-100"
  - id: design.density
    axis: design
    stage: 1
    label: {ko: "정보 밀도", en: "Density"}
    teach_text: {ko: "한 화면의 정보량과 여백. 미술관(여유) vs 조종석(빽빽).", en: "..."}
    examples: {ko: "Apple(여유 D1-D3), GitHub(빽빽 D4-D8)", en: "..."}
    token_hint: "py-8/gap-8 vs py-1/gap-1"
  - id: design.shape
    axis: design
    stage: 1
    label: {ko: "모서리 곡률", en: "Shape"}
    teach_text: {ko: "버튼/카드의 둥글기. 설계도(각진) vs 젤리(둥근).", en: "..."}
    examples: {ko: "Vercel(각진), Toss(둥근)", en: "..."}
    token_hint: "rounded-none/md vs rounded-2xl"
  - id: design.typography
    axis: design
    stage: 1
    label: {ko: "글꼴 스타일", en: "Typography"}
    teach_text: {ko: "서체로 신뢰도/가독성 결정. 붓글씨(명조) vs 깔끔한(고딕).", en: "..."}
    examples: {ko: "Notion(Pretendard 고딕), Stripe(Satoshi 세리프)", en: "..."}
    token_hint: "system sans vs elegant serif"
  - id: design.motion
    axis: design
    stage: 1
    label: {ko: "인터랙션 감도", en: "Motion"}
    teach_text: {ko: "전환 시 움직임의 속도/탄성. 부드러운 스프링 vs 즉각 반응.", en: "..."}
    examples: {ko: "Arc(spring), Linear(instant)", en: "..."}
    token_hint: "spring(duration-300 ease-out) vs instant(duration-0)"

  # ---- STAGE 2: DOMAIN (app-type ontology) ----
  - id: domain.content_service   # e.g. saju/fortune, blog, media
    axis: domain
    stage: 2
    implies: []                  # domain choice seeds derived-axis defaults
  - id: domain.marketplace
    axis: domain
    stage: 2
    label: {ko: "마켓플레이스", en: "Marketplace"}
    teach_text: {ko: "판매자와 구매자를 연결하는 중개 플랫폼.", en: "..."}
    implies: [feature.payments, security.auth]
  - id: domain.dashboard
    axis: domain
    stage: 2
    label: {ko: "대시보드/분석", en: "Dashboard"}
    teach_text: {ko: "데이터를 시각화하고 모니터링하는 관리 화면.", en: "..."}
    implies: [security.auth]
  - id: domain.booking
    axis: domain
    stage: 2
    label: {ko: "예약/스케줄링", en: "Booking"}
    teach_text: {ko: "시간/자원을 예약하고 관리하는 서비스.", en: "..."}
    implies: [feature.notifications, ops.scheduled_jobs]
  - id: domain.community
    axis: domain
    stage: 2
    label: {ko: "커뮤니티/소셜", en: "Community"}
    teach_text: {ko: "사용자끼리 소통하고 콘텐츠를 공유하는 플랫폼.", en: "..."}
    implies: [data.user_generated, ops.admin_review, security.auth]
  - id: domain.ai_agent
    axis: domain
    stage: 2
    label: {ko: "AI 에이전트", en: "AI Agent"}
    teach_text: {ko: "AI가 핵심 기능을 수행하는 지능형 서비스.", en: "..."}
    implies: [cost.infra_complexity]
  - id: domain.internal_tool
    axis: domain
    stage: 2
    label: {ko: "내부 도구", en: "Internal Tool"}
    teach_text: {ko: "조직 내부 업무를 효율화하는 사내 전용 앱.", en: "..."}
    implies: [security.auth]

  # ---- STAGE 3: DERIVED (each carries derived_from) ----
  - id: security.pii_protection
    axis: security
    stage: 3
    derived_from: [domain.content_service]   # birth data → sensitive
    label: {ko: "개인정보 보호", en: "..."}
    teach_text: {ko: "생년월일·위치 등 민감정보를 수집하면 암호화·보존정책이 필요합니다.", en: "..."}
    implies: [data.retention_policy, ops.scheduled_jobs]
    risk_class: high
    cost_class: 2
    auto_activate_rules: ["생년월일", "birth", "사주", "personal"]
  - id: security.auth              # login/session
  - id: data.retention_policy      # 파기/보존
  - id: data.user_generated        # UGC
  - id: feature.payments           # implies security.pci
  - id: feature.notifications      # implies ops.scheduled_jobs
  - id: ops.scheduled_jobs         # cron
  - id: ops.admin_review           # moderation/approval
  - id: cost.infra_complexity      # roll-up flag
```

Full file: ~14 design + domain + derived entries, each with the full field set from the
schema (id, axis, stage, label{ko,en}, teach_text{ko,en}, examples{ko,en}, implies?,
conflicts?, derived_from?, risk_class?, cost_class?, followup_questions?, auto_activate_rules?).

### Invariant enforced by Phase-1 verifier
- `axis_order[0].axis == design` and `stage == 1`.
- Every `implies`/`conflicts`/`derived_from` id ∈ entries.
- Every stage-3 entry has non-empty `derived_from`.
- All 6 design dials present.

### Verifier command (Phase 1)
`python3 devlog/_plan/260704_catalog_discovery/check_catalog.py` (NEW, tiny script:
loads YAML, asserts the 4 invariants, prints PASS/FAIL). Kept in the plan folder, not shipped.

## Files touched (Phase 1)
- NEW `skills/dev-pabcd/references/catalog-discovery.yaml`
- NEW `devlog/_plan/260704_catalog_discovery/check_catalog.py` (verifier, plan-local)
