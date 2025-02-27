from odoo import models, fields, api

class PdpConsent(models.Model):
    _name = 'pdp.consent'
    _description = 'Pdp Consent'

    name = fields.Char(
        string="Reference",
        default=lambda self: 'New',
        copy=False,
        readonly=True,
        tracking=True
    )
    title = fields.Char(string='Title of Consent')
    body = fields.Html(string='Dialog Consent & Agreement', sanitize=False)
    expired_date = fields.Date(string='Expired Date')
    valid_date = fields.Date(string='Valid Date')
    activity_form = fields.Many2one(string='Activities form')
    required = fields.Boolean(string='Required Agree?', default=False)
    save = fields.Boolean(string='Required Agree?', default=False)
    cancel = fields.Boolean(string='Required Agree?', default=False)
    version = fields.Char(string='version')
    parent_id = fields.Many2one('pdp.consent', "parent")
    child_ids = fields.One2many('pdp.consent', 'parent_id', string="child")
    region = fields.Many2one('res.country', 'Region')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('waiting', 'Waiting'),
        ('approve', 'Approved'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, copy="false")
    attach_file = fields.Binary(string='insert')
    is_agree = fields.Boolean(string='agree?')
    is_agree = fields.Boolean(string="Agreed to Terms", default=False)
    is_disagree = fields.Boolean(string="Disagreed to Terms", default=False)
    user_id = fields.Many2one('res.users', "User", required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('pdp.consent') or 'New'
        return super().create(vals_list)

    def button_confirm (self):
        self.write({
            'state': "waiting"
        })
    
    def button_cancel (self):
        self.write({
            'state': "cancel"
        })
    def button_done (self):
        self.write({
            'state': "done"
        })
    def button_approve (self):
        self.write({
            'state': "approve"
        })
