# models/contract.py
from odoo import models, fields

class EstateRentContract(models.Model):
    _name = 'estate.rent.contract'
    _description = 'عقد إيجار'

    name = fields.Char(string="المرجع", default="New", copy=False)
    booking_id = fields.Many2one('estate.booking', string="حجز الوحدة")
    tenant_id = fields.Many2one('res.partner', string="المستأجر", required=True)
    unit_id = fields.Many2one('estate.sub.unit', string="الوحدة", required=True)
    date_start = fields.Date(string="تاريخ البداية", required=True)
    date_end = fields.Date(string="تاريخ النهاية", required=True)
    rent_amount = fields.Monetary(string="إيجار شهري")
    deposit = fields.Monetary(string="التأمين")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id.id)
    state = fields.Selection([
        ('draft', 'مسودة'),
        ('running', 'ساري'),
        ('done', 'منتهي'),
        ('cancelled', 'ملغي'),
    ], string="الحالة", default='draft')
