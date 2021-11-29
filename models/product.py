from odoo import api, fields, models, _
from odoo.tools.float_utils import float_round
from datetime import datetime

class Product(models.Model):
    _name = "toy.product"
    _description = "Product about Toys"
    _inherit = ['mail.thread','mail.activity.mixin', 'image.mixin']


    name = fields.Char(string="Tên sản phẩm", required=True, index= True, translate= True, track_visibility="always")
    active = fields.Boolean("Active",default=True)
    sequence = fields.Integer(string="STT", default=1, help="Gives the sequence order when displaying a product list")
    description = fields.Text(string="Mô tả",transalte=True, track_visibility="onchange")
    category_id = fields.Many2one(comodel_name="toy.category", string="Loại mặt hàng")
    expiry_date = fields.Datetime(string="Hạn Sử Dụng")
    date_of_manufacture = fields.Datetime(string="Ngày sản xuất")
    barcode = fields.Integer(string="Mã Vạch")
    sale_price = fields.Float(string="Giá bán", default=1.0, digits="Product Price",
                              help="Price at which the product is sold to customers")
    volume = fields.Float("Volume", digits="Volume", store="True")
    weight = fields.Float("Weight", digits="Stock Weight", store="True")
    unit_id = fields.Many2one(comodel_name="toy.unit", string="Đơn Vị Tính")
    internal_code = fields.Char("Mã sản phẩm", store="True", required=True)


    #Muahang
    purchased_product_qty = fields.Float(compute="_compute_purchase_product_qty",string="Số lượng đã mua")
    picked_product_qty = fields.Float(compute="_compute_pick_product_qty",string="Số lượng đã nhâp")

    def _compute_purchase_product_qty(self):
        domain = [('order_id.state','in',['approved']),('product_id','in',self.ids)]
        order_lines = self.env['toy.purchase.order.line'].read_group(domain, ['product_id', 'product_qty'], ['product_id'])
        purchased_data = dict([(data['product_id'][0],data['product_qty']) for data in order_lines])
        for product in self:
            product.purchased_product_qty = float_round(purchased_data.get(product.id, 0), precision_rounding=2)


    def _compute_pick_product_qty(self):
        domain = [('order_id.state', 'in', ['picking']), ('product_id', 'in', self.ids)]
        order_lines = self.env['toy.purchase.order.line'].read_group(domain, ['product_id', 'product_picked'],
                                                                     ['product_id'])
        picked_data = dict([(data['product_id'][0], data['product_picked']) for data in order_lines])
        for product in self:
            product.picked_product_qty = float_round(picked_data.get(product.id, 0), precision_rounding=2)


    #bánhàng
    sold_product_qty = fields.Float(compute="_compute_sold_product_qty", string="Số lượng đã bán")

    def _compute_sold_product_qty(self):
        domain = [('order_id.state','in',['payed']),('product_id','in',self.ids)]
        order_lines = self.env['toy.order.line'].read_group(domain, ['product_id', 'product_qty'], ['product_id'])
        sold_data = dict([(data['product_id'][0],data['product_qty']) for data in order_lines])
        for product in self:
            product.sold_product_qty = float_round(sold_data.get(product.id, 0), precision_rounding=2)


    #cònlại
    on_hand_product = fields.Float(string="Sản phẩm còn lại",compute="_compute_on_hand_product_qty")

    def _compute_on_hand_product_qty(self):
        for product in self:
            product.on_hand_product = product.picked_product_qty - product.sold_product_qty