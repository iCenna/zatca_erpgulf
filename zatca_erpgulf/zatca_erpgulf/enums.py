from enum import Enum


class RefundReason(Enum):
    CANCEL_OR_SUSPEND = (
        1,
        "Cancellation or suspension of the supplies after its occurrence either wholly or partially",
        "تم إلغاء أو وقف التوريد بعد حدوثه أو اعتباره كلياً أو جزئياً"
    )
    PRICE_CHANGE = (
        2,
        "Essential change or amendment in the supply leading to a VAT change",
        "وجود تغيير أو تعديل جوهري في طبيعة التوريد بحيث يؤدي الى تغيير الضريبة المستحقة"
    )
    SUPPLY_VALUE_CHANGE = (
        3,
        "Amendment of the supply value pre-agreed between supplier and consumer",
        "تم الاتفاق على تعديل قيمة التوريد مسبقاً"
    )
    RETURN_ITEMS = (
        4,
        "Goods or services refund",
        "عند ترجيع السلع أو الخدمات"
    )
    PARTIES_DATA_CHANGE = (
        5,
        "Change in seller's or buyer's information",
        "عند التعديل على بيانات المورد أو المشتري"
    )

    def __new__(cls, value, english_description, arabic_description):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.english_description = english_description
        obj.arabic_description = arabic_description
        return obj


def get_refund_reason_description(code):
    """Return the English description for a RefundReason code.

    Accepts bare digits ("1") or the full label stored by the Select field
    ("1 - Cancellation or suspension...").  Falls back to reason 1 text.
    """
    try:
        numeric = int(str(code).strip()[0])
        return RefundReason(numeric).english_description
    except (ValueError, KeyError, TypeError, IndexError):
        return RefundReason.CANCEL_OR_SUSPEND.english_description


def get_select_options():
    """Return newline-separated option strings for the Frappe Select field."""
    return "\n".join(
        f"{r.value} - {r.english_description}" for r in RefundReason
    )
