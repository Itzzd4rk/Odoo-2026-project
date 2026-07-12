from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EsgConfigSettings(models.TransientModel):
    _name = 'esg.config.settings'
    _inherit = 'res.config.settings'
    _description = 'ESG Settings'

    esg_auto_emission_calc = fields.Boolean(config_parameter='esg_management.auto_emission_calc')
    esg_evidence_required = fields.Boolean(config_parameter='esg_management.evidence_required')
    esg_badge_auto_award = fields.Boolean(config_parameter='esg_management.badge_auto_award')
    esg_weight_environmental = fields.Float(default=40, config_parameter='esg_management.weight_environmental')
    esg_weight_social = fields.Float(default=30, config_parameter='esg_management.weight_social')
    esg_weight_governance = fields.Float(default=30, config_parameter='esg_management.weight_governance')
    esg_notify_compliance_issue = fields.Boolean(default=True, config_parameter='esg_management.notify_compliance_issue')
    esg_notify_approval_decision = fields.Boolean(default=True, config_parameter='esg_management.notify_approval_decision')
    esg_notify_policy_reminder = fields.Boolean(default=True, config_parameter='esg_management.notify_policy_reminder')
    esg_notify_badge_unlocked = fields.Boolean(default=True, config_parameter='esg_management.notify_badge_unlocked')
    esg_notify_reward_redemption = fields.Boolean(default=True, config_parameter='esg_management.notify_reward_redemption')

    @api.constrains('esg_weight_environmental', 'esg_weight_social', 'esg_weight_governance')
    def _check_weights(self):
        for record in self:
            if round(record.esg_weight_environmental + record.esg_weight_social + record.esg_weight_governance, 6) != 100:
                raise ValidationError('Environmental, social, and governance weights must total 100.')
