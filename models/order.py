from odoo import api, fields, models, _
from datetime import datetime,time


class OrderToy(models.Model):
    _name = "toy.order"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Order Toy"


    name = fields.Char('Số SO', related="session_id.name",index=True, copy=False)
    priority = fields.Selection(
        [('0', 'Bình thường'), ('1', 'Khẩn cấp')], 'Mức độ ưu tiên', default='0', index=True)
    date_order = fields.Datetime('Ngày đặt hàng', required=True, index=True, copy=False, default=fields.Datetime.now)
    order_note = fields.Text("Ghi chú bán hàng")
    payment_method = fields.Char("Phương pháp thanh toán")
    customer_id = fields.Many2one('toy.partner', string='Khách hàng', tracking=True, domain="[('company_type','=','customer')]")
    session_id = fields.Many2one("toy.session", string="Ca")
    employee_id = fields.Many2one( related="session_id.employee_id", string='Nhân viên bán hàng', index=True, tracking=True)
    state = fields.Selection([
        ('sale', 'Đang bán hàng'),
        ('payed', 'Đã thanh toán')
    ], string='State', index=True, default='sale', tracking=True)
    order_line = fields.One2many('toy.order.line', 'order_id', string='Sản phẩm', copy=True)
    amount_total = fields.Integer(string='Tổng số tiền', store=True, readonly=True, compute='_amount_all')
    paid_by_customer = fields.Integer(string='Khách hàng trả', store=True)
    amount_remain = fields.Integer(string='Số tiền còn lại', store=True)

    @api.depends('order_line.price_subtotal')
    def _amount_all(self):
        for order in self:
            amount_total = 0
            for line in order.order_line:
                amount_total += line.price_subtotal
            order.amount_total = amount_total

    @api.onchange('paid_by_customer', 'amount_total')
    def onchange_price_paid(self):
        if self.amount_total and self.paid_by_customer:
            self.amount_remain = self.paid_by_customer - self.amount_total


class OrderLineToy(models.Model):
    _name = 'toy.order.line'
    _description = 'Order Line Toy'

    order_id = fields.Many2one('toy.order', string='Số SO', index=True, required=True, ondelete='cascade')
    product_id = fields.Many2one('toy.product', string="Tên sản phẩm")
    product_unit = fields.Many2one('toy.unit', related="product_id.unit_id", string='Đơn vị')
    sequence = fields.Integer(string='STT', default=10)
    product_qty = fields.Integer(string='Số lượng bán', digits='Product Unit of Measure', required=True)
    price_unit = fields.Float(string='Đơn giá',related="product_id.sale_price", required=True, readonly=True)
    price_subtotal = fields.Integer(string='Tổng tiền', store=True)

    #đơn hàng
    state = fields.Selection(related='order_id.state', store=True, readonly=False, string="Trạng thái")
    customer_id = fields.Many2one('toy.partner', related='order_id.customer_id', string='Khách hàng', readonly=True, store=True)
    date_order = fields.Datetime(related='order_id.date_order', string='Ngày đặt hàng', readonly=True)


    @api.onchange('product_qty','price_unit')
    def onchange_qty_amount(self):
        if self.product_qty and self.price_unit:
            self.price_subtotal = self.price_unit * self.product_qty



