from odoo import models, fields, api

class HelloWorld(models.Model):
    _name = 'hello.world'
    _description = 'Hello World Model'

    name = fields.Char(string='Name', required=True)

    @api.model
    def create_hello(self, name):
        hello = self.create({'name': name})
        print(f'Hello, {hello.name}!')
        return hello