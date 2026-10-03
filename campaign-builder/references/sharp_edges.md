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

## Thin Online Presence

- **Id**: thin-online-presence
- **Summary**: The client has few or no reviews and a minimal website, leaving little to build differentiators from.
- **Severity**: high
- **Situation**: A new business, a business that relies on referrals, or one whose listings were never claimed.
- **Why**: Review-mined differentiators need several reviewers saying the same thing; with five reviews there is no pattern to find.
- **Solution**:
    - Say plainly in the brief which sources were thin or empty.
    - Shift the interview toward differentiators: ask the user what the client does that competitors do not, and mark those claims as user-stated.
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
    - Apply Margin-First Budget Fit and cut from the bottom of the margin ranking.
    - When the user insists on including a service below the floor, flag it in the brief as below the floor with the budget it needs.
    - Run the Budget Shortfall Verdict when even the top service fails the floor.
- **Symptoms**:
    - Estimated clicks per day per ad group below 5.
    - Budget divided evenly across many ad groups.
- **Detection Pattern**: Any funded ad group whose daily budget divided by its estimated CPC is below the floor stated in the brief, without a below-floor flag.

---

## Margin Estimate Treated as Fact

- **Id**: margin-estimate-treated-as-fact
- **Summary**: The industry-benchmark margin ranking drives budget cuts without the user confirming it.
- **Severity**: high
- **Situation**: The interview skips margin confirmation, or the user gives a vague answer and the estimate stands without a label.
- **Why**: Margins vary sharply by client (equipment deals, labor costs, specialties), and the margin ranking decides which services get any budget at all.
- **Solution**:
    - Present the estimated ranking in the interview and invite actual figures.
    - Mark the ranking in the brief as estimated, user-confirmed, or user-supplied.
- **Symptoms**:
    - The brief's margin ranking carries no source label.
    - The user is surprised by which services were cut.
- **Detection Pattern**: A margin ranking in the brief lacking a label of estimated, user-confirmed, or user-supplied, or a budget allocation produced before the margin question was asked.

---

## CPC Estimates Far Off

- **Id**: cpc-estimates-far-off
- **Summary**: Estimated CPCs differ substantially from what the auction charges, so the budget fit is wrong from day one.
- **Severity**: high
- **Situation**: No Keyword Planner or account data is available, the market is a competitive metro, or the industry has volatile auctions (legal, insurance, emergency services).
- **Why**: Public CPC benchmarks are national averages; local auctions can run several times higher or lower.
- **Solution**:
    - Invite Keyword Planner data in the interview and use it when given.
    - Show a CPC range rather than a single figure, and fit the budget to the high end of the range.
    - List CPCs under Estimates To Verify and recommend re-checking the budget fit after the first two weeks of spend.
- **Symptoms**:
    - Brief shows single-point CPCs with no range or source.
    - Live campaign exhausts its budget by mid-day or spends far under budget.
- **Detection Pattern**: A budget allocation computed from single-point CPC figures with no stated range and no Keyword Planner or account data source.

---

## Unsourced Claim Disapproval

- **Id**: unsourced-claim-disapproval
- **Summary**: Ad copy includes claims Google Ads disapproves or the client cannot substantiate.
- **Severity**: high
- **Situation**: Copy uses superlatives ("#1", "best"), unverifiable stats, guarantees the client has not confirmed, or prices that may change.
- **Why**: Google Ads requires third-party verification on the landing page for comparative or superlative claims, and claims that fail review leave the ad group with fewer eligible ads.
- **Solution**:
    - Trace every claim to a review theme, listing, client page, or user statement, recorded in the brief.
    - Replace superlatives with cited facts ("4.8 Stars From 212 Reviews").
- **Symptoms**:
    - Headlines containing "#1", "best", "top", or "guaranteed" without a cited source.
    - Ads stuck in "Disapproved" or "Eligible (limited)" after posting.
- **Detection Pattern**: Headlines or descriptions containing superlatives, rankings, guarantees, percentages, or prices that do not appear in the brief's differentiator sources.

---

## Geo Targeting Leak

- **Id**: geo-targeting-leak
- **Summary**: Ads show to people outside the client's service area.
- **Severity**: medium
- **Situation**: Location targeting uses Google's default "Presence or interest", or the targeted area is larger than the area the client serves.
- **Why**: "Presence or interest" includes people merely searching about the area, which wastes local-service budgets on unservable leads.
- **Solution**:
    - Set location targeting to Presence.
    - Target the confirmed cities, ZIP codes, or radius from the interview, and list the targeted area in the brief.
- **Symptoms**:
    - Leads from outside the service area.
    - Location column empty or set to a whole state for a single-city business.
- **Detection Pattern**: A campaign row whose location targeting is missing, broader than the confirmed service area, or set to presence or interest.

---

## Message Mismatch Penalty

- **Id**: message-mismatch-penalty
- **Summary**: Ad groups land on pages that do not lead with the searched service, lowering Quality Score and conversion rate.
- **Severity**: medium
- **Situation**: The client site has no service-specific pages, or the build sends everything to the homepage.
- **Why**: Landing page experience is part of Quality Score, so a mismatched page raises CPCs and wastes the clicks a tight budget buys.
- **Solution**:
    - Run the Destination Audit per ad group.
    - Recommend a landing page with a spec where message match is poor.
- **Symptoms**:
    - Several ad groups share the homepage as Final URL.
    - Low "Landing page experience" ratings after launch.
- **Detection Pattern**: Two or more ad groups sharing one Final URL, or an ad group whose Final URL page does not mention the ad group's service in its main heading.

---

## Character Limit Overflow

- **Id**: character-limit-overflow
- **Summary**: RSA headlines, descriptions, paths, or asset text exceed Google Ads character limits and fail import.
- **Severity**: medium
- **Situation**: Copy is written without counting characters, especially with location names or phone numbers inserted.
- **Why**: Google Ads Editor rejects over-limit text, and truncated copy loses its meaning.
- **Solution**:
    - Count characters for every line before writing the CSV and show the counts in the brief's ad copy section.
    - Shorten by dropping filler words rather than abbreviating the service name.
- **Symptoms**:
    - Editor import errors on the ads or assets file.
- **Detection Pattern**: Any headline over 30 characters, description over 90, path over 15, sitelink text over 25, sitelink description over 35, or callout over 25.
