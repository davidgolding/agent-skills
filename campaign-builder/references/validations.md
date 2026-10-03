# Validations

This document defines the validations used by campaign-builder.

---

## Budget Within Client Budget

- **Id**: campaign-budget-within-limit
- **Severity**: error
- **Type**: schema
- **Pattern**: The sum of daily budgets across all campaigns in the build, multiplied by 30.4, exceeds the monthly budget the user supplied.
- **Message**: The build spends more than the client's monthly budget.
- **Fix Action**: Reduce daily budgets or cut the lowest-ranked ad group until the monthly total fits the client's budget.
- **Applies To**:
    - campaigns.csv
    - *build-sheet*.md

---

## Allocation Table Totals 100%

- **Id**: campaign-allocation-totals
- **Severity**: error
- **Type**: schema
- **Pattern**: A Launch Budget Allocation table whose percentages do not total 100%, whose monthly budgets do not sum to the allocated total, or whose daily budgets differ from monthly / 30.4 by more than one cent per row.
- **Message**: The launch budget allocation does not add up.
- **Fix Action**: Recompute each row from the confirmed allocation so percentages total 100% and daily equals monthly / 30.4; state any intentionally unspent budget as its own row.
- **Applies To**:
    - *build-sheet*.md

---

## Demand Estimate for Every Funded Service

- **Id**: campaign-demand-per-service
- **Severity**: error
- **Type**: semantic
- **Pattern**: A funded service, segment, or targeted area with no demand range, confidence level, cited signals, or demand-ceiling estimate in the brief's Demand Analysis.
- **Message**: This service is funded without evidence that local demand can absorb its budget.
- **Fix Action**: Run the Segment and Area Demand Map, Demand Signal Ladder, and Demand Ceiling patterns for the service and re-run the ranking.
- **Applies To**:
    - *brief*.md

---

## Allocation Within Demand Ceiling

- **Id**: campaign-allocation-within-ceiling
- **Severity**: error
- **Type**: semantic
- **Pattern**: A campaign or ad group whose monthly allocation exceeds its demand-ceiling spend by more than 20% without a stated reason (for example, a planned peak-season surge or a broad match test).
- **Message**: Budget is allocated beyond what local demand can absorb.
- **Fix Action**: Cap the allocation at the demand-ceiling spend and reallocate the excess per Profit-First Budget Fit, or state the reason.
- **Applies To**:
    - *brief*.md
    - *build-sheet*.md

---

## Profit-Potential Ranking Inputs Labeled

- **Id**: campaign-ranking-inputs-labeled
- **Severity**: error
- **Type**: semantic
- **Pattern**: A profit-potential ranking whose margin, average ticket, lead rate, close rate, CPC, or demand inputs lack a label of estimated, user-confirmed, or user-supplied.
- **Message**: The ranking that decides funding rests on unlabeled inputs.
- **Fix Action**: Label every input with its source and list estimated inputs under Estimates To Verify.
- **Applies To**:
    - *brief*.md

---

## Every Service Tiered

- **Id**: campaign-service-tiers
- **Severity**: error
- **Type**: schema
- **Pattern**: A candidate service from the research sweep that has no Tier 1, Tier 2, or Tier 3 assignment, or a tier assignment without a one-line reason.
- **Message**: Every candidate service needs a tier and a reason.
- **Fix Action**: Assign the service a tier per the Service Tiering pattern with a one-line reason.
- **Applies To**:
    - *brief*.md

---

## Click-Volume Floor Met

- **Id**: campaign-click-floor
- **Severity**: error
- **Type**: semantic
- **Pattern**: A funded ad group whose daily budget divided by its estimated CPC falls below the smaller of the stated floor and its demand ceiling, and which the brief does not flag as below the floor with the user's approval.
- **Message**: This ad group cannot buy enough clicks per day to learn which keywords and ads convert.
- **Fix Action**: Cut the lowest-ranked ad group and reallocate its budget, or flag the ad group as below the floor and record the user's approval in the brief.
- **Applies To**:
    - *brief*.md

---

## Campaign Split Reasons Recorded

