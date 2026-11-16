# Validations

This document defines the validations used by car-purchaser.

---

## Volatile Figure Lacks Source and Date

- **Id**: deal-figure-uncited
- **Severity**: error
- **Type**: semantic
- **Pattern**: A price, fee, rate, money factor, incentive, tax figure, fee cap, or state rule stated in a deal-folder file or in a reply to the buyer without a named source and a check date.
- **Message**: Every volatile figure needs its source and the date it was checked, so the buyer can trust it and the next session can tell when it has gone stale.
- **Fix Action**: Check the figure live and rewrite it as "value (source, checked YYYY-MM-DD)", or mark it "estimated" and give the basis.
- **Applies To**:
    - car-deal/*.md

---

## Quote Missing Out-the-Door Total

- **Id**: deal-quote-not-normalized
- **Severity**: error
- **Type**: schema
- **Pattern**: A row in the quote ledger without seller, date received, VIN or stock number, selling price, itemized fees, tax and title, out-the-door total, and flags; or a ledger ranked by anything other than out-the-door total.
- **Message**: Quotes are comparable only as itemized out-the-door totals.
- **Fix Action**: Fill each missing field, using the buyer's state research for any line the seller left out (marked "estimated"), and re-rank by out-the-door total.
- **Applies To**:
    - car-deal/quotes.md

---

## Plan Missing Walk-Away Number or Route Reason

- **Id**: deal-plan-incomplete
- **Severity**: error
- **Type**: schema
- **Pattern**: A buying plan without a walk-away out-the-door figure, a stated route (remote or hybrid), a dated route log with a reason for every switch to hybrid, ordered steps, and scripts for the scenario's pressure points.
- **Message**: The plan has to tell the buyer when to walk away and why the route was chosen.
- **Fix Action**: Add the walk-away number from the profile, the route with its reason, the ordered steps, and the scripts for the scenario.
- **Applies To**:
    - car-deal/plan.md

---

## Signing Sheet Not Self-Contained

- **Id**: deal-signing-sheet-incomplete
- **Severity**: error
- **Type**: schema
- **Pattern**: A signing sheet missing any of: seller, VIN, locked out-the-door total and its date, every allowed line item with amount, rate, term, and lender (or outside financing), trade-in value and payoff (when there's a trade-in), accepted add-ons, walk-away triggers with a script for each, and the check sequence; or one that refers to other deal files instead of stating the figure.
- **Message**: The signing sheet has to work on a phone with no access to the rest of the deal folder.
- **Fix Action**: Copy each missing figure and trigger into the signing sheet itself.
- **Applies To**:
    - car-deal/signing-sheet.md

---

## Outbound Draft Leaks Leverage or Personal Data

- **Id**: deal-draft-leak
- **Severity**: error
- **Type**: semantic
- **Pattern**: A drafted seller message that reveals the buyer's walk-away number, target monthly payment, credit score or tier, income, Social Security number, date of birth, or primary phone number, or that mixes price with trade-in, financing, or add-ons in a single ask.
- **Message**: Drafts give sellers only what they need to quote, and one negotiation at a time.
- **Fix Action**: Remove the leaked detail, and split the message so it raises only the number currently being negotiated.
- **Applies To**:
    - car-deal/messages.md

---

## Agent Transmitted a Message or Personal Data

- **Id**: deal-agent-sent
- **Severity**: error
- **Type**: semantic
- **Pattern**: An agent action that sends an email or text, submits a lead, credit, or contact form, or enters the buyer's personal data on a seller, lender, or listing site.
- **Message**: The buyer sends every message and submits every form themselves.
- **Fix Action**: Hand the buyer the draft or the form values to submit, and log it in `messages.md` once the buyer confirms it was sent.
- **Applies To**:
    - car-deal/messages.md
    - car-deal/plan.md

---

## Monthly Payment Used as the Negotiating Figure

- **Id**: deal-payment-framing
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - (?i)\b(?:target|aim for|offer|counter)\b.{0,40}\b(?:per month|/mo|monthly payment)\b
- **Message**: Negotiating by monthly payment invites payment packing.
- **Fix Action**: Restate the ask as an out-the-door total, and keep the buyer's payment comfort level private in the profile.
- **Applies To**:
    - car-deal/messages.md
    - car-deal/plan.md

---

## Lease Quote Missing Components

- **Id**: deal-lease-incomplete
- **Severity**: error
- **Type**: schema
- **Pattern**: A lease entry without capitalized cost, money factor with its APR equivalent, residual value, acquisition and disposition fees, mileage allowance, due-at-signing amount, and a lease-versus-buy comparison over the same period.
- **Message**: A lease can only be judged on its parts, not its payment.
- **Fix Action**: Ask the seller for each missing component in writing, and add the comparison.
- **Applies To**:
    - car-deal/quotes.md
    - car-deal/plan.md

---

## Vehicle Fails a Recorded Need

- **Id**: deal-needs-mismatch
- **Severity**: error
- **Type**: semantic
- **Pattern**: A candidate vehicle recommended in research or the plan that doesn't meet a must-have or deal-breaker recorded in the buyer's profile (seating, car seats, cargo, towing, range, accessibility, or a named feature), without the shortfall stated.
- **Message**: Every recommended vehicle has to meet every physical need from the interview, or name the gap plainly.
- **Fix Action**: Drop the vehicle, or state the specific gap and get the buyer's decision on it.
- **Applies To**:
    - car-deal/research.md
    - car-deal/plan.md

---

## Directive Money Advice

- **Id**: deal-advice-framing
- **Severity**: warning
- **Type**: semantic
- **Pattern**: Financing, trade-in, add-on, tax, or legal guidance phrased as a personal directive ("you should pay cash," "this contract is illegal") with no comparison math or no referral to a qualified source.
- **Message**: Money and legal guidance is framed as decision support: math, benchmarks, and questions to ask.
- **Fix Action**: Show the comparison and its inputs, and name who can give a binding answer where it fits.
- **Applies To**:
    - car-deal/*.md

---

## Reply Buries the Next Action

- **Id**: deal-reply-length
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A reply whose first two lines don't state the verdict and the buyer's next action; or a reply over about 150 words (excluding ready-to-send drafts and scripts) when the buyer is at the signing desk, asked for a quick read, said they're tired, or is on their first turn.
- **Message**: The buyer needs the action first, and in a short reply when time or energy is short.
- **Fix Action**: Move the verdict and next action to the top, cut the rest to what the decision needs, write the full analysis to the deal folder, and offer it in one line.
- **Applies To**:
    - car-deal/reply text shown to the buyer in chat

---

## Deal Folder Incomplete

- **Id**: deal-folder-structure
- **Severity**: warning
- **Type**: schema
- **Pattern**: A deal folder past the interview stage that lacks `profile.md`, `research.md`, or `plan.md`, or one past the first quote that lacks `quotes.md` and `messages.md`, or one with a locked quote that lacks `signing-sheet.md`.
- **Message**: Later sessions resume from the deal folder alone, so each stage leaves its file.
- **Fix Action**: Create the missing file from the current conversation and existing files, dated.
- **Applies To**:
    - car-deal/*.md
