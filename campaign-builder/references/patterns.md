# Campaign Builder Patterns & Anti-Patterns

This document defines the patterns and anti-patterns used by campaign-builder.

## Patterns

- **Name**: Whole-Presence Research Sweep
- **Description**: Check every public source on the client in a fixed order and record the source of each fact: the client website, Google Business Profile, review platforms (Google, Yelp, Facebook, Angi, BBB, and industry-specific sites such as Avvo, Healthgrades, or Houzz), directory listings, social profiles, and press or local news mentions. From the website, capture the primary business category, core and secondary services, highest-intent and highest-value services, service area and locations, business hours, emergency availability, promotions, financing, guarantees, certifications, awards, years in business, trust signals, calls-to-action, phone, form, and booking strategy, and every service-specific page. Conclude with what the client actually wants to be contacted for, judged by which services the site leads with, links from navigation, and repeats in CTAs, rather than every service mentioned anywhere. Note any source that returned nothing so the brief shows what was checked.
- **When**: Phase 02, for every client, before the interview.
- **Example**:
```
    Source log
    - clientsite.com: leads with commercial lot plowing and salting; residential driveways mentioned once in the footer
    - Google Business Profile: 4.9 stars, 64 reviews, service area lists 6 cities, open 24 hours in season
    - Facebook: active; 11 reviews
    - BBB: not listed
    - Local news: none found
    Wants to be contacted for: commercial snow and ice contracts (lots, apartment complexes)
```

---

- **Name**: Review-Mined Differentiators
- **Description**: Read the client's reviews for themes that recur across several reviewers, weighting recent reviews over old ones. Record each theme with a count and two or three short quotes. Recurring specifics (same-day service, upfront pricing, a named technician, a specific service) are the differentiators; one-off praise and generic praise ("great job") are not.
- **When**: Phase 02, whenever the client has reviews, and again when writing ad copy and landing page proof points.
- **Example**:
```
    Differentiator: Lots cleared before opening
    Evidence: 14 of 64 Google reviews (9 in the last 12 months)
    Quotes: "lot was clear by 5 AM every storm", "never had to call them, they were already here"
    Usable in ads as: "Cleared Before You Open"
```

---

- **Name**: Industry Primer
- **Description**: Before choosing keywords, outline the industry's service categories, how buyers search (emergency versus planned, research-heavy versus impulse, consumer versus business buyer), seasonality, typical ticket sizes, typical margin ranges by service, typical lead and close rates, and typical local CPC ranges. Use this outline to estimate the margin ranking, CPCs, and conversion rates, and cite the benchmark sources.
- **When**: Phase 02, for every client, and in more depth when the industry is unfamiliar.
- **Example**:
```
    Snow and ice management
    - Buyers: commercial property managers (seasonal contracts, research-heavy) vs. homeowners (per-push or seasonal, urgent)
    - Seasonality: searches climb Oct-Nov for contracts, spike during storms Dec-Feb
    - Relative margin (estimate): commercial seasonal contracts > salting/de-icing add-ons > residential per-push
    - Local CPC (estimate): commercial $6-$10, residential $3-$5
```

---

- **Name**: Competitive Landscape Scan
- **Description**: For each candidate service and area, record who competes: advertisers seen on the search results page, map-pack and Local Services listings, and the strongest organic competitors, with their review counts and apparent positioning. Rate each service-area pair as light, moderate, or heavy competition, and use the rating to adjust CPC ranges, achievable impression share, and the client's positioning against named competitors.
- **When**: Phase 02, for every Tier 1 candidate service and every area in the suggested geography.
- **Example**:
```
    Commercial snow removal - Peoria
    - Ads seen: 2 advertisers (one national franchise, one local landscaper)
    - Map pack: 3 local firms, 20-140 reviews each
    - Rating: moderate -> CPC $7-$10, achievable impression share 40-60%
    - Positioning gap: no competitor ad mentions pre-opening clearing or 24/7 storm monitoring
```

---

