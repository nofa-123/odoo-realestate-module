from odoo import models, fields, api

class EstateBooking(models.Model):
    _name = 'estate.booking'
    _description = 'حجز وحدة عقارية'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="المرجع", default="New", copy=False, tracking=True)
    tenant_id = fields.Many2one(
        'res.partner', string="المستأجر", required=True,
        domain=[('estate_role', '=', 'tenant')], tracking=True
    )
    unit_id = fields.Many2one(
        'estate.sub.unit', string="الوحدة", required=True,
        domain=[('status', '=', 'available')], tracking=True
    )
    booking_type = fields.Selection(
        [('rent', 'تأجير'), ('sale', 'تمليك')],
        string="نوع الحجز", default='rent', tracking=True
    )
    amount = fields.Monetary(string="مبلغ الحجز", tracking=True)
    currency_id = fields.Many2one(
        'res.currency', default=lambda self: self.env.company.currency_id.id
    )
    state = fields.Selection([
        ('draft', 'مسودة'),
        ('confirmed', 'مؤكد'),
        ('cancelled', 'ملغي'),
    ], string="الحالة", default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('estate.booking') or 'New'
        return super().create(vals)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'
            rec.unit_id.status = 'reserved'
