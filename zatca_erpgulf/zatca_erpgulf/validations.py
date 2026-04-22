"""
ZATCA Compliance Hooks for Frappe

This file contains hook functions related to ZATCA (Zakat, Tax, and Customs Authority)
compliance for invoice processing in the Frappe system. The hooks ensure that invoices
are properly submitted, validated, and duplicated according to ZATCA requirements.

"""

from frappe import _
import frappe


def zatca_done_or_not(doc, method=None):  # pylint: disable=unused-argument
    """
    Ensures that the invoice is submitted to ZATCA before submission.
    """
    if doc.custom_zatca_status not in ("REPORTED", "CLEARED"):
        frappe.throw(_("Please send this invoice to ZATCA, before submitting"))


def before_save(doc, method=None):  # pylint: disable=unused-argument
    """
    Prevents editing, canceling, or saving of invoices that are already submitted to ZATCA.
    """
    if doc.custom_zatca_status in ("REPORTED", "CLEARED"):
        frappe.throw(
            _(
                "This invoice is already submitted to ZATCA. You cannot edit, cancel or save it."
            )
        )


def duplicating_invoice(doc, method=None):  # pylint: disable=unused-argument
    """
    Duplicates the invoice for Frappe version 13,
    where the no-copy setting on fields is not available.
    """
    if int(frappe.__version__.split(".", maxsplit=1)[0]) == 13:
        frappe.msgprint(_("Duplicating invoice"))
        doc.custom_uuid = "Not submitted"
        doc.custom_zatca_status = "Not Submitted"
        doc.save()


def validate_debit_note(doc, method=None):  # pylint: disable=unused-argument
    """
    Validates debit note constraints before submission.
    A ZATCA debit note (type 383) must reference an existing submitted invoice
    and must not itself be a return document.
    """
    if not getattr(doc, "custom_is_debit_note", 0):
        return
    if doc.is_return:
        frappe.throw(
            _("A Debit Note cannot be a return document. Uncheck 'Is Return' or 'Is Debit Note (ZATCA 383)'.")
        )
    if not doc.return_against:
        frappe.throw(
            _("'Return Against' is required for a Debit Note. Please reference the original invoice.")
        )
    original_status = frappe.db.get_value("Sales Invoice", doc.return_against, "docstatus")
    if original_status != 1:
        frappe.throw(
            _(f"The referenced invoice '{doc.return_against}' must be submitted before creating a Debit Note against it.")
        )


def test_save_validate(doc, method=None):  # pylint: disable=unused-argument
    """
    Used for testing purposes to display a message during save validation.
    """
    frappe.msgprint(_("Test save validated and stopped it here"))