- **Name**: Segment and Area Demand Map
- **Description**: Estimate monthly local search demand as a range for each candidate service, split by segment wherever segments differ in buyer or intent (commercial vs. residential, emergency vs. planned, repair vs. replacement) and by area within the service geography. Show seasonal peaks and troughs when the industry is seasonal. Give each range a confidence level (high with Keyword Planner or account data, medium with several converging signals, low with benchmarks alone).
- **When**: Phase 03, for every candidate service.
- **Example**:
```
    Service / segment        Area             Searches/mo (peak season)   Confidence
    Snow removal - commercial  Peoria metro    300-600                     medium
    Snow removal - residential Peoria metro    2,000-3,500                 medium
    Snow removal - commercial  Metamora        under 20                    low
    Signals: Keyword Planner not supplied; Google Trends regional interest, metro population 400k, ~1,900 commercial properties with parking lots, 4 apartment complexes over 100 units
```

---

- **Name**: Demand Signal Ladder
- **Description**: Build demand estimates from the strongest available signal and cite the signals used for each estimate. In order of strength: user-supplied Keyword Planner or account search-term data; Google Trends relative interest and seasonality by region; the size of the buying base per area (population and households for consumer services, counts of businesses, commercial properties, or apartment complexes for commercial services); competitor density on Maps and Local Services and ad density on the search results page; industry benchmarks. When signals disagree, give the wider range and lower the confidence level.
- **When**: Phase 03, whenever a demand estimate is produced or revised.
- **Example**:
```
    Commercial snow removal, Peoria metro: 300-600/mo (medium)
    - Buying base: ~1,900 commercial lots + 4 large apartment complexes (county parcel and business data)
    - Trends: "commercial snow removal" regional interest 3x higher Nov-Jan than Oct
    - Ad density: 2 advertisers on core terms -> demand exists but is not heavily contested
```

---

- **Name**: Demand Ceiling
- **Description**: Estimate the most clicks each service can produce per month regardless of budget: monthly searches multiplied by achievable impression share (40-60% for a new account, lower under heavy competition) multiplied by expected CTR (4-8% for local service search ads). Multiply by the CPC midpoint to get the most budget the service can usefully spend. Budget allocated above a service's ceiling goes unspent or buys low-quality clicks, so reallocate it.
- **When**: Phase 03 for the estimate; Phase 05 when allocating budget.
- **Example**:
```
    Commercial snow removal: 450 searches x 50% IS x 7% CTR = ~16 clicks/mo -> ~$126/mo at $8 CPC
    Residential snow removal: 2,750 searches x 50% IS x 7% CTR = ~96 clicks/mo -> ~$384/mo at $4 CPC
    Combined usable spend in peak season: ~$510/mo of a $1,153/mo budget
```

---

- **Name**: Profit-Potential Ranking
- **Description**: Rank services by expected profit per ad dollar, then cap each service by its demand ceiling. Profit per click = lead rate x close rate x average ticket x margin %. Profit per dollar = profit per click / CPC midpoint. Monthly profit potential = profit per click x clicks the service can capture (the lower of budget-bought clicks and its demand ceiling). Adjust for competition through the CPC and impression share inputs. Label every input as estimated, user-confirmed, or user-supplied, and re-run the ranking whenever an input changes.
- **When**: Phase 03 for the draft; Phase 04 and Phase 05 whenever inputs change.
- **Example**:
```
    Commercial contracts: .08 lead x .20 close x $6,000 x 35% = $33.60/click -> $4.20 per $1 -> ~16 clicks/mo -> ~$538/mo potential
    Residential seasonal: .12 lead x .30 close x $450 x 40% = $6.48/click -> $1.62 per $1 -> ~96 clicks/mo -> ~$622/mo potential
    Specialty roof snow removal: $60/click but 10-30 searches/mo -> ~1 click/mo -> ~$60/mo potential (Tier 3: insufficient demand)
```

---

- **Name**: Service Tiering
- **Description**: Classify every candidate service as Tier 1 (launch now), Tier 2 (add after initial data or more budget), or Tier 3 (do not prioritize), each with a one-line reason. Place services by profit potential first, then weigh search intent, demand, commercial value, competition, CPC, lead likelihood, landing page quality, client priority, geographic demand, and budget. Tier 1 services feed the build; Tier 2 feeds the Phase 2 list; Tier 3 feeds the Do Not Build Yet list.
- **When**: Phase 03 for the draft tiers; Phase 05 for the confirmed tiers.
- **Example**:
```
    Tier 1 - Commercial snow and ice contracts: highest profit per dollar, client's stated focus, strong landing page
    Tier 1 - Residential seasonal plowing: most demand in the metro; fills budget the commercial ceiling leaves unspent
    Tier 2 - Salting/de-icing as a standalone service: good margin, but searches mostly bundle it with plowing
    Tier 3 - Roof snow removal: 10-30 searches/mo, no service page
```

