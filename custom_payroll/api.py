import frappe
from frappe.utils import getdate, add_days, flt


@frappe.whitelist()
def get_weekday_working_days(employee=None, company=None, start_date=None, end_date=None, leave_without_pay=0, absent_days=0):
    """
    Count only weekdays (Mon-Fri) between start_date and end_date.
    Exclude holidays from Employee Holiday List or Company Default Holiday List.
    """

    if not start_date or not end_date:
        return {
            "total_working_days": 0,
            "payment_days": 0,
            "holiday_list": None,
            "holidays": []
        }

    start_date = getdate(start_date)
    end_date = getdate(end_date)

    holiday_list = get_applicable_holiday_list(employee, company)
    holiday_dates = get_holiday_dates(holiday_list, start_date, end_date)

    total_working_days = 0
    current_date = start_date

    while current_date <= end_date:
        # Monday = 0, Sunday = 6
        if current_date.weekday() < 5 and current_date not in holiday_dates:
            total_working_days += 1
        current_date = add_days(current_date, 1)

    payment_days = flt(total_working_days) - flt(leave_without_pay) - flt(absent_days)
    if payment_days < 0:
        payment_days = 0

    return {
        "total_working_days": total_working_days,
        "payment_days": payment_days,
        "holiday_list": holiday_list,
        "holidays": [str(d) for d in sorted(holiday_dates)]
    }


def get_applicable_holiday_list(employee=None, company=None):
    holiday_list = None

    if employee:
        holiday_list = frappe.db.get_value("Employee", employee, "holiday_list")

    if not holiday_list and company:
        holiday_list = frappe.db.get_value("Company", company, "default_holiday_list")

    return holiday_list


def get_holiday_dates(holiday_list, start_date, end_date):
    if not holiday_list:
        return set()

    holidays = frappe.get_all(
        "Holiday",
        filters={
            "parent": holiday_list,
            "holiday_date": ["between", [start_date, end_date]]
        },
        fields=["holiday_date"]
    )

    return {getdate(row.holiday_date) for row in holidays}