from datetime import timedelta

from odoo import fields
from odoo.exceptions import AccessError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestEsgRuntimeVerification(TransactionCase):
    """Regression coverage for the ESG workflows previously checked manually."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.department = cls.env['esg.department'].create({
            'name': 'Runtime Verification',
            'code': 'RUNTIME',
        })
        cls.user_group = cls.env.ref('esg_management.group_esg_user')
        cls.manager_group = cls.env.ref('esg_management.group_esg_manager')
        cls.employee, cls.esg_user = cls._create_employee_and_user(
            'ESG User', 'esg.user.runtime@example.com', [cls.user_group.id]
        )
        cls.other_employee, _other_user = cls._create_employee_and_user(
            'Other ESG User', 'esg.other.runtime@example.com', [cls.user_group.id]
        )
        cls.manager_employee, cls.esg_manager = cls._create_employee_and_user(
            'ESG Manager', 'esg.manager.runtime@example.com', [cls.manager_group.id]
        )
        cls.csr_activity = cls.env['esg.csr.activity'].create({
            'name': 'Runtime CSR Activity',
            'department_id': cls.department.id,
            'date': fields.Date.today(),
            'status': 'completed',
        })

    @classmethod
    def _create_employee_and_user(cls, name, login, group_ids):
        user = cls.env['res.users'].with_context(no_reset_password=True).create({
            'name': name,
            'login': login,
            'email': login,
            'groups_id': [(6, 0, [cls.env.ref('base.group_user').id, *group_ids])],
        })
        employee = cls.env['hr.employee'].create({
            'name': name,
            'user_id': user.id,
            'work_email': login,
            'esg_department_id': cls.department.id,
        })
        return employee, user

    def _set_parameter(self, key, value):
        self.env['ir.config_parameter'].sudo().set_param(
            'esg_management.%s' % key, str(value)
        )

    def test_badge_auto_award_is_event_driven_and_idempotent(self):
        self._set_parameter('badge_auto_award', True)
        self._set_parameter('notify_badge_unlocked', False)
        badge = self.env['esg.badge'].create({
            'name': 'First Steps',
            'unlock_rule_type': 'xp_threshold',
            'unlock_rule_value': 10,
        })
        participation = self.env['esg.employee.participation'].create({
            'employee_id': self.employee.id,
            'activity_id': self.csr_activity.id,
            'completion_date': fields.Date.today(),
        })

        participation.write({'approval_status': 'approved'})
        awards = self.env['esg.employee.badge'].search([
            ('employee_id', '=', self.employee.id),
            ('badge_id', '=', badge.id),
        ])
        self.assertEqual(len(awards), 1)

        self.employee._check_and_award_badges()
        self.assertEqual(self.env['esg.employee.badge'].search_count([
            ('employee_id', '=', self.employee.id),
            ('badge_id', '=', badge.id),
        ]), 1)

    def test_compliance_cron_marks_overdue_issues_and_schedules_follow_up(self):
        self._set_parameter('notify_compliance_issue', True)
        audit = self.env['esg.audit'].create({
            'name': 'Runtime Audit',
            'department_id': self.department.id,
            'audit_date': fields.Date.today(),
        })
        issue = self.env['esg.compliance.issue'].create({
            'name': 'Overdue runtime issue',
            'audit_id': audit.id,
            'owner_id': self.employee.id,
            'severity': 'high',
            'due_date': fields.Date.today() - timedelta(days=1),
        })
        self.assertTrue(issue.is_overdue)
        activity_domain = [
            ('res_model', '=', 'esg.compliance.issue'),
            ('res_id', '=', issue.id),
        ]
        self.assertEqual(self.env['mail.activity'].search_count(activity_domain), 1)

        self.env['esg.compliance.issue']._cron_check_overdue_compliance_issues()
        issue.invalidate_recordset(['is_overdue'])
        self.assertTrue(issue.is_overdue)
        self.assertEqual(self.env['mail.activity'].search_count(activity_domain), 2)

    def test_department_score_and_snapshot_cron_apply_configured_weights(self):
        self._set_parameter('weight_environmental', 40)
        self._set_parameter('weight_social', 30)
        self._set_parameter('weight_governance', 30)
        self._set_parameter('notify_compliance_issue', False)
        factor = self.env['esg.emission.factor'].create({
            'name': 'Runtime factor',
            'activity_type': 'purchase',
            'factor_value': 2,
        })
        self.env['esg.carbon.transaction'].create({
            'source_type': 'purchase',
            'department_id': self.department.id,
            'emission_factor_id': factor.id,
            'quantity': 10,
            'transaction_date': fields.Date.today(),
            'state': 'confirmed',
        })
        activity = self.env['esg.csr.activity'].create({
            'name': 'Scoring CSR activity',
            'department_id': self.department.id,
            'date': fields.Date.today(),
            'status': 'completed',
        })
        self.env['esg.employee.participation'].create({
            'employee_id': self.employee.id,
            'activity_id': activity.id,
            'approval_status': 'approved',
            'completion_date': fields.Date.today(),
        })
        audit = self.env['esg.audit'].create({
            'name': 'Scoring audit',
            'department_id': self.department.id,
        })
        self.env['esg.compliance.issue'].create({
            'name': 'Open scoring issue',
            'audit_id': audit.id,
            'owner_id': self.employee.id,
            'severity': 'medium',
            'due_date': fields.Date.today(),
        })

        score = self.env['esg.department.score'].create({
            'department_id': self.department.id,
            'period_start': fields.Date.today(),
            'period_end': fields.Date.today(),
        })
        self.assertAlmostEqual(score.environmental_score, 80.0)
        self.assertAlmostEqual(score.social_score, 10.0)
        self.assertAlmostEqual(score.governance_score, 90.0)
        self.assertAlmostEqual(score.total_score, 62.0)

        self.env['esg.department.score']._cron_snapshot_scores()
        self.assertEqual(self.env['esg.department.score'].search_count([
            ('department_id', '=', self.department.id),
            ('period_start', '=', fields.Date.today().replace(day=1)),
            ('period_end', '=', fields.Date.today()),
        ]), 1)

    def test_esg_user_record_rules_and_manager_access(self):
        own_participation = self.env['esg.employee.participation'].with_user(self.esg_user).create({
            'employee_id': self.employee.id,
            'activity_id': self.csr_activity.id,
            'completion_date': fields.Date.today(),
        })
        other_participation = self.env['esg.employee.participation'].create({
            'employee_id': self.other_employee.id,
            'activity_id': self.csr_activity.id,
            'completion_date': fields.Date.today(),
        })

        visible_to_user = self.env['esg.employee.participation'].with_user(self.esg_user).search([])
        self.assertEqual(visible_to_user, own_participation)
        self.assertIn(other_participation.id, self.env['esg.employee.participation'].with_user(self.esg_manager).search([]).ids)
        restricted_activity = self.env['esg.csr.activity'].create({
            'name': 'Restricted CSR Activity',
            'department_id': self.department.id,
        })
        with self.assertRaises(AccessError):
            self.env['esg.employee.participation'].with_user(self.esg_user).create({
                'employee_id': self.other_employee.id,
                'activity_id': restricted_activity.id,
            })

    def test_reports_export_actions_and_menu_actions_are_loaded(self):
        score = self.env['esg.department.score'].create({
            'department_id': self.department.id,
            'period_start': fields.Date.today(),
            'period_end': fields.Date.today(),
        })
        static_reports = {
            'esg_management.action_report_environmental': b'Environmental Report',
            'esg_management.action_report_social': b'Social Report',
            'esg_management.action_report_governance': b'Governance Report',
            'esg_management.action_report_summary': b'ESG Summary Report',
        }
        for xmlid, expected_heading in static_reports.items():
            html, _content_type = self.env['ir.actions.report']._render_qweb_html(xmlid, score.ids)
            self.assertIn(expected_heading, html)

        wizard = self.env['esg.report.builder.wizard'].create({'module': 'all'})
        self.assertEqual(len(wizard._build_report_data()['rows']), 4)
        self.assertIn('/xlsx', wizard.action_export_excel()['url'])
        self.assertIn('/csv', wizard.action_export_csv()['url'])
        pdf_action = wizard.action_export_pdf()
        if pdf_action['type'] == 'ir.actions.act_window':
            pdf_action = pdf_action['context']['report_action']
        self.assertEqual(pdf_action['type'], 'ir.actions.report', pdf_action)
        custom_html, _content_type = self.env['ir.actions.report']._render_qweb_html(
            'esg_management.report_custom_esg', wizard.ids
        )
        self.assertIn(b'Custom ESG Report', custom_html)

        root_menu = self.env.ref('esg_management.menu_esg_root')
        self.assertTrue(root_menu.groups_id & self.user_group)
        menu_model = self.env['ir.ui.menu']
        user_visible_menus = menu_model.with_user(self.esg_user)._visible_menu_ids()
        manager_visible_menus = menu_model.with_user(self.esg_manager)._visible_menu_ids()
        self.assertIn(root_menu.id, user_visible_menus)
        for xmlid in (
            'esg_management.menu_esg_reports',
            'esg_management.menu_esg_settings',
            'esg_management.menu_esg_master_data',
        ):
            menu_id = self.env.ref(xmlid).id
            self.assertNotIn(menu_id, user_visible_menus)
            self.assertIn(menu_id, manager_visible_menus)
        action_menus = self.env['ir.ui.menu'].with_user(self.esg_manager).search([
            ('id', 'child_of', root_menu.id),
            ('action', '!=', False),
        ])
        self.assertTrue(action_menus)
        self.assertTrue(all(menu.action.exists() for menu in action_menus))
