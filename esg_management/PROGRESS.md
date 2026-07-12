# EcoSphere ESG — Build Progress
Last updated: Step 13 — GitHub README, improvement backlog, and license consistency completed

## Status Summary
Done: 12 / 12 acceptance items

## ✅ Completed
- [x] All 8 Master Data models implemented with listed fields
- [x] All 9 Transactional Data models implemented with listed fields
- [x] Challenge state machine has all 5 states + guarded transition methods
- [x] Auto Emission Calculation toggle actually branches behavior, not just stored and ignored
- [x] Evidence Requirement toggle actually blocks Approval via constraint
- [x] Badge Auto-Award is event-driven and idempotent
- [x] Reward Redemption deducts points and decrements stock atomically
- [x] Compliance Issue overdue flag computed + cron + notification wired together
- [x] Department Score computes 3 pillar scores + weighted total using configurable weights
- [x] Security groups + access rules + record rules present
- [x] All 4 static reports + Custom Report Builder wizard with 3 export formats
- [x] Menu structure matches the module's 6 functional areas
- [x] Source-level Python and XML validation completed

## 🚧 In Progress
- [ ] Optional runtime installation test (blocked: no local Odoo executable/server; Docker Desktop daemon is not running)

## ⬜ Remaining
- [ ] Optional end-to-end runtime test against an Odoo 17 Community database

## 💡 Improvement Backlog

### High priority — production readiness
- [ ] Add an Odoo 17 automated test suite covering installation, access rules, approval evidence, challenge transitions, score snapshots, notifications, and reward-redemption concurrency.
- [ ] Run an end-to-end install/upgrade test against Odoo 17 Community with PostgreSQL and capture the exact upgrade command/output.
- [ ] Add a configurable ESG department mapping on purchase orders or analytic accounts instead of using the first active ESG department for automatic purchase emissions.
- [ ] Add native automatic adapters for Manufacturing, Expenses, and Fleet when their optional Odoo applications are installed.
- [ ] Add a migration/versioning policy and test upgrades from each released module version.

### Medium priority — product depth
- [ ] Add evidence review comments, rejection reasons, and employee resubmission flows for CSR and challenge participation.
- [ ] Add score trend graphs, drill-down filters, and period comparison to the dashboard.
- [ ] Add configurable metrics/formulas per environmental goal, including activity-normalised emission intensity.
- [ ] Add multi-company fields and company-aware record rules, sequences, reports, and scheduled jobs.
- [ ] Add policy document version comparison, expiry/review dates, and a publish approval workflow.
- [ ] Add reward fulfilment states, delivery tracking, and cancellation/refund handling.
- [ ] Add a self-service employee ESG portal or a mobile-friendly participation interface.

### Lower priority — integrations and polish
- [ ] Add import wizards for historical factors, carbon transactions, policy acknowledgements, and targets.
- [ ] Add configurable report branding, saved report filters, scheduled report emails, and spreadsheet attachments.
- [ ] Add external data-provider connectors for emission-factor libraries and utility/fleet activity data.
- [ ] Add translations, accessibility review, onboarding sample data, user documentation, and a demo video.
- [ ] Add CI for linting, tests, XML validation, manifest checks, and Odoo module installation smoke tests.

## ⚠️ Known Gaps / Assumptions
- ASSUMPTION: Auto emissions are generated from purchase-order lines, as manufacturing, expenses, and fleet require optional or non-core models.
- ASSUMPTION: ESG department membership is maintained through `esg.department.member_ids` to remain decoupled from HR departments.

## 🔜 Next Step
- Start an Odoo 17 Community environment, add this repository to `addons_path`, upgrade `esg_management`, then exercise approval, purchase confirmation, cron, and export flows.
