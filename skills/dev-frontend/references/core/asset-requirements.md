# Asset Requirements

Visual surfaces need real visual evidence. Abstract backgrounds, blobs, and generic icons are not enough when users need to understand a product, place, object, workflow, game, or state.

## Asset Decision Table

| Surface | Required Asset Type |
| --- | --- |
| Product / object / venue / person page | real or generated bitmap showing the subject |
| Marketing / landing page | concrete product, scene, screenshot, or generated hero image |
| Dashboard / tool | real state preview, chart, table, workflow screenshot, or diagram |
| AI tool | process state, provenance, result preview, permission boundary, or diagram |
| Education / kids / community | illustration, character, or guided visual allowed |
| Fintech / gov / B2B | restrained screenshot, data view, trust visual, or high-polish semantic 3D |
| Game | game assets mandatory |
| Documentation | screenshots or diagrams when they clarify a task |

## What Does Not Count

- abstract gradient mesh
- decorative blob/orb
- generic icon row
- fake dashboard with random numbers
- low-polish AI image
- stock photo unrelated to the task
- public 3D icon pack used without brand adaptation
- integration/partner logo wall using generic icons instead of brand SVGs (see `brand-asset-sourcing.md`)

## Asset Sourcing Workflow

This source-priority list applies to CONTENT assets used in builds: photos,
illustrations, textures, motion clips, screenshots, diagrams, charts, and
brand-safe SVGs. The concept-mockup pass in `dev-uiux-design` is a process
step outside this sourcing order; when its trigger fires, it runs before code
even though its outputs are not shippable UI pixels.

Try each source in order. Stop at the first that produces a usable asset.

| Priority | Source | When to Use |
|----------|--------|-------------|
| 1 | Project existing assets | `images/`, `public/`, `assets/` in the repo |
| 2 | Built-in or environment-provided image generation tool, if available | Hero images, product shots, custom illustrations. Use only when the tool is confirmed working |
| 3 | Stock photo API | `source.unsplash.com/800x600/?coffee`, Pexels. Always include `alt` text and credit |
| 4 | CSS device frame + screenshot | App mockup heroes (Toss/카카오 style). Pure CSS phone/laptop frame wrapping a real screenshot or UI |
| 5 | Placeholder service (last resort) | `picsum.photos/800/600`, `placehold.co`. Mark as TODO for replacement |

Row 2 also covers textures, illustrations, and motion clips when the available
generator has those modes. Confirm it is working before relying on it: probe
its status, and if it needs a local service or session, start it and re-check
once before declaring it unavailable. Write its prompts per § Agent Image
Prompt Protocol. A runtime may have no image generation capability at all;
when it has none, skip row 2 and continue down the ladder rather than
substituting gradients or decorative shapes for the missing asset.

### Korean Service Patterns

Korean product pages almost always use concrete visual evidence in the first viewport:

| Pattern | Example | Implementation |
|---------|---------|---------------|
| Device mockup hero | Toss, 카카오뱅크, 당근 | CSS device frame (`border-radius: 40px`, `box-shadow`) + app screenshot inside |
| Real product photo | 배민, 무신사, 마켓컬리 | Full-bleed or contained product image, not a gradient placeholder |
| App screenshot carousel | 토스, 네이버 | Horizontal scroll of actual app screens |
| Data visualization hero | 토스증권, 뱅크샐러드 | Real (or realistic) chart/graph as primary visual |

Never ship a Korean-facing product page with only SVG icons and text. If no image source is available, state the gap explicitly rather than filling with gradients or decorative shapes.

## Mockup Production Pipeline (verified 2026-07-09)

When a product/device mockup asset is required (product-led heroes, app
screenshots in scenes):

- **Device-mockup tools** (Rotato, MockRocket, Shots, Smartmockups, Figma
  mockup plugins): map a real screenshot onto a 3D device render; stills and
  short movies, no 3D skills needed.
