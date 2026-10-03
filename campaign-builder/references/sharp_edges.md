# Sharp Edges

This document defines the sharp edges used by campaign-builder.

---

## Wrong Business Researched

- **Id**: wrong-business-researched
- **Summary**: Research attaches reviews or listings from a different business with a similar name to the client.
- **Severity**: critical
- **Situation**: The client has a common name ("Premier Plumbing"), shares a name with a business in another city, or has rebranded or changed owners.
- **Why**: Name searches return the most prominent match, not necessarily the client, and review platforms list many same-named businesses.
- **Solution**:
    - Match every listing to the client's website URL, phone number, or street address before using it.
    - Confirm the exact business with the user at intake when the name is common or no URL is given.
- **Symptoms**:
    - Listings show an address, phone number, or service area that differs from the client site.
    - Reviews mention services the client does not offer.
- **Detection Pattern**: A listing or review source whose address, phone number, or website differs from the client's confirmed details, or reviews describing services absent from the client's site.

---

## Margin Without Demand

- **Id**: margin-without-demand
- **Summary**: A high-margin service is funded even though local search demand cannot absorb its budget.
- **Severity**: critical
- **Situation**: The client or the margin estimate favors a specialty or premium service that few people in the target area search for.
- **Why**: Budget allocated above a service's demand ceiling either goes unspent or buys loosely related clicks, while services with real demand go underfunded.
- **Solution**:
    - Rank services with the Profit-Potential Ranking, which multiplies margin by captured demand.
    - Cap each allocation at the service's Demand Ceiling and reallocate the excess.
    - Place services with too little demand in Tier 2 or Tier 3 with "insufficient local demand" as the reason.
- **Symptoms**:
    - A funded service with an estimated demand range under a few dozen searches per month.
    - Allocated budget for a service exceeds its demand-ceiling spend.
- **Detection Pattern**: A funded service whose allocated monthly budget is larger than its estimated monthly searches multiplied by achievable impression share, CTR, and CPC midpoint.

---

## Demand Estimate Overconfidence

- **Id**: demand-estimate-overconfidence
- **Summary**: Demand estimates built from weak signals are presented with more precision than they deserve, and the ranking rests on them.
- **Severity**: high
- **Situation**: No Keyword Planner or account data is available, the area is small, or the service is niche, so estimates come from benchmarks and proxies.
- **Why**: Proxy signals (population, business counts, Trends interest) indicate relative demand well but absolute volume poorly; small-area volumes are especially noisy.
- **Solution**:
    - Give every estimate as a range with a confidence level and the signals used, per the Demand Signal Ladder.
    - Ask for Keyword Planner data in the interview and explain that it replaces the estimates driving the ranking.
    - When two services rank within each other's ranges, say the order is uncertain and let client priority break the tie.
- **Symptoms**:
    - Single-number search volumes with no range or source.
    - Ranking changes sharply once real data arrives.
- **Detection Pattern**: A demand figure in the brief given as a single number, or lacking a confidence level or cited signals.

---

## Blended Segments

- **Id**: blended-segments
- **Summary**: Segments with different buyers or intent (commercial vs. residential, emergency vs. planned) share one campaign or ad group, and the higher-volume segment absorbs the budget.
- **Severity**: high
- **Situation**: Keywords such as "snow removal" or "plumber" serve both segments, and the client cares more about the lower-volume, higher-value one.
- **Why**: Shared budgets flow to whichever segment produces the most cheap clicks, which is often the less valuable one, and shared ad copy speaks to neither buyer well.
- **Solution**:
    - Map demand per segment in the Segment and Area Demand Map.
    - Split segments into separate campaigns when the Campaign Split Test supports it, with cross-negatives between them.
    - Write segment-specific RSAs and destinations.
- **Symptoms**:
    - One ad group mixes "commercial" and "driveway" style keywords.
    - Search terms are mostly from the segment the client deprioritized.
- **Detection Pattern**: An ad group or campaign containing keywords from two segments the demand map lists separately, or campaigns for different segments without cross-negatives.

---

## Seasonal Demand Mistiming

- **Id**: seasonal-demand-mistiming
- **Summary**: The budget plan assumes flat monthly demand for a seasonal service.
- **Severity**: medium
- **Situation**: Snow removal, HVAC, landscaping, pools, tax services, and similar industries where searches swing several-fold across the year.
- **Why**: A flat daily budget overspends against thin off-season demand and caps out during peaks when the best leads are available.
- **Solution**:
    - Show peak and off-peak demand ranges in the demand map.
    - Recommend when to launch, scale up, and scale down, and where peak budget should come from.
