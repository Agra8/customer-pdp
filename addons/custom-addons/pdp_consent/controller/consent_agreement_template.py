from odoo import http
from odoo.http import request

class PdpConsentController(http.Controller):

    @http.route('/agreement', type='http', auth='public', website=True)
    def agreement_page(self, **kwargs):
        # Fetch the latest consent record
        consent = request.env['pdp.consent'].sudo().search([], limit=1)
        company = request.env['res.company'].sudo().search([], limit=1)
        company_name = company.name if company else "Perusahaan Tidak Diketahui"
        mobile_number = company.phone if company and company.phone else "Nomor Tidak Tersedia"

        return request.render('pdp_consent.pdp_agreement_template', {
            'consent': consent,
            'company_name': company_name,
            'mobile_number': mobile_number 
        })
        
        # If token is missing, show an error message
        token = consent.token if consent and consent.token else ""
        if not token:
            return request.render('pdp_consent.pdp_agreement_template', {
                'error_message': 'Token tidak ditemukan.',
            })

        # Fetch the latest consent record (optional)
        consent = request.env['pdp.consent'].sudo().search([], limit=1)

        
    @http.route(['/agreement/accept'], type='http', auth="public", website=True, methods=['POST'])
    def button_accept(self, **post):
        token = post.get('token')  # Get token from form submission
        if not token:
            return request.render('pdp_consent.pdp_agreement_template', {
                'error_message': 'Token tidak ditemukan.',
            })

        is_agree = bool(post.get('is_agree'))  # Convert "on" to True/False
        is_disagree = bool(post.get('is_disagree'))  # Convert "on" to True/False


        request.env['pdp.consent'].sudo().create({
        'is_agree': is_agree,
        'is_disagree': is_disagree,
        'user_id': request.env.user.id,
        })
        return request.redirect(f'/request_form?token={token}')  # Redirect to request form