- **AI scene + real screenshot compositing**: generate the environment/scene
  image, then composite the actual product UI screenshot into or above it;
  never AI-generate the product UI itself — the interface pixels must be real.
  This binds shipped assets; § Concept Mockup Boundary carves out pre-code
  concept exploration, which never ships.
- **Frame extraction**: for scroll-driven playback, render the mockup motion
  to video and extract frames (see `motion.md` § Frame Sequence Format Guide).

The screenshot inside any mockup must be a real, current capture of the
product; a fabricated UI in a real frame is still a fake asset.

### Concept Mockup Boundary (FE-ASSET-CONCEPT-01, DEFAULT)

Generated CONCEPT mockups of a page or component, including generated concept
passes and mockup references from any image generator, are exploration
artifacts. They are legal and encouraged before code when the concept-pass
trigger fires, but they must never ship as UI pixels.

The "never AI-generate the product UI itself" rule is scoped to shipped
assets. It does not ban pre-code concept exploration, and it does not ban
generated photographic, texture, illustration, or motion CONTENT assets in real
builds. Those content assets are not product UI pixels; they may ship when
they satisfy provenance, licensing, accessibility, performance, and visual QA
requirements.

## Rules

- Use the repo's existing asset system first.
- If no asset exists and the surface needs one, follow the sourcing workflow above.
- For external or generated assets, record provenance/licensing in the dev note, PR description, or project asset manifest when one exists.
- For captured third-party reference material, use `reference-capture.md` and keep the required manifest next to the capture. Captured assets never move into shipped project assets.
- Make the first viewport identify the product/place/object when relevant.
- Do not obscure text or primary actions with visuals.
- Verify assets render on mobile and desktop.
- Verify intrinsic dimensions, aspect ratio, crop, alt text, and loading behavior.
- Optimize heavy media; do not ship huge 3D/video assets without a reason.
- Ship gate: no captured third-party asset may appear in the shipped build.

## Agent Image Prompt Protocol

### Generator Capability Vocabulary

This protocol is written against CAPABILITIES, not against one tool. Image
generators differ in which of the following they expose, and a runtime may
expose none of them. Check once which of these your generator has, and read
every rule below against that answer instead of assuming a command exists:

| Capability | What it means |
|---|---|
| **Single-request batch** | One request, N images from one prompt. The N candidates share the prompt and differ only by sampling |
| **Streaming multi-slot mode** | One prompt fans out into independent generation slots that arrive incrementally; individual slots can be cancelled early |
| **Independent parallel jobs** | Several separate requests launched concurrently, each with its own prompt, provider, or model |
| **Job listing and cancel** | Surfaces that enumerate in-flight generations and abort one. Frequently absent |
| **Edit / inpaint pass** | Re-generate a region of an existing image from a targeted instruction |
| **Video / motion mode** | Generate a moving clip, usually from a prompt plus a still reference frame |
| **Reference-image attachment** | Attach one or more images as composition, style, or brand references |
| **Interactive canvas** | A human-in-the-loop surface for masking and cleanup, exporting with alpha or a matte |
| **Provider routing** | Send a request to one of several configured model providers |
| **Quality and size controls** | Select a quality tier and output dimensions per request |
| **Direct prompt mode** | Send the prompt through without server-side rewriting |

Where a rule below depends on a capability the runtime does not have, the
degradation is named explicitly in that rule. Do not simulate a missing
capability by pretending the output is equivalent; state the limitation in the
dev note instead.

Whatever generator is in use, inspect every generated candidate visually before
using it, with whatever image-viewing surface the runtime provides. "The file
was created" is not evidence that the asset is usable.

### Long Prompt and Motion Rule (FE-ASSET-PROMPT-01, DEFAULT)

When an AI agent generates image prompts — for a single-request batch, a
streaming multi-slot run, an edit pass, a video generation, or a plain
single-image call — the prompt must be **exhaustively detailed**. Vague
one-liners produce generic, unusable output. Write every prompt as if you are
briefing a senior photographer, illustrator, or motion designer who cannot ask
follow-up questions.

