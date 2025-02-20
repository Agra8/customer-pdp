from odoo import models, fields, api, _

class Job(models.Model):
    _inherit = "hr.job"
    _description = "Job"
    
    group_id = fields.Many2one(comodel_name='res.groups',  string='Group',  help='')