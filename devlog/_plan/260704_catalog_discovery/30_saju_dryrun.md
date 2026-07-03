# Phase 3 — Saju Persona Dry-Run Walkthrough

Proving the design-first flow works end-to-end on a novice persona.
All entry IDs below exist in `skills/dev-pabcd/references/catalog-discovery.yaml`.

## Persona

Complete novice. No tech background. Korean speaker.
Initial request: **"사주 앱 만들고 싶어"**

---

## Stage 1 — Design/UX (asked FIRST per CATALOG-DESIGN-FIRST-01)

### Q1: design.mood (분위기)
**Show:** "앱을 열었을 때 어떤 느낌이면 좋겠어요?"
| Option | 설명 | Trade-off |
|---|---|---|
| 친근하고 따뜻한 | 동네 점집의 아늑한 분위기 | 접근성↑ 신뢰감은 별도 장치 필요 |
| 세련되고 프리미엄 | 고급 상담실 느낌 | 고급감↑ 캐주얼한 친밀감↓ |
| **신비롭고 몰입적** | 우주 탐험, 별자리 테마 | **테마 몰입↑** 정보 명료성 주의 |

**Answer:** 신비롭고 몰입적 → `implies_token: "dark cosmic palette"`

### Q2: design.lightness (밝기)
**Show:** "사주 결과를 보는 화면 분위기는?"
| Option | Trade-off |
|---|---|
| **어두운 모드** | 밤하늘+별자리 몰입 — mood 선택과 일관 |
| 밝은 모드 | 한지+먹물 명료 — mood와 충돌 가능 |

**Answer:** 어두운 모드 → `implies_token: "bg-gray-950 / text-gray-100"`

### Q3: design.density (정보 밀도)
**Show:** "사주 풀이 결과를 어떻게 보여줄까요?"
| Option | Trade-off |
|---|---|
| **여유롭게** | 카드 스토리 한 장씩 — 초보 친화, 스크롤↑ |
| 정보 밀집 | 차트 대시보드 한눈에 — 숙련자 효율, 첫인상 복잡 |

**Answer:** 여유롭게 → `implies_token: "py-8 / gap-8 (D1-D3)"`

### Q4: design.shape (모서리 곡률)
**Show:** "카드와 버튼 모양은?"
| Option | Trade-off |
|---|---|
| **둥근 형태** | 우주적·부드러운 느낌 — 신비 mood와 일관 |
| 각진 형태 | 정밀·구조적 — 데이터 분석 느낌 |

**Answer:** 둥근 형태 → `implies_token: "rounded-2xl (16px+)"`

### Q5: design.typography (글꼴 스타일)
**Show:** "사주 해설 텍스트의 글씨체는?"
| Option | Trade-off |
|---|---|
| **명조/서예체** | 역사적 깊이와 감성↑ 좁은 화면 가독성 주의 |
| 고딕체 | 가독성 안정↑ 전통미↓ |

**Answer:** 명조/서예체 → `implies_token: "Serif display"`

### Q6: design.motion (인터랙션 감도)
**Show:** "화면 전환과 애니메이션은?"
| Option | Trade-off |
|---|---|
| **부드러운 스프링** | 고급감·신비감↑ 체감 속도↓ |
| 즉각 반응 | 빠르고 명료↑ 감성↓ |

**Answer:** 부드러운 스프링 → `implies_token: "spring easing"`

**Stage 1 완료.** Design tokens 확정:
`dark cosmic palette + bg-gray-950 + D1-D3 spacious + rounded-2xl + Serif + spring`

---

## Stage 2 — Domain (app type)

**Show:** "어떤 종류의 앱인가요?"
- 콘텐츠 서비스 (사주·운세·블로그)
- 마켓플레이스 / 대시보드 / 예약 / 커뮤니티 / AI 에이전트 / 내부 도구

**Answer:** 콘텐츠 서비스 → `domain.content_service` selected.
`implies[]` = [] (no direct implications from this domain).

**auto_activate_rules scan** on original query "사주 앱 만들고 싶어":
- "사주" matches `security.pii_protection.auto_activate_rules` → **auto-activated**

---

