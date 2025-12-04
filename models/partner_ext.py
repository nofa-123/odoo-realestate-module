from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    estate_role = fields.Selection([
        ('owner', 'مالك'),
        ('tenant', 'مستأجر'),
    ], string="دور العقار")
