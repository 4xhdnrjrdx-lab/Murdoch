"""Supporting exhibits and transparent assumption notes, excluded as appendices."""
APPENDIX_A = [
('Exhibit 1. SWOT and response', ['Factor','Project implication','Proposed response'],[
['Strength: regional platform and merchants','Capabilities may be reused; availability is unconfirmed.','Obtain an internal sponsor and costed service agreement.'],
['Weakness: untested Jordan service','Delivery costs and slow returns can erode contribution.','Limit categories and launch area; use local returns handling.'],
['Opportunity: digital access and payment options','Reach is plausible, but willingness to pay remains unknown.','Run paid-order tests at the full checkout price.'],
['Threat: established alternatives and disruption','Competitors can undercut the offer; border delays affect trust.','Benchmark baskets, retain stop rights and monitor route exposure.']]),
('Exhibit 2a. Customer and order assumptions', ['Metric','2027','2028','2029'],[
['Active customers','20,000','40,000','60,000'],['Orders per customer','3.00','3.75','4.00'],['Net completed orders','60,000','150,000','240,000'],['Average goods basket, JOD','45.00','45.00','45.00']]),
('Exhibit 2b. Planned sales mix, 2027', ['Category','Order share','Basket JOD','GMV JOD'],[
['Home accessories, non-electrical','40%','50','1,200,000'],['Fashion accessories','35%','40','840,000'],['Phone accessories, non-powered','25%','44','660,000'],['Total / weighted basket','100%','45','2,700,000']]),
]
ASSUMPTIONS = [
('Demand and timing','2027 is an illustrative first full year. The 2028 JV and 2029 scale-up depend on gates, not calendar entitlement. All orders are fulfilled, paid and net of goods refunds. No primary demand research has occurred.'),
('Revenue','Commission is 15% of net goods GMV; delivery income is JOD 3 per completed order, net of tax. No advertising, membership, finance income or seller storage fees are assumed. Goods proceeds belong to merchants. The 15% benchmark resembles home-category rates in noon’s UAE FBP fee page (noon, n.d.-c), which contains old and revised September 2026 tables. It is not a quoted Jordan rate; commission bases and categories require a new agreement.'),
('Variable costs','Payment cost is 2% of goods GMV, a blended planning allowance including collection and gateway costs. Logistics covers ordinary handling, cross-border freight where applicable, brokerage allocation and last mile. JOD 0.90/0.70/0.60 adds failed-delivery, return handling and loss allowance per net order; it does not count goods refunds twice.'),
('Cost improvement','Logistics at JOD 7.00/4.80/4.50 per order assumes local stocking and delivery density after the pilot. These are target economics, not carrier quotations. They must be rejected if supplier bids do not support them.'),
('Fixed costs and setup','Annual fixed costs cover personnel, marketing, platform support and rent/advisers/admin. The JOD 100,000 setup expense consists of configuration 40,000, legal work 20,000, merchant onboarding 20,000 and training 20,000. These are incremental planning envelopes.'),
('Capex and working capital','Capex of JOD 90,000/90,000/30,000 covers equipment and local fit-out, separately from expensed setup. Three-year straight-line depreciation, zero residual value, acquisition at each January start. Closing net operating working capital is JOD 40,000/100,000/160,000; increases are funded each January. This excludes inventory and safeguarded seller funds.'),
('Tax and duties','21% of positive accounting profit is a scenario reserve, not confirmed tax advice. No loss carry-forward, deferred tax, subsidy or tax holiday is assumed. Recoverable transaction taxes and merchant goods receipts are pass-through. Non-recoverable import charges must be recovered in merchant prices or explicitly added as costs; no blanket zero-duty assumption is made.'),
('Funding and ownership','JOD 600,000 equity is assumed at January 2027 and JOD 300,000 at January 2028. No commitment, investor split, dividend or debt is assumed. Statements show 100% of project economics before allocation to partners, not IFRS group consolidation.'),
('Capacity and price levels','Nominal JOD, no separate inflation escalator. Rising personnel and fixed budgets allow expansion; variable cost reductions require operating evidence. AOV and commission remain fixed in the base case. No terminal value, IRR, NPV or three-year payback is claimed.'),
]
RISK_ROWS = [
['Unverified legal or tariff treatment','Before first paid order or new SKU','Counsel and customs broker','Hold affected launch/SKUs; obtain written classification and approval.'],
['Negative order contribution','Weekly, or a loss-making campaign','Finance lead','Pause acquisition; revise price, categories or delivery terms.'],
['Cash below JOD 100,000','Monthly rolling 13-week forecast','Country lead and sponsor','Freeze discretionary expansion; confirm funding or orderly exit.'],
['Delivery below 95% on time or failures at/above 8%','Monthly pilot review','Operations lead','Correct route/address issues; delay JV and narrow delivery area.'],
['Repeat purchase below 35%','90-day eligible customer cohorts','Commercial lead','Investigate price and service; repeat the test before expansion.'],
['Border closure, unsafe goods or data incident','Immediate notification to operating lead','Operations / legal / privacy lead','Stop affected orders, contain harm and arrange lawful customer remedies.'],
]
TEAM_ROWS = [
['Aram','Company profile, business model and data; poster weeks 1 to 3','Verify company structure, markets and sponsor assumptions.'],
['Faiaz','Jordan macro/micro environment and SWOT; poster weeks 4 to 6','Challenge demand proxies, legal caveats and competitor comparisons.'],
['Abdoul','Strategy, entry mode and finance; poster weeks 7 to 9','Recalculate model and challenge costs, funding and transition gates.'],
['Hatim','Sources, editing, report and slides; poster weeks 10 to 12','Check citations, natural language, formatting and bibliography.'],
['Denis','Overall coordination','Confirm topic approval, final reviewer, internal deadline and named uploader.'],
]
SCHEDULE_ROWS = [
['By 24 October','Each proposed reviewer checks assigned sections and records corrections.'],
['By 28 October','Team resolves strategy, model assumptions, topic approval and AI-use permission.'],
['By 2 November','Integrate verified changes; complete genuine contribution records and peer forms.'],
['By 4 November','Leader checks final PDF, word count, citations and submission requirements.'],
['6 November, 19:55 Dubai','Official Moodle report deadline; leader submits only after team approval.'],
]
