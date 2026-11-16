# Car Purchaser Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by car-purchaser.

## Patterns

- **Name**: Deal Folder
- **Description**: All deal state lives in one local folder, `car-deal/`, in the buyer's working directory. It holds six Markdown files: `profile.md` (needs, budget, credit tier, trade-in, location, timeline), `research.md` (candidate vehicles, benchmarks, state rules, each with source and check date), `plan.md` (route, steps, walk-away number, scripts, red flags, route-change log), `quotes.md` (the quote ledger), `messages.md` (every drafted and received message, dated), and `signing-sheet.md`. Each session reads the folder first and writes to it as decisions land.
- **When**: At the start of every invocation, and whenever a decision, quote, or message comes in.
- **Example**:
```
    car-deal/
      profile.md        # 3 riders + 2 car seats, 60 mi/day commute, OTD cap $36,000
      research.md       # RAV4 Hybrid XLE: market avg $34,150 (source, checked 2026-11-16)
      plan.md           # Route: remote. Walk-away OTD: $35,400
      quotes.md         # 4 dealers, normalized to OTD
      messages.md       # 2026-11-17 draft to Dealer B, buyer sent 2026-11-17
      signing-sheet.md  # phone-readable, works on its own
```

---

- **Name**: One-Question Interview
- **Description**: The interview asks one question at a time and moves needs → money → logistics. Needs: riders, car seats, cargo, towing, commute distance, climate, parking, accessibility, must-have and deal-breaker features. Money: walk-away out-the-door total, comfortable monthly figure (recorded but not used to negotiate), down payment, credit tier, current loan or lease payoff, trade-in details. Logistics: ZIP code, how far the buyer will travel, deadline. Stop as soon as the plan can be written, and record unknowns as open items.
- **When**: Phase 01 of a new deal, or when a returning buyer's circumstances change.
- **Example**:
```
    Ask: "How many people ride along on a normal week, and do any of them need a car seat?"
    Record in profile.md: "Riders: 4 typical; 2 rear-facing seats -> needs LATCH x2 + rear legroom >= 37 in"
```

---

- **Name**: Scenario and Route Selection
- **Description**: Choose the scenario (new from a dealer, used or CPO from a dealer, private-party used, or lease) from the interview. When lease versus buy is unsettled, compare both over the buyer's expected ownership period. Start every dealer and online-seller deal on the remote route. Switch to the hybrid route only for one of these reasons, recorded in `plan.md`: the model is scarce (few units within the buyer's travel radius, or market price above MSRP); two or more sellers refuse written out-the-door quotes; it's a private-party sale; or the buyer must see or drive the specific unit before quoting means anything (a used car with condition questions).
- **When**: After the interview and first research sweep, and again whenever new evidence meets a switch reason.
- **Example**:
```
    plan.md -> Route log
    2026-11-16  Route: remote (12 matching units within 150 mi; no market markups found)
    2026-11-20  Route: hybrid. Reason: 3 of 4 dealers replied "come in for pricing"; 1 unit left in region
```

---

- **Name**: Remote Route Sequence
- **Description**: The remote route runs in a fixed order. (1) Settle exact specs: trim, packages, colors acceptable, build or VIN. (2) Get outside financing pre-approval and independent trade-in offers. (3) Test drive the model at a dealer you won't buy from, or one that doesn't have your contact details, or skip it if the buyer has already driven one. (4) Send out-the-door quote requests to several sellers, including online retailers with home delivery. (5) Normalize the quotes in the ledger and send counters that cite the best competing figure. (6) Lock the winner in writing, itemized. (7) Generate the signing sheet. (8) One visit to sign, or home delivery.
- **When**: Every dealer or online-seller deal on the remote route.
- **Example**:
```
    plan.md
    [ ] 1 Specs locked: 2026 RAV4 Hybrid XLE, Weather Pkg, any of 3 colors
    [ ] 2 Credit union pre-approval: 5.9% / 60 mo (source, date)  |  Trade offers: CarMax $14,200, Carvana $13,900
    [ ] 3 Test drive at Dealer Z (not in bidding), using alias email only
    [ ] 4 OTD requests -> Dealers A, B, C, D + 1 online retailer
    ...
```

