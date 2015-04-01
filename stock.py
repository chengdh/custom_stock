#coding: utf-8
#重写stock.picking,添加单价和金额
from openerp.osv import fields, osv
import math
from datetime import datetime
from openerp.tools.translate import _
import openerp.tools as tools
import openerp.addons.decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)

class stock_picking(osv.osv):
  '''
  库存调拨
  '''
  _name = "stock.picking"
  _inherit = 'stock.picking'
  _description = "stock picking custom"

  def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
    res = {}
    for picking in self.browse(cr, uid, ids, context=context):
      val = 0.0
      for line in picking.move_lines:
        val += line.price_subtotal

      res[picking.id] = val

    return res

  _columns = {
    'amount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total'),
      }

class stock_move(osv.osv):
  '''
  库存移动明细
  '''

  _name = "stock.move"
  _inherit = 'stock.move'
  _description = "Stock Move custom"

  def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
    res = {}
    if context is None:
      context = {}

    for line in self.browse(cr, uid, ids, context=context):
      res[line.id] = line.price_unit*line.product_qty

    return res


  _columns = {
        'price_unit': fields.float('Unit Price', digits_compute= dp.get_precision('Product Price')),
        'price_subtotal': fields.function(_amount_line, string='Subtotal', digits_compute= dp.get_precision('Account')),
      }

  _defaults = {
      'price_unit' : 0,
      }

 
