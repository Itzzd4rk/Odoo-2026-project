from odoo import api, models


class EsgDashboard(models.AbstractModel):
    _name = 'esg.dashboard'
    _description = 'ESG Dashboard Service'

    @api.model
    def get_kpis(self):
        latest_scores = self.env['esg.department.score'].search([], order='period_end desc, id desc')
        by_department = {}
        for score in latest_scores:
            by_department.setdefault(score.department_id.id, score)
        scores = list(by_department.values())
        denominator = len(scores) or 1
        return {
            'overall': round(sum(s.total_score for s in scores) / denominator, 1),
            'environmental': round(sum(s.environmental_score for s in scores) / denominator, 1),
            'social': round(sum(s.social_score for s in scores) / denominator, 1),
            'governance': round(sum(s.governance_score for s in scores) / denominator, 1),
            'open_issues': self.env['esg.compliance.issue'].search_count([('status', 'not in', ['resolved', 'closed'])]),
            'leaders': [{'name': row.employee_id.name, 'xp': row.total_xp} for row in self.env['esg.leaderboard'].search([], limit=5)],
        }
