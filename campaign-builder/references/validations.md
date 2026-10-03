# Validations

This document defines the validations used by campaign-builder.

---

## Budget Within Client Budget

- **Id**: campaign-budget-within-limit
- **Severity**: error
- **Type**: schema
- **Pattern**: The sum of daily budgets across all campaigns in the build, multiplied by 30.4, exceeds the monthly budget the user supplied.
- **Message**: The build spends more than the client's monthly budget.
- **Fix Action**: Reduce daily budgets or cut the lowest-margin ad group until the monthly total fits the client's budget.
- **Applies To**:
    - campaigns.csv
    - *brief*.md

---

## Click-Volume Floor Met

- **Id**: campaign-click-floor
- **Severity**: error
- **Type**: semantic
- **Pattern**: A funded ad group whose daily budget divided by its estimated CPC falls below the floor stated in the brief, and which the brief does not flag as below the floor with the user's approval.
- **Message**: This ad group cannot buy enough clicks per day to learn which keywords and ads convert.
- **Fix Action**: Cut the lowest-margin ad group and reallocate its budget, or flag the ad group as below the floor and record the user's approval in the brief.
- **Applies To**:
    - *brief*.md

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

## Asset Text Limits

- **Id**: campaign-asset-limits
- **Severity**: error
- **Type**: schema
- **Pattern**: A sitelink text over 25 characters, a sitelink description line over 35 characters, or a callout over 25 characters.
- **Message**: Asset text exceeds Google Ads character limits.
- **Fix Action**: Shorten the asset text to fit its limit.
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
    - Any competitor name the user listed during the interview, matched case-insensitively in headline or description text
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
- **Message**: campaign-builder produces Search campaigns on Google Search only.
- **Fix Action**: Set Campaign Type to Search and Networks to Google search only.
- **Applies To**:
    - campaigns.csv

---

## Geo Targeting Set to Presence

- **Id**: campaign-geo-presence
- **Severity**: error
- **Type**: schema
- **Pattern**: A campaign with no location targets, with targets broader than the confirmed service area, or with the location option set to presence or interest.
- **Message**: Location targeting must match the confirmed service area and use Presence.
- **Fix Action**: Set location targets to the cities, ZIP codes, or radius confirmed in the interview, with the Presence option.
- **Applies To**:
    - campaigns.csv

---

## Negative Keywords Present

- **Id**: campaign-negatives-present
- **Severity**: warning
- **Type**: schema
- **Pattern**: A keywords file with no campaign-level negative keywords.
- **Message**: The campaign has no negative keywords and will pay for job-seeker, DIY, and off-service searches.
- **Fix Action**: Add the Negative Keyword Baseline from `references/patterns.md` plus negatives for services the client does not offer.
- **Applies To**:
    - keywords.csv

---

## Destination Recommended per Ad Group

- **Id**: campaign-destination-per-ad-group
- **Severity**: error
- **Type**: semantic
- **Pattern**: A funded ad group with no destination recommendation in the brief, or an ad group routed to a landing page with no matching landing page spec.
- **Message**: Every funded ad group needs a destination decision, and every landing page decision needs a spec.
- **Fix Action**: Run the Destination Audit for the ad group and write the landing page spec where one is recommended.
- **Applies To**:
    - *brief*.md
    - *landing-page*.md

---

## Estimates Labeled

- **Id**: campaign-estimates-labeled
- **Severity**: error
- **Type**: semantic
- **Pattern**: A CPC, search volume, click count, or margin figure in the brief with no label marking it as estimated, user-confirmed, or user-supplied.
- **Message**: Unlabeled estimates read as measured data.
- **Fix Action**: Label each figure with its source and list every estimate under Estimates To Verify.
- **Applies To**:
    - *brief*.md

---

## Brief Sections Complete

- **Id**: campaign-brief-sections
- **Severity**: error
- **Type**: schema
- **Pattern**: A strategy brief missing any of the sections Client Snapshot, Industry Notes, Differentiators, Conversion Goal, Margin Ranking, Budget Allocation, Destination Recommendations, Geo Targeting, Estimates To Verify, or Research Source Log.
- **Message**: The strategy brief is missing a required section.
- **Fix Action**: Add the missing section per the Strategy Brief Structure pattern in `references/patterns.md`.
- **Applies To**:
    - *brief*.md

---

## Strategy Confirmed Before Build

- **Id**: campaign-confirmed-before-build
- **Severity**: error
- **Type**: semantic
- **Pattern**: Import files written in a run where the user has not explicitly confirmed the strategy presented in Phase 04.
- **Message**: Build files were produced before the strategy was confirmed.
- **Fix Action**: Present the strategy, end the turn, and write the build files after the user explicitly confirms.
- **Applies To**:
    - *.csv
