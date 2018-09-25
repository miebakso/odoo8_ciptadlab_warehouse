from openerp import models, fields, api
from openerp.exceptions import ValidationError
from datetime import datetime

class stock_picking_type(models.Model):

    _inherit = 'stock.picking.type'

    is_direct_transfer = fields.Boolean('Direct Transfer ?', default=False)

class stock_picking(models.Model):

    _inherit = 'stock.picking'

    combined_date = fields.Datetime('Date', required=True, default=datetime.today())

    temp_is_direct_transfer = fields.Boolean('temp_is_direct_transfer', compute="_compute_temp_is_direct_transfer")

    @api.model
    def create(self, vals):
        optype = self.env['stock.picking.type'].browse(vals['picking_type_id'])
        optype_locsrc = optype.default_location_src_id.id
        optype_locdest = optype.default_location_dest_id.id
        product_env = self.env['product.product']
        for line in vals['move_lines']:
            product = product_env.browse(line[2]['product_id'])
            line[2]['location_id'] = optype_locsrc
            line[2]['location_dest_id'] = optype_locdest
            line[2]['name'] = product.partner_ref

        if optype.is_direct_transfer == True:
            vals['date'] = vals['min_date'] = vals['combined_date']

        inst = super(stock_picking, self).create(vals)

        if optype.is_direct_transfer == True:
            inst.action_confirm()
            inst.force_assign() #inst.action_assign()
            inst.do_transfer()

        return inst

    @api.depends('picking_type_id')
    def _compute_temp_is_direct_transfer(self):
        self.temp_is_direct_transfer = self.picking_type_id.is_direct_transfer