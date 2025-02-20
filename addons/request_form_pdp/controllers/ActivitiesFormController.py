from odoo import http
from odoo.http import request
from datetime import date
import logging
import re
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ActivitiesFormController(http.Controller):
    
    def validate_request_form(self, token):
        """
        Validasi token dan kembalikan request_form jika valid.
        """
        if not token:
            # _logger.warning("Token tidak ditemukan.")
            return False, "Token tidak ditemukan."
        
        request_form = request.env['pdp.request.form'].sudo().search([('token', '=', token)], limit=1)
        if not request_form:
            # _logger.warning("Token tidak valid: %s", token)
            return False, "Token tidak valid."

        if not request_form.activity_form_id:
            return False, "Formulir tidak ditemukan."

        today = date.today()
        # _logger.info("Token today: %s", today)

        if request_form.valid_date and today < request_form.valid_date:
            # _logger.warning("Token belum aktif: %s", token)
            return False, "Token belum aktif!!!."
        
        if request_form.expired_date and today > request_form.expired_date:
            # _logger.warning("Token sudah kedaluwarsa: %s", token)
            return False, "Token sudah kedaluwarsa."
        
        if request_form.limit_usage <= 0:
            return False, "Token sudah tidak bisa digunakan lagi."
        
        # _logger.info("Token valid: %s", token)
        return True, request_form

    def validate_partner_data(self, post, activity_form_id):
        """
        Validasi data pengguna sebelum disimpan ke res.partner.
        """
        field_mapping = {
            'Nama': 'name',
            'Telepon Mobile': 'phone',
            'Email': 'email',
            'Jalan': 'street',
            'Bahasa': 'lang',
            'Judul': 'title',
            'Perusahaan': 'company',
            'Jabatan Kerja': 'function',
        }

        required_fields = ['Nama', 'Email', 'Telepon Mobile']
        partner_vals = {'active': True}
        errors = []

        for line in activity_form_id.activity_form_line:
            field_name = line.field_name.strip()
            field_key = f'field_{line.field_id.id}'
            field_value = str(post.get(field_key, '')).strip()

            if field_name in required_fields and not field_value:
                errors.append(f"{field_name} harus diisi.")
                # _logger.warning("Field wajib tidak diisi: %s", field_name)
                continue

            if field_name == 'Email' and field_value:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", field_value):
                    errors.append("Format email tidak valid.")
                    # _logger.warning("Email tidak valid: %s", field_value)

            if field_name == 'Telepon Mobile' and field_value:
                if not field_value.isdigit():
                    errors.append("Nomor telepon hanya boleh berisi angka.")
                    # _logger.warning("Nomor telepon tidak valid: %s", field_value)

            partner_vals[field_mapping.get(field_name, f'x_{field_name}')] = field_value

        return partner_vals, errors

    

    @http.route(['/request_form'], type='http', auth="public", website=True)
    def request_form(self, token=None, **kw):
        _logger.info("Mengakses request_form dengan token: %s", token)
        
        valid, result = self.validate_request_form(token)
        if not valid:
            # Kirim kesalahan ke template untuk ditampilkan dengan pop-up
            return request.render('request_form_pdp.invalid_token_template', {'error_message': result})
        
        request_form = result
        activity_form_id = request_form.activity_form_id
      
        fields_data = [
            {
                'id': line.field_id.id,
                'name': line.field_name.strip(),
                'type': line.field_type,
                'required': line.field_name.strip() in ['Nama', 'Email', 'Telepon Mobile'],
                'options': (
                    line.field_option.split(',') if line.field_type == 'selection' else
                    [{'id': rec.id, 'name': rec.name} for rec in request.env[line.field_id.relation].sudo().search([])]
                    if line.field_type == 'many2one' and hasattr(line.field_id, 'relation') else []
                )
            }
            for line in activity_form_id.activity_form_line
        ]

        # _logger.info("fields_data  fields_data %s", fields_data)


        return request.render('request_form_pdp.request_form_template', {
            'token': token,
            'fields_data': fields_data,
            'form_name': activity_form_id.name
        })



    @http.route(['/request_form/submit'], type='http', auth="public", website=True, methods=['POST'])
    def request_form_submit(self, **post):
        _logger.info("Menerima form submission dengan data: %s", post)

        token = post.get('token', '').strip()
        valid, result = self.validate_request_form(token)
        if not valid:
            return request.render('request_form_pdp.request_form_template', {'error_message': result})
        
        request_form = result
        activity_form_id = request_form.activity_form_id

        if not activity_form_id:
            return request.render('request_form_pdp.request_form_template', {'error_message': 'Formulir tidak ditemukan.'})
        
        partner_vals, errors = self.validate_partner_data(post, activity_form_id)
        if errors:
            return request.render('request_form_pdp.request_form_template', {'error_message': "<br/>".join(errors)})

        try:
            new_partner = request.env['res.partner'].sudo().create(partner_vals)
            _logger.info("Berhasil membuat res.partner dengan ID: %s", new_partner.id)
            request_form.sudo().write({'limit_usage': request_form.limit_usage - 1})
            return request.render('request_form_pdp.thanks_template')
        except Exception as e:
            # _logger.error("Gagal menyimpan data ke res.partner: %s", str(e))
            return request.render('request_form_pdp.request_form_template', {'error_message': 'Terjadi kesalahan saat menyimpan data. Silakan coba lagi.'})
