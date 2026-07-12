from odoo import fields, models


class EsgEmployeeBadge(models.Model):
    _name = 'esg.employee.badge'
    _description = 'Employee ESG Badge'

    employee_id = fields.Many2one('hr.employee', required=True, ondelete='cascade')
    badge_id = fields.Many2one('esg.badge', required=True, ondelete='cascade')
    awarded_date = fields.Date(default=fields.Date.today, required=True)

    _sql_constraints = [('esg_employee_badge_unique', 'unique(employee_id, badge_id)', 'This badge has already been awarded to this employee.')]