- **Id**: campaign-split-reasons
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A build with more than one non-brand campaign where any campaign lacks a split reason drawn from budget control, geography, bidding, service priority, profitability, or search intent.
- **Message**: This campaign split has no recorded reason and may fragment budget and data.
- **Fix Action**: Record the reason per the Campaign Split Test, or merge the campaign into another as ad groups.
- **Applies To**:
    - *brief*.md

---

## Campaign Naming Convention

- **Id**: campaign-naming-convention
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - ^(?!Search \| [^|]+ \| (?:Non-Brand|Brand|Competitor) \| [^|]+$).+$
- **Message**: Campaign names follow `Search | Service or Segment | Non-Brand, Brand, or Competitor | Geo`.
- **Fix Action**: Rename the campaign to match the convention in the Campaign Split Test pattern.
- **Applies To**:
    - Campaign column of campaigns.csv

---

## Bid Strategy With Transition Trigger

- **Id**: campaign-bid-strategy-ladder
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A campaign with no starting bid strategy, no stated trigger for the next bid strategy, or a conversion-based starting strategy while primary conversion tracking is unverified.
- **Message**: Each campaign needs a starting bid strategy its data supports and a trigger for the next rung.
- **Fix Action**: Apply the Bid Strategy Ladder pattern.
- **Applies To**:
    - *brief*.md
    - *build-sheet*.md

---

## Broad Match Justified

- **Id**: campaign-broad-match-justified
- **Severity**: warning
- **Type**: semantic
- **Pattern**: A keyword with Criterion Type Broad whose ad group has no stated reason for broad match in the brief.
- **Message**: Broad match needs a stated reason tied to tracking, bidding, and demand.
- **Fix Action**: Change the keyword to phrase or exact, or record the reason per Intent-Grouped Ad Groups.
- **Applies To**:
    - keywords.csv
    - *brief*.md

---

## Price Terms Evaluated, Not Blocked

- **Id**: campaign-price-negatives
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - (?i)^\s*(?:cheap|cost|costs|price|prices|pricing|affordable)\s*$
- **Message**: Price-related terms can carry strong buying intent; blanket negatives cut qualified demand.
- **Fix Action**: Remove the negative, or keep it and record the positioning or lead-quality reason in the brief.
- **Applies To**:
    - Negative keyword rows of keywords.csv

---

## RSA Headline Limits

- **Id**: campaign-rsa-headline-limits
- **Severity**: error
- **Type**: schema
- **Pattern**: A responsive search ad with fewer than 3 or more than 15 headlines, or any headline longer than 30 characters.
- **Message**: Headlines must number 3-15 and each be 30 characters or fewer.
- **Fix Action**: Add or remove headlines to land in range (aim for 10-15) and shorten any headline over 30 characters.
- **Applies To**:
    - ads.csv

---

## RSA Description and Path Limits

- **Id**: campaign-rsa-description-limits
- **Severity**: error
- **Type**: schema
- **Pattern**: A responsive search ad with fewer than 2 or more than 4 descriptions, any description longer than 90 characters, or any display path longer than 15 characters.
- **Message**: Descriptions must number 2-4 at 90 characters or fewer, and display paths must be 15 characters or fewer.
- **Fix Action**: Adjust the description count and shorten any over-limit description or path.
- **Applies To**:
    - ads.csv

---

## Headline Variety

- **Id**: campaign-headline-variety
- **Severity**: warning
- **Type**: semantic
- **Pattern**: An RSA whose headlines cover fewer than five of the headline types (keyword, service, location, benefit, trust, differentiator, CTA, offer, legitimate urgency, brand), or contain near-duplicates differing by one word.
- **Message**: Headlines repeat each other instead of giving Google distinct messages to combine.
- **Fix Action**: Replace near-duplicates with headlines of missing types per Responsive Search Ad Construction.
- **Applies To**:
    - ads.csv

---

## Asset Text Limits and Counts

- **Id**: campaign-asset-limits
- **Severity**: error
- **Type**: schema
- **Pattern**: A sitelink text over 25 characters, a sitelink description line over 35 characters, a callout over 25 characters, or fewer than 8 callouts.
- **Message**: Asset text exceeds Google Ads character limits, or too few callouts are provided.
- **Fix Action**: Shorten the asset text to fit its limit and bring callouts to 8-12 sourced entries.
- **Applies To**:
    - assets.csv

---

## Claims Traced to Sources

