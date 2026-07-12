from odoo import api, fields, models
from .esg_tools import send_template_notification, setting_enabled


class EsgComplianceIssue(models.Model):
    _name = 'esg.compliance.issue'
    _description = 'Compliance Issue'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, tracking=True)
    audit_id = fields.Many2one('esg.audit', required=True, ondelete='cascade')
    severity = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('critical', 'Critical')], required=True, tracking=True)
    description = fields.Text()
    owner_id = fields.Many2one('hr.employee', required=True)
    due_date = fields.Date(required=True)
    status = fields.Selection([('open', 'Open'), ('in_progress', 'In Progress'), ('resolved', 'Resolved'), ('closed', 'Closed')], default='open', required=True, tracking=True)
    is_overdue = fields.Boolean(compute='_compute_is_overdue', store=True)

    @api.depends('status', 'due_date')
    def _compute_is_overdue(self):
        today = fields.Date.today()
        for record in self:
            record.is_overdue = bool(record.due_date and record.due_date < today and record.status not in ('resolved', 'closed'))

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            send_template_notification(record, 'esg_management.mail_template_esg_compliance_issue', 'notify_compliance_issue', record.owner_id.work_contact_id)
            if record.owner_id.user_id:
                record.activity_schedule('mail.mail_activity_data_todo', user_id=record.owner_id.user_id.id, summary='Resolve ESG compliance issue', note=record.name)
        return records

    @api.model
    def _cron_check_overdue_compliance_issues(self):
        """Refresh overdue values and make overdue work actionable for its owner."""
        issues = self.search([('due_date', '<', fields.Date.today()), ('status', 'not in', ['resolved', 'closed'])])
        issues._compute_is_overdue()
        for issue in issues:
            if setting_enabled(self.env, 'notify_compliance_issue', True):
                send_template_notification(issue, 'esg_management.mail_template_esg_compliance_issue', 'notify_compliance_issue', issue.owner_id.work_contact_id)
            if issue.owner_id.user_id and setting_enabled(self.env, 'notify_compliance_issue', True):
                issue.activity_schedule('mail.mail_activity_data_todo', user_id=issue.owner_id.user_id.id, summary='Overdue ESG compliance issue', note=issue.name)
