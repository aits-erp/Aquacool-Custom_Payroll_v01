import frappe
from frappe.utils import getdate, add_days


@frappe.whitelist()
def get_working_days_sunday_only(start_date=None, end_date=None):
    """
    Only calculate Working Days
    Exclude ONLY Sundays
    Do NOT touch payment_days
    """

    if not start_date or not end_date:
        return {
            "total_working_days": 0
        }

    start_date = getdate(start_date)
    end_date = getdate(end_date)

    total_working_days = 0
    current_date = start_date

    while current_date <= end_date:
        # Exclude Sunday only
        if current_date.weekday() != 6:
            total_working_days += 1

        current_date = add_days(current_date, 1)

    return {
        "total_working_days": total_working_days
    }