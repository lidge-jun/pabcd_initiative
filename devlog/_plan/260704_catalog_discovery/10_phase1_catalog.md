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
  followups: [mood_adjective_translation, reference_first, progressive_design_read]

entries:
  # ---- STAGE 1: DESIGN (6 dials, leading) ----
  - id: design.mood
    axis: design
    stage: 1
    label: {ko: "분위기", en: "Mood"}
    teach_text: {ko: "앱을 열었을 때의 첫인상과 감성적 온도. 카페 vs 유리 사무실 vs 럭셔리 쇼룸.", en: "..."}
    examples: {ko: "Toss(친근), Stripe(세련)", en: "..."}
    token_hint: "personality/palette branch"
  - id: design.lightness   # 밝기: light vs dark
  - id: design.density     # 정보 밀도: 미술관 vs 조종석
  - id: design.shape       # 모서리 곡률: 각짐 vs 둥긂
  - id: design.typography  # 글꼴: 명조 vs 고딕
  - id: design.motion      # 인터랙션 감도: spring vs instant

  # ---- STAGE 2: DOMAIN (app-type ontology) ----
  - id: domain.content_service   # e.g. saju/fortune, blog, media
    axis: domain
    stage: 2
    implies: []                  # domain choice seeds derived-axis defaults
  - id: domain.marketplace
  - id: domain.dashboard
  - id: domain.booking
  - id: domain.community
  - id: domain.ai_agent
  - id: domain.internal_tool

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