## Stage 3 — Derived (surfaced from Stage 1+2)

### Derivation chain

1. `domain.content_service` selected →
   - `security.pii_protection` (via `derived_from` + auto_activate "사주") → **surfaced**
   - `feature.notifications` (via `derived_from: [domain.content_service]`) → **surfaced**
   - `feature.payments` (via `derived_from: [domain.content_service]`) → ask user

2. `security.pii_protection` implies →
   - `data.retention_policy` → **auto-activated**
   - `ops.scheduled_jobs` → **auto-activated**

3. `feature.notifications` implies →
   - `ops.scheduled_jobs` → already activated

4. `ops.scheduled_jobs` implies →
   - `ops.task_queues` → **auto-activated**

### Questions asked (only for entries needing user choice)

**Q7:** "유료 서비스나 구독을 받을 계획이 있나요?" (feature.payments)
- 있다 → risk_class: high, cost_class: 3, implies security.auth
- **없다** → skip

**Q8:** "사주 풀이를 생년월일로 하나요?" (confirming security.pii_protection)
- **예** → 생년월일 = 민감 개인정보. 암호화, 동의 절차, 보존/파기 정책 필요.

### Final selection set

| Entry ID | Axis | How surfaced | risk | cost |
|---|---|---|---|---|
| security.pii_protection | security | auto_activate "사주" | high | 2 |
| data.retention_policy | data | implied by pii_protection | high | 1 |
| feature.notifications | feature | derived from content_service | low | 2 |
| ops.scheduled_jobs | ops | implied by notifications + retention | low | 2 |
| ops.task_queues | ops | implied by scheduled_jobs | low | 2 |

Skipped: feature.payments (user said no), security.auth (no login needed for MVP).

---

## Configurator Output

### Mini-PRD

**Product:** 사주 풀이 앱 (Korean Fortune-Telling App)
**Design direction:** Mystical/cosmic dark theme, spacious card-based layout, rounded corners, serif typography, smooth spring animations.

**Functional requirements:**
1. Birth data input (solar/lunar date picker) with PII encryption
2. Saju interpretation display (card-by-card flow)
3. Daily fortune push notification (scheduled at user-set time)
4. Data retention/deletion policy (auto-purge on account deletion or 1yr inactivity)

**Non-functional requirements:**
1. Personal data encryption at rest (security.pii_protection)
2. GDPR/PIPA-compliant consent flow
3. Background job scheduler for notifications + data cleanup
4. Task queue for heavy saju calculation jobs

### MVP Cut (by cost_class)

| Priority | Entry | cost_class |
|---|---|---|
| P0 (must) | security.pii_protection | 2 |
| P0 (must) | data.retention_policy | 1 |
| P1 (should) | feature.notifications | 2 |
| P1 (should) | ops.scheduled_jobs | 2 |
| P2 (could) | ops.task_queues | 2 |

### Risk Register

| Entry | risk_class | Mitigation |
|---|---|---|
| security.pii_protection | **high** | Birth data encrypted at rest; consent flow before collection |
| data.retention_policy | **high** | Auto-purge cron; deletion confirmation UI; audit log |

### PABCD Plan Seed

- **Work class:** C3 (cross-domain — frontend + backend + security + ops)
- **Loop archetype:** spec/repair (a verifier defines done — feature completeness against PRD)
- **Suggested phases:** Design system → Core saju engine → Notification pipeline → PII compliance

---

## Verification Checklist

- [x] Design questions (Q1-Q6) appear BEFORE security/data/ops questions (Q7-Q8)
- [x] Every entry ID in transcript exists in catalog-discovery.yaml (verified: design.mood, design.lightness, design.density, design.shape, design.typography, design.motion, domain.content_service, security.pii_protection, data.retention_policy, feature.notifications, feature.payments, ops.scheduled_jobs, ops.task_queues)
- [x] implies[] chains resolve correctly: pii→retention+scheduled; notifications→scheduled; scheduled→task_queues
- [x] No question improvised — all options from catalog question_options or teach_text
- [x] CATALOG-DESIGN-FIRST-01 proven: Stage 1 (6 design Qs) completes before Stage 2 starts
