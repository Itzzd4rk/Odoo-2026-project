from odoo import api, fields, models
from odoo.exceptions import ValidationError
from .esg_tools import send_template_notification, setting_enabled


class EsgEmployeeParticipation(models.Model):
    _name = 'esg.employee.participation'
    _description = 'CSR Employee Participation'

    employee_id = fields.Many2one('hr.employee', required=True, ondelete='cascade')
    activity_id = fields.Many2one('esg.csr.activity', required=True, ondelete='cascade')
    proof = fields.Binary(attachment=True)
    approval_status = fields.Selection([('submitted', 'Submitted'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='submitted', required=True)
    points_earned = fields.Integer(compute='_compute_points_earned', store=True)
    completion_date = fields.Date()

    _sql_constraints = [('esg_csr_participation_unique', 'unique(employee_id, activity_id)', 'An employee can participate in an activity only once.')]

    @api.depends('approval_status')
    def _compute_points_earned(self):
        for record in self:
            # ASSUMPTION: each approved CSR participation earns ten points.
            record.points_earned = 10 if record.approval_status == 'approved' else 0

    @api.constrains('approval_status', 'proof')
    def _check_evidence_before_approval(self):
        if setting_enabled(self.env, 'evidence_required', False):
            for record in self:
                if record.approval_status == 'approved' and not record.proof:
                    raise ValidationError('Evidence is required before approving this CSR participation.')

    def write(self, vals):
        previous = {record.id: record.approval_status for record in self}
        result = super().write(vals)
        for record in self:
            if 'approval_status' in vals and previous[record.id] != record.approval_status:
                send_template_notification(record, 'esg_management.mail_template_esg_csr_decision', 'notify_approval_decision', record.employee_id.work_contact_id)
                record.employee_id._check_and_award_badges()
        return result
