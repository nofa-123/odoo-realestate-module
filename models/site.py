from odoo import models, fields

class RealEstateSite(models.Model):
    _name = 'real.estate.site'
    _description = 'Real Estate Site/Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='الاسم', required=True, tracking=True)
    parent_id = fields.Many2one('real.estate.site', string='المشروع / المرحلة الأم', tracking=True)
    child_ids = fields.One2many('real.estate.site', 'parent_id', string='مراحل/أطفال')
    company_id = fields.Many2one('res.company', string='شركة', default=lambda self: self.env.company, tracking=True)

    street = fields.Char(string='الشارع')
    street2 = fields.Char(string='الشارع 2')
    city = fields.Char(string='المدينة')
    state_id = fields.Many2one('res.country.state', string='المحافظة')
    zip = fields.Char(string='الرمز البريدي')
    country_id = fields.Many2one('res.country', string='الدولة')
