# EcoSphere ESG — Build Progress
Last updated: Odoo 17 clean install/upgrade and four core workflows runtime-verified

## Status Summary
Done (implemented): 12 / 12 acceptance items

Done (runtime-verified): 4 / 12 acceptance items

## ✅ Completed (implemented; runtime results noted where available)
- [x] All 8 Master Data models implemented with listed fields
- [x] All 9 Transactional Data models implemented with listed fields
- [x] Challenge state machine has all 5 states + guarded transition methods — runtime-verified through Draft → Active → Under Review → Completed and archive from Completed.
- [x] Auto Emission Calculation toggle actually branches behavior, not just stored and ignored — runtime-verified for both enabled (creates a transaction) and disabled (creates none) purchase-order paths.
- [x] Evidence Requirement toggle actually blocks Approval via constraint — runtime-verified for CSR participation without and then with proof.
- [x] Badge Auto-Award is event-driven and idempotent
- [x] Reward Redemption deducts points and decrements stock atomically — runtime-verified.
- [x] Compliance Issue overdue flag computed + cron + notification wired together
- [x] Department Score computes 3 pillar scores + weighted total using configurable weights
- [x] Security groups + access rules + record rules present
- [x] All 4 static reports + Custom Report Builder wizard with 3 export formats
- [x] Menu structure matches the module's 6 functional areas
- [x] Source-level Python and XML validation completed

## 🚧 In Progress
- [x] Odoo 17 clean install and upgrade smoke test passed in database `ecosphere_runtime_verify`; the module loaded after all dependencies without install errors.
- [x] Static Python compilation and XML parsing passed in the Odoo 17 image.
- [ ] Runtime-verify the remaining acceptance areas: badges, compliance cron/notifications, department scoring, access rules, reports/exports, and menu/UI behavior.

## ⬜ Remaining
- [ ] Exercise the remaining workflows through the browser UI with appropriate manager and ESG-user accounts; the completed runtime checks used the ORM shell against the isolated test database.

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
- SCOPE GAP: Only purchase orders have automatic carbon-transaction generation. Manufacturing, employee expenses, and fleet automatic adapters are not implemented; those source types are available for manual records only.
- ESG department membership is independent from Odoo HR departments and uses one paired relationship: `hr.employee.esg_department_id` (Many2one, canonical stored field) and `esg.department.member_ids` (its inverse One2many field).

## 🔜 Next Step
- Create manager and ESG-user test accounts in `ecosphere_runtime_verify`, then verify access rules, reports/exports, scoring, badges, compliance crons, and the browser UI before increasing the runtime-verified count.