---

- **Name**: Out-the-Door Quote Request
- **Description**: Every quote request asks for an itemized out-the-door price on a specific vehicle (VIN or stock number when available). It states that the buyer is comparing several sellers in writing, has outside financing, and is negotiating any trade-in separately. It asks for every line: selling price, each dealer fee, each add-on, tax, title, and registration. Keep it short and polite, and leave out the buyer's phone number, credit details, and target price.
- **When**: Remote route step 4, and any new seller added later.
- **Example**:
```
    Subject: OTD quote request - stock #A1234, 2026 RAV4 Hybrid XLE

    Hello, I'm buying this vehicle within the next two weeks and am collecting written
    out-the-door quotes from several dealers. Please email an itemized OTD price for
    stock #A1234: selling price, every dealer fee, any installed add-ons, tax, title,
    and registration for ZIP 80202. I have outside financing arranged and will handle
    any trade separately. Email is the best way to reach me. Thank you.
```

---

- **Name**: Quote Normalization Ledger
- **Description**: Every quote goes into `quotes.md` as a row: seller, date received, VIN or stock number, selling price, each fee by name, add-ons, tax, title and registration, out-the-door total, expiry, and flags. Fill missing lines from the buyer's state research and mark them "estimated." Rank by out-the-door total. Flags: a missing line, a fee above state norms or caps, a pre-installed add-on, a quote given only as a monthly payment, or a total that quietly changes between replies.
- **When**: Whenever a quote arrives, including verbal quotes the buyer relays.
- **Example**:
```
    | Seller | Date | Stock | Price | Doc fee | Add-ons | Tax/Title/Reg | OTD | Flags |
    | A | 11-18 | A1234 | 32,400 | 299 | 0 | 2,415 | 35,114 | - |
    | B | 11-18 | B5521 | 31,900 | 599 | 1,295 "appearance pkg" | 2,520 | 36,314 | add-on pre-loaded; doc fee high |
```

---

- **Name**: Counter With Competing Figures
- **Description**: A counter cites the best competing out-the-door total in the ledger (without naming the dealer when the buyer prefers), asks the seller to beat it in writing, and gives a reply deadline. Keep price, trade-in, financing, and add-ons out of the same message.
- **When**: After at least two normalized quotes are in.
- **Example**:
```
    Thanks for the quote. I have a written out-the-door offer of $35,114 for the same
    trim and packages. If you can beat that OTD in writing by Friday, I'm ready to
    schedule signing.
```

---