- **Id**: campaign-claims-sourced
- **Severity**: error
- **Type**: semantic
- **Pattern**: A headline, description, callout, or landing page proof point stating a fact (rating, review count, speed, price, guarantee, credential, years in business) that does not appear in the brief's differentiator list or source log.
- **Message**: This claim has no cited source and may be disapproved or be untrue.
- **Fix Action**: Add the source to the brief if one exists, or replace the claim with a sourced differentiator.
- **Applies To**:
    - ads.csv
    - assets.csv
    - *landing-page*.md

---

## Superlatives and Competitor Trademarks

- **Id**: campaign-superlative-trademark
- **Severity**: warning
- **Type**: regex
- **Pattern**:
    - (?i)#\s?1\b
    - (?i)\b(?:best|top-rated|number one|cheapest|guaranteed lowest)\b
    - Any competitor name from the Competitive Landscape Scan or interview, matched case-insensitively in headline or description text
- **Message**: Superlatives need third-party verification on the landing page, and competitor names in ad text risk trademark disapproval.
- **Fix Action**: Replace the superlative with a cited fact (such as a star rating and review count) and remove competitor names from ad text.
- **Applies To**:
    - ads.csv
    - assets.csv

---

## Search-Only Network Settings

- **Id**: campaign-search-only-networks
- **Severity**: error
- **Type**: schema
- **Pattern**: A campaign row whose Campaign Type is not Search, or whose Networks setting includes Search Partners or the Display Network.
- **Message**: campaign-builder builds Search campaigns on Google Search only; Performance Max and other types appear only as recommendations.
- **Fix Action**: Set Campaign Type to Search and Networks to Google search only, and move any other campaign type to the Phase 2 or Do Not Build Yet list.
- **Applies To**:
    - campaigns.csv

---

## Brand, Competitor, and PMax Decisions Recorded

- **Id**: campaign-brand-competitor-pmax
- **Severity**: error
- **Type**: schema
- **Pattern**: A brief missing a Build Now, Phase 2, or Do Not Build Yet decision with a reason for any of Brand Search, Competitor Search, or Performance Max.
- **Message**: Each run records a decision on brand, competitor, and Performance Max campaigns.
- **Fix Action**: Apply the Brand, Competitor, and Performance Max Decisions pattern.
- **Applies To**:
    - *brief*.md

---

## Geo Targeting Set to Presence

- **Id**: campaign-geo-presence
- **Severity**: error
- **Type**: schema
- **Pattern**: A campaign with no location targets, with targets broader than the confirmed service area, or with the location option set to presence or interest without a stated reason.
- **Message**: Location targeting must match the confirmed service area and use Presence.
- **Fix Action**: Set location targets per Geo Targeting From Demand, with the Presence option.
- **Applies To**:
    - campaigns.csv

---

## Ad Schedule Present

- **Id**: campaign-ad-schedule
- **Severity**: warning
- **Type**: schema
- **Pattern**: A campaign with no ad schedule in the build sheet, or a schedule that restricts ads to office hours without a stated reason when form leads are captured.
- **Message**: Each campaign needs an explicit initial ad schedule with reasoning.
- **Fix Action**: Add a day / start / end schedule per the Ad Schedule Table pattern.
- **Applies To**:
    - *build-sheet*.md

---

## Audiences in Observation Only

- **Id**: campaign-audiences-observation
- **Severity**: error
- **Type**: schema
- **Pattern**: An audience applied to a Search campaign or ad group with Targeting in place of Observation.
- **Message**: Audience targeting narrows high-intent search reach; use Observation.
- **Fix Action**: Switch the audience setting to Observation.
- **Applies To**:
    - *build-sheet*.md
    - *.csv

---

## Primary Conversions Are High-Intent

- **Id**: campaign-primary-conversions
- **Severity**: error
- **Type**: semantic
- **Pattern**: A primary conversion action that is a page view, button click, form start, scroll, or directions click, without a stated reason tying it to revenue.
- **Message**: Bidding toward low-intent actions lowers lead quality.
- **Fix Action**: Move the action to secondary/observation per the Conversion Hierarchy pattern.
- **Applies To**:
    - *brief*.md
    - *build-sheet*.md

---

## Negative Keyword Layers Present

