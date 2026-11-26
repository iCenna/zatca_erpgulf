from unittest import TestCase
from unittest.mock import Mock, call, patch

import frappe

from zatca_erpgulf import migrate


class TestSalesInvoiceMigration(TestCase):
    def test_restores_positions_overwritten_by_icenna(self):
        old_positions = {
            "custom_zatca_third_party_invoice": "naming_series",
            "custom_b2c": "customer",
            "custom_is_debit_note": "custom_self_billed_invoice",
            "custom_zatca_status": "due_date",
            "custom_uuid": "tax_id",
            "custom_zatca_tax_category": "custom_zatca_status",
        }
        fixture = frappe.get_file_json(
            frappe.get_app_path("zatca_erpgulf", "fixtures", "custom_field.json")
        )
        fields = {
            row["name"]: frappe._dict(row) for row in fixture if row["dt"] == "Sales Invoice"
        }
        expected_updates = []
        for fieldname, old_position in old_positions.items():
            field = fields[f"Sales Invoice-{fieldname}"]
            expected_updates.append(
                call("Custom Field", field.name, "insert_after", field.insert_after)
            )
            field.insert_after = old_position

        def set_value(doctype, name, property_name, value):
            fields[name][property_name] = value

        with patch.object(migrate, "frappe", wraps=frappe) as framework:
            framework.get_all.return_value = list(fields.values())
            framework.db = Mock()
            framework.clear_cache.return_value = None
            framework.db.set_value.side_effect = set_value

            migrate.restore_sales_invoice_zatca_options()
            self.assertCountEqual(framework.db.set_value.call_args_list, expected_updates)
            framework.clear_cache.assert_called_once_with(doctype="Sales Invoice")

            migrate.restore_sales_invoice_zatca_options()
            self.assertCountEqual(framework.db.set_value.call_args_list, expected_updates)
            framework.clear_cache.assert_called_once_with(doctype="Sales Invoice")
