from odoo import models, fields, api

class Position(models.Model):
    _name = "toy.position"
    _inherit=["mail.thread"]

    name = fields.Char(string="Tên công việc",required=True, index=True)
    active = fields.Boolean("Active", default=True)
    description = fields.Text(string='Mô tả công việc')
    requirements = fields.Text('Yêu cầu công việc')
    department_id = fields.Many2one('toy.department', string='Phòng ban phụ trách')
    state = fields.Selection([
        ('recruit', 'Cần tuyển dụng'),
        ('open', 'Chưa tuyển dụng')],string="State",requirdesed=True)