- **Symptoms**:
    - Demand map shows one number per service with no seasonal note for a seasonal industry.
    - Campaigns limited by budget during storm or heat weeks.
- **Detection Pattern**: A seasonal industry identified in the Industry Primer with no peak or off-peak demand ranges and no seasonal budget recommendation in the brief.

---

## Thin Online Presence

- **Id**: thin-online-presence
- **Summary**: The client has few or no reviews and a minimal website, leaving little to build differentiators from.
- **Severity**: high
- **Situation**: A new business, a business that relies on referrals, or one whose listings were never claimed.
- **Why**: Review-mined differentiators need several reviewers saying the same thing; with five reviews there is no pattern to find.
- **Solution**:
    - Say plainly in the brief which sources were thin or empty.
    - Shift the interview toward differentiators: ask what the client does that competitors do not, and mark those claims as user-stated.
    - Recommend the client collect reviews as a near-term action in the brief.
- **Symptoms**:
    - Fewer than 10 reviews across all platforms.
    - Differentiator list is empty or holds only generic praise.
- **Detection Pattern**: A research source log with fewer than ten total reviews or a differentiator list containing no theme mentioned by three or more reviewers.

---

## Underfunded Ad Groups

- **Id**: underfunded-ad-groups
- **Summary**: Funded ad groups receive daily budgets below the click-volume floor at their estimated CPCs.
- **Severity**: critical
- **Situation**: The budget is small relative to local CPCs, or the user asks to include every service.
- **Why**: An ad group buying one or two clicks a day takes months to show which keywords and ads convert, and Smart Bidding never leaves its learning period.
- **Solution**:
    - Apply Profit-First Budget Fit and cut from the bottom of the ranking.
    - When the user insists on including a service below the floor, flag it in the brief as below the floor with the budget it needs.
    - Run the Budget Shortfall Verdict when even the top Tier 1 service fails the floor.
- **Symptoms**:
    - Estimated clicks per day per ad group below the floor while demand would support more.
    - Budget divided evenly across many ad groups.
- **Detection Pattern**: Any funded ad group whose daily budget divided by its estimated CPC is below the smaller of the stated floor and its demand ceiling, without a below-floor flag.

---

## Over-Fragmented Account

- **Id**: over-fragmented-account
- **Summary**: The account splits into more campaigns or ad groups than the budget and demand can feed.
- **Severity**: high
- **Situation**: Each service, city, or keyword variant gets its own campaign or ad group.
- **Why**: Every split divides budget and conversion data, slowing learning and starving each piece.
- **Solution**:
    - Apply the Campaign Split Test and record a reason for every split.
    - Group keywords by closely related intent rather than one keyword per ad group.
- **Symptoms**:
    - More campaigns than Tier 1 services.
    - Ad groups with one or two keywords each.
- **Detection Pattern**: A campaign without a recorded split reason, campaigns differing only by city without a demand or CPC difference, or ad groups holding a single keyword.

---

## Margin Estimate Treated as Fact

- **Id**: margin-estimate-treated-as-fact
- **Summary**: The industry-benchmark margin, ticket, or lead-rate inputs drive the ranking without the user confirming them.
- **Severity**: high
- **Situation**: The user skips margin confirmation, or the estimate stands without a label.
- **Why**: Margins vary sharply by client (equipment deals, labor costs, specialties), and the ranking decides which services get any budget.
- **Solution**:
    - Present the estimated inputs in the interview and invite actual figures.
    - Label each ranking input as estimated, user-confirmed, or user-supplied, and list skipped confirmations as assumptions.
- **Symptoms**:
    - Ranking inputs carry no source label.
    - The user is surprised by which services were cut.
- **Detection Pattern**: A profit-potential ranking in the brief whose margin, ticket, lead-rate, or close-rate inputs lack a label of estimated, user-confirmed, or user-supplied.

---

## CPC Estimates Far Off

- **Id**: cpc-estimates-far-off
- **Summary**: Estimated CPCs differ substantially from what the auction charges, so the budget fit is wrong from day one.
- **Severity**: high
- **Situation**: No Keyword Planner or account data is available, the market is a competitive metro, or the industry has volatile auctions (legal, insurance, emergency services).
- **Why**: Public CPC benchmarks are national averages; local auctions can run several times higher or lower.
- **Solution**:
    - Use the Competitive Landscape Scan to adjust CPC ranges per service and area.
    - Fit the budget to the high end of each CPC range.
    - List CPCs under Estimates To Verify and recommend re-checking the budget fit after the first two weeks of spend.
- **Symptoms**:
    - Brief shows single-point CPCs with no range or source.
    - Live campaign exhausts its budget by mid-day or spends far under budget.
