from odoo import api, fields, models
from .esg_tools import send_template_notification, setting_enabled


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    esg_department_id = fields.Many2one('esg.department', string='ESG Department')
    csr_participation_ids = fields.One2many('esg.employee.participation', 'employee_id', string='CSR Participations')
    challenge_participation_ids = fields.One2many('esg.challenge.participation', 'employee_id', string='Challenge Participations')
    reward_redemption_ids = fields.One2many('esg.reward.redemption', 'employee_id', string='Reward Redemptions')
    total_xp = fields.Integer(compute='_compute_esg_points', string='Total ESG XP')
    available_points = fields.Integer(compute='_compute_esg_points', string='Available ESG Points')
    badge_ids = fields.One2many('esg.employee.badge', 'employee_id', string='ESG Badges')

    @api.depends(
        'csr_participation_ids.points_earned',
        'challenge_participation_ids.xp_awarded',
        'challenge_participation_ids.challenge_id.status',
        'reward_redemption_ids.points_deducted',
    )
    def _compute_esg_points(self):
        Challenge = self.env['esg.challenge.participation']
        Csr = self.env['esg.employee.participation']
        Redemption = self.env['esg.reward.redemption']
        for employee in self:
            challenge_xp = sum(Challenge.search([('employee_id', '=', employee.id)]).mapped('xp_awarded'))
            csr_xp = sum(Csr.search([('employee_id', '=', employee.id)]).mapped('points_earned'))
            total = challenge_xp + csr_xp
            redeemed = sum(Redemption.search([('employee_id', '=', employee.id)]).mapped('points_deducted'))
            employee.total_xp = total
            employee.available_points = total - redeemed

    def _check_and_award_badges(self):
        """Evaluate badge rules through a rule-dispatch table and award only missing badges."""
        if not setting_enabled(self.env, 'badge_auto_award', False):
            return
        evaluators = {
            'xp_threshold': lambda employee, badge: employee.total_xp >= badge.unlock_rule_value,
            'challenges_completed': lambda employee, badge: self.env['esg.challenge.participation'].search_count([('employee_id', '=', employee.id), ('challenge_id.status', '=', 'completed'), ('approval', '=', 'approved')]) >= badge.unlock_rule_value,
            'csr_completed': lambda employee, badge: self.env['esg.employee.participation'].search_count([('employee_id', '=', employee.id), ('approval_status', '=', 'approved')]) >= badge.unlock_rule_value,
            # ASSUMPTION: custom badges are manager-awarded by disabling automatic eligibility.
            'custom': lambda employee, badge: False,
        }
        EmployeeBadge = self.env['esg.employee.badge']
        for employee in self:
            for badge in self.env['esg.badge'].search([('active', '=', True)]):
                if evaluators[badge.unlock_rule_type](employee, badge) and not EmployeeBadge.search_count([('employee_id', '=', employee.id), ('badge_id', '=', badge.id)]):
                    award = EmployeeBadge.create({'employee_id': employee.id, 'badge_id': badge.id})
                    send_template_notification(award, 'esg_management.mail_template_esg_badge_unlocked', 'notify_badge_unlocked', employee.work_contact_id)