Image assets need very explicit long prompts covering subject, composition,
palette, lighting, style or medium, materials, aspect ratio, constraints, and
avoid-list. When motion is wanted, use the generator's video/motion mode rather
than simulating richness with static CSS washes; if it has no video mode, say
so and choose a different asset strategy instead of faking motion with
gradients. Prefer real photographic, generated bitmap, texture, illustration,
or video assets over CSS gradient backgrounds; gradients remain scarce semantic
devices under `anti-slop.md` FE-GRADIENT-01.

### Required Spec Fields

Every agent-authored prompt MUST include all applicable fields below. Omit a
field only when it genuinely does not apply (e.g. no text in the image).

```text
Use case: <taxonomy slug from the project's image-generation reference, if it defines one>
Asset type: <where the asset will be used: hero, OG image, card, avatar, icon, texture, etc.>
Primary request: <one clear sentence describing the desired image>
Scene/backdrop: <specific environment, not "nice background">
Subject: <main subject with identifying details — material, color, shape, posture, expression>
Style/medium: <exact style: editorial photography, flat illustration, 3D render, watercolor, etc.>
Composition/framing: <camera angle, crop, subject placement, negative space intent>
Lighting/mood: <light source, direction, color temperature, mood, time of day>
Color palette: <specific colors or named palette — not "modern colors">
Materials/textures: <surface details: matte plastic, brushed steel, linen, weathered wood, etc.>
Text (verbatim): "<exact text to render>" with font style, size, placement
Dimensions: <target pixel dimensions and aspect ratio>
Constraints: <must-keep invariants>
Avoid: <explicit negative constraints>
```

### Specificity Rules

| Bad (vague) | Good (specific) |
|---|---|
| "a nice hero image" | "wide landscape product shot of a matte black thermos on a wet granite countertop, soft morning window light from the left, shallow depth of field, warm neutral tones, negative space on the right for headline overlay" |
| "modern background" | "soft radial gradient from #f8f9fa center to #e9ecef edges, subtle paper grain texture at 3% opacity, no objects, no patterns" |
| "Korean food photo" | "overhead flat-lay of budae-jjigae in a black stone pot, surrounded by small banchan dishes on a dark wood table, steam visible, warm tungsten lighting, editorial food photography style" |
| "logo on white" | "centered geometric mark: two interlocking triangles forming a hexagonal negative space, flat #1a1a2e on #ffffff, no gradients, strong silhouette at 32px, generous padding" |
| "a dashboard screenshot" | "realistic SaaS dashboard UI: top nav with avatar, left sidebar with 6 nav items, main area showing a line chart (3 series, 12 months) and a 4-column data table with 8 rows, light theme, Inter font, compact density" |

### Quality and Size Selection

Quality tiers below are the common low/medium/high split; map them onto
whatever tiers the generator exposes. If it exposes no quality control, treat
the size column as the binding requirement.

| Asset Purpose | Quality | Size |
|---|---|---|
| Quick draft / iteration | `low` | `1024x1024` |
| Final hero / product shot | `high` | `1536x1024` (landscape) or target aspect |
| OG / social card | `high` | `1200x630` (round to nearest 16px multiple) |
| Mobile hero | `high` | `1024x1536` (portrait) |
| Print / 4K | `high` | `3840x2160` or `2160x3840` |
| Texture / tile | `medium` | `1024x1024` |
| Icon / avatar | `medium` | `512x512` or `256x256` |

### Multi-Candidate Strategy

For important visual assets (hero images, key illustrations), generate multiple
candidates and select the best:

- **Same prompt, quick variations** — request a single-request batch of 4 from
  one detailed prompt into a candidates directory.
- **Same prompt, structurally different directions** — run a streaming
  multi-slot generation capped at 4 slots into the same directory.
- **Neither capability available** — generate 3-4 candidates one at a time,
  inspecting between calls (see § When Only Single-Image Generation Exists).

