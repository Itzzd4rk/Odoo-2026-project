from odoo import api, fields, models


class EsgDepartmentScore(models.Model):
    _name = 'esg.department.score'
    _description = 'Department ESG Score Snapshot'
    _order = 'period_end desc, department_id'

    department_id = fields.Many2one('esg.department', required=True, ondelete='cascade')
    period_start = fields.Date(required=True)
    period_end = fields.Date(required=True)
    environmental_score = fields.Float(compute='_compute_scores', store=True)
    social_score = fields.Float(compute='_compute_scores', store=True)
    governance_score = fields.Float(compute='_compute_scores', store=True)
    total_score = fields.Float(compute='_compute_scores', store=True)

    _sql_constraints = [('esg_score_period_unique', 'unique(department_id, period_start, period_end)', 'A department score already exists for this period.')]

    @api.depends('department_id', 'period_start', 'period_end')
    def _compute_scores(self):
        params = self.env['ir.config_parameter'].sudo()
        weights = [float(params.get_param('esg_management.weight_environmental', 40)), float(params.get_param('esg_management.weight_social', 30)), float(params.get_param('esg_management.weight_governance', 30))]
        for record in self:
            domain = [('department_id', '=', record.department_id.id), ('transaction_date', '>=', record.period_start), ('transaction_date', '<=', record.period_end), ('state', '=', 'confirmed')]
            emissions = sum(self.env['esg.carbon.transaction'].search(domain).mapped('calculated_emissions'))
            record.environmental_score = max(0, 100 - emissions)
            csr = self.env['esg.employee.participation'].search_count([('activity_id.department_id', '=', record.department_id.id), ('approval_status', '=', 'approved'), ('completion_date', '>=', record.period_start), ('completion_date', '<=', record.period_end)])
            record.social_score = min(100, csr * 10)
            issues = self.env['esg.compliance.issue'].search_count([('audit_id.department_id', '=', record.department_id.id), ('status', 'not in', ['resolved', 'closed'])])
            record.governance_score = max(0, 100 - issues * 10)
            record.total_score = sum(score * weight / 100 for score, weight in zip((record.environmental_score, record.social_score, record.governance_score), weights))

    @api.model
    def _cron_snapshot_scores(self):
        """Create one monthly score snapshot per department for trend reporting."""
        today = fields.Date.today()
        period_start = today.replace(day=1)
        for department in self.env['esg.department'].search([('status', '=', 'active')]):
            score = self.search([('department_id', '=', department.id), ('period_start', '=', period_start), ('period_end', '=', today)], limit=1)
            if not score:
                self.create({'department_id': department.id, 'period_start': period_start, 'period_end': today})
