# EcoSphere ESG — Build Progress
Last updated: Odoo 17 clean install and regression suite runtime-verified

## Status Summary
Done (implemented): 12 / 12 acceptance items

Done (runtime-verified): 10 / 12 acceptance items

## ✅ Completed (implemented; runtime results noted where available)
- [x] All 8 Master Data models implemented with listed fields
- [x] All 9 Transactional Data models implemented with listed fields
- [x] Challenge state machine has all 5 states + guarded transition methods — runtime-verified through Draft → Active → Under Review → Completed and archive from Completed.
- [x] Auto Emission Calculation toggle actually branches behavior, not just stored and ignored — runtime-verified for both enabled (creates a transaction) and disabled (creates none) purchase-order paths.
- [x] Evidence Requirement toggle actually blocks Approval via constraint — runtime-verified for CSR participation without and then with proof.
- [x] Badge Auto-Award is event-driven and idempotent — runtime-verified by the Odoo 17 regression suite.
- [x] Reward Redemption deducts points and decrements stock atomically — runtime-verified.
- [x] Compliance Issue overdue flag computed + cron + notification wired together — runtime-verified, including activity follow-up.
- [x] Department Score computes 3 pillar scores + weighted total using configurable weights — runtime-verified, including monthly snapshots.
- [x] Security groups + access rules + record rules present — runtime-verified with distinct ESG-user and manager accounts.
- [x] All 4 static reports + Custom Report Builder wizard with 3 export formats — runtime-verified for QWeb rendering and PDF/Excel/CSV actions.
- [x] Menu structure matches the module's 6 functional areas — runtime-verified through Odoo's per-user menu visibility API and action resolution.
- [x] Source-level Python and XML validation completed

## 🚧 In Progress
- [x] Odoo 17 clean install and upgrade smoke test passed in database `ecosphere_runtime_verify`; the module loaded after all dependencies without install errors.
- [x] Static Python compilation and XML parsing passed in the Odoo 17 image.
- [x] A clean install in `ecosphere_runtime_suite` passed, followed by five Odoo 17 regression tests with 0 failures and 0 errors. The suite covers badges, compliance crons/activities, score snapshots, access rules, reports/export actions, and menu visibility.
- [ ] Browser-level visual smoke check remains: the login screen at `http://localhost:8069` is reachable, but no test login was supplied or entered.

## ⬜ Remaining
- [ ] Exercise the browser UI with an ESG-user and manager account, including visual layout and actual HTTP XLSX/CSV downloads. All current workflow checks are ORM-level tests in the isolated `ecosphere_runtime_suite` database.

## 💡 Improvement Backlog

### High priority — production readiness
- [ ] Extend the Odoo 17 automated test suite beyond its current badge, compliance, scoring, access, report, and menu coverage to include installation, evidence approval, challenge transitions, and reward-redemption concurrency.
- [ ] Run an end-to-end upgrade test against Odoo 17 Community with PostgreSQL and capture the exact upgrade command/output.
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
- SCOPE GAP: Only purchase orders have automatic carbon-transaction generation. Manufacturing, employee expenses, and fleet automatic adapters are not implemented; those source types are available for manual records only.
- ESG department membership is independent from Odoo HR departments and uses one paired relationship: `hr.employee.esg_department_id` (Many2one, canonical stored field) and `esg.department.member_ids` (its inverse One2many field).

## 🔜 Next Step
- With permission to enter a disposable test-account password, run the remaining browser-level UI and HTTP-download smoke test. Then extend the automated suite to evidence, challenge, and reward-concurrency coverage.
