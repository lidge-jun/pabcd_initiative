# Phase 3 — Saju persona dry-run [STUB — filled in Phase 3]

Walkthrough proving the design-first flow on "사주 앱 만들고 싶어":
1. Design questions asked FIRST (mood → 신비로운 우주 / 따뜻한 점집 / 정밀 분석실; lightness; density; typography).
2. Domain resolved (content_service).
3. Derived questions surface from answers: birth data → security.pii_protection auto-activates
   (rule "사주"/"생년월일") → implies data.retention_policy + ops.scheduled_jobs.
4. Configurator output: PRD skeleton + MVP cut + risk register (pii=high) + PABCD plan seed.

Verifier (Phase 3): the doc's question sequence shows design Qs (steps 1) strictly before
security/data Qs (step 3), proving design LEADS.
