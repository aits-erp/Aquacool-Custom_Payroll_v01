import frappe
from frappe.utils import getdate, add_days, flt


@frappe.whitelist()
def get_weekday_working_days(employee=None, company=None, start_date=None, end_date=None, leave_without_pay=0, absent_days=0):
    """
    Calculate working days by excluding ONLY Sundays.
    Example:
    - 31 days month with 4 Sundays => 27 working days
    - Payment Days = Working Days - Leave Without Pay - Absent Days
    """

    if not start_date or not end_date:
        return {
            "total_working_days": 0,
            "payment_days": 0
        }

    start_date = getdate(start_date)
    end_date = getdate(end_date)

    total_working_days = 0
    current_date = start_date

    while current_date <= end_date:
        # Monday=0 ... Saturday=5, Sunday=6
        if current_date.weekday() != 6:
            total_working_days += 1

        current_date = add_days(current_date, 1)

    payment_days = flt(total_working_days) - flt(leave_without_pay) - flt(absent_days)

    if payment_days < 0:
        payment_days = 0

    return {
        "total_working_days": total_working_days,
        "payment_days": payment_days
    }