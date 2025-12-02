from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class EstateMainUnit(models.Model):
    _name = 'estate.main.unit'
    _description = 'Main Real Estate Unit (Tower/Building)'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # أساسية
    name = fields.Char(string='الاسم', required=True, tracking=True)
    code = fields.Char(string='الكود', tracking=True)
    site_id = fields.Many2one('real.estate.site', string='المشروع', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='شركة', default=lambda self: self.env.company, tracking=True)
    owner_id = fields.Many2one('res.partner', string='المالك')
    active = fields.Boolean(string='نشط', default=True)

    # أصل محاسبي (اختياري: يعمل إن توفّر app الحسابات)
    asset_id = fields.Many2one('account.asset', string='الأصل المحاسبي')

    # تواريخ وحالة
    purchase_date = fields.Date(string='تاريخ الشراء')
    launch_date = fields.Date(string='تاريخ الإطلاق')
    property_type = fields.Selection([
        ('tower','برج'), ('building','عمارة'), ('mall','مول'), ('villa','فيلا'), ('other','أخرى'),
    ], string='نوع العقار', default='building')
    state = fields.Selection([('active','نشط'), ('hidden','مخفي')], string='حالة العقار', default='active')

    # مساحات وواجهات
    area_roof = fields.Float(string='المسطح', default=0.0)
    area_total = fields.Float(string='إجمالي الفراغ', default=0.0)
    area_common = fields.Float(string='مساحة الخدمات', default=0.0)
    face_east = fields.Float(string='جبهة من الشرق', default=0.0)
    face_west = fields.Float(string='جبهة من الغرب', default=0.0)
    face_north = fields.Float(string='جبهة من الشمال', default=0.0)
    face_south = fields.Float(string='جبهة من الجنوب', default=0.0)

    # مُدخلات توليد
    floors = fields.Integer(string='عدد الطوابق', default=0)
    flats_per_floor = fields.Integer(string='عدد الشقق/الطابق', default=0)
    shops = fields.Integer(string='عدد المحلات', default=0)
    warehouses = fields.Integer(string='عدد المستودعات', default=0)

    # علاقة فرعية
    sub_unit_ids = fields.One2many('estate.sub.unit', 'main_unit_id', string='الوحدات الفرعية')

    # وسائط
    image_128 = fields.Image(string='صورة', max_width=128, max_height=128)
    image_1024 = fields.Image(string='صور إضافية')
    attachment_ids = fields.Many2many('ir.attachment', string='مستندات')

    @api.model
    def _generate_name(self, base, seq):
        return f"{base} {seq}"

    def action_generate_sub_units(self):
        Sub = self.env['estate.sub.unit']
        for rec in self:
            if not rec.site_id:
                raise UserError(_('يجب تحديد المشروع قبل التوليد.'))

            floors = max(rec.floors or 0, 0)
            flats = max(rec.flats_per_floor or 0, 0)
            shops = max(rec.shops or 0, 0)
            warehouses = max(rec.warehouses or 0, 0)

            if not any([floors and flats, shops, warehouses]):
                raise UserError(_('رجاءً أدخل قيماً موجبة (طوابق/شقق أو محلات/مستودعات).'))

            to_create = []
            for f in range(1, floors + 1):
                for i in range(1, flats + 1):
                    to_create.append({
                        'name': f'شقة طابق {f} رقم {i}',
                        'main_unit_id': rec.id,
                        'site_id': rec.site_id.id,
                        'category': 'flat',
                        'status': 'available',
                    })
            for i in range(1, shops + 1):
                to_create.append({
                    'name': f'محل {i}',
                    'main_unit_id': rec.id,
                    'site_id': rec.site_id.id,
                    'category': 'shop',
                    'status': 'available',
                })
            for i in range(1, warehouses + 1):
                to_create.append({
                    'name': f'مستودع {i}',
                    'main_unit_id': rec.id,
                    'site_id': rec.site_id.id,
                    'category': 'warehouse',
                    'status': 'available',
                })
            if to_create:
                Sub.create(to_create)
                _logger.info("CREATED %s sub units for main_unit %s", len(to_create), rec.id)
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def action_generate_asset(self):
        # حماية: العمل فقط عند توفر تطبيق المحاسبة
        if 'account.asset' not in self.env:
            raise UserError(_('تطبيق المحاسبة غير مثبت، لا يمكن إنشاء أصل.'))
        for rec in self:
            if rec.asset_id:
                raise UserError(_('تم إنشاء أصل مسبقاً لهذه الوحدة.'))
            if not rec.name or not rec.company_id:
                raise UserError(_('يرجى تعبئة الاسم والشركة قبل إنشاء الأصل.'))
            vals = {
                'name': rec.name,
                'company_id': rec.company_id.id,
                'acquisition_date': rec.purchase_date or fields.Date.today(),
                'original_value': rec.area_total or 0.0,
                'state': 'draft',
            }
            asset = self.env['account.asset'].create(vals)
            rec.asset_id = asset.id
        return {'type': 'ir.actions.client', 'tag': 'reload'}
