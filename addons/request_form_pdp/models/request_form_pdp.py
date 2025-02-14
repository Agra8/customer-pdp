# -*- coding: utf-8 -*-
from odoo import models, fields, api
import qrcode
import base64
import hashlib
import secrets
from io import BytesIO
from datetime import datetime
import pyperclip


class RequestPDPForm(models.Model):
    _name = 'pdp.request.form'
    _description = ' Request PDP Form'

    name = fields.Char(string='Form Name',readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True)
    activities_form = fields.Selection([
        ('prospect', 'Prospect Process'),
        ('onboarding', 'Onboarding Process'),
        ('followup', 'Follow-up Process')
    ], string='Activities Form', required=True, default='prospect')
    valid_on = fields.Date(string='Valid On')
    expired_on = fields.Date(string='Expired On')
    limit_usage = fields.Integer(string='Limit Usage', default=1)
    email_to = fields.Char(string='Email To')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('on_customer', 'On Customer'),
        ('completed', 'Completed'),
        ('cancel', 'canceled'),
        ('expired', 'Expired')
    ], string='Status', default='draft', tracking=True)

    qr_code = fields.Binary(string='Unique QR Code', compute='_generate_qr_code', store=True)
    link_form = fields.Char(string='Link Form', compute='_generate_link', store=True)
    token = fields.Char(string='Token', readonly=True)

    @api.model
    def create(self, vals):
        record = super(RequestPDPForm, self).create(vals)
        record._update_sequence()
        return record

    def _update_sequence(self):
        for record in self:
            year = datetime.today().strftime('%y')  
            month = datetime.today().strftime('%m')

            sequence = self.env['ir.sequence'].search([('code', '=', 'pdp.request.form')], limit=1)
            if sequence:
                sequence.write({'prefix': f'REQ/TM/{year}/{month}/'})
                record.name = sequence.next_by_code('pdp.request.form')
            else:
                record.name = f'REQ/TM/{year}/{month}/0001'

    def _generate_token(self):
        # Generatee a unique wtoken for the form
        for record in self:
            token_str = f"{secrets.token_hex(16)}"
            record.token = hashlib.sha256(token_str.encode()).hexdigest()

    @api.depends('token')
    def _generate_qr_code(self):
        # ggenerate QR code based on the form URL
        for record in self:
            if record.token:
                qr = qrcode.make(record._get_form_url())
                buffer = BytesIO()
                qr.save(buffer, format='PNG')
                record.qr_code = base64.b64encode(buffer.getvalue())

    @api.depends('token')
    def _generate_link(self):
        for record in self:
            if record.token:
                record.link_form = f"{record._get_form_url()}?token={record.token}"

    def _get_form_url(self):
        # Retrieve the base URL and construct the form UR
        # base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        # return f"https://anichin.co.id/{self.id}"

        # def _get_form_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"http://linkedin.com/in/ahmaddaudjuned/{self.id}"

    def action_generate(self):
        self.write({'status': 'on_customer'})

    def action_cancel(self):
        self.write({'status': 'cancel'})
    def action_confirm(self):
        self.write({'status': 'completed'})
    
    # Tambahkan method untuk berbagi melalui WhatsApp
    def action_share_link(self):
        for record in self:
            if record.link_form:
                wa_url = f"https://api.whatsapp.com/send?text={record.link_form}"
                return {
                    'type': 'ir.actions.act_url',
                    'url': wa_url,
                    'target': 'new',
                }

    # Tambahkan method untuk menyalin link
    # def action_copy_link(self):
    #     for record in self:
    #         if record.link_form:
    #             pyperclip.copy(record.link_form)
    def action_copy_link(self):
        for record in self:
            if record.link_form:
                    pyperclip.copy(record.link_form)

    def action_generate_link(self):
        self._generate_token()
        self._generate_link()
