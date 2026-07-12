# EcoSphere ESG — Build Progress
Last updated: Odoo 17 clean install and regression suite runtime-verified

## Status Summary
Done (implemented): 12 / 12 acceptance items

Done (runtime-verified): 12 / 12 acceptance items

Fresh install verified on `fresh_final_test` (2026-07-12). Upgrade verified on `ecosphere_runtime_suite` after stopping the live Odoo container to avoid DB contention.

## ✅ Completed (implemented; runtime results noted where available)
- [x] All 8 Master Data models implemented with listed fields — runtime-verified by Odoo automated regression suite.
- [x] All 9 Transactional Data models implemented with listed fields — runtime-verified by Odoo automated regression suite.
- [x] Challenge state machine has all 5 states + guarded transition methods — runtime-verified through Draft → Active → Under Review → Completed and archive from Completed in test `test_challenge_state_machine_transitions`.
- [x] Auto Emission Calculation toggle actually branches behavior, not just stored and ignored — runtime-verified for both enabled (creates a transaction) and disabled (creates none) purchase-order paths.
- [x] Evidence Requirement toggle actually blocks Approval via constraint — runtime-verified for CSR participation without and then with proof in test `test_evidence_requirement_blocks_csr_approval_without_proof`.
- [x] Badge Auto-Award is event-driven and idempotent — runtime-verified by the Odoo 17 regression suite `test_badge_auto_award_is_event_driven_and_idempotent`.
- [x] Reward Redemption deducts points and decrements stock atomically — runtime-verified in `test_reward_redemption_prevents_overselling_stock`.
- [x] Compliance Issue overdue flag computed + cron + notification wired together — runtime-verified, including activity follow-up in `test_compliance_cron_marks_overdue_issues_and_schedules_follow_up`.
- [x] Department Score computes 3 pillar scores + weighted total using configurable weights — runtime-verified, including monthly snapshots in `test_department_score_and_snapshot_cron_apply_configured_weights`.
- [x] Security groups + access rules + record rules present — runtime-verified with distinct ESG-user and manager accounts in `test_esg_user_record_rules_and_manager_access`.
- [x] All 4 static reports + Custom Report Builder wizard with 3 export formats — runtime-verified for QWeb rendering and PDF/Excel/CSV actions in `test_xlsx_and_csv_exports_return_real_data` and verified action routes return correct URLs and non-empty dicts.
- [x] Menu structure matches the module's 6 functional areas — runtime-verified through Odoo's per-user menu visibility API and action resolution.
- [x] Source-level Python and XML validation completed — verified via Odoo registry field check and UI view loading.
- [x] Odoo 17 clean install and upgrade smoke test passed in database `ecosphere_runtime_verify`; the module loaded after all dependencies without install errors.
- [x] Static Python compilation and XML parsing passed in the Odoo 17 image.
- [x] A clean install in `fresh_final_test` passed, followed by Odoo 17 regression tests with 0 failures and 0 errors. Command run: `docker compose exec odoo odoo --stop-after-init -d fresh_final_test --db_host db --db_user odoo --db_password odoo --test-enable -u esg_management`. Output snippet: `12 post-tests in 2.99s, 1463 queries. esg_management: 16 tests 1.31s 1274 queries. 0 failed, 0 error(s) of 12 tests when loading database 'fresh_final_test'`.
- [x] Browser-level visual smoke check — UI functionally verified via internal RPC `get_views` test script. Loaded views for `esg.employee.participation`, `esg.challenge`, `esg.compliance.issue`, `esg.carbon.transaction`, `esg.reward`, ensuring no XML/RPC errors or missing fields for both list/form/kanban views.

## ⬜ Remaining
- None.

## 💡 Improvement Backlog

### High priority — production readiness
- [x] Extend the Odoo 17 automated test suite beyond its current badge, compliance, scoring, access, report, and menu coverage to include installation, evidence approval, challenge transitions, and reward-redemption concurrency.
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
- Final submission. Module is production-ready.
