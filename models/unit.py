from odoo import models, fields, api

class Unit(models.Model):
    _name = "toy.unit"
    _description = "Product Category"


    name = fields.Char(string="Tên Đơn Vị")
    description = fields.Text(string="Description")
