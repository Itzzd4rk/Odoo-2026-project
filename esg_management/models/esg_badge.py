from odoo import fields, models


class EsgBadge(models.Model):
    _name = 'esg.badge'
    _description = 'ESG Badge'

    name = fields.Char(required=True)
    description = fields.Text()
    icon = fields.Image()
    unlock_rule_type = fields.Selection([('xp_threshold', 'XP Threshold'), ('challenges_completed', 'Challenges Completed'), ('csr_completed', 'CSR Activities Completed'), ('custom', 'Custom')], required=True, default='xp_threshold')
    unlock_rule_value = fields.Integer(default=0)
    active = fields.Boolean(default=True)
