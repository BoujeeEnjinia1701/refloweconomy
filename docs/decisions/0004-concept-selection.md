---
doc_id: RFE-DDR-004
title: ReflowEconomy concept selection
project: ReflowEconomy
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-10-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-25'
  author: Amish Chadha
  change: Concept selection between option A (reference micro-factory) and option B (sort-and-bale hub) at the kit 1.9.1 upgrade; proposed, awaiting Amish
---

# 0004: Concept selection

- **Date:** 2026-10-25
- **Status:** proposed, awaiting Amish (RFE-DEC-001 D4)

> **Safety:** Option A melts plastic under enclosing hoods and runs a shredder and two presses; option B runs one hydraulic baler with an interlocked gate. Neither choice relaxes a safety rule in the playbook.

## Context

Kit 1.8 requires at least two concept options with different working principles, scored against the user requirements (STANDARDS section 21). ReflowEconomy was designed before kit 1.8, so its reference micro-factory is option A and is not redesigned without Amish's go. Option B, a sort-and-bale hub, was added at the kit 1.9.1 upgrade on 2026-10-25 and modelled at detail level D3 like A (`cad/src/detail_b.py`). The scoring, first-order numbers and STEM rows are in RFE-OPT-001 and RFE-STM-001.

## Options considered

1. **A, reference micro-factory (thermal remanufacture).** Wash, shred, float-sink, dry, then extrude and press HDPE and PP into products; PET sold as clean flake. Keeps 51.6 % of input local on paper; USD 25,505 of equipment; morning loads about 55 A against a 40 A single-phase supply (RFE-DEC-001 D1).
2. **B, sort-and-bale hub (mechanical densification).** Hand-sort by polymer and colour and bale for a regional reprocessor. About 300 kg a shift, about USD 8,000 of equipment, about 24 A; keeps no remanufacturing on site.
3. **A with a staged start taken from B.** A stays the reference; the playbook adds a first stage in which a site runs as a sort-and-bale hub on single phase, then adds the remanufacturing line once supply and buyers are confirmed.

## Decision

Proposed, awaiting Amish. B outscores A in RFE-OPT-001 by more than 10 %, so both go to Amish with a recommendation: option 3. It keeps the pitch (recover and remanufacture locally), which B alone gives up, and it takes B's low-capital, low-power start. Option 3 adds a stage to the playbook, which changes its scope, so it is not made without Amish's word. Until he decides, the drawing, BOM and build plan describe A, as they have since RFE-DDR-001.

## Consequences

- If Amish chooses option 3: the playbook gains a staged-start section and the cost and supply figures for stage 1 (B's numbers), with no change to A's model, drawings or BOM.
- If he chooses B: the reference design, BOM, drawings, build plan, CAL and requirements are redone for B, and the pitch changes.
- If he chooses A alone: nothing changes beyond recording the choice; the supply decision (D1) still has to be made.
