"""Bootstrap disposable ESG browser-test users in an Odoo database."""
from odoo import SUPERUSER_ID

PASSWORD = 'esg_demo_pass'
USER_GROUP = 'esg_management.group_esg_user'
MANAGER_GROUP = 'esg_management.group_esg_manager'


def _ensure_user(env, name, login, group_xmlid):
    group = env.ref(group_xmlid)
    user = env['res.users'].with_context(no_reset_password=True).search([('login', '=', login)], limit=1)
    base_group = env.ref('base.group_user')
    values = {
        'name': name,
        'login': login,
        'email': login,
        'password': PASSWORD,
        'groups_id': [(6, 0, [base_group.id, group.id])],
    }
    if user:
        user.write(values)
    else:
        user = env['res.users'].with_context(no_reset_password=True).create(values)
    employee = env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
    department = env['esg.department'].search([], limit=1)
    if not department:
        department = env['esg.department'].create({'name': 'Demo Department', 'code': 'DEMO'})
    employee_values = {
        'name': name,
        'user_id': user.id,
        'work_email': login,
        'esg_department_id': department.id,
    }
    if employee:
        employee.write(employee_values)
    else:
        env['hr.employee'].create(employee_values)
    return user


def main(env):
    env = env(user=SUPERUSER_ID)
    _ensure_user(env, 'ESG Demo User', 'esg.demo.user@example.com', USER_GROUP)
    _ensure_user(env, 'ESG Demo Manager', 'esg.demo.manager@example.com', MANAGER_GROUP)
    print('Browser test users ready: esg.demo.user@example.com / esg.demo.manager@example.com (password: %s)' % PASSWORD)


main(env)