After generation, inspect every candidate visually before selecting.
Do not blindly use the first result.

### Parallel Generation Patterns (FE-ASSET-PARALLEL-01, DEFAULT)

There are three ways to get several candidates at once. They are not
interchangeable; choose by intent, and choose only among the ones the generator
actually has:

| Strategy | Capability required | When to Use | Behavior |
|----------|---------------------|-------------|----------|
| **Single-request batch** | One request returning N images from one prompt | Same prompt, want quick variations | One request in flight; N images come back together |
| **Streaming multi-slot** | Incremental slot-by-slot generation with per-slot cancel | Same prompt, want structurally different directions | Progress arrives slot by slot; each slot is an independent generation and can be cancelled early |
| **Independent parallel jobs** | Ability to launch several requests concurrently | Different prompts, or mixed providers/models | Each is a separate request, fully independent; nothing is shared between them |

**Single-request batch** is fastest for same-prompt variations. **Streaming
multi-slot** is better when you want to see each candidate arrive and
potentially cancel early. **Independent parallel jobs** are for concept
exploration with different prompts or provider/model mixes.

#### Independent Parallel Recipe

The strategy is what matters: launch three genuinely different prompts
concurrently, watch them, and stop the ones you no longer need as soon as a
better candidate lands. In a shell where the generator is a command,
that reads as:

```bash
# Launch 3 different prompts concurrently
<generator> "editorial hero with serif headline" --quality high -o ./out/editorial.png &
<generator> "product-led hero with device mockup" --quality high -o ./out/product.png &
<generator> "abstract gradient hero with floating shapes" --quality high -o ./out/abstract.png &

# Monitor active jobs, if the generator has a job-listing surface

# Cancel a job if a better candidate arrives first, if it has a cancel surface

# Wait for all to finish
wait
```

If the generator is not a shell command, the same three-prompt fan-out applies
through whatever call surface it does have. If it cannot run requests
concurrently at all, run the three prompts sequentially and accept the latency;
do not collapse them into one prompt, because the point of the pattern is three
different directions.

#### Monitoring and Cancellation

For long-running generation (high quality, large size, video), monitor progress
through the generator's job-listing surface if it has one — typically request
id, kind, phase, start time, and a truncated prompt — and abort unwanted work
through its cancel surface.

Both surfaces are frequently absent. When they are, treat every launched job as
uninterruptible: launch fewer jobs at a time, and prefer smaller/faster quality
tiers while exploring, since a wrong direction cannot be stopped once started.

#### Capacity Guard

A generator backed by a job server usually caps concurrent jobs and rejects
overflow rather than queueing it, commonly as a rate-limit response (HTTP 429)
with a `Retry-After` hint. Read the actual cap from the generator's own
documentation rather than assuming a number. Agent pattern: check the in-flight
job count before launching a batch; if it is near the cap, wait or cancel
low-priority jobs first. With no job-listing surface, track what you launched
yourself and keep the fan-out small.

#### When Only Single-Image Generation Exists

Some runtimes provide only one image per call. In that case, for parallel
exploration, generate sequentially and inspect each result before the next.
Streaming multi-slot and independent parallel jobs have no equivalent; degrade
to single-image iteration with prompt refinement between rounds, and budget for
the extra wall-clock time in the plan rather than silently cutting the candidate
count to one.

### Variant Selection Workflow (FE-ASSET-SELECT-01, DEFAULT)

After generating multiple candidates (via a batch, a multi-slot run, or
independent parallel jobs), select using a two-stage process:

**Stage 1 — Exploration (broad):** Generate 3-5 candidates with different
directions. Inspect all of them visually. Do not select yet.

**Stage 2 — Synthesis (not winner-picking):** Do NOT pick one winner. Build
an element ledger — for each design token (palette, composition, type
treatment, hero visual, stat row, section rhythm), note WHICH candidate did
it best and WHY. The final direction is assembled from the best elements
across all candidates. This mirrors `dev-uiux-design` UX-CONCEPT-GEN-01 step 3.

