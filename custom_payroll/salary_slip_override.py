from custom_payroll.api import get_salary_days


def apply_working_days_only(doc, method=None):
    if not doc.start_date or not doc.end_date:
        return

    result = get_salary_days(
        start_date=doc.start_date,
        end_date=doc.end_date,
        absent_days=doc.absent_days or 0,
        leave_without_pay=doc.leave_without_pay or 0
    )

    doc.total_working_days = result.get("total_working_days", 0)
    doc.absent_days = result.get("absent_days", 0)
    doc.payment_days = result.get("payment_days", 0)