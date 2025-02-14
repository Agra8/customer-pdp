from odoo import models, fields, api

class PDPMasterFields(models.Model):
    _name = 'pdp.master.fields'
    _description = 'Master Fields'
    _rec_name = 'field_name'


    field_id = fields.Many2one('ir.model.fields', string='Field',domain="[('model_id.model', '=', 'res.partner')]")
    field_name = fields.Char(related='field_id.field_description', string='field_name')
    field_type = fields.Selection(related='field_id.ttype', string='Field Type')
    field_option = fields.Char(related='field_id.field_description', string='field_option')  