from odoo import fields, models
from odoo.exceptions import ValidationError
from .esg_tools import send_template_notification


class EsgRewardRedemption(models.Model):
    _name = 'esg.reward.redemption'
    _description = 'Reward Redemption'

    employee_id = fields.Many2one('hr.employee', required=True)
    reward_id = fields.Many2one('esg.reward', required=True)
    redemption_date = fields.Datetime(default=fields.Datetime.now, required=True)
    points_deducted = fields.Integer(required=True, readonly=True)

    @classmethod
    def _redeem_for(cls, employee, reward, existing_redemption=None):
        """Lock the reward row, validate balance, then decrement inventory and record the debit atomically."""
        env = employee.env
        with env.cr.savepoint():
            env.cr.execute('SELECT id FROM esg_reward WHERE id = %s FOR UPDATE', [reward.id])
            reward.invalidate_recordset()
            if reward.stock <= 0:
                raise ValidationError('This reward is out of stock.')
            if employee.available_points < reward.points_required:
                raise ValidationError('The employee does not have enough available ESG points.')
            reward.write({'stock': reward.stock - 1})
            redemption = existing_redemption or env['esg.reward.redemption'].create({'employee_id': employee.id, 'reward_id': reward.id, 'points_deducted': reward.points_required})
            if existing_redemption:
                redemption.write({'points_deducted': reward.points_required})
        send_template_notification(redemption, 'esg_management.mail_template_esg_reward_redemption', 'notify_reward_redemption', employee.work_contact_id)
        return redemption

    def action_redeem(self):
        for record in self:
            if record.points_deducted:
                raise ValidationError('This reward redemption has already been processed.')
            self._redeem_for(record.employee_id, record.reward_id, record)
