from openerp import models, fields, api
from openerp.exceptions import ValidationError

class stock_picking_type(models.Model):

    _inherit = 'stock.picking.type'

    is_direct_transfer = fields.Boolean('Direct Transfer ?', default=False)

class stock_picking(models.Model):

    _inherit = 'stock.picking'
    def create(self, vals):
    	pass