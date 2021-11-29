from odoo import api, fields, models, _
from datetime import datetime,time


class PickingToy(models.Model):
    _name = "toy.picking"
    _inherit = ['mail.thread','mail.activity.mixin']
    _description = "Picking Toy"


    name = fields.Char('Số Phiếu Nhập', required=True, index=True, copy=False, default='New')
    purchase_id = fields.Many2one(
        'toy.purchase', string='Phiếu mua hàng', index=True, tracking=True)
    priority = fields.Selection(
        [('0', 'Bình thường'), ('1', 'Khẩn cấp')], 'Mức độ ưu tiên', default='0', index=True)
    date_create = fields.Datetime('Ngày lập phiếu', required=True, index=True, copy=False)
    date_picking = fields.Datetime('Ngày nhập hàng', required=True, index=True, copy=False)
    date_planned = fields.Datetime( realated="purchase_id.date_planned",
        string='Ngày dự kiến nhập hàng', index=True, readonly='1')
    supplier_id = fields.Many2one( realated="purchase_id.supplier_id", string='Nhà cung cấp', required=True, tracking=True)
    employee_id = fields.Many2one(
        'toy.employee', string='Nhân viên nhập hàng', index=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('waiting', 'Đợi nhập hàng'),
        ('done', 'Đã nhập hàng')
    ], string='State', index=True, default='draft', tracking=True)
    picking_line = fields.One2many('toy.picking.line', 'picking_id', string='Sản phẩm', copy=True)
    notes = fields.Text('Ghi chú sản phẩm')
    amount_total = fields.Integer(string='Tổng số tiền', store=True, readonly=True, compute='_amount_all')


    @api.depends('order_line.price_subtotal')
    def _amount_all(self):
        for picking in self:
            amount_total = 0
            for line in  picking.picking_line:
                amount_total += line.price_subtotal
            picking.amount_total = amount_total

    def button_draft(self):
        self.write({'state': 'draft'})

    def button_waiting(self):
        self.write({'state': 'waiting','date_create': fields.Datetime.now()})

    def button_done(self):
        self.write({'state': 'done'})

class PickingLineToy(models.Model):
    _name = 'toy.picking.line'
    _description = 'Picking Line Toy'

    picking_id = fields.Many2one('toy.picking', string='Phiếu nhập hàng', index=True, required=True, ondelete='cascade')
    product_id = fields.Many2one('toy.product', string="Product")
    product_unit = fields.Many2one('toy.unit', related="product_id.unit_id", string='Đơn vị')
    sequence = fields.Integer(string='STT', default=10)
    name = fields.Char(string='Nội dung')
    # product_request = fields.Integer(related="product_id.order_line_id", digits='Product Unit of Measure', required=True)
    product_qty = fields.Integer(string='Số lượng nhập', digits='Product Unit of Measure', required=True)
    product_type = fields.Many2one(related='product_id.category_id', readonly=True, string="Loại mặt hàng")
    price_unit = fields.Float(string='Đơn giá', required=True)
    price_subtotal = fields.Integer(string='Tổng tiền', store=True)

    state = fields.Selection(related='order_id.state', store=True, readonly=False)
    supplier_id = fields.Many2one('toy.partner', related='order_id.supplier_id', string='Nhà cung cấp', readonly=True, store=True)
    date_order = fields.Datetime(related='order_id.date_order', string='Ngày đặt hàng', readonly=True)


    @api.onchange('product_qty','price_unit')
    def onchange_qty_amount(self):
        if self.product_qty and self.price_unit:
            self.price_subtotal = self.price_unit * self.product_qty

