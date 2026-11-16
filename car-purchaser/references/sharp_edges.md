# Sharp Edges

This document defines the sharp edges used by car-purchaser.

The first group is the bundled tactics playbook: durable seller tactics and their counters, last reviewed 2026-11-16. The second group covers the skill's own failure risks. Treat every dollar figure, rate, and legal rule here as a starting point to verify live. When live research disagrees, the live finding wins and the conflict goes into `research.md`.

---

## Payment Packing

- **Id**: tactic-payment-packing
- **Summary**: The seller steers the conversation to a monthly payment, then hides add-ons, a longer term, or a higher rate inside it.
- **Severity**: critical
- **Situation**: "What monthly payment are you looking for?" comes up early, or a quote arrives as a payment with no itemized total.
- **Why**: Buyers judge affordability by the monthly figure, and stretching 60 months to 84 can absorb thousands of dollars without the payment moving much.
- **Solution**:
    - Answer with the out-the-door focus script, and ask for an itemized out-the-door total.
    - Recompute any payment the seller offers from price, rate, and term, and reconcile the difference line by line.
- **Symptoms**:
    - The quote shows a payment but no total, or a term longer than the buyer asked for.
- **Detection Pattern**: A seller message or document that presents a monthly payment without an itemized out-the-door total, or a term longer than the term recorded in the buyer's profile.

---

## Four-Square Blending

- **Id**: tactic-four-square
- **Summary**: A worksheet ties price, trade-in, down payment, and payment together so concessions in one box are clawed back in another.
- **Severity**: high
- **Situation**: In-person negotiation, often on a printed grid, or a reply that bundles a trade-in figure with a price.
- **Why**: Moving four numbers at once hides where the money went.
- **Solution**:
    - Use the Separate Negotiations Order and lock each figure in writing before the next.
- **Symptoms**:
    - A raised trade-in offer arrives together with a lower discount or a higher rate.
- **Detection Pattern**: A seller proposal that changes two or more of price, trade-in value, rate, or down payment in the same offer.

---

## Signing-Desk Drift

- **Id**: tactic-signing-desk-drift
- **Summary**: The buyer's order or contract at signing differs from the agreed figure through added fees, add-ons, or a changed rate or term.
- **Severity**: critical
- **Situation**: Paperwork stage, often late in the day after hours at the dealership, sometimes as an electronic signature pad that shows only signature lines.
- **Why**: A tired buyer who has already "bought" the car emotionally rarely restarts the negotiation over a few hundred dollars.
- **Solution**:
    - Run the signing-sheet check line by line before any signature.
    - Ask to see the full document behind any e-signature pad.
    - Walk away when a trigger fires and the seller won't correct it.
- **Symptoms**:
    - A new line item, a higher total, a different rate, term, or lender, or blank fields.
- **Detection Pattern**: A signing document whose total, line items, rate, term, or VIN differs from the locked quote recorded in the signing sheet.

---

## Spot Delivery and Yo-Yo Financing

- **Id**: tactic-yo-yo-financing
- **Summary**: The buyer drives home before financing is final, then is called back to sign at a worse rate because the loan "didn't go through."
- **Severity**: critical
- **Situation**: Dealer-arranged financing with contract language like "subject to financing approval" or a separate bailment or rescission agreement.
- **Why**: Once the buyer has the car and the trade-in is gone, they have little leverage to refuse the new terms.
- **Solution**:
    - Bring outside pre-approval and use it unless the dealer beats it with final, funded terms.
    - Decline delivery until financing is confirmed final in writing.
    - Keep the trade-in until the deal is final.
- **Symptoms**:
    - A conditional-approval clause, a separate rescission form, or a call days later about financing.
- **Detection Pattern**: Contract or addendum language that makes the sale conditional on later financing approval, or a seller message after delivery asking the buyer to re-sign.

---

## Dealer Rate Markup

- **Id**: tactic-rate-markup
- **Summary**: The dealer arranges a loan at a rate above the one the lender approved and keeps the difference as dealer reserve.
- **Severity**: high
- **Situation**: Dealer-arranged financing, especially when the buyer has no competing pre-approval.
- **Why**: Lenders commonly allow dealers to add a couple of points, and the buyer never sees the approved "buy rate."
- **Solution**:
    - Get pre-approval first, ask the dealer to beat it in writing, and compare APR and term exactly.
- **Symptoms**:
    - An offered APR noticeably above the buyer's pre-approval or published rates for their credit tier.
- **Detection Pattern**: A dealer financing offer whose APR exceeds the buyer's recorded pre-approval or the cited market rate for their credit tier.

---

## Pre-Loaded Add-Ons and Market Adjustments

- **Id**: tactic-preloaded-addons
- **Summary**: Lines such as "protection package," nitrogen tires, VIN etching, paint sealant, or "market adjustment" are already printed on the price sticker or quote.
- **Severity**: high
- **Situation**: Dealer quotes and addendum stickers next to the window sticker.
- **Why**: Printed add-ons look non-negotiable, and buyers assume they're already installed and can't be removed.
- **Solution**:
    - Ask for an out-the-door quote without them. Treat them as optional, and push back or walk away.
    - Compare against other sellers that don't carry them.
