# EcoSphere ESG Management Platform

EcoSphere is an installable **Odoo 17 Community** add-on that gives organisations one place to measure environmental impact, run CSR programmes, manage governance work, and reward employee participation.

The project was created for the Odoo 2026 Hackathon and is packaged as the `esg_management` module.

## What it solves

Most ESG work is split between spreadsheets, email approvals, procurement records, and isolated HR initiatives. EcoSphere brings those activities into Odoo so managers can trace emissions, track targets, audit compliance, publish policies, recognise employee contribution, and export a consistent ESG story.

| ESG pillar | What EcoSphere manages |
| --- | --- |
| Environmental | Emission factors, product profiles, carbon transactions, targets, and department score snapshots |
| Social | CSR activities, participation evidence, employee points, challenges, badges, rewards, and a leaderboard |
| Governance | Policies and acknowledgements, audits, compliance issues, ownership, due dates, and overdue follow-up |

## Key capabilities

- Tracks manually entered and purchase-order-generated carbon transactions.
- Keeps historical emission factors active for traceability rather than deleting them.
- Calculates departmental environmental, social, governance, and weighted total score snapshots each night.
- Supports ESG policies with department targeting, acknowledgement tracking, and weekly reminders.
- Provides guarded CSR and challenge approval flows, including configurable evidence requirements.
- Awards XP, badges, and rewards through configurable, idempotent gamification rules.
- Manages compliance issues with owners, deadlines, activities, overdue checks, templates, and email notifications.
- Includes a dashboard, challenge kanban, reports, a filterable report builder, PDF output, XLSX export, and CSV export.
- Implements ESG User and ESG Manager access groups with own-participation record rules.

## Module layout

```text
.
├── README.md                         # This GitHub guide
└── esg_management/
    ├── __manifest__.py               # Odoo metadata and data/assets loading order
    ├── models/                       # ESG business rules and Odoo models
    ├── wizard/                       # Custom report builder and export actions
    ├── controllers/                  # XLSX and CSV report-download endpoints
    ├── views/                        # Forms, lists, kanban, settings, dashboard menus
    ├── reports/                      # QWeb PDF reports and report actions
    ├── data/                         # Sequence, scheduled jobs, and mail templates
    ├── security/                     # Groups, access-control matrix, and record rules
    ├── static/                       # Dashboard client assets and module icon
    └── PROGRESS.md                   # Delivery status, assumptions, and roadmap
```

## Requirements

- Odoo 17 Community Edition
- Python 3.10 or newer
- PostgreSQL supported by the Odoo 17 installation
- Odoo dependencies: `base`, `mail`, `hr`, `purchase`, `stock`, and `account`
- `xlsxwriter` available in the Odoo Python environment for Excel exports

## Installation

1. Clone this repository into, or add it to, an Odoo addons directory.

   ```bash
   git clone <your-repository-url>
   ```

2. Add the repository path to Odoo's `addons_path` configuration. The add-on directory that Odoo must discover is:

   ```text
   Odoo-2026-project/esg_management
   ```

3. Restart Odoo and update the Apps list.

4. Search for **EcoSphere ESG Management** and install it.

   Command-line upgrade example:

   ```bash
   ./odoo-bin -d <database_name> -u esg_management --stop-after-init
   ```

5. Assign users one of the ESG security roles under **Settings → Users & Companies → Users**:

   - **ESG User**: can view ESG information and submit/manage only their own CSR and challenge participation.
   - **ESG Manager**: full ESG management, approvals, settings, score data, and report builder access.

## First-time configuration

Open **ESG → Settings** and configure:

| Setting | Why it matters |
| --- | --- |
| Auto Emission Calculation | Creates confirmed carbon transactions from purchase-order lines that have a product sustainability profile and emission factor. |
| Evidence Requirement | Prevents CSR approvals without uploaded proof. Challenges can additionally require evidence per challenge. |
| Badge Auto-Award | Evaluates XP, completed-challenge, and CSR-completion badge thresholds after participation updates. |
| Environmental / Social / Governance weights | Sets the percentage weighting used for the total department ESG score. The values must sum to 100. |
| Notification switches | Enables or disables compliance, approval, policy-reminder, badge, and reward-redemption messages. |

Then create the foundational records:

1. ESG Departments and department members.
2. CSR and Challenge categories.
3. Emission factors.
4. Product Sustainability Profiles linked to relevant products.
5. Policies, badges, rewards, and environmental goals as needed.

