from odoo import fields, models, tools


class EsgLeaderboard(models.Model):
    _name = 'esg.leaderboard'
    _description = 'ESG Leaderboard'
    _auto = False
    _order = 'total_xp desc, employee_id'

    employee_id = fields.Many2one('hr.employee', readonly=True)
    department_id = fields.Many2one('esg.department', readonly=True)
    total_xp = fields.Integer(readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW esg_leaderboard AS (
                SELECT e.id AS id, e.id AS employee_id, e.esg_department_id AS department_id,
                    COALESCE(cp.xp, 0) + COALESCE(ep.points, 0) AS total_xp
                FROM hr_employee e
                LEFT JOIN (SELECT employee_id, SUM(xp_awarded) AS xp FROM esg_challenge_participation GROUP BY employee_id) cp ON cp.employee_id = e.id
                LEFT JOIN (SELECT employee_id, SUM(points_earned) AS points FROM esg_employee_participation GROUP BY employee_id) ep ON ep.employee_id = e.id
            )''')
