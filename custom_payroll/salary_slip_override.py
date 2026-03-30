from custom_payroll.api import get_weekday_working_days


def apply_weekday_working_days(doc, method=None):
    result = get_weekday_working_days(
        employee=doc.employee,
        company=doc.company,
        start_date=doc.start_date,
        end_date=doc.end_date,
        leave_without_pay=doc.leave_without_pay,
        absent_days=doc.absent_days
    )

    doc.total_working_days = result.get("total_working_days", 0)
    doc.payment_days = result.get("payment_days", 0)