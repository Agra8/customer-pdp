# -*- coding: utf-8 -*-
from odoo import models, fields, api,exceptions 
import qrcode
import base64
import hashlib
import secrets
from io import BytesIO
from datetime import datetime


class RequestPDPForm(models.Model):
    _name = 'pdp.request.form'
    _description = ' Request PDP Form'

    name = fields.Char("Form Name", default=lambda self: ('New'), copy=False, readonly=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', required=True)
    activity_form_id = fields.Many2one(
        'pdp.activity.form', 
        string='Activity Form', 
        domain=[('name', '!=', False)]
    )
    valid_date = fields.Date(string='Valid Date')
    expired_date = fields.Date(string='Expired Date')
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

    # make sure valid date and expired_date
    @api.constrains('valid_date', 'expired_date')
    def _check_dates(self):
        for record in self:
            if record.valid_date and record.expired_date and record.valid_date > record.expired_date:
                raise exceptions.ValidationError("The valid date cannot be after the expired date.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('pdp.request.form') or 'New'
        return super().create(vals_list)
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
        # def _get_form_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"{base_url}/agreement/"

    def action_generate(self):
        self.write({'status': 'on_customer'})

    def action_cancel(self):
        self.write({'status': 'cancel'})
    def action_confirm(self):
        self.write({'status': 'completed'})
    
    #method untuk berbagi melalui WhatsApp
    def action_share_link(self):
        for record in self:
            if record.link_form:
                wa_url = f"https://api.whatsapp.com/send?text={record.link_form}"
                return {
                    'type': 'ir.actions.act_url',
                    'url': wa_url,
                    'target': 'new',
                }

    def action_generate_link(self):
        self._generate_token()
        self._generate_link()