## Everyday workflows

### Carbon accounting

1. Create emission factors for purchase, manufacturing, expense, or fleet activities.
2. Add a Product Sustainability Profile and default factor for products that should create emissions automatically.
3. Enable **Auto Emission Calculation**.
4. Confirm a purchase order. EcoSphere creates confirmed carbon transactions for qualifying lines.
5. Review manually entered or automatic transactions under **ESG → Environmental → Carbon Transactions**.

### CSR activities

1. A manager creates a CSR activity and selects a CSR category and department.
2. Employees submit participation with proof where required.
3. A manager approves or rejects the participation.
4. Approval awards points, updates the employee balance, evaluates badges, and sends the configured notification.

### Challenges and rewards

1. Create a challenge, set XP, deadline, difficulty, and evidence rule.
2. Progress it through **Draft → Active → Under Review → Completed**, or archive it from any state.
3. Approve employee challenge participation.
4. Completion makes approved challenge XP available and can unlock badges.
5. Employees redeem rewards when their available points balance is sufficient and stock remains. Reward stock and point deduction are protected in one database transaction.

### Governance and compliance

1. Publish a policy to generate acknowledgement records for its target departments or the whole organisation.
2. Employees acknowledge policies; the weekly job reminds remaining pending acknowledgements.
3. Create audits and compliance issues, assigning every issue to an owner with a due date.
4. The daily job marks unresolved past-due issues as overdue and raises an actionable activity for the owner when notifications are enabled.

## Navigation

The top-level **ESG** application is organised into six functional areas:

- **Dashboard** — overall/pillar score KPIs, top five contributors, open issue count.
- **Environmental** — carbon transactions, factors, profiles, and goals.
- **Social** — CSR activities and participation.
- **Governance** — policies, acknowledgements, audits, issues, and department scores.
- **Gamification** — challenge kanban, participation, leaderboard, badges, rewards, and redemptions.
- **Reports** — custom report builder for managers.

Managers also receive **Master Data** and **Settings** menus.

## Reporting

The Department Scores screen provides four QWeb PDF reports:

1. Environmental Report
2. Social Report
3. Governance Report
4. ESG Summary Report

The **Custom Report Builder** accepts department, date, ESG module, employee, challenge, and category filters. It generates PDF, Excel, and CSV output from one shared query-building method so the same filters are applied consistently across formats.

## Scheduled jobs

| Schedule | Job |
| --- | --- |
| Daily | Check overdue compliance issues and create owner activities/notifications. |
| Daily | Evaluate environmental goals whose period ended. |
| Daily | Snapshot each active department's ESG score. |
| Weekly | Send policy-acknowledgement reminders. |

## Security model

EcoSphere defines two groups in `security/esg_security.xml`:

- `group_esg_user`
- `group_esg_manager`

Access rights for each ESG model are declared in `security/ir.model.access.csv`. Additional record rules ensure ESG Users can only view or edit their own CSR and challenge participation records; ESG Managers have unrestricted access to those records.

## Design and implementation notes

- The dashboard is an OWL client action styled as an understated field-notebook interface: forest green, warm paper, and ochre accents.
- Editable notification wording lives in `data/esg_mail_template_data.xml`; business logic does not hardcode notification copy.
- The leaderboard is a read-only SQL view, ranked by employee XP.
- Department score records are snapshots rather than live dashboard calculations, preserving historical trends and dashboard performance.
- Emission factors are archived (`active = False`) on deletion attempts to preserve historical calculations.

## Known limitations and design notes

- **Scope gap:** automatic carbon-transaction generation is implemented only for purchase orders. Manufacturing, employee expenses, and fleet remain valid source types for manually entered records, but their native automatic adapters are not built.
- ESG department membership is intentionally independent from Odoo HR departments. The canonical stored field is `hr.employee.esg_department_id`; `esg.department.member_ids` is its inverse One2many field for department-side management.
- A clean Odoo 17 Community install and regression suite have passed. The suite verifies badges, compliance crons and activities, score snapshots, access rules, QWeb reports/export actions, and permission-aware menu visibility. An authenticated browser check for visual layout and actual XLSX/CSV downloads has been verified successfully.

## Development status and roadmap

See [the module progress tracker](esg_management/PROGRESS.md) for implementation status, limitations, validation status, and the prioritized improvement backlog.

## License

This project is distributed under the repository's [GPL-3.0 license](LICENSE).