#### Selection Scorecard

Rate each candidate on these axes before synthesizing:

| Axis | What to Check |
|------|---------------|
| Subject fidelity | Does the main subject match the brief? |
| Composition | Framing, negative space, visual weight balance |
| Palette | Color harmony, brand alignment, contrast |
| Text render | Korean/English text legibility (if applicable) |
| Asset-type fit | Right dimensions, crop safety, overlay space |
| Technical quality | No artifacts, correct lighting, clean edges |

#### When Only Single-Image Generation Exists

With one image per call, generate 1-2 candidates, inspect them, refine the
prompt based on what is wrong, and iterate. The synthesis step still applies
when comparing across iteration rounds: the ledger compares rounds instead of
siblings.

### Provider Routing (FE-ASSET-PROVIDER-01, DEFAULT)

When your generator can route across multiple providers, choose by asset type.
The "Why" column is the portable part; the provider examples are the landscape
as observed 2026-07 and should be re-checked, not trusted as fixed:

| Asset Type | Preferred provider class | Why |
|-----------|--------------------------|-----|
| Product hero, editorial, UI mockup | Strongest general image model, via an authenticated account when both account and metered key are configured | Best composition, text rendering, style control |
| Trending/cultural reference needed | A provider that grounds generation in a live web search | The search grounds the generation in current references |
| Budget draft, quick iteration | The cheapest configured provider | Cheapest per-image cost |
| High-fidelity product photo | Strongest general image model at its highest quality tier | Best detail, lighting, material rendering |
| Korean text in image | Strongest text-rendering model in direct (no-rewrite) prompt mode | Best Hangul rendering with exact-text prompts |

Route per request, not by changing a global default: an asset-type choice that
outlives the request will silently mis-route the next asset.

#### When The Generator Has One Provider

Many runtimes expose exactly one image model and no routing at all. Then no
provider routing is needed; quality and style are controlled through prompt
detail and the quality setting alone. Do not report a routing decision that the
runtime cannot make.

### Reference Image Workflow

When a design reference, brand guide, or existing asset exists, always attach it
if the generator supports reference-image attachment:

```text
Style reference: style-guide.png (role: style)
Composition + style: layout-ref.png (role: composition)
                     brand-colors.png (role: color/style)
```

Label each reference's role in the prompt text: "Use Image 1 as composition
reference. Use Image 2 as color/style reference."

If the generator accepts no reference images, describe the reference in words
inside the prompt — exact hex values, measured proportions, named type
treatment — and expect lower fidelity; note the substitution in the dev note.

### Korean Text in Images

When generating images with Korean text:
- Write the exact Korean string in quotes: `"오늘의 추천"`, not "some Korean text"
- Specify font style: `고딕체 (Gothic/Sans)` or `명조체 (Myeongjo/Serif)`
- Specify placement and approximate size relative to the canvas
- For mixed Korean + English, specify which script appears where
- Verify rendered text after generation — garbled Hangul is common and must be caught

### Asset Background Strategy (FE-ASSET-BG-01, DEFAULT)

Current large image models do not reliably produce true transparent (alpha)
backgrounds. Requesting "transparent background" or "PNG with alpha" yields
unpredictable results — sometimes a faint checkerboard pattern, sometimes a
solid color pretending to be transparent. Use the solid-background-then-remove
strategy:

**Generation: pure solid background.**

For cutout assets (icons, product shots, 3D objects, illustrations, logos,
stickers, UI elements that must float over arbitrary backgrounds):