- **Detection Pattern**: A budget allocation computed from single-point CPC figures with no stated range and no Keyword Planner, account data, or competition source.

---

## Tracking Gaps at Launch

- **Id**: tracking-gaps-at-launch
- **Summary**: Campaigns launch without working primary conversion tracking, or optimize toward low-intent actions.
- **Severity**: critical
- **Situation**: The client site has no conversion tags, call tracking is missing, or the only tracked actions are page views or clicks.
- **Why**: Without primary conversions, Maximize Conversions has nothing to learn from, CPL cannot be measured, and the bid strategy ladder never advances.
- **Solution**:
    - Follow the Conversion Hierarchy and list missing tracking as Must Fix Before Launch.
    - Start bidding on the first rung of the Bid Strategy Ladder until tracking is verified.
- **Symptoms**:
    - Conversion actions list includes page views or button clicks as primary.
    - Brief recommends Maximize Conversions while tracking is unverified.
- **Detection Pattern**: A build whose primary conversions include low-intent actions, or whose bid strategy relies on conversions while the destination audit shows tracking missing.

---

## Unsourced Claim Disapproval

- **Id**: unsourced-claim-disapproval
- **Summary**: Ad copy includes claims Google Ads disapproves or the client cannot substantiate.
- **Severity**: high
- **Situation**: Copy uses superlatives ("#1", "best"), unverifiable stats, guarantees the client has not confirmed, or prices that may change.
- **Why**: Google Ads requires third-party verification on the landing page for comparative or superlative claims, and claims that fail review leave the ad group with fewer eligible ads.
- **Solution**:
    - Trace every claim to a review theme, listing, client page, or user statement, recorded in the brief.
    - Replace superlatives with cited facts ("4.9 Stars From 64 Reviews").
- **Symptoms**:
    - Headlines containing "#1", "best", "top", or "guaranteed" without a cited source.
    - Ads stuck in "Disapproved" or "Eligible (limited)" after posting.
- **Detection Pattern**: Headlines or descriptions containing superlatives, rankings, guarantees, percentages, or prices that do not appear in the brief's differentiator sources.

---

## Geo Targeting Leak

- **Id**: geo-targeting-leak
- **Summary**: Ads show to people outside the client's service area, or the targeted area ignores where demand actually sits.
- **Severity**: medium
- **Situation**: Location targeting uses Google's default "Presence or interest", the targeted area is larger than the area the client serves, or the user's suggested areas are accepted without checking demand.
- **Why**: "Presence or interest" includes people merely searching about the area, and areas with little demand dilute budget that higher-demand areas could use.
- **Solution**:
    - Set location targeting to Presence.
    - Apply Geo Targeting From Demand and state why each area is targeted, observed, or excluded.
- **Symptoms**:
    - Leads from outside the service area.
    - Location column empty or set to a whole state for a single-city business.
- **Detection Pattern**: A campaign whose location targeting is missing, broader than the confirmed service area, set to presence or interest, or includes an area the demand map rates as negligible without a stated reason.

---

## Message Mismatch Penalty

- **Id**: message-mismatch-penalty
- **Summary**: Ad groups land on pages that do not lead with the searched service, lowering Quality Score and conversion rate.
- **Severity**: medium
- **Situation**: The client site has no service-specific pages, or the build sends everything to the homepage.
- **Why**: Landing page experience is part of Quality Score, so a mismatched page raises CPCs and wastes the clicks a tight budget buys.
- **Solution**:
    - Run the Destination Audit per ad group and classify each issue by urgency.
    - Recommend a landing page with a spec where message match is poor.
- **Symptoms**:
    - Several ad groups share the homepage as Final URL.
    - Low "Landing page experience" ratings after launch.
- **Detection Pattern**: Two or more ad groups with different intent sharing one Final URL, or an ad group whose Final URL page does not mention the ad group's service in its main heading.

---

## Character Limit Overflow

- **Id**: character-limit-overflow
- **Summary**: RSA headlines, descriptions, paths, or asset text exceed Google Ads character limits and fail import.
- **Severity**: medium
- **Situation**: Copy is written without counting characters, especially with location names or phone numbers inserted.
- **Why**: Google Ads Editor rejects over-limit text, and truncated copy loses its meaning.
- **Solution**:
    - Count characters for every line before writing the CSV and show the counts in the build sheet.
    - Shorten by dropping filler words rather than abbreviating the service name.
- **Symptoms**:
    - Editor import errors on the ads or assets file.
- **Detection Pattern**: Any headline over 30 characters, description over 90, path over 15, sitelink text over 25, sitelink description over 35, or callout over 25.
