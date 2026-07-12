from odoo import api, fields, models


class EsgPolicy(models.Model):
    _name = 'esg.policy'
    _description = 'ESG Policy'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, tracking=True)
    description = fields.Text()
    version = fields.Char()
    department_ids = fields.Many2many('esg.department', string='Target Departments')
    document = fields.Binary(attachment=True)
    status = fields.Selection([('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')], default='draft', tracking=True)
    acknowledgement_ids = fields.One2many('esg.policy.acknowledgement', 'policy_id', string='Acknowledgements')
    acknowledgement_rate = fields.Float(compute='_compute_acknowledgement_rate', string='Acknowledgement Rate (%)')

    @api.depends('acknowledgement_ids.status', 'department_ids')
    def _compute_acknowledgement_rate(self):
        Employee = self.env['hr.employee']
        for policy in self:
            employees = Employee.search([('esg_department_id', 'in', policy.department_ids.ids)]) if policy.department_ids else Employee.search([])
            acknowledged = len(policy.acknowledgement_ids.filtered(lambda a: a.status == 'acknowledged'))
            policy.acknowledgement_rate = (acknowledged / len(employees) * 100.0) if employees else 0.0

    def action_publish(self):
        for policy in self:
            policy.status = 'published'
            employees = self.env['hr.employee'].search([('esg_department_id', 'in', policy.department_ids.ids)]) if policy.department_ids else self.env['hr.employee'].search([])
            existing = set(policy.acknowledgement_ids.mapped('employee_id').ids)
            self.env['esg.policy.acknowledgement'].create([{'policy_id': policy.id, 'employee_id': employee.id} for employee in employees if employee.id not in existing])