```text
# Pure black background — best for light/reflective subjects (chrome, glass, metal)
Prompt: 3D render of a liquid chrome splash blob, organic starburst shape,
  mirror-polished surface with iridescent cyan and gold reflections.
  Floating on a PURE SOLID BLACK background. The background must be 100% flat
  pure black hex #000000. No checkerboard, no transparency pattern, no gradient,
  no floor plane, no shadow, no vignette, no ambient glow on the background.
Settings: highest quality tier, 1024x1024, direct prompt mode
Output: chrome-splash.png

# Pure white background — best for dark/opaque subjects (products, dark UI elements)
Prompt: Clean product photo of a matte black wireless earbud, centered,
  floating at slight angle. PURE SOLID WHITE background hex #ffffff.
  No shadow, no gradient, no surface, no reflection plane.
Settings: highest quality tier, 1024x1024, direct prompt mode
Output: earbud-cutout.png

# Solid brand color background — when the target surface color is known
Prompt: Flat illustration of a coffee cup with steam, centered.
  PURE SOLID background hex #f5f0eb (exact match required).
  No gradient, no texture, no shadow.
Settings: medium quality tier, 512x512, direct prompt mode
Output: coffee-icon.png
```

**Background prompt rules:**
- State the exact hex code and repeat the constraint: "PURE SOLID [color] background hex #XXXXXX"
- Explicitly ban common AI additions: "No checkerboard, no transparency pattern, no gradient, no floor plane, no shadow, no vignette, no ambient glow"
- Use direct prompt mode, if the generator has one, to prevent server-side prompt rewriting that might soften the constraint. Without it, repeat the background constraint twice in the prompt so a rewrite is less likely to drop it
- Black works best for reflective/metallic/glass subjects; white for dark/matte subjects
- Match the target page background color when the destination is known

**Post-processing: background removal.**

| Method | When to Use | How |
|--------|-------------|-----|
| **CSS `mix-blend-mode`** | Black bg → light page | `mix-blend-mode: screen` makes black transparent, keeps light content |
| **CSS `mix-blend-mode`** | White bg → dark page | `mix-blend-mode: multiply` makes white transparent, keeps dark content |
| **Interactive canvas**, if available | Interactive cleanup | Open the asset in the generator's canvas surface → background cleanup → export with alpha or matte |
| **Programmatic removal** | Build pipeline | `sharp` / ImageMagick / rembg for batch processing |
| **Edit / inpaint pass**, if available | Targeted fix | Re-run the asset through the edit surface with "remove the background completely, keep only the [subject]" |

**CSS blend-mode recipe (zero post-processing):**

```css
/* Black background asset on a light page */
.chrome-asset {
  mix-blend-mode: screen; /* black → transparent, light content preserved */
}

/* White background asset on a dark page */
.product-asset {
  mix-blend-mode: multiply; /* white → transparent, dark content preserved */
}

/* For arbitrary backgrounds, layer with isolation */
.asset-container {
  isolation: isolate; /* prevent blend from leaking to parent */
}
```

**When the generator has no canvas or edit surface:** the same solid-background
prompting strategy still applies. Use CSS blend modes or programmatic removal
only.

**Anti-pattern:** requesting "transparent background" or "PNG with alpha channel"
directly in the prompt. The model will often produce a fake checkerboard pattern
burned into the image, or ignore the request entirely. Always use the
solid-background strategy above.

### Prompt Iteration

- Start with one high-detail prompt. Inspect the result before iterating.
- On the next iteration, make ONE targeted change and re-specify all constraints.
  Do not rewrite the entire prompt from scratch.
- Repeat invariants every iteration to prevent drift.
- If the model consistently fails on a detail, try rephrasing or breaking the
  request into a base generation + edit pass. With no edit capability, break it
  into a simpler subject and composite in code instead.

### Frontend Asset Quick Recipes

**Hero image (landing page):**
```text
Prompt: Use case: product-mockup. Asset type: landing page hero. A premium wireless headphone floating at a slight angle against a soft warm-gray studio backdrop. Matte black finish with brushed aluminum accents. Soft three-point studio lighting, key light from upper-left. Shallow depth of field. Wide composition with generous negative space on the right for headline overlay. No text, no logos, no watermark.
Settings: highest quality tier, 1536x1024
Output: hero.png
```

