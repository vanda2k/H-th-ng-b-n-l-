from odoo import models, fields, api



class EmployeeToy(models.Model):
    _name = "toy.employee"
    _description = "Toy Employee"
    _inherit = ['mail.thread','mail.activity.mixin','image.mixin']


    name = fields.Char('Tên nhân viên', required=True, track_visibility="always")
    active = fields.Boolean("Active", default=True)
    color = fields.Integer("Color Index", default=0)
    job_id = fields.Many2one("toy.position","Vị trí công việc", tracking=True)
    department_id = fields.Many2one('toy.department', string='Tên phòng ban')
    address = fields.Char("Nơi ở")
    work_phone = fields.Char("Số điện thoại", store=True)
    work_email = fields.Char("Email")
    user_id = fields.Many2one("res.users")
    date_of_birth = fields.Date(string="Ngày Sinh")
    gender = fields.Selection(selection=[("1", "Nam"), ("2", "Nữ")], string="Giới Tính", required=True)
    identity_card = fields.Integer(string="CMND/CCCD")
    date_maternity = fields.Date("Ngày nghỉ thai sản")
    duration_maternity = fields.Integer("Thời gian nghỉ thai sản")
    date_layoff = fields.Date("Ngày nghỉ việc")
    state = fields.Selection([('0','Đang làm việc'),('1','Nghỉ thai sản'),('2','Nghỉ phép'),('3','Nghỉ việc')],string="State",index=True, default='0', tracking=True)

    def button_work(self):
        self.write({'state': '0'})

    def button_maternity(self):
        self.write({'state': '1', 'date_maternity': fields.Datetime.now()})

    def button_leave(self):
        self.write({'state': '2'})

    def button_layoff(self):
        self.write({'state': '3','date_layoff': fields.Datetime.now()})



