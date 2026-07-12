"""Small shared services for configurable ESG notifications."""


def setting_enabled(env, key, default=True):
    return env['ir.config_parameter'].sudo().get_param('esg_management.%s' % key, str(default)).lower() in ('1', 'true', 'yes')


def send_template_notification(record, xmlid, toggle, partner=None):
    """Post the editable template and send its mail only when that channel is enabled."""
    if not setting_enabled(record.env, toggle):
        return
    template = record.env.ref(xmlid, raise_if_not_found=False)
    if template:
        if 'message_post' in record._fields:
            body = template._render_field('body_html', record.ids, compute_lang=True)[record.id]
            record.message_post(body=body, partner_ids=[partner.id] if partner else [])
        template.send_mail(record.id, force_send=False)