- **Symptoms**:
    - An addendum sticker, or a line item in the quote with a marketing name and no clear service.
- **Detection Pattern**: Any quote or sticker line beyond selling price, government fees, tax, and a single documentation fee.

---

## F&I Office Pressure

- **Id**: tactic-fi-menu
- **Summary**: After price is agreed, the finance office sells extended warranties, GAP, maintenance plans, and protection products at large markups, often framed as required or "included."
- **Severity**: high
- **Situation**: The finance-and-insurance step at signing.
- **Why**: Add-ons get rolled into the loan, so their cost looks like a small payment change, and buyers are tired by this point.
- **Solution**:
    - Decide in advance which products, if any, to accept, using fair-price benchmarks. GAP is often cheaper through the buyer's insurer or credit union.
    - Ask that any product be shown as its own price, and know that most can be cancelled after signing for a prorated refund.
- **Symptoms**:
    - "The bank requires it," a menu with only bundled options, or a payment that moves without explanation.
- **Detection Pattern**: Finance-office products presented as required for loan approval, or a payment change with no matching itemized product price.

---

## Trade-In Lowball and Negative Equity Rollover

- **Id**: tactic-trade-in
- **Summary**: The dealer undervalues the trade or quietly rolls the remaining loan balance into the new loan.
- **Severity**: high
- **Situation**: Any deal with a trade-in, especially one where more is owed than the car is worth.
- **Why**: Without independent offers the buyer has no anchor, and rolled-in negative equity disappears into the amount financed.
- **Solution**:
    - Get instant offers from independent buyers before negotiating, and sell outright if they beat the dealer.
    - State the negative equity explicitly and pay it down where possible.
- **Symptoms**:
    - A trade-in figure well below independent offers, or an amount financed above price plus tax and fees.
- **Detection Pattern**: A trade-in value below the lowest recorded independent offer, or an amount financed that exceeds the out-the-door total minus the down payment and trade-in equity.

---

## Lead Capture and Follow-Up Hounding

- **Id**: tactic-lead-capture
- **Summary**: Test drives, "check availability" forms, and price-unlock buttons collect the buyer's phone and email, which feed sales follow-up calls.
- **Severity**: medium
- **Situation**: Online listings, test-drive sign-ins, and license scans at the dealership.
- **Why**: The dealer's sales process measures contact attempts, so sharing a phone number invites daily calls.
- **Solution**:
    - Recommend an alias email and a forwarding number used only for this deal, and the buyer's preference for email-only contact.
    - Test drive at a dealer that isn't in the bidding, or after quotes are locked.
- **Symptoms**:
    - Unsolicited calls or texts from dealers the buyer hasn't contacted by email.
- **Detection Pattern**: A plan step that has the buyer submit a lead form or test drive using their primary phone number before quotes are locked.

---

## Bait-and-Switch Listings

- **Id**: tactic-bait-and-switch
- **Summary**: An advertised price or unit disappears on arrival ("just sold"), or the price requires conditions the buyer doesn't meet (dealer financing, a trade-in, a loyalty rebate).
- **Severity**: high
- **Situation**: Low internet prices, and travel to a dealer based on a listing.
- **Why**: Once at the dealership, the buyer is easier to sell a different unit to.
- **Solution**:
    - Confirm by email that the stock number is available and that the out-the-door price holds, with every condition listed, before traveling.
- **Symptoms**:
    - Fine print like "with dealer financing," "includes all rebates," or "must trade," or vague answers about availability.
- **Detection Pattern**: A listing price with qualifying conditions in its fine print, or a seller reply that confirms the model but not the stock number and price.

---

## Online Retailer Fine Print

- **Id**: tactic-online-fine-print
- **Summary**: Home-delivery retailers carry their own traps: delivery and processing fees, return windows that start on delivery, mileage caps on returns, title and registration delays, and their own financing markups.
- **Severity**: medium
- **Situation**: Buying from an online used-car retailer or a manufacturer's online store.
- **Why**: The checkout feels like ordinary online shopping, so buyers skip reading the purchase agreement.
- **Solution**:
    - Pull the current return policy, fees, and title-processing timeline live, and treat the retailer as one more seller in the ledger.
    - Arrange an independent inspection within the return window.
- **Symptoms**:
    - A delivery or "shipping" fee that appears at checkout, or a return policy shorter than advertised.
- **Detection Pattern**: An online seller quote without the return window, delivery fee, and title-processing terms recorded in the ledger.

---

## Private-Party Title and Payment Scams

- **Id**: tactic-private-party-scams
- **Summary**: Private sales carry curbstoning (unlicensed dealers posing as owners), liens and title washing, odometer fraud, and payment scams (escrow fakes, deposit requests, overpayment).
- **Severity**: critical
- **Situation**: Private-party listings, especially below market.
- **Why**: There is no dealer liability, and once money changes hands it's rarely recoverable.
- **Solution**:
    - Check that the title is in the seller's name, has no lien, and matches the VIN on the car.
    - Run a history report and an independent pre-purchase inspection.
    - Pay in person at the buyer's bank or the seller's lender, with a cashier's check or a transfer made there, and transfer the title the same day.
