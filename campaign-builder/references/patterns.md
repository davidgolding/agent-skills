# Campaign Builder Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by campaign-builder.

## Patterns

- **Name**: Whole-Presence Research Sweep
- **Description**: Check every public source on the client in a fixed order and record the source of each fact: the client website (services, service area, CTAs, phone, hours, page inventory), Google Business Profile, review platforms (Google, Yelp, Facebook, Angi, BBB, and industry-specific sites such as Avvo, Healthgrades, or Houzz), directory listings, social profiles, and press or local news mentions. Note any source that returned nothing so the brief shows what was checked.
- **When**: Phase 02, for every client, before the interview.
- **Example**:
```
    Source log
    - clientsite.com/services: drain cleaning, water heaters, repiping, sewer line (4 service pages)
    - Google Business Profile: 4.8 stars, 212 reviews, service area lists 6 cities
    - Yelp: 4.5 stars, 38 reviews
    - Facebook: page inactive since 2023; no reviews
    - BBB: A+ rating, no complaints
    - Local news: none found
```

---

- **Name**: Review-Mined Differentiators
- **Description**: Read the client's reviews for themes that recur across several reviewers, weighting recent reviews over old ones. Record each theme with a count and two or three short quotes. Recurring specifics (same-day service, upfront pricing, a named technician, a specific service) are the differentiators; one-off praise and generic praise ("great job") are not.
- **When**: Phase 02, whenever the client has reviews, and again when writing ad copy and landing page proof points.
- **Example**:
```
    Differentiator: Same-day service
    Evidence: 31 of 212 Google reviews (19 in the last 12 months)
    Quotes: "came out the same afternoon", "called at 9, fixed by noon"
    Usable in ads as: "Same-Day Service Available"
```

---

- **Name**: Industry Primer
- **Description**: Before choosing keywords, outline the industry's service categories, how buyers search (emergency versus planned, research-heavy versus impulse), seasonality, typical ticket sizes, typical margin ranges by service, and typical local CPC ranges. Use this outline to estimate the margin ranking and CPCs, and cite the benchmark sources.
- **When**: Phase 02, for every client, and in more depth when the industry is unfamiliar.
- **Example**:
```
    HVAC (residential)
    - Intent split: emergency repair (high urgency, high CPC) vs. replacement (research-heavy, highest ticket)
    - Seasonality: AC peaks Jun-Aug, heating peaks Dec-Feb
    - Relative margin (estimate): system replacement > maintenance plans > repair > diagnostics
    - Local CPC (estimate): $8-$25 depending on metro
```

---

