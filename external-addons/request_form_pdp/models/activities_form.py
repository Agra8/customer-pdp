from odoo import models, fields, api

class ActivitiesForm(models.Model):
    _name = 'pdp.activities.form'
    _description = ' Activites Form'

    name = fields.Char('name')
    company_id = fields.Many2one('res.company', string='company')
    activities_form_line_ids = fields.One2many('pdp.activities.form.line', 'activies_form_id', string='activities_form_line')
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

class ActiviesFormLine(models.Model):
    _name = 'pdp.activities.form.line'
    _description = 'model.technical.name'

    activies_form_id = fields.Many2one('pdp.activities.form', string='activies_form', domain="[('model_id.model', '=', 'res.partner')]")
    field_id = fields.Many2one('ir.model.fields', string='Field')
    field_name = fields.Char(related='field_id.field_description', string='field_name')
    field_type = fields.Char(related='field_id.ttype', string='Field Type')
    field_option = fields.Char(related='field_id.field_description', string='field_option')    