- **Name**: Plan Format Selection
- **Description**: Choose the plan's format from the scenario's shape. A checklist suits linear routes (remote dealer purchase, online retailer). A decision flow chart suits routes with forks (private-party inspection outcomes, lease versus buy, a hybrid route with walk-away branches). A script set suits a phase the buyer runs live (test drive, a phone call with a private seller, the F&I office). Combine formats when the plan has more than one of these shapes, and write flow charts as Mermaid inside `plan.md`.
- **When**: Writing or rewriting `plan.md`.
- **Example**:
```
    ```mermaid
    flowchart TD
      A[Private seller listing] --> B{Title in seller's name, no lien?}
      B -- No --> X[Walk away]
      B -- Yes --> C{Independent inspection passes?}
      C -- No, minor --> D[Renegotiate with repair quote]
      C -- No, major --> X
      C -- Yes --> E[Pay at buyer's bank, title transfer same day]
    ```
```

---

- **Name**: Separate Negotiations Order
- **Description**: Negotiate in this order: vehicle out-the-door price → trade-in value → financing rate → add-ons. Lock each in writing before raising the next. When a seller merges them (a "four-square" worksheet, or "what payment works for you?"), the buyer steers back to the single number on the table.
- **When**: Every dealer deal, in writing or in person.
- **Example**:
```
    Script: "I'm only discussing the out-the-door price of the vehicle right now.
    Once that's set in writing, we can talk about my trade."
```

---

- **Name**: Lease Math in Plain Numbers
- **Description**: For a lease, get the capitalized cost (negotiated like a purchase price), money factor, residual value, acquisition and disposition fees, mileage allowance, and any due-at-signing amount. Convert the money factor to an APR (multiply by 2,400) and compare it with the lender's published base rate. Compare the total lease cost with buying over the same period, including expected excess-mileage and wear charges.
- **When**: The lease scenario, or a lease-versus-buy comparison.
- **Example**:
```
    Money factor 0.00250 x 2400 = 6.0% APR (captive base 0.00185 = 4.4%, source, date)
    -> 1.6-point markup; ask for the base money factor in writing.
```

---

- **Name**: Self-Contained Signing Sheet
- **Description**: `signing-sheet.md` fits on one phone screen per section and reads without the rest of the deal folder. It holds the seller and VIN, the locked out-the-door total and its date, every allowed line item and amount, the agreed rate, term, and lender (or "outside financing"), the trade-in value and payoff, add-ons accepted (normally none), walk-away triggers, and a one-line script for each trigger. It ends with a short check sequence: compare the VIN, then each line, then the total, then rate and term, then blank fields, then any "spot delivery" or "financing pending" language.
- **When**: As soon as a quote is locked, and again on any change.
- **Example**:
```
    LOCKED OTD: $35,114 (Dealer A, email 11-19)  VIN ...4XYZ
    Lines: Price 32,400 | Doc 299 | Tax 2,215 | Title/Reg 200
    Rate: outside CU 5.9% / 60 mo | Trade: $14,200 (payoff $9,800)
    WALK if: any new line item | total > 35,114 | rate/term differs | blank fields | "pending approval" clause
    SAY: "This doesn't match the written quote from 11-19. Please correct it to match, or I'll leave."
```

---

- **Name**: Live Research With Citations
- **Description**: Each session researches what changes: local and online inventory, market price benchmarks, manufacturer incentives, loan and lease rates, recalls and reliability, the buyer's state rules (doc-fee caps, tax and title, lemon law, used-car rules, cooling-off rights), and emerging scams or tactics. Every figure is written as "value (source, checked YYYY-MM-DD)." When a live finding contradicts this skill's references, use the live finding and record the conflict in `research.md`.
- **When**: Phase 02, any inventory sweep, and any time the buyer asks about a figure older than about a week.
- **Example**:
```
    research.md
    State doc fee: no statutory cap found; local median $399 (state AG consumer page; dealer survey, checked 2026-11-16)
    Conflict: sharp_edges.md lists "doc-fee capped in some states"; buyer's state has none. Live finding used.
```

---

- **Name**: Inventory Sweep and Opt-In Watch
- **Description**: By default, inventory search runs on demand. It covers dealer sites, aggregators, and online retailers within the buyer's travel radius, and ranks by out-the-door estimate and fit. Each hit gets a quick pre-screen: price against market, history-report flags, days on market, and the seller's complaint record. When the buyer asks for a recurring watch, set it up with the harness's scheduling feature after the buyer approves the schedule and criteria. When scheduling is unavailable, say so and suggest how often to ask for a new sweep.
- **When**: Phase 02, and whenever the buyer asks for new listings.
- **Example**:
```
    Sweep 2026-11-18: 9 matches. Top 3 by est. OTD:
    1. Dealer C stock C88 - est OTD $34,900, 41 days on lot (leverage), clean history
    2. Online retailer - $35,300 delivered, 7-day return (fine print: restocking fee $0, checked)
```

---

- **Name**: Post-Purchase Close-Out
- **Description**: After signing, produce a dated checklist: copies of every signed document; cancellation windows for any add-on accepted under pressure (with the refund method); confirmation that the trade-in loan was paid off; title and registration status; insurance updated before driving; recall registration with the manufacturer; turning off any alias email or forwarding number; and a final update to the deal folder.
- **When**: Phase 07, right after the buyer reports signing.
- **Example**:
```
    [ ] Cancel "tire & wheel" plan by 2026-12-19 (prorated refund to loan principal)
    [ ] Confirm trade payoff posted to old lender by 2026-12-05
    [ ] Retire alias email after final delivery confirmation
```

---

- **Name**: Verdict-First Reply
- **Description**: The first one or two lines of every reply give the verdict (sign or don't, scam or not, good quote or not) and the buyer's single next action. Then fit the length to the moment. At the signing desk, for a quick read, for a tired buyer, or on a first turn: about 150 words or fewer, plus any ready-to-send draft or script. Put the full reasoning, math, and tables in the deal folder and offer them in one line. During planning and research sessions where the buyer is at a desk with time, longer replies are fine, still verdict first.
- **When**: Every reply to the buyer.
- **Example**:
```
    Don't sign - this doesn't match your 11-15 quote ($35,114). Hand it back and say:
    "Please remove the $695 package and the dealer financing so it matches the written quote, or I'll leave."
    Walk if they refuse. Also flagged: 6.9%/72 vs your 5.9%/60, and a "subject to financing approval"
    clause - both must go. Full line-by-line check is in your signing sheet; ask if you want it here.
```

---

## Anti-Patterns

- **Name**: Wall of Explanation
- **Description**: Leading with background, tactic names, or a full line-by-line analysis before the buyer learns what to do, or sending a long reply when the buyer is under time pressure or asked for a quick read.
- **Why**: A buyer at the desk or worn out from dealer contact needs the action in seconds. A long reply buries the action and adds to the fatigue the skill exists to reduce.
- **Instead**: Use the Verdict-First Reply pattern, put the detail in the deal folder, and offer it in one line.

---

- **Name**: Monthly-Payment Negotiation
- **Description**: Discussing or ranking deals by monthly payment instead of out-the-door total.
- **Why**: A payment target lets the seller stretch the loan term, mark up the rate, or pack in add-ons while the payment still "fits."
- **Instead**: Negotiate and rank only by out-the-door total, and record the buyer's comfortable payment privately in `profile.md` as an affordability check.

---

- **Name**: Blended Negotiation
- **Description**: Letting price, trade-in, financing, and add-ons be discussed as one package.
- **Why**: A higher trade-in offer can be paid for with a higher price or rate, and the buyer can't see where the money moved.
- **Instead**: Follow the Separate Negotiations Order and lock each figure in writing before raising the next.

---

- **Name**: Stale Figure Stated as Fact
- **Description**: Quoting a price, rate, incentive, fee cap, or rule from memory or from this skill's references without a live check.
- **Why**: Incentives, rates, and state rules change monthly, and a stale figure gives the seller an opening and the buyer false confidence.
- **Instead**: Research live, cite the source and check date, and record any conflict with the references.

---

- **Name**: Agent-Sent Outreach
- **Description**: Sending messages, filling out seller lead forms, or submitting credit applications for the buyer.
- **Why**: The buyer chose to keep control of every contact channel. A submitted lead form exposes their real contact details and triggers the follow-up calls they want to avoid.
- **Instead**: Draft the message, show it to the buyer, and log it in `messages.md` once the buyer confirms they sent it.

---

- **Name**: Generic Buying Guide
- **Description**: Producing a plan that reads like general car-buying advice instead of this buyer's route, vehicles, numbers, and dates.
- **Why**: Generic advice leaves the buyer to work out the steps that matter, and leaves them unprepared for the moments they're pressured.
- **Instead**: Fill the plan with the buyer's walk-away number, candidate vehicles, named sellers, locked benchmarks, deadlines, and scripts for their scenario.

---

- **Name**: Inventory Before Needs
- **Description**: Searching listings before the needs and walk-away budget are recorded.
- **Why**: A listing that's about to sell creates urgency, and the buyer ends up adjusting their needs to fit what's available.
- **Instead**: Finish the needs and money parts of the interview first, then sweep against those criteria.

---

- **Name**: Folder-Dependent Signing Check
- **Description**: A signing sheet that refers to other deal files ("see quotes.md") instead of carrying the numbers itself.
- **Why**: At the desk the buyer may only have a phone session that can't open the deal folder.
- **Instead**: Put every figure and trigger the check needs into `signing-sheet.md` itself.
