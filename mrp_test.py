from odoo.tests.common import TransactionCase

class MrpTest(TransactionCase):
    def setUp(self):
        super(MrpTest, self).setUp()
        # Create test product
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'product',
            'detailed_type': 'product',
            'list_price': 100,
            'route_ids': [(6, 0, [self.env.ref('stock.route_warehouse0_mto').id,
                                  self.env.ref('mrp.route_warehouse0_manufacture').id])],
        })
        # Create Work Centers
        self.work_center1 = self.env['mrp.workcenter'].create({
            'name': 'Test Work Center 1',
            'time_start': 10,
            'time_stop': 10,
            'costs_hour': 10,
        })
        self.work_center2 = self.env['mrp.workcenter'].create({
            'name': 'Test Work Center 2',
            'time_start': 10,
            'time_stop': 10,
            'costs_hour': 10,
        })
        # Create BOM for the product
        self.component_product = self.env['product.product'].create({
            'name': 'Test Component',
            'type': 'product',
            'uom_id': self.env.ref('uom.product_uom_unit').id,
        })
        self.bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'product_qty': 1,
            'bom_line_ids': [(0, 0, {
                'product_id': self.component_product.id,
                'product_qty': 1,
            })]
        })
        # Create Routing
        self.routing_workcenter1 = self.env['mrp.routing.workcenter'].create({
            'name': 'Test Work Order 1',
            'workcenter_id': self.work_center1.id,
            'time_cycle': 60,
            'bom_id': self.bom.id,
        })
        self.routing_workcenter2 = self.env['mrp.routing.workcenter'].create({
            'name': 'Test Work Order 2',
            'workcenter_id': self.work_center2.id,
            'time_cycle': 60,
            'bom_id': self.bom.id,
        })
        # Ensure stock availability for components
        self.env['stock.quant']._update_available_quantity(
            self.component_product,
            self.env.ref('stock.stock_location_stock'),
            1000
        )
        # Create production orders
        self.production_order1 = self.env['mrp.production'].create({
            'name': 'Test Production Order 1',
            'product_id': self.product.id,
            'product_qty': 10,
            'bom_id': self.bom.id,
            'state': 'draft',
        })
        self.production_order2 = self.env['mrp.production'].create({
            'name': 'Test Production Order 2',
            'product_id': self.product.id,
            'product_qty': 20,
            'bom_id': self.bom.id,
            'state': 'draft',
        })
        self.production_order3 = self.env['mrp.production'].create({
            'name': 'Test Production Order 3',
            'product_id': self.product.id,
            'product_qty': 30,
            'bom_id': self.bom.id,
            'state': 'draft',
        })
