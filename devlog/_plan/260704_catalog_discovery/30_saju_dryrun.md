# Phase 3 — Saju persona dry-run walkthrough

## Part 1 — Plain explanation

A simulated interview proving the design-first flow actually works. A novice says
"사주 앱 만들고 싶어" and the catalog_discovery mode walks them through design
questions FIRST, then domain, then derived — producing a mini-PRD.

## Expected structure

### Persona
Complete novice. No tech background. Wants a Korean fortune-telling (사주) app.

### Dry-run transcript format
Simulated Q&A showing:
1. **Stage 1 (Design/UX) — asked FIRST**:
   - mood: 신비로운 우주 탐험 / 따뜻한 동네 점집 / 정밀 데이터 분석실
   - lightness: 밤하늘+별자리(dark) vs 한지+먹물(light)
   - density: 카드 스토리(spacious) vs 차트 대시보드(dense)
   - shape: 둥근(cosmic-friendly) vs 각진(data-precise)
   - typography: 명조(고풍) vs 고딕(정밀)
   - motion: spring(부드러운) vs instant(즉각)
2. **Stage 2 (Domain)**: domain.content_service selected (saju/fortune)
3. **Stage 3 (Derived)**: auto_activate_rules fire from "사주":
   - security.pii_protection (birth data = sensitive personal data)
   - → implies data.retention_policy, ops.scheduled_jobs
   - feature.notifications (daily fortune push)
4. **Configurator output**: mini-PRD + MVP cut + risk register + PABCD plan seed

### Verification criteria
- Design questions appear BEFORE any security/data/ops/feature question
- Every entry id in the transcript exists in catalog-discovery.yaml
- implies[] chains resolve correctly in the configurator output
- No question is improvised (all sourced from catalog)
- CATALOG-DESIGN-FIRST-01 invariant proven: stage 1 completes before stage 2 starts
