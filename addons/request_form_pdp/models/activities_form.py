from odoo import models, fields, api

class ActivitiesForm(models.Model):
    _name = 'pdp.activities.form'
    _description = 'Activites Form'

    name = fields.Char('name')
    company_id = fields.Many2one('res.company', string='company')
    activities_form_line_ids = fields.One2many('pdp.activities.form.line', 'activities_form_id', string='activities_form_line')
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
  
class ActivitiesFormLine(models.Model):
    _name = 'pdp.activities.form.line'
    _description = 'Activities Form Line'

    activities_form_id = fields.Many2one('pdp.activities.form', string='Activities Form')

    field_id = fields.Many2one('pdp.master.fields', string='Field')
    field_name = fields.Char(related='field_id.field_name', string='Field Name')
    field_type = fields.Selection(related='field_id.field_type', string='Field Type')
    field_option = fields.Char(related='field_id.field_option', string='Field Option')

    used_field_ids = fields.Many2many('pdp.master.fields', compute='_compute_used_field_ids', store=False)
    @api.depends('field_id')
    def _compute_used_field_ids(self):
        for rec in self:
            rec.used_field_ids = [(6, 0, rec.activities_form_id.activities_form_line_ids.mapped('field_id').ids)]
