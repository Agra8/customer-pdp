from odoo import models, fields, api

class activityForm(models.Model):
    _name = 'pdp.activity.form'
    _description = 'Activity Form'

    name = fields.Char('name')
    company_id = fields.Many2one('res.company', string='company')
    activity_form_line = fields.One2many('pdp.activity.form.line', 'activity_form_id', string='activity_form_line')
    consent_agreement_id = fields.Many2one('pdp.consent', string='Consent Agreement')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('on_customer', 'On Customer'),
        ('completed', 'Completed'),
        ('cancel', 'canceled'),
        ('expired', 'Expired')
    ], string='Status', default='draft', tracking=True)

    def action_generate(self):
        self.write({'status': 'on_customer'})

    def action_cancel(self):
        self.write({'status': 'cancel'})
    def action_confirm(self):
        self.write({'status': 'completed'})
  
class activityFormLine(models.Model):
    _name = 'pdp.activity.form.line'
    _description = 'activity Form Line'

    activity_form_id = fields.Many2one('pdp.activity.form', string='Activity Form')

    field_id = fields.Many2one('pdp.master.fields', string='Field')
    field_name = fields.Char(related='field_id.field_name', string='Field Name')
    field_type = fields.Selection(related='field_id.field_type', string='Field Type')
    field_option = fields.Char(related='field_id.field_option', string='Field Option')
    required = fields.Boolean(string='Required')
    min_char = fields.Integer(string='Min')
    max_char = fields.Integer(string='Max')

    used_field_ids = fields.Many2many('pdp.master.fields', compute='_compute_used_field_ids', store=False)
    @api.depends('field_id')
    def _compute_used_field_ids(self):
        for rec in self:
            rec.used_field_ids = [(6, 0, rec.activity_form_id.activity_form_line.mapped('field_id').ids)]