- **Symptoms**:
    - The seller isn't on the title, pushes for a deposit or "escrow" link, or the price is far below market.
- **Detection Pattern**: A private listing or seller message involving a name mismatch with the title, a deposit request before inspection, a third-party escrow link, or a price more than about 20 percent below market.

---

## Used-Car "As Is" and Reconditioning Fees

- **Id**: tactic-used-as-is
- **Summary**: Used cars are sold "as is" with reconditioning or certification fees added, and the CPO warranty may be narrower than advertised.
- **Severity**: medium
- **Situation**: Dealer used and CPO purchases.
- **Why**: Buyers assume dealer inspection protects them, and fees named "reconditioning" look mandatory.
- **Solution**:
    - Read the federally required Buyers Guide on the window, get an independent inspection, and compare the CPO warranty terms live.
    - Treat reconditioning fees as part of the price to negotiate.
- **Symptoms**:
    - An "as is" box checked, or a reconditioning line on the quote.
- **Detection Pattern**: A used-car quote with reconditioning or certification fees listed separately, or no record of the Buyers Guide warranty status in the deal folder.

---

## Lease Money Factor and Residual Games

- **Id**: tactic-lease-games
- **Summary**: The lease is quoted by payment, while the money factor is marked up, the capitalized cost isn't negotiated, or fees and drive-off amounts are inflated.
- **Severity**: high
- **Situation**: Any lease negotiation.
- **Why**: Lease terms are unfamiliar, and the payment hides the parts.
- **Solution**:
    - Get capitalized cost, money factor, residual, fees, and mileage in writing. Convert the money factor to an APR and compare with the captive lender's base rate, checked live.
- **Symptoms**:
    - A quote with a payment but no money factor or residual, or large "due at signing" amounts.
- **Detection Pattern**: A lease quote that omits money factor, residual value, or capitalized cost, or whose money factor exceeds the cited base rate.

---

## Stale Playbook Figures

- **Id**: skill-stale-figures
- **Summary**: The agent states incentives, rates, fee caps, or tax-credit rules from this file or from memory as current fact.
- **Severity**: critical
- **Situation**: Any figure or rule that changes over time, especially EV and state incentives, which change often.
- **Why**: Bundled guidance ages, and a confidently wrong figure costs the buyer money or credibility in a negotiation.
- **Solution**:
    - Check live, cite source and date, and record any conflict in `research.md`.
- **Symptoms**:
    - Figures with no source or date, or references to programs that have since ended.
- **Detection Pattern**: A price, rate, incentive, fee cap, or legal rule stated in a deal-folder file or chat reply without a source and check date.

---

## Lost Deal State

- **Id**: skill-lost-state
- **Summary**: A session works from chat memory and skips updating the deal folder, so the next session re-asks questions or misses a quote.
- **Severity**: high
- **Situation**: Long coaching stretches, or quick phone sessions.
- **Why**: The deal spans days and several sessions, and the folder is the only shared memory.
- **Solution**:
    - Read the folder at the start of every session, and write to it when each decision, quote, or message lands.
- **Symptoms**:
    - The agent asks for information the profile already holds, or the ledger is missing a quote the buyer relayed.
- **Detection Pattern**: A session that ends after receiving a quote, decision, or message without a matching dated entry in the deal folder.

---

## Overreach Into Acting for the Buyer

- **Id**: skill-overreach
- **Summary**: The agent sends a message, fills a lead or credit form, or treats the buyer's "just handle it" as permission to contact sellers.
- **Severity**: critical
- **Situation**: The buyer is tired and asks the agent to take over outreach.
- **Why**: The buyer chose agent-drafts, buyer-sends to protect their contact details and keep control. Sending exposes them to follow-up calls and commits them to terms.
- **Solution**:
    - Hand over a ready-to-send draft, and offer to make sending faster (pre-filled subject, list of recipients).
- **Symptoms**:
    - Tool calls that send email, submit forms, or enter personal data on seller sites.
- **Detection Pattern**: Any agent action that transmits a message or personal data to a seller, lender, or listing site.

---

## Advice Beyond Decision Support

- **Id**: skill-advice-overreach
- **Summary**: The agent tells the buyer what they should do with their money as personalized financial, legal, or tax advice instead of laying out math and options.
- **Severity**: medium
- **Situation**: Questions like "should I pay cash or finance?" or "is this contract legal?"
- **Why**: The skill isn't a licensed advisor, and contract disputes and tax questions depend on facts it can't verify.
- **Solution**:
    - Show the comparison math and the questions to ask, and point to a credit union officer, the state attorney general's consumer office, or a tax professional where it fits.
- **Symptoms**:
    - Directive money advice with no math shown, or a legal conclusion about a specific contract.
- **Detection Pattern**: A reply that tells the buyer what to do with their money or declares a contract legal or illegal without showing the comparison or naming who to consult.
