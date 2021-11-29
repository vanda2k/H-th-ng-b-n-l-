from odoo import api, fields, models, _
from datetime import datetime,time



class PartnerToy(models.Model):
    _description = 'Partner Toy'
    _inherit = ['mail.thread','mail.activity.mixin', 'image.mixin']
    _name = "toy.partner"

    name = fields.Char(index=True)
    ref = fields.Char(string='Mã khách hàng', index=True)
    vat = fields.Char(string='Mã số thuế', index=True)
    bank_id = fields.Char( string='Số tài khoản')
    bank_name = fields.Char(string='Chủ tài khoản')
    bank = fields.Char(string='Ngân hàng')
    website = fields.Char('Link website')
    comment = fields.Text(string='Ghi chú')
    active = fields.Boolean(default=True)
    street = fields.Char("Địa chỉ")
    email = fields.Char("Email")
    phone = fields.Char(string="Số điện thoại")
    mobile = fields.Char(string="Số di dộng")
    industry_id = fields.Many2one('toy.industry', 'Ngành nghề')
    company_type = fields.Selection(selection=[('customer','Khách hàng'), ('supplier','Nhà cung cấp')],required=True, string="Kiểu đối tác", default="customer")
    color = fields.Integer(string='Color Index', default=0)


class IndustryToy(models.Model):
    _description = 'Industry Toy'
    _name = "toy.industry"
    _order = "name"

    name = fields.Char('Tên ngành', translate=True)
    full_name = fields.Char('Tên đầy đủ của ngành', translate=True)
    active = fields.Boolean('Active', default=True)

