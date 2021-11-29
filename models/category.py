from odoo import models, fields, api


class Category(models.Model):
    _name = "toy.category"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']

    name = fields.Char(string="Loại mặt hàng")
    description = fields.Text(string="Description")
    product_ids = fields.One2many(comodel_name="toy.product", inverse_name="category_id", string="Tên Sản Phẩm",readonly=True)
    product_count = fields.Integer("Product Count", compute="get_product_count", helps = "The number of products under this category")

    @api.depends('product_ids')
    def get_product_count(self):
        for category in self:
            category.product_count = len(category.product_ids)
