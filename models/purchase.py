from odoo import api, fields, models, _
from datetime import datetime,time


class PurchaseToy(models.Model):
    _name = "toy.purchase"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Purchase Toy"


    name = fields.Char('Số PO', required=True, index=True, copy=False, default='New')
    priority = fields.Selection(
        [('0', 'Bình thường'), ('1', 'Khẩn cấp')], 'Mức độ ưu tiên', default='0', index=True)
    date_order = fields.Datetime('Ngày đặt hàng', required=True, index=True, copy=False, default=fields.Datetime.now)
    date_approve = fields.Datetime('Ngày duyệt đơn hàng', index=True, copy=False)
    date_planned = fields.Datetime(
        string='Ngày dự kiến nhập hàng', index=True, copy=False, store=True, readonly=False)
    date_picking = fields.Datetime('Ngày nhập hàng', index=True, copy=False)
    picking_note = fields.Text("Ghi chú nhập hàng")
    date_payed = fields.Datetime('Ngày thanh toán', index=True, copy=False)
    payment_method = fields.Char("Phương pháp thanh toán")
    payment_note = fields.Text("Ghi chú thanh toán")
    supplier_id = fields.Many2one('toy.partner', string='Nhà cung cấp', required=True, tracking=True, domain="[('company_type','=','supplier')]")
    employee_id = fields.Many2one(
        'toy.employee', string='Nhân viên mua hàng', index=True, tracking=True)
    state = fields.Selection([
        ('purchase', 'Yêu cầu mua hàng'),
        ('approved', 'Đã mua hàng'),
        ('picking', 'Nhập hàng'),
        ('payed', 'Đã thanh toán'),
         ('cancel', 'Đã hủy')
    ], string='State', index=True, default='purchase', tracking=True)
    order_line = fields.One2many('toy.purchase.order.line', 'order_id', string='Sản phẩm', copy=True)
    notes = fields.Text('Điều khoản thanh toán')
    amount_total = fields.Integer(string='Tổng số tiền', store=True, readonly=True, compute='_amount_all')


    @api.depends('order_line.price_subtotal')
    def _amount_all(self):
        for order in self:
            amount_total = 0
            for line in order.order_line:
                amount_total += line.price_subtotal
            order.amount_total = amount_total

    def button_unlock(self):
        self.write({'state': 'purchase'})

    def button_approved(self):
        self.write({'state': 'approved','date_approve':fields.Datetime.now()})

    def button_cancel(self):
        self.write({'state': 'cancel'})

    def button_picking(self):
        self.write({'state': 'picking','date_picking':fields.Datetime.now()})

    def button_payed(self):
        self.write({'state': 'payed','date_payed':fields.Datetime.now()})



