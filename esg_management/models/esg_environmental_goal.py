from odoo import api, fields, models


class EsgEnvironmentalGoal(models.Model):
    _name = 'esg.environmental.goal'
    _description = 'Environmental Goal'

    name = fields.Char(required=True)
    department_id = fields.Many2one('esg.department')
    target_metric = fields.Selection([('total_emissions', 'Total Emissions'), ('emission_intensity', 'Emission Intensity'), ('custom', 'Custom')], default='total_emissions', required=True)
    target_value = fields.Float()
    current_value = fields.Float(compute='_compute_current_value')
    start_date = fields.Date()
    end_date = fields.Date()
    status = fields.Selection([('draft', 'Draft'), ('active', 'Active'), ('achieved', 'Achieved'), ('missed', 'Missed')], default='draft', required=True)

    @api.depends('department_id', 'start_date', 'end_date', 'target_metric')
    def _compute_current_value(self):
        Carbon = self.env['esg.carbon.transaction']
        for record in self:
            domain = [('state', '=', 'confirmed')]
            if record.department_id:
                domain.append(('department_id', '=', record.department_id.id))
            if record.start_date:
                domain.append(('transaction_date', '>=', record.start_date))
            if record.end_date:
                domain.append(('transaction_date', '<=', record.end_date))
            emissions = sum(Carbon.search(domain).mapped('calculated_emissions'))
            record.current_value = emissions

    @api.model
    def _cron_evaluate_goals(self):
        """Close active goals after their period using a lower-is-better emissions target."""
        today = fields.Date.today()
        for goal in self.search([('status', '=', 'active'), ('end_date', '<=', today)]):
            goal.status = 'achieved' if goal.current_value <= goal.target_value else 'missed'
