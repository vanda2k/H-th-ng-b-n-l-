from odoo import api, fields, models, _

class PurchaseOrderLineToy(models.Model):
    _name = 'toy.purchase.order.line'
    _description = 'Purchase Order Line Toy'

    order_id = fields.Many2one('toy.purchase', string='Phiếu mua hàng', index=True, required=True, ondelete='cascade')
    product_id = fields.Many2one('toy.product', string="Tên sản phẩm")
    product_name = fields.Char(related="product_id.name", string="Tên sản phẩm")
    product_unit = fields.Many2one('toy.unit', related="product_id.unit_id", string='Đơn vị')
    sequence = fields.Integer(string='STT', default=10)
    name = fields.Char(string='Nội dung')
    product_qty = fields.Integer(string='Số lượng yêu cầu', digits='Product Unit of Measure', required=True)
    product_type = fields.Many2one(related='product_id.category_id', readonly=True, string="Loại mặt hàng")
    price_unit = fields.Float(string='Đơn giá', required=True)
    price_subtotal = fields.Integer(string='Tổng tiền', store=True)

    #đơn hàng
    state = fields.Selection(related='order_id.state', store=True, readonly=False, string="Trạng thái")
    supplier_id = fields.Many2one('toy.partner', related='order_id.supplier_id', string='Nhà cung cấp', readonly=True, store=True)
    date_order = fields.Datetime(related='order_id.date_order', string='Ngày đặt hàng', readonly=True)

    #nhập hàng
    product_picked = fields.Integer('Số lượng nhập hàng',digits='Product Unit of Measure')
    product_pick_plan = fields.Integer("Số lượng còn phải nhập",digits='Product Unit of Measure')

    @api.onchange('product_qty','price_unit')
    def onchange_qty_amount(self):
        if self.product_qty and self.price_unit:
            self.price_subtotal = self.price_unit * self.product_qty

    @api.onchange('product_qty', 'product_picked')
    def onchange_qty_picked(self):
        if self.product_qty and self.product_picked:
            self.product_pick_plan = self.product_qty - self.product_picked