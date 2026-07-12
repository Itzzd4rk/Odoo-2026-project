from odoo import fields, models, _
from odoo.exceptions import ValidationError


class EsgChallenge(models.Model):
    _name = 'esg.challenge'
    _description = 'ESG Challenge'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    title = fields.Char(required=True, tracking=True)
    description = fields.Text()
    category_id = fields.Many2one('esg.category', domain=[('type', '=', 'challenge')])
    xp_value = fields.Integer(required=True, string='XP Value')
    difficulty = fields.Selection([('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='easy')
    evidence_required = fields.Boolean()
    deadline = fields.Date()
    status = fields.Selection([('draft', 'Draft'), ('active', 'Active'), ('under_review', 'Under Review'), ('completed', 'Completed'), ('archived', 'Archived')], default='draft', required=True, tracking=True)
    participation_ids = fields.One2many('esg.challenge.participation', 'challenge_id', string='Participations')

    def action_activate(self):
        """Activate a draft challenge only while its deadline remains in the future."""
        for record in self:
            if record.status != 'draft':
                raise ValidationError(_('Only draft challenges can be activated.'))
            if record.deadline and record.deadline < fields.Date.today():
                raise ValidationError(_('A challenge cannot be activated after its deadline.'))
            record.status = 'active'

    def action_submit_for_review(self):
        """Move an active challenge to review after at least one employee has participated."""
        for record in self:
            if record.status != 'active' or not record.participation_ids:
                raise ValidationError(_('Only an active challenge with participation can be submitted for review.'))
            record.status = 'under_review'

    def action_complete(self):
        """Complete a reviewed challenge; approved participant XP then becomes awardable."""
        for record in self:
            if record.status != 'under_review':
                raise ValidationError(_('Only challenges under review can be completed.'))
            record.status = 'completed'
            for participation in record.participation_ids.filtered(lambda p: p.approval == 'approved'):
                participation.employee_id._check_and_award_badges()

    def action_archive(self):
        """Archive a challenge from any state."""
        self.write({'status': 'archived'})
