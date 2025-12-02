from odoo import models, fields

class EstateSubUnit(models.Model):
    _name = 'estate.sub.unit'
    _description = 'Sub Real Estate Unit'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # الهوية والحالة
    name = fields.Char(string='اسم الوحدة', required=True, tracking=True)
    category = fields.Selection([
        ('flat','شقة'), ('shop','محل'), ('warehouse','مستودع')
    ], string='نوع الوحدة', required=True, tracking=True)
    status = fields.Selection([
        ('available','متاح'), ('reserved','محجوز'),
        ('rented','مؤجر'), ('hidden','مخفي')
    ], string='الحالة', default='available', tracking=True)
    active = fields.Boolean(string='نشط', default=True)

    # توفر للبيع/الإيجار
    can_rent = fields.Boolean(string='متوفر للإيجار', default=True)
    can_sell = fields.Boolean(string='متوفر للبيع', default=True)

    # علاقات
    site_id = fields.Many2one('real.estate.site', string='المشروع/الموقع', required=True, tracking=True)
    main_unit_id = fields.Many2one('estate.main.unit', string='الوحدة الرئيسية', required=True, ondelete='cascade', tracking=True)
    owner_id = fields.Many2one('res.partner', string='المالك')
    salesperson_id = fields.Many2one('res.users', string='مسؤول المبيعات', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='الشركة', default=lambda self: self.env.company)

    # تواريخ وروابط
    available_date = fields.Date(string='تاريخ الإتاحة')
    video_url = fields.Char(string='رابط الفيديو')

    # وسائط
    image_128 = fields.Image(string='صورة', max_width=128, max_height=128)

    # تكاليف وأسعار
    cost = fields.Float(string='التكلفة')
    sale_price = fields.Float(string='سعر البيع')
    rent_amount = fields.Float(string='مبلغ الإيجار/الشهر')
    deposit_amount = fields.Float(string='مبلغ التأمين')

    # مساحات وواجهات
    area = fields.Float(string='المساحة (م²)')
    area_roof = fields.Float(string='المسطح')
    area_service = fields.Float(string='مساحة الخدمات')
    facade_total = fields.Float(string='إجمالي الواجهة')
    face_north = fields.Float(string='واجهة شمال')
    face_south = fields.Float(string='واجهة جنوب')
    face_east = fields.Float(string='واجهة شرق')
    face_west = fields.Float(string='واجهة غرب')

    # خدمات
    elec_system = fields.Selection([('public','شبكة عامة'), ('solar','طاقة شمسية')], string='عداد الكهرباء/الكهرباء')
    heating_system = fields.Selection([('none','بدون'), ('gas','غاز'), ('electric','كهرباء')], string='نظام التدفئة/التسخين')
    water_source = fields.Selection([('public','شبكة عامة'), ('well','بئر')], string='مصدر المياه')
    solar_system = fields.Boolean(string='نظام الطاقة الشمسية', default=False)

    # وصف ومحتويات
    position_desc = fields.Char(string='وصف/موقع داخلي')
    contents = fields.Text(string='محتويات/تجهيزات')
    notes = fields.Text(string='ملاحظات داخلية')

    # مستندات وأطراف
    license_ref = fields.Char(string='رقم الترخيص')
    partner_ids = fields.Many2many('res.partner', string='جهات اتصال/ملاك')

    # موقع جغرافي
    geo_lat = fields.Float(string='Latitude')
    geo_lng = fields.Float(string='Longitude')

    # اختياري: محاسبة تحليليّة (يتطلب account_analytic)
    analytic_account = fields.Many2one('account.analytic.account', string='حساب تحليلي')

    # مساحات إضافية اختيارية
    garden_area = fields.Float(string='مساحة الحديقة', default=0.0)
    balcony_area = fields.Float(string='مساحة البلكونات', default=0.0)
    apply_tax = fields.Boolean(string='تطبيق الضريبة')