- **Id**: campaign-negatives-present
- **Severity**: warning
- **Type**: schema
- **Pattern**: A keywords file with no account-level negatives, or a multi-campaign build with no campaign-level cross-negatives.
- **Message**: The build lacks a negative keyword layer and will pay for irrelevant or overlapping searches.
- **Fix Action**: Add the layers from the Negative Keyword Layers pattern.
- **Applies To**:
    - keywords.csv

---

## Destination and Issue Urgency per Ad Group

- **Id**: campaign-destination-per-ad-group
- **Severity**: error
- **Type**: semantic
- **Pattern**: A funded ad group with no destination recommendation in the brief, a destination issue not classified as Must Fix Before Launch, Highly Recommended, or Optimization Opportunity, or an ad group routed to a landing page with no matching landing page spec.
- **Message**: Every funded ad group needs a destination decision with classified issues, and every landing page decision needs a spec.
- **Fix Action**: Run the Destination Audit for the ad group and write the landing page spec where one is recommended.
- **Applies To**:
    - *brief*.md
    - *landing-page*.md

---

## Estimates Labeled as Ranges

- **Id**: campaign-estimates-labeled
- **Severity**: error
- **Type**: semantic
- **Pattern**: A search volume, CPC, click, lead, CPL, or margin figure in the brief that is an unlabeled estimate or an estimate given as a single number where a range is expected.
- **Message**: Unlabeled or falsely precise estimates read as measured data.
- **Fix Action**: Give the figure as a range, label its source, and list every estimate under Estimates To Verify.
- **Applies To**:
    - *brief*.md

---

## Assumptions Listed

- **Id**: campaign-assumptions-listed
- **Severity**: error
- **Type**: semantic
- **Pattern**: An interview topic the user skipped or left unanswered that does not appear in the brief's Assumptions section with its reasoning.
- **Message**: A skipped topic shaped the plan without being shown to the user.
- **Fix Action**: Add the assumption with its reasoning per the Assume and Label pattern.
- **Applies To**:
    - *brief*.md

---

## Brief Sections Complete

- **Id**: campaign-brief-sections
- **Severity**: error
- **Type**: schema
- **Pattern**: A strategy brief missing any section listed in the Strategy Brief Structure pattern.
- **Message**: The strategy brief is missing a required section.
- **Fix Action**: Add the missing section per the Strategy Brief Structure pattern in `references/patterns.md`.
- **Applies To**:
    - *brief*.md

---

## Build Sheet Complete

- **Id**: campaign-build-sheet-sections
- **Severity**: error
- **Type**: schema
- **Pattern**: A build sheet missing any element listed in the Build Sheet pattern, including the Launch Budget Allocation table and the Build Now, Phase 2, and Do Not Build Yet lists.
- **Message**: The build sheet cannot be implemented as written.
- **Fix Action**: Add the missing element per the Build Sheet pattern.
- **Applies To**:
    - *build-sheet*.md

---

## Search-Term Plan Present

- **Id**: campaign-search-term-plan
- **Severity**: warning
- **Type**: schema
- **Pattern**: A brief without a search-term management plan covering days 7, 14, 30, and 60-90 with the triggers for each action.
- **Message**: The post-launch search-term plan is missing or incomplete.
- **Fix Action**: Add the plan per the Search-Term Management Plan pattern.
- **Applies To**:
    - *brief*.md

---

## Self-Check Recorded

- **Id**: campaign-self-check
- **Severity**: error
- **Type**: semantic
- **Pattern**: A brief whose Self-Check Revisions section is missing, or whose final self-check answer is not yes.
- **Message**: The build has not passed the owner's-money self-check.
- **Fix Action**: Run the Owner's-Money Self-Check, revise until the answer is yes, and record each revision.
- **Applies To**:
    - *brief*.md

---

## Strategy Confirmed Before Build

- **Id**: campaign-confirmed-before-build
- **Severity**: error
- **Type**: semantic
- **Pattern**: A build sheet or import files written in a run where the user has not explicitly confirmed the strategy presented in Phase 05.
- **Message**: Build files were produced before the strategy was confirmed.
- **Fix Action**: Present the strategy, end the turn, and write the build files after the user explicitly confirms.
- **Applies To**:
    - *build-sheet*.md
    - *.csv
