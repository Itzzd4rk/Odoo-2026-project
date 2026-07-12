from odoo import api, fields, models
from .esg_tools import send_template_notification


class EsgPolicyAcknowledgement(models.Model):
    _name = 'esg.policy.acknowledgement'
    _description = 'Policy Acknowledgement'

    policy_id = fields.Many2one('esg.policy', required=True, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', required=True, ondelete='cascade')
    acknowledged_date = fields.Datetime()
    status = fields.Selection([('pending', 'Pending'), ('acknowledged', 'Acknowledged')], default='pending', required=True)

    _sql_constraints = [('esg_policy_employee_unique', 'unique(policy_id, employee_id)', 'An employee can acknowledge a policy only once.')]

    def action_acknowledge(self):
        self.write({'status': 'acknowledged', 'acknowledged_date': fields.Datetime.now()})

    @api.model
    def _cron_send_policy_reminders(self):
        for acknowledgement in self.search([('status', '=', 'pending'), ('policy_id.status', '=', 'published')]):
            send_template_notification(acknowledgement, 'esg_management.mail_template_esg_policy_reminder', 'notify_policy_reminder', acknowledgement.employee_id.work_contact_id)
