from odoo import models, fields, api


class DepartmentToy(models.Model):
    _name = "toy.department"
    _description = "Toy Department"
    _inherit = ['mail.thread']


    name = fields.Char('Tên phòng ban', required=True, track_visibility="always")
    active = fields.Boolean("Active", default=True)
    manager_id = fields.Many2one("toy.employee", string="Người quản lý", tracking=True)
    note = fields.Text("Ghi chú")
    color = fields.Integer("Color Index")