- **Name**: Infer-Then-Confirm
- **Description**: Bring a proposed answer from research to every confirmable question and ask the user to confirm or correct it. Use this for the conversion goal (read from the site's primary CTAs: click-to-call, quote form, booking widget, cart), the margin ranking, and the service area.
- **When**: Phase 03, for each question where research produced a likely answer.
- **Example**:
```
    "The site leads with 'Call for a free estimate' in the header and on every service page, and the only form is a short contact form. I'd optimize for phone calls, with form leads as a secondary conversion. Does that match how this client gets business?"
    Options: Calls primary (Recommended) / Form leads primary / Online booking / Something else
```

---

- **Name**: Margin-First Budget Fit
- **Description**: Order the client's services by confirmed margin, highest first. Walk down the list and fund each service as its own ad group while the remaining budget still lets every funded ad group clear the click-volume floor. Stop at the first service that would push any funded ad group below the floor; list every service past that point in the brief as cut, with the reason and the extra budget it would need.
- **When**: Phase 04, every run.
- **Example**:
```
    Budget: $3,000/month = ~$98.68/day
    1. Repiping (margin high, est. CPC $12): floor 5 clicks/day = $60/day  -> funded $60
    2. Water heaters (margin high, est. CPC $9): floor = $45/day            -> remaining $38.68 < $45, stop
    Funded: Repiping at $98.68/day (~8 clicks/day)
    Cut: Water heaters (needs +$6.32/day for the floor; recommend ~$3,200/month to add it), drain cleaning, sewer line
```

---

- **Name**: Click-Volume Floor
- **Description**: Require each funded ad group's daily budget to buy at least 5 clicks per day at its estimated CPC (daily budget = monthly budget / 30.4). Let the user raise or lower the floor, and state the floor used in the brief. The floor keeps every ad group gathering enough data to learn from within weeks rather than months.
- **When**: Phase 04, inside the Margin-First Budget Fit.
- **Example**:
```
    Ad group: Water Heater Installation
    Estimated CPC: $9.00
    Floor: 5 clicks/day -> minimum $45.00/day
```

---

- **Name**: Budget Shortfall Verdict
- **Description**: When the full daily budget cannot buy the floor for the single highest-margin service, report the shortfall in plain numbers, recommend the minimum monthly budget that clears the floor for that service, and ask the user to choose between raising the budget and a narrow build flagged as below the floor.
- **When**: Phase 04, whenever the top-margin service fails the floor on the full budget.
- **Example**:
```
    "At $500/month (~$16/day) and an estimated $150 per click for car accident keywords locally, this budget buys about one click every nine days. The floor for one ad group is about $750/day (~$22,800/month). A practical minimum to test one practice area is ~$4,500/month at 1 click/day. Raise the budget, or build a single flagged ad group at $500?"
```

---

- **Name**: Single-Theme Ad Groups
- **Description**: Build one ad group per funded service, with keywords that all express that one service and intent, so the RSA headlines and the destination page match every keyword in the group. Use phrase and exact match for core terms, and add broad match only when the user confirms the account has conversion tracking and Smart Bidding.
- **When**: Phase 05, when structuring the campaign.
- **Example**:
```
    Ad group: Water Heater Installation
    Keywords: "water heater installation", [water heater replacement], "tankless water heater installer", "new water heater near me"
```

---

- **Name**: Negative Keyword Baseline
- **Description**: Add a campaign-level negative list covering job seekers, DIY and education, free or cheap seekers, and services the client does not offer, plus ad-group-level negatives that keep each service's searches in its own ad group.
- **When**: Phase 05, every build.
- **Example**:
```
    Campaign negatives: jobs, careers, salary, hiring, how to, diy, youtube, course, training, free, cheap, used, parts, wholesale
    Ad group negatives (Water Heater Installation): repair, leaking, pilot light
```

---

- **Name**: Responsive Search Ad Construction
- **Description**: Write one RSA per ad group with 10-15 headlines (max 30 characters each) and 4 descriptions (max 90 characters each), plus two display paths (max 15 characters each). Cover keyword match, differentiators from reviews, an offer or proof point, and a CTA matching the conversion goal. Include the location in at least two headlines when the client is local. Pin only when a legal or brand requirement demands it.
- **When**: Phase 05, for every funded ad group.
- **Example**:
```
    H1: Water Heater Installation (25)
    H2: Same-Day Service Available (26)
    H3: 4.8 Stars From 212 Reviews (26)
    H4: Serving Mesa & Gilbert (21)
    H5: Call for a Free Estimate (24)
    D1: Licensed plumbers install tank and tankless water heaters, often the same day. (79)
    Path: water-heaters / install
```

---

- **Name**: Assets From Research
- **Description**: Build sitelinks (text max 25 characters, descriptions max 35), callouts (max 25), structured snippets (Services header), and a call asset when calls are a conversion. Point each sitelink at a real page found during the research sweep.
- **When**: Phase 05, every build.
- **Example**:
```
    Callouts: Same-Day Service | Upfront Pricing | Licensed & Insured | 4.8-Star Rated
    Sitelink: Water Heaters -> clientsite.com/water-heaters ("Tank & tankless installs" / "Same-day appointments")
```

---

- **Name**: Destination Audit
- **Description**: For each funded ad group, score the best existing page on message match (does the page lead with that service?), mobile usability, load speed signals, conversion path clarity (CTA above the fold, short form, tap-to-call), and trust signals (reviews, licenses, guarantees). Recommend the existing page when it scores well on message match and conversion path; recommend a dedicated landing page otherwise, and state the expected benefit (higher conversion rate, better Quality Score and lower CPC from message match, cleaner tracking).
- **When**: Phase 02 for the audit, Phase 04 for the recommendation.
- **Example**:
```
    Ad group: Repiping
    Best existing page: homepage (no repiping page exists)
    Message match: poor (repiping is item 7 of 10 in a list)
    Conversion path: phone in header, form below the fold
    Recommendation: dedicated landing page - expect a higher conversion rate and better Quality Score from a page that leads with repiping and puts the call button first
```

---

- **Name**: Landing Page Spec
- **Description**: For each ad group routed to a landing page, write a spec with: the target keyword theme, headline and subhead echoing the ad, primary CTA matching the conversion goal (repeated top, middle, bottom), sections in order (hero, service detail, differentiators, review quotes, credentials, service area, FAQ, final CTA), proof points with their review sources, and a conversion tracking note.
- **When**: Phase 05, for each ad group whose destination is a landing page.
- **Example**:
```
    Landing page: Repiping
    Headline: Whole-Home Repiping in Mesa & Gilbert
    Subhead: Licensed plumbers, upfront pricing, most homes done in 1-2 days
    Primary CTA: Call (480) 555-0100 for a free repipe estimate
    Proof: "Repiped our 1970s house in two days, spotless cleanup" - Google review, Mar 2026
```

---

- **Name**: Strategy Brief Structure
- **Description**: Write the brief with these sections in order: Client Snapshot, Industry Notes, Differentiators (with sources), Conversion Goal, Margin Ranking (marked estimated or user-supplied), Budget Allocation (funded ad groups, daily budgets, estimated clicks, cut services and what it would take to add them), Destination Recommendations, Geo Targeting, Estimates To Verify, and Research Source Log.
- **When**: Phase 05, every run.
- **Example**:
```
    ## Budget Allocation
    | Ad group | Daily budget | Est. CPC | Est. clicks/day |
    | Repiping | $98.68 | $12.00 (estimate) | ~8 |
    Cut: Water heaters - needs ~$3,200/month total to fund at the 5-click floor.
```

---

- **Name**: Editor Import File Set
- **Description**: Write the build as CSV files that Google Ads Editor imports by header name: one file each for campaigns, ad groups, keywords (including negatives), responsive search ads, and assets. Use Editor's column headers (Campaign, Campaign Type, Budget, Bid Strategy Type, Networks, Location, Ad Group, Keyword, Criterion Type, Headline 1-15, Description 1-4, Path 1, Path 2, Final URL). Set networks to Google Search only, exclude Search Partners and Display, and set location targeting to Presence (people in or regularly in the area). Start new campaigns paused so the user posts them deliberately.
- **When**: Phase 05, every build.
- **Example**:
```
    campaigns.csv
    Campaign,Campaign Type,Budget,Bid Strategy Type,Networks,Campaign Status
    Acme Plumbing - Search - Repiping,Search,98.68,Maximize conversions,Google search,Paused
```

---

## Anti-Patterns

- **Name**: Spread-Thin Campaign
- **Description**: Funding an ad group for every service the client offers regardless of budget.
- **Why**: Each ad group gets a click or two a day, nothing reaches statistical signal, Smart Bidding cannot learn, and the client pays for a campaign that never improves.
- **Instead**: Apply Margin-First Budget Fit with the Click-Volume Floor and list the cut services with the budget each would need.

---

- **Name**: Unsourced Superlatives
- **Description**: Ad copy claiming "#1", "best", "top-rated", or specific numbers that no review, listing, or user statement supports.
- **Why**: Google Ads disapproves unsupported superlatives, and claims the client cannot back up erode trust and create legal exposure.
- **Instead**: Write claims from Review-Mined Differentiators and cited facts; use "Highly Rated" or a cited star count in place of "#1".

---

- **Name**: Generic Industry Copy
- **Description**: Ads that could run for any competitor ("Quality Service", "Call Today", "Experienced Team").
- **Why**: Generic copy wins no clicks against local competitors and wastes the research the skill performed.
- **Instead**: Lead with the client's specific differentiators, service area, and proof from reviews.

---

- **Name**: Estimates Presented as Data
- **Description**: Stating estimated CPCs, search volumes, or margins in the brief as though they were measured.
- **Why**: The user prices the campaign to the client on these numbers; an unlabeled estimate that proves wrong damages the user's credibility.
- **Instead**: Label every estimate as an estimate, list it under Estimates To Verify, and replace it when the user supplies real data.

---

- **Name**: Homepage by Default
- **Description**: Sending every ad group to the homepage without auditing message match.
- **Why**: A homepage listing ten services converts worse and earns a lower Quality Score than a page leading with the searched service.
- **Instead**: Run the Destination Audit per ad group and recommend a landing page where the existing page scores poorly.

---

- **Name**: Building Before Confirmation
- **Description**: Writing import files before the user has explicitly confirmed the strategy.
- **Why**: A wrong margin ranking or service area invalidates the whole build, and rework costs more than one confirmation turn.
- **Instead**: Run Phase 04 Strategy Confirmation and write build files only after an explicit yes.

---

- **Name**: Competitor Trademarks in Ad Text
- **Description**: Using a competitor's brand name in headlines or descriptions.
- **Why**: Trademark complaints get ads disapproved and can expose the client to legal claims.
- **Instead**: Use competitor research to sharpen positioning in the client's own words, and propose competitor-name keywords only as a separate, user-approved decision with the brand kept out of ad text.