---

- **Name**: Profit-First Budget Fit
- **Description**: Walk the Tier 1 services in order of profit per dollar. Allocate each the lower of its demand-ceiling spend and the remaining budget, checking the Click-Volume Floor as you go. Stop and cut at the first service that would push any funded ad group below the floor. When every Tier 1 service reaches its ceiling with budget left over, report the unspendable amount and recommend how to use it: promote a Tier 2 service, widen the geography, add a segment, or hold the budget for peak season. List cut services in the brief with the budget each would need.
- **When**: Phase 05, every run.
- **Example**:
```
    Budget: $1,153/mo = ~$37.93/day
    1. Commercial contracts: ceiling $126/mo -> allocate $126 (16 clicks/mo; demand-limited, clears floor)
    2. Residential seasonal: ceiling $384/mo -> allocate $384 (96 clicks/mo)
    Unspendable at current scope: ~$643/mo
    Recommendation: widen commercial targeting to Bloomington-Normal (+250-450 searches/mo) and promote salting to Tier 1, or run at ~$510/mo and bank the rest for storm weeks
```

---

- **Name**: Click-Volume Floor
- **Description**: Require each funded ad group's budget to buy at least the smaller of 5 clicks per day or its demand ceiling, at its estimated CPC (daily budget = monthly budget / 30.4). An ad group limited by demand rather than budget clears the floor, because it is already buying every click available. Let the user raise or lower the floor, and state the floor used in the brief.
- **When**: Phase 05, inside the Profit-First Budget Fit.
- **Example**:
```
    Ad group: Residential Driveway Plowing
    Estimated CPC: $4.00, demand ceiling ~3.2 clicks/day
    Floor: min(5, 3.2) = 3.2 clicks/day -> minimum $12.80/day
```

---

- **Name**: Budget Feasibility Ranges
- **Description**: Report what the budget can realistically buy as ranges: daily budget, CPC range, clicks per month, lead range, and a starting CPL expectation, per campaign and in total. State plainly whether the budget can support all Tier 1 services at the floor, and what is prioritized if it cannot.
- **When**: Phase 05, every run, and again in the brief.
- **Example**:
```
    Total: $510-$1,153/mo usable | CPC $3-$10 | 90-140 clicks/mo | 8-16 leads/mo | starting CPL $45-$95
    Supports all Tier 1 services: yes, with budget left over at the current geography
```

---

- **Name**: Budget Shortfall Verdict
- **Description**: When the full daily budget cannot buy the floor for the single highest-ranked Tier 1 service, report the shortfall in plain numbers, recommend the minimum monthly budget that clears the floor for that service, and ask the user to choose between raising the budget and a narrow build flagged as below the floor.
- **When**: Phase 05, whenever the top Tier 1 service fails the floor on the full budget.
- **Example**:
```
    "At $500/month (~$16/day) and an estimated $150 per click for car accident keywords locally, this budget buys about one click every nine days. Clearing the 5-click floor for one ad group takes about $750/day (~$22,800/month); a 1-click/day test needs ~$4,560/month. Raise the budget, or build a single flagged ad group at $500?"
```

---

