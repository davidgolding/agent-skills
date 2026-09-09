# Data Schemas

This document defines the TOON shape of the four persistent documents. TOON is indentation-based key:value notation; arrays of uniform objects use the compact tabular form `name[N]{col1,col2,...}:` followed by one comma-separated row per item.

All four documents live together in the agent's configured or default training data directory. The skill instructions remain file-path agnostic, allowing the agent environment to manage the storage path through its own settings.

---

## `profile.toon`

```
updated: 2026-01-15
identity:
  name: Alex
  age: 34
  sex: female
  training_age_years: 2
goals[2]{goal,target_date,priority}:
  General strength and a first pull-up,2026-07-01,primary
  Improve 5k time,,secondary
history:
  background: Recreational lifter, ran track in college, 2 years off before restarting.
  current_capacity: Squat 185x5, deadlift 225x5, can run 5k in 28:00.
equipment:
  access: Full commercial gym, 4x/week
  home_backup: Adjustable dumbbells, pull-up bar
schedule:
  days_per_week: 4
  session_length_minutes: 60
  fixed_days: Mon,Tue,Thu,Sat
preferences:
  likes: Barbell work, running outdoors
  dislikes: Group classes, burpees
  modalities_of_interest: strength,endurance,mobility
medical_screen:
  conditions: none
  medications: none
  injuries: Right shoulder impingement, resolved 2024, occasional stiffness overhead
  surgeries: none
  pregnancy: not applicable
  cardiac_flags: none
  last_screened: 2026-01-15
contraindications[1]{movement_pattern,reason,severity}:
  Heavy overhead pressing,History of right shoulder impingement,caution
```

- `goals` — array; `priority` is `primary` or `secondary`.
- `contraindications` — derived from `medical_screen`, not restated from it; this is the field programming actually checks against (see `references/safety.md`). `severity` is `caution` (modify/monitor) or `hard` (exclude entirely).
- `medical_screen.last_screened` — the field block review checks for staleness.

---

## `program.toon`

```
block:
  name: Block 3 — strength base
  start_date: 2026-01-15
  end_date: 2026-02-26
  goal_focus: General strength and a first pull-up
week_template[4]{day,modality,focus,notes}:
  Mon,strength,Lower body — squat pattern,
  Tue,endurance,Zone 2 run 30min,
  Thu,strength,Upper body — press/pull,Watch overhead volume per contraindication
  Sat,hiit,Intervals 6x400m,Placed after 48h from Thu upper session
current_week: 3
```

- `week_template` is the standing weekly allocation this block programs against — this is what single-session requests get checked against (Integrated Weekly Load Management pattern).
- Reshaped in full at block review; not touched by session-level autoregulation, which instead adjusts the next log entry's prescribed loads.

---

## `log.toon`

Two sections: recent full-detail entries (current block) and compressed prior-block summaries.

```
entries[2]{date,modality,planned,actual,rir_or_rpe,notes}:
  2026-02-01,strength,Squat 5x5 @185,Squat 5x5 @185,RIR 3,Felt strong
  2026-02-03,endurance,Zone 2 run 30min,Zone 2 run 28min,RPE 5,Cut short - time
compressed[1]{block_name,date_range,summary}:
  Block 2 — hypertrophy,2025-12-04..2026-01-14,"Squat 155->185x5, deadlift 205->225x5, 1 missed session (illness wk3), no pain reported"
```

- `entries` — only the current block's rows; this is the bounded window sessions read.
- `compressed` — one row per prior block, written by block review's compression step. Preserves trend (start->end numbers), adherence (missed sessions), and any flagged pain/symptoms — not set-by-set detail.

---

## `measurements.toon`

```
entries[3]{date,metric,value}:
  2026-01-15,bodyweight_lb,142
  2026-01-15,squat_1rm_est_lb,205
  2026-02-01,bodyweight_lb,141
```

- Free-form `metric` names so any tracked marker (bodyweight, estimated 1RMs, 5k time, resting HR) fits the same table.
- Read in full, or filtered by metric for a specific trend question — this file stays small enough that compression isn't needed.
