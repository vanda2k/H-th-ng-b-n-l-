from odoo import models, fields, api


class InventoryToy(models.Model):
    _name = "toy.inventory"
    _description = "Toy Inventory"
    _inherit = ['mail.thread']


    name = fields.Char('Tên kho', required=True, track_visibility="always")
    active = fields.Boolean("Active", default=True)
    manager_id = fields.Many2one("toy.employee", string="Người quản lý", tracking=True)
    note = fields.Text("Ghi chú")
    color = fields.Integer("Color Index")