- **Name**: Infer-Then-Confirm
- **Description**: Bring a proposed answer from research to every confirmable question and ask the user to confirm or correct it. Use this for the conversion goal (read from the site's primary CTAs: click-to-call, quote form, booking widget, cart), the margin ranking, the demand estimates, and the service area.
- **When**: Phase 04, for each question where research produced a likely answer.
- **Example**:
```
    "The site leads with 'Request a Snow Contract Quote' and a four-field form, with the phone in the header. I'd make quote requests the primary conversion and calls over 60 seconds a second primary. Does that match how this client gets business?"
    Options: Quote forms + calls (Recommended) / Calls only / Forms only / Skip - assume for me
```

---

- **Name**: Assume and Label
- **Description**: When the user skips a question or information is unavailable, choose the assumption the research best supports, write it down with the reasoning and the evidence behind it, mark it "Assumption" in the brief, and continue. Gather every assumption into one list shown at strategy confirmation, so the user can correct any of them at once.
- **When**: Phase 04 on every skipped question; any phase where a needed fact is missing.
- **Example**:
```
    Assumption: Call-answering hours are 6 AM-8 PM daily in season.
    Reasoning: GBP lists 24-hour storm service but the site's contact page lists office hours of 8-5; a 6-8 window covers both storm calls and contract inquiries.
```

---

- **Name**: Campaign Split Test
- **Description**: Start from one non-brand campaign and add another only when a split serves one of these: budget control (a service needs a guaranteed share), geography (areas with materially different demand, CPC, or service terms), bidding (different conversion values or bid strategies), service priority, profitability, or search intent (different buyers, such as commercial vs. residential). Record the reason for each split. Name campaigns `Search | Service or Segment | Non-Brand | Geo`, with `Brand` or `Competitor` in the third position for those campaigns.
- **When**: Phase 05, when designing the architecture.
- **Example**:
```
    Search | Commercial Snow & Ice | Non-Brand | Peoria Metro   (split reason: different buyer and contract value; budget control)
    Search | Residential Snow | Non-Brand | Peoria Metro       (split reason: different intent and CPC; keeps residential from draining commercial)
```

---

- **Name**: Bid Strategy Ladder
- **Description**: Start each campaign on a bid strategy its data supports and state the trigger for moving up: Maximize Clicks with a CPC cap or Manual CPC for a new account without conversion history, Maximize Conversions once tracking is verified and the campaign records roughly 15-30 conversions in 30 days, and Target CPA once results are stable at that volume. Name the campaign's current rung and the next rung's trigger in both the brief and the build sheet.
- **When**: Phase 05 and Phase 06, for every campaign.
- **Example**:
```
    Search | Commercial Snow & Ice: Maximize Clicks, max CPC $12 -> Maximize Conversions after tracking is verified and 15+ conversions in 30 days -> Target CPA at the observed CPL after 30+ conversions in 30 days
```

---

- **Name**: Intent-Grouped Ad Groups
- **Description**: Group keywords into ad groups by closely related search intent, so the RSA headlines and the destination page match every keyword in the group, while keeping enough keywords per group to accumulate data. Use exact and phrase match for core terms. Add broad match only with a stated reason (tracking verified, Smart Bidding active, and demand too thin for exact and phrase to spend the budget), or list it as a Phase 2 test. Favor high-commercial-intent modifiers: service, repair, installation, replacement, company, contractor, near me, local, emergency, and pricing or cost terms where they fit. Keep keyword lists tight rather than padded with near-duplicates.
- **When**: Phase 06, when structuring each campaign.
- **Example**:
```
    Ad group: Parking Lot Snow Removal
    Exact: [parking lot snow removal], [commercial snow plowing], [snow removal company]
    Phrase: "parking lot snow plowing", "commercial snow removal near me", "snow plowing contractor"
    Broad: none at launch - Phase 2 test once 30+ conversions are recorded
```

---

- **Name**: Negative Keyword Layers
- **Description**: Build two layers. An account-level list covering jobs, careers, salary, training, certification, DIY, how-to, courses, school, free, used equipment, parts, manuals, PDFs, wholesale, definitions, and research intent, plus services the client does not offer. Campaign-level cross-negatives that keep campaigns from competing for each other's searches. Evaluate price-related terms (cheap, cost, price, affordable) for intent and keep them eligible unless the client's positioning or lead quality data says otherwise.
- **When**: Phase 06, every build.
- **Example**:
```
    Account: jobs, careers, hiring, salary, how to, diy, youtube, course, training, free, used, parts, manual, pdf, wholesale, definition
    Search | Residential Snow: commercial, parking lot, business, property management, hoa
    Search | Commercial Snow & Ice: driveway, residential, home, house
    Price terms: "snow removal cost" kept eligible - buyers comparing quotes convert well for contracts
```

---

- **Name**: Responsive Search Ad Construction
- **Description**: Write at least one RSA per ad group with 10-15 headlines (max 30 characters each), 4 descriptions (max 90 characters each), and two display paths (max 15 characters each). Mix headline types deliberately: primary keyword, service, location, benefit, trust, differentiator, CTA, offer, urgency only when legitimate, and brand, with each headline saying something the others do not. Descriptions combine service, differentiators, trust, benefits, and a CTA matching the conversion goal. Pin only when a legal or brand requirement demands it.
- **When**: Phase 06, for every funded ad group.
- **Example**:
```
    H1: Commercial Snow Removal (23)       [keyword]
    H2: Lots Cleared Before You Open (28)  [differentiator]
    H3: 4.9 Stars From 64 Reviews (25)     [trust]
    H4: Serving Peoria & East Peoria (28)  [location]
    H5: Get a Seasonal Contract Quote (29) [CTA]
    D1: 24/7 storm monitoring and lots cleared before opening. Request a seasonal quote. (83)
    Path: commercial / snow-contracts
```

---

- **Name**: Assets From Research
- **Description**: Build sitelinks from real pages found in the research sweep (text max 25 characters, two description lines max 35 each), 8-12 callouts (max 25 each) supported by the site or user statements, structured snippets with appropriate headers and values, and a recommendation on each of call, location, lead form, promotion, and image assets with the reason and, for call assets, when they should run.
- **When**: Phase 06, every build.
- **Example**:
```
    Callouts: 24/7 Storm Monitoring | Cleared Before Opening | Seasonal Contracts | Salting & De-Icing | Fully Insured | Locally Owned | Free Site Assessment | Apartment Complexes
    Structured snippet - Services: Lot Plowing, Salting, Sidewalk Clearing, Snow Hauling
    Call asset: yes, during call-answering hours | Lead form asset: no - contract buyers want a site assessment, not an instant form
```

---

- **Name**: Geo Targeting From Demand
- **Description**: Test the user's suggested geography against the Segment and Area Demand Map and recommend the targeting to use: cities, ZIP codes, counties, radius, multiple radiuses, DMA, or a combination, plus any areas to exclude. Set the location option to Presence (people in or regularly in the targeted locations) unless there is a stated reason otherwise. Recommend whether areas with materially different demand are combined, split into campaigns, observed first, or adjusted later.
- **When**: Phase 05, every run.
- **Example**:
```
    Suggested: Peoria, East Peoria, Morton, Washington, Germantown Hills, Metamora
    Recommended: 15-mile radius around Peoria plus Morton and Washington as named cities; Metamora and Germantown Hills observed inside the radius rather than targeted separately (under 20 commercial searches/mo each)
    Location option: Presence
```

---

- **Name**: Ad Schedule Table
- **Description**: Recommend the initial ad schedule as a day / start / end table, reasoning from business hours, call-answering hours, form handling, emergency service, after-hours lead handling, lead response time, and how the industry searches. Keep ads running outside office hours whenever form leads can still be captured and answered promptly; run call assets only during call-answering hours. Explain any 24/7 recommendation.
- **When**: Phase 06, every build.
- **Example**:
```
    Day        Start     End
    Mon-Fri    12:00 AM  11:59 PM   (forms answered by 8 AM; storm searches peak overnight)
    Sat-Sun    12:00 AM  11:59 PM
    Call asset: 6:00 AM-8:00 PM daily
```

---

- **Name**: Observation Audiences
- **Description**: Add relevant audiences in Observation mode only, such as in-market segments, business decision makers, homeowners, remarketing lists, and Customer Match, so the data informs later bid adjustments without narrowing high-intent search reach.
- **When**: Phase 06, every build.
- **Example**:
```
    Search | Commercial Snow & Ice: Observation - In-market: Business Services; Affinity: Business Professionals; Remarketing: site visitors 90 days
```

---

- **Name**: Brand, Competitor, and Performance Max Decisions
- **Description**: Record a decision for each of three campaign types every run, choosing among Build Now, Phase 2, and Do Not Build Yet, with the reason. Brand Search: build when brand searches are meaningful or competitors bid on the brand; hold back when volume is negligible and budget is tight. Competitor Search: weigh budget, volume, CPC, trademark limits, intent, and opportunity cost against core services; when worth testing, list it as Phase 2 rather than taking budget from Tier 1. Performance Max: assess conversion data, creative, tracking, first-party data, and budget, and place it in Phase 2 or Do Not Build Yet, keeping the build files Search-only.
- **When**: Phase 05 for the decisions; Phase 06 for any brand or competitor campaign built.
- **Example**:
```
    Brand Search: Do Not Build Yet - under 10 brand searches/mo; organic listing ranks first
    Competitor Search: Phase 2 - test after Tier 1 reaches stable CPL; keep competitor names out of ad text
    Performance Max: Do Not Build Yet - no conversion history, no image or video library, budget below $1,500/mo
```

---

- **Name**: Destination Audit
- **Description**: For each funded ad group, evaluate the best existing page on headline relevance, service relevance, geographic relevance, CTA and phone visibility, form length, trust signals, reviews, offers, page speed, mobile usability, and service-area messaging. Classify each issue as Must Fix Before Launch, Highly Recommended, or Optimization Opportunity. Recommend the existing page when nothing is Must Fix and message match is strong, and say so plainly when a page is good enough to launch despite imperfections. Recommend a dedicated landing page otherwise, with the expected benefit (higher conversion rate, better Quality Score and lower CPC from message match, cleaner tracking).
- **When**: Phase 02 for the audit, Phase 05 for the recommendation.
- **Example**:
```
    Ad group: Parking Lot Snow Removal -> clientsite.com/commercial
    Must Fix Before Launch: quote form has no conversion tracking
    Highly Recommended: add review quotes above the fold
    Optimization Opportunity: compress hero image (3.1 MB)
    Verdict: launch on this page once tracking is fixed
```

---

- **Name**: Landing Page Spec
- **Description**: For each ad group routed to a landing page, write a spec with: the target keyword theme, headline and subhead echoing the ad, primary CTA matching the conversion goal (repeated top, middle, bottom), sections in order (hero, service detail, differentiators, review quotes, credentials, service area, FAQ, final CTA), proof points with their review sources, and a conversion tracking note.
- **When**: Phase 06, for each ad group whose destination is a landing page.
- **Example**:
```
    Landing page: Residential Driveway Plowing
    Headline: Driveway Snow Plowing in Peoria - Seasonal Plans
    Primary CTA: Get your seasonal plowing quote (3-field form) + tap-to-call
    Proof: "plowed before I left for work every single storm" - Google review, Jan 2026
```

---

- **Name**: Conversion Hierarchy
- **Description**: Separate primary conversions (qualified calls with a duration threshold, form submissions, quote requests, appointment bookings, purchases, chat leads) from secondary or observation conversions, and optimize bidding only toward primary ones. Keep page views, button clicks, form starts, scrolls, and directions clicks as observation-only unless a stated reason ties one to revenue. Recommend the tracking setup: Google Ads conversion tracking, GA4, Google Tag Manager, enhanced conversions, call tracking, and offline conversion imports or CRM integration when the client can close the loop.
- **When**: Phase 05 for the decision; Phase 06 for the brief and build sheet.
- **Example**:
```
    Primary: Quote form submit; Calls from ads 60s+; Website calls 60s+
    Secondary (observation): Contract page views, Click-to-email
    Setup: Google Ads tag via GTM, enhanced conversions for leads, call tracking number on site; offline import once the CRM records signed contracts
```

---

- **Name**: Search-Term Management Plan
- **Description**: Write a concise review plan for days 7, 14, 30, and 60-90, naming what triggers each action: adding negatives, adding keywords, changing match types, creating ad groups, shifting budget, pausing keywords, and changing geography.
- **When**: Phase 06, every build.
- **Example**:
```
    Day 7: add negatives for irrelevant terms with 3+ clicks; confirm conversions are firing
    Day 14: pause keywords with 20+ clicks and no leads; add converting search terms as exact
    Day 30: shift budget toward the campaign with the lower CPL; review area performance
    Day 60-90: test broad match or a new ad group where exact/phrase hit the demand ceiling
```

---

- **Name**: Strategy Brief Structure
- **Description**: Write the brief as `<client>-strategy-brief.md` with these sections in order: Client Snapshot, Industry Notes, Competitive Landscape, Demand Analysis, Differentiators (with sources), Service Tiers, Profit-Potential Ranking, Budget Feasibility, Campaign Architecture (with split reasons and bid strategy ladder), Geo Targeting, Ad Schedule, Audiences, Conversion Tracking, Destination Recommendations, Brand / Competitor / Performance Max Decisions, Search-Term Management Plan, Assumptions, Estimates To Verify, Self-Check Revisions, and Research Source Log.
- **When**: Phase 06, every run.
- **Example**:
```
    ## Demand Analysis
    | Service / segment | Area | Searches/mo | Ceiling clicks/mo | Confidence |
    | Commercial snow | Peoria metro | 300-600 | 10-25 | medium |
```

---

- **Name**: Build Sheet
- **Description**: Write `<client>-build-sheet.md` as the final structure with no explanations: Account, then each campaign (name, objective, monthly and daily budget, bid strategy, geography, location option, schedule, landing page), each ad group (exact and phrase keywords, RSA headlines and descriptions), account negatives, campaign negatives, sitelinks, callouts, structured snippets, conversion actions, a Launch Budget Allocation table (campaign, monthly budget, daily budget, percent of budget, totaling 100%), and the launch priorities Build Now, Phase 2, and Do Not Build Yet.
- **When**: Phase 06, every run.
- **Example**:
```
    LAUNCH BUDGET ALLOCATION
    | Campaign                                                       | Monthly | Daily  | %      |
    | Search | Commercial Snow & Ice | Non-Brand | Peoria & Bloomington | $769    | $25.30 | 66.7%  |
    | Search | Residential Snow | Non-Brand | Peoria Metro              | $384    | $12.63 | 33.3%  |
    | Total                                                          | $1,153  | $37.93 | 100%   |
```

---

- **Name**: Editor Import File Set
- **Description**: Write the build as CSV files that Google Ads Editor imports by header name: one file each for campaigns, ad groups, keywords (including negatives), responsive search ads, and assets. Use Editor's column headers (Campaign, Campaign Type, Budget, Bid Strategy Type, Networks, Location, Ad Schedule, Ad Group, Keyword, Criterion Type, Headline 1-15, Description 1-4, Path 1, Path 2, Final URL). Set networks to Google Search only with Search Partners and Display expansion off, and set location targeting to Presence. Include only Search campaigns marked Build Now. Start new campaigns paused so the user posts them deliberately.
- **When**: Phase 06, every build.
- **Example**:
```
    campaigns.csv
    Campaign,Campaign Type,Budget,Bid Strategy Type,Networks,Campaign Status
    Search | Commercial Snow & Ice | Non-Brand | Peoria & Bloomington,Search,25.30,Maximize clicks,Google search,Paused
```

---

- **Name**: Owner's-Money Self-Check
- **Description**: Before handoff, answer in the brief: "If this were my money and I had to generate qualified leads for this business with this monthly budget, is this the exact structure I would launch?" Test the answer against the over-fragmentation, demand ceiling, conversion hierarchy, and claim sourcing rules. When the answer is no, revise and record each revision with its reason; repeat until the answer is yes.
- **When**: Phase 07, every run.
- **Example**:
```
    Self-check 1: No - the residential campaign's daily budget exceeds its demand ceiling in December.
    Revision: cap residential at $384/mo and move the difference to commercial salting (promoted from Tier 2).
    Self-check 2: Yes.
```

---

## Anti-Patterns

- **Name**: Spread-Thin Campaign
- **Description**: Funding an ad group or campaign for every service the client offers regardless of budget.
- **Why**: Each ad group gets a click or two a day, nothing reaches statistical signal, Smart Bidding cannot learn, and the client pays for a campaign that never improves.
- **Instead**: Apply Profit-First Budget Fit with the Click-Volume Floor, and list the cut services with the budget each would need.

---

- **Name**: Margin Without Demand
- **Description**: Funding a service because its margin is highest without checking how many people search for it locally.
- **Why**: A high-margin service with almost no local demand cannot spend its budget, so the money buys low-quality clicks or sits idle while better-demand services go underfunded.
- **Instead**: Rank by Profit-Potential Ranking, which multiplies margin by captured demand, and cap allocations at the Demand Ceiling.

---

- **Name**: Over-Fragmented Structure
- **Description**: Splitting campaigns because services differ slightly, or building single-keyword ad groups.
- **Why**: Fragmentation divides already-limited data and budget, slows learning, and adds management cost without improving relevance.
- **Instead**: Apply the Campaign Split Test and Intent-Grouped Ad Groups, recording a reason for every split.

---

- **Name**: Reflexive Price Negatives
- **Description**: Adding cheap, cost, price, or affordable as blanket negative keywords.
- **Why**: Many buyers who search for cost are ready to buy and comparing quotes; excluding them cuts qualified demand.
- **Instead**: Evaluate price terms for intent per the Negative Keyword Layers pattern and exclude them only with a stated reason.

---

- **Name**: Default Automation
- **Description**: Adding broad match, Performance Max, automated bidding, or Google's automated recommendations because they are available.
- **Why**: Automation needs conversion data, tracking, and budget to work; without them it spends on loosely related traffic and hides what is working.
- **Instead**: Adopt each with a stated reason tied to this account, or list it in Phase 2 with the trigger that would justify it.

---

- **Name**: Low-Intent Conversion Optimization
- **Description**: Counting page views, button clicks, form starts, scrolls, or directions clicks as primary conversions.
- **Why**: Smart Bidding then optimizes toward cheap actions that do not produce leads, inflating conversion counts while lead quality falls.
- **Instead**: Follow the Conversion Hierarchy and keep low-intent actions as observation-only.

---

- **Name**: Unexamined Inputs
- **Description**: Accepting the user's suggested geography, service priorities, or structure without testing them against research.
- **Why**: A suggestion made before the demand analysis can point budget at areas or services with little demand.
- **Instead**: Test each suggestion against the demand map and competition scan, and recommend a change with the numbers when the evidence disagrees.

---

- **Name**: Stalling on Missing Information
- **Description**: Halting the run until every interview topic has an answer.
- **Why**: Users often lack margins, competitor lists, or Keyword Planner access, and a stalled run delivers nothing.
- **Instead**: Apply Assume and Label, continue the run, and surface every assumption at strategy confirmation.

---

- **Name**: Unsourced Superlatives
- **Description**: Ad copy claiming "#1", "best", "top-rated", or specific numbers that no review, listing, or user statement supports.
- **Why**: Google Ads disapproves unsupported superlatives, and claims the client cannot back up erode trust and create legal exposure.
- **Instead**: Write claims from Review-Mined Differentiators and cited facts; use a cited star count in place of "#1".

---

- **Name**: Generic Industry Copy
- **Description**: Ads that could run for any competitor ("Quality Service", "Call Today", "Experienced Team").
- **Why**: Generic copy wins no clicks against local competitors and wastes the research the skill performed.
- **Instead**: Lead with the client's specific differentiators, service area, and proof from reviews, and use the Competitive Landscape Scan to find positioning gaps.

---

- **Name**: Estimates Presented as Data
- **Description**: Stating estimated search volumes, CPCs, lead rates, or margins as though they were measured.
- **Why**: The user prices the campaign to the client on these numbers; an unlabeled estimate that proves wrong damages the user's credibility.
- **Instead**: Give estimates as ranges with a confidence level, label each as estimated, list it under Estimates To Verify, and replace it when the user supplies real data.

---

- **Name**: Homepage by Default
- **Description**: Sending every ad group to the homepage without auditing message match.
- **Why**: A homepage listing ten services converts worse and earns a lower Quality Score than a page leading with the searched service.
- **Instead**: Run the Destination Audit per ad group and recommend a landing page where the existing page scores poorly.

---

- **Name**: Building Before Confirmation
- **Description**: Writing the build sheet or import files before the user has explicitly confirmed the strategy.
- **Why**: A wrong margin, demand estimate, or service area invalidates the whole build, and rework costs more than one confirmation turn.
- **Instead**: Run Phase 05 Strategy Confirmation and write build files only after an explicit yes.

---

- **Name**: Competitor Trademarks in Ad Text
- **Description**: Using a competitor's brand name in headlines or descriptions.
- **Why**: Trademark complaints get ads disapproved and can expose the client to legal claims.
- **Instead**: Use the Competitive Landscape Scan to sharpen positioning in the client's own words; when a Competitor campaign is built, target competitor names as keywords only and keep them out of ad text.
