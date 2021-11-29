from odoo import api, fields, models, _
from datetime import datetime



class PosSessionToy(models.Model):
    _name = 'toy.session'
    _order = 'id desc'
    _description = 'Point of Sale Session Toy'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Session Name', required=True )
    employee_id = fields.Many2one("toy.employee", string= 'Nhân viên phụ trách' )
    start_at = fields.Datetime(string='Thời gian mở phiên', default=fields.Datetime.now)
    stop_at = fields.Datetime(string='Thời gian đóng phiên')
    state = fields.Selection([
        ('open', 'Mở phiên bán hàng'),
        ('close', 'Đóng phiên bán hàng')], default="open")
    order_ids = fields.One2many(comodel_name="toy.order", inverse_name="session_id", string="Đơn đặt hàng",
                                  readonly=True)
    order_count = fields.Integer("Order Count", compute="get_order_count",
                                   helps="The number of Oder under this session")

    @api.depends('order_ids')
    def get_order_count(self):
        for order in self:
            order.order_count = len(order.order_ids)


    def button_close(self):
        self.write({'state': 'close','stop_at':fields.Datetime.now()})