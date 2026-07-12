from odoo import api, fields, models
from odoo.exceptions import ValidationError
from .esg_tools import send_template_notification


class EsgChallengeParticipation(models.Model):
    _name = 'esg.challenge.participation'
    _description = 'Challenge Participation'

    challenge_id = fields.Many2one('esg.challenge', required=True, ondelete='cascade')
    employee_id = fields.Many2one('hr.employee', required=True, ondelete='cascade')
    progress = fields.Float(default=0.0)
    proof = fields.Binary(attachment=True)
    approval = fields.Selection([('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', required=True)
    xp_awarded = fields.Integer(compute='_compute_xp_awarded', store=True)

    _sql_constraints = [
        ('esg_challenge_employee_unique', 'unique(challenge_id, employee_id)', 'An employee can join a challenge only once.'),
        ('esg_challenge_progress_range', 'CHECK(progress >= 0 AND progress <= 100)', 'Progress must be between 0 and 100.'),
    ]

    @api.depends('approval', 'challenge_id.status', 'challenge_id.xp_value')
    def _compute_xp_awarded(self):
        for record in self:
            record.xp_awarded = record.challenge_id.xp_value if record.approval == 'approved' and record.challenge_id.status == 'completed' else 0

    @api.constrains('approval', 'proof', 'challenge_id')
    def _check_challenge_evidence_before_approval(self):
        """Respect a challenge's own evidence requirement before approving participation."""
        for record in self:
            if record.approval == 'approved' and record.challenge_id.evidence_required and not record.proof:
                raise ValidationError('Evidence is required before approving this challenge participation.')

    def write(self, vals):
        previous = {record.id: record.approval for record in self}
        result = super().write(vals)
        for record in self:
            if 'approval' in vals and previous[record.id] != record.approval:
                send_template_notification(record, 'esg_management.mail_template_esg_challenge_decision', 'notify_approval_decision', record.employee_id.work_contact_id)
            if set(vals) & {'approval', 'progress'}:
                record.employee_id._check_and_award_badges()
        return result
