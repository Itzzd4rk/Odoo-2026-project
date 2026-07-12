from odoo import fields, models


class EsgAudit(models.Model):
    _name = 'esg.audit'
    _description = 'ESG Audit'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, tracking=True)
    auditor_id = fields.Many2one('hr.employee', string='Internal Auditor')
    external_auditor_id = fields.Many2one('res.partner', string='External Auditor')
    department_id = fields.Many2one('esg.department')
    audit_date = fields.Date()
    scope = fields.Text()
    status = fields.Selection([('planned', 'Planned'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='planned', tracking=True)
    compliance_issue_ids = fields.One2many('esg.compliance.issue', 'audit_id')
