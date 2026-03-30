import frappe
from frappe.utils import getdate, add_days, flt


@frappe.whitelist()
def get_salary_days(start_date=None, end_date=None, absent_days=0, leave_without_pay=0):
    """
    Calculate:
    - total_working_days = total days excluding only Sundays
    - payment_days = total_working_days - absent_days - leave_without_pay

    Does not change absent_days on its own; it uses the value passed in.
    """

    if not start_date or not end_date:
        return {
            "total_working_days": 0,
            "absent_days": flt(absent_days),
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

    absent_days = flt(absent_days)
    leave_without_pay = flt(leave_without_pay)

    payment_days = total_working_days - absent_days - leave_without_pay
    if payment_days < 0:
        payment_days = 0

    return {
        "total_working_days": total_working_days,
        "absent_days": absent_days,
        "payment_days": payment_days
    }