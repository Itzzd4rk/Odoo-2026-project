from odoo import fields, models


class EsgReportBuilderWizard(models.TransientModel):
    _name = 'esg.report.builder.wizard'
    _description = 'ESG Custom Report Builder'

    department_ids = fields.Many2many('esg.department')
    date_from = fields.Date()
    date_to = fields.Date()
    module = fields.Selection([('environmental', 'Environmental'), ('social', 'Social'), ('governance', 'Governance'), ('gamification', 'Gamification'), ('all', 'All')], default='all', required=True)
    employee_ids = fields.Many2many('hr.employee')
    challenge_ids = fields.Many2many('esg.challenge')
    esg_category_ids = fields.Many2many('esg.category')

    def _build_report_data(self):
        """Build all export payloads from one consistently filtered metric query."""
        self.ensure_one()
        departments = self.department_ids or self.env['esg.department'].search([])
        date_domain = []
        if self.date_from:
            date_domain.append(('transaction_date', '>=', self.date_from))
        if self.date_to:
            date_domain.append(('transaction_date', '<=', self.date_to))
        carbon = self.env['esg.carbon.transaction'].search([('department_id', 'in', departments.ids), ('state', '=', 'confirmed')] + date_domain)
        csr_domain = [('activity_id.department_id', 'in', departments.ids), ('approval_status', '=', 'approved')]
        if self.date_from:
            csr_domain.append(('completion_date', '>=', self.date_from))
        if self.date_to:
            csr_domain.append(('completion_date', '<=', self.date_to))
        if self.employee_ids:
            csr_domain.append(('employee_id', 'in', self.employee_ids.ids))
        if self.esg_category_ids:
            csr_domain.append(('activity_id.category_id', 'in', self.esg_category_ids.ids))
        csr = self.env['esg.employee.participation'].search(csr_domain)
        challenge_domain = [('approval', '=', 'approved'), ('challenge_id.status', '=', 'completed')]
        if self.date_from:
            challenge_domain.append(('challenge_id.deadline', '>=', self.date_from))
        if self.date_to:
            challenge_domain.append(('challenge_id.deadline', '<=', self.date_to))
        if self.employee_ids:
            challenge_domain.append(('employee_id', 'in', self.employee_ids.ids))
        if self.challenge_ids:
            challenge_domain.append(('challenge_id', 'in', self.challenge_ids.ids))
        if self.esg_category_ids:
            challenge_domain.append(('challenge_id.category_id', 'in', self.esg_category_ids.ids))
        challenges = self.env['esg.challenge.participation'].search(challenge_domain)
        issues = self.env['esg.compliance.issue'].search([('audit_id.department_id', 'in', departments.ids)])
        rows = []
        if self.module in ('environmental', 'all'):
            rows.append({'pillar': 'Environmental', 'metric': 'Confirmed emissions (kg CO2e)', 'value': sum(carbon.mapped('calculated_emissions'))})
        if self.module in ('social', 'all'):
            rows.append({'pillar': 'Social', 'metric': 'Approved CSR participations', 'value': len(csr)})
        if self.module in ('governance', 'all'):
            rows.append({'pillar': 'Governance', 'metric': 'Open compliance issues', 'value': len(issues.filtered(lambda i: i.status not in ('resolved', 'closed')))})
        if self.module in ('gamification', 'all'):
            rows.append({'pillar': 'Gamification', 'metric': 'Challenge XP awarded', 'value': sum(challenges.mapped('xp_awarded'))})
        return {'wizard': self, 'rows': rows, 'title': 'Custom ESG Report'}

    def action_export_pdf(self):
        return self.env.ref('esg_management.action_report_custom_esg').report_action(self)

    def action_export_excel(self):
        return {'type': 'ir.actions.act_url', 'url': '/esg/report/%s/xlsx' % self.id, 'target': 'self'}

    def action_export_csv(self):
        return {'type': 'ir.actions.act_url', 'url': '/esg/report/%s/csv' % self.id, 'target': 'self'}
