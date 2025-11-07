from odoo import models, fields

class HelloWorld(models.Model):
    _name = 'hello.world'
    _description = 'Hello World Model'

    name = fields.Char(string='Name', required=True)

    def action_say_hello(self):
        for record in self:
            print(f"Hello, {record.name or 'World'}!")
