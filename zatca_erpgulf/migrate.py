import frappe


def restore_sales_invoice_zatca_options():
    """Restore the fixture's field positions after iCenna syncs its customizations."""
    doctype = "Sales Invoice"
    fields_to_restore = {
        "custom_zatca_third_party_invoice",
        "custom_b2c",
        "custom_is_debit_note",
        "custom_zatca_status",
        "custom_uuid",
        "custom_zatca_tax_category",
    }
    fixture = frappe.get_file_json(
        frappe.get_app_path("zatca_erpgulf", "fixtures", "custom_field.json")
    )
    positions = {
        field["fieldname"]: field["insert_after"]
        for field in fixture
        if field["dt"] == doctype and field["fieldname"] in fields_to_restore
    }
    required_fields = fields_to_restore | set(positions.values())
    current_fields = {
        field.fieldname: field
        for field in frappe.get_all(
            "Custom Field",
            filters={"dt": doctype, "fieldname": ["in", sorted(required_fields)]},
            fields=["name", "fieldname", "insert_after"],
        )
    }
    if not required_fields <= current_fields.keys():
        return

    changes = {
        current_fields[fieldname].name: insert_after
        for fieldname, insert_after in positions.items()
        if current_fields[fieldname].insert_after != insert_after
    }
    for name, insert_after in changes.items():
        frappe.db.set_value("Custom Field", name, "insert_after", insert_after)
    if changes:
        frappe.clear_cache(doctype=doctype)
