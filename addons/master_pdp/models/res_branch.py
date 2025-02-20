from odoo import api, fields, models

class Branch(models.Model):
    _name = "res.branch"
    _description = "Branches"
    _order = 'name'

    def _get_company(self):
        res_user = self.env['res.users'].browse(self._uid)
        return res_user.company_id.id

    company_id = fields.Many2one('res.company', string='Company', index=True,default=_get_company)
    code = fields.Char(string='Branch Code', required=True)
    name = fields.Char(string='Branch Name')
    profit_centre = fields.Char(string='Profit Centre', required=True, help='please contact your Accounting Manager to get Profit Center.')
    street = fields.Char(string='Address')
    street2 = fields.Char()
    rt = fields.Char(string='RT',size=3)
    rw = fields.Char(string='RW',size=3)
    state_id = fields.Many2one('res.country.state',string='Province')
    kabupaten_id = fields.Many2one('res.city','Kabupaten')
    kecamatan_id = fields.Many2one('res.kecamatan','Kecamatan', domain="[('city_id','=',kabupaten_id)]")
    kecamatan = fields.Char(string="Kecamatan") 
    kelurahan_id = fields.Many2one('res.kelurahan',string='Kelurahan', domain="[('kecamatan_id','=',kecamatan_id)]")
    kelurahan = fields.Char(string="Kelurahan")
    kode_pos = fields.Char(string="Kode Pos")
    phone = fields.Char(string='Phone')
    mobile = fields.Char(string='Mobile')
    fax = fields.Char(string='Fax')
    email = fields.Char(string='e-mail')
    pimpinan_id = fields.Many2one('hr.employee',string='Pimpinan')

    kawil_id = fields.Many2one(comodel_name='hr.employee', string='Kepala Wilayah', domain=[('job_id.sales_force','=','am')])
    owner_id = fields.Many2one(comodel_name='hr.employee', string='Owner')
    kacab_id = fields.Many2one(comodel_name='hr.employee', string='Kepala Cabang', domain=[('job_id.sales_force','=','soh')])
    adh_id = fields.Many2one(comodel_name='hr.employee', string='Admin Head')
    kabeng_id = fields.Many2one(comodel_name='hr.employee', string='Kepala Bengkel')
    kasir_id = fields.Many2one(comodel_name='hr.employee', string='Kasir')