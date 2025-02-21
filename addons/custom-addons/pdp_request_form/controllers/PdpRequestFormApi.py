from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class PdpRequestFormApi(http.Controller):

    @http.route('/api/pdp/forms', type='json', auth='public', csrf=False, methods=['POST'])
    def create_form(self, **kwargs):
        try:
            # Ambil data dari request body
            body = request.httprequest.data.decode('utf-8')
            parsed_body = json.loads(body)
            # _logger.info(f"Received data: {parsed_body}")

            # Pastikan data yang dibutuhkan ada
            required_fields = [
                'name', 'company_id', 'activities_form', 'valid_on', 'expired_on', 
                'limit_usage', 'email_to', 'link_form', 'token', 'qr_code'
            ]
            form_data = {field: parsed_body.get(field) for field in required_fields}

            # Buat record di model pdp.request.form
            form = request.env['pdp.request.form'].sudo().create(form_data)

            return {
                'id': form.id,
                'name': form.name,
                'company_id': form.company_id.id if form.company_id else None,
                'activities_form': form.activities_form,
                'valid_on': form.valid_on,
                'expired_on': form.expired_on,
                'limit_usage': form.limit_usage,
                'email_to': form.email_to,
                'link_form': form.link_form,
                'token': form.token,
                'qr_code': form.qr_code
            }

        except json.JSONDecodeError:
            # _logger.error("Invalid JSON format")
            return {'error': 'Invalid JSON format'}
        except Exception as e:
            # _logger.error(f"Error creating form: {str(e)}")
            return {'error': str(e)}