**OG / social share image:**
```text
Prompt: Use case: ads-marketing. Asset type: social share card. Clean product flat-lay of a notebook, pen, and ceramic mug on a white marble desk. Overhead shot. Soft diffused daylight. Space in the upper third for title overlay. Warm neutral palette. No text, no logos, no watermark.
Settings: highest quality tier, 1200x640
Output: og-image.png
```

**App screenshot mockup background:**
```text
Prompt: Use case: stylized-concept. Asset type: hero background for device mockup. Soft abstract gradient from #f0f4f8 to #dbeafe with subtle geometric shapes at 5% opacity. Clean, modern, minimal. No objects, no patterns, no text.
Settings: medium quality tier, 1920x1088
Output: mockup-bg.png
```

**Avatar / profile placeholder:**
```text
Prompt: Use case: stylized-concept. Asset type: user avatar. Friendly stylized portrait of a young professional, neutral expression, looking slightly left. Flat illustration style with subtle shadows. Solid #e5e7eb background. Circular crop safe. No text.
Settings: medium quality tier, 512x512
Output: avatar.png
```

---

## Image-Set Continuity (FE-IMAGE-SET-CONTINUITY-01, DEFAULT)

Source: taste-skill imagegen-frontend-web (62k stars), adapted for the
agent image-generation workflow in this skill family.

Multi-image sets for landing/marketing pages must maintain visual-world continuity
across all frames. A viewer flipping through every per-section frame must still
recognize one brand — anything that breaks brand recall is over-variation.

### Frame-count defaults

| Request type | Sections | Frames |
|-------------|----------|--------|
| Hero only | 1 | 1 |
| Landing page | 6 | 6 |
| Full website | 8 | 8 |
| Marketing site | 8 | 8 |
| Product page | 6 | 6 |
| Portfolio | 6 | 6 |

Generate one separate horizontal image (16:9 or 21:9) per section. Each image
is one section, generated as its own call. Attach the first frame as a style
reference for every subsequent frame; if the generator accepts no reference
images, carry the continuity contract below in the prompt text of every frame
instead and check the set for drift after generation.

### Continuity contract (enforce across all frames)

- Same brand world, palette, and accent logic
- Same type-scale logic and spacing discipline
- Same CTA family (style variations fine, identity changes not)
- Same icon/illustration mood and image treatment (grade, framing, material)
- Same tonal language in copy
- Same border-radius language

### Allowed variation

- Composition anchor (MUST vary — see FE-IMAGE-ANCHOR-ROTATION-01)
- Background mode (solid, full-bleed photo, duotone, atmospheric)
- Section size and density
- Placement of the single second-read moment

---

## Image Anchor Rotation (FE-IMAGE-ANCHOR-ROTATION-01, DEFAULT)

Source: taste-skill imagegen-frontend-web, adapted for UX-CONCEPT-GEN-01.

### Composition anchors (pick one per section)

- Centered statement
- Top-left lead, support bottom-right
- Bottom-left text over background image
- Bottom-right CTA cluster
- Left-third caption + right-two-thirds visual
- Right-third caption + left-two-thirds visual
- Centered low
- Off-grid editorial offset
- Stacked center
- Image-as-canvas with text overlaid in clean safe area

### Rotation rules

- At least 3 different anchors must appear across a multi-section set.
- Same anchor cannot repeat more than 2 sections in a row.
- Same background mode cannot repeat more than 3 sections in a row.
- The classic left-third/right-two-thirds anchor: sparingly, never twice in a row.
- Non-minimalist sites must include at least one full-bleed/duotone/atmospheric
  background AND at least one mini-minimalist section.

### Application to UX-CONCEPT-GEN-01

In the 5-render concept pass, each render MUST vary the composition anchor.
Repetitive same-layout renders are wasted candidates. The element ledger
(step 3) must cite WHICH variant used which anchor and which was best.
