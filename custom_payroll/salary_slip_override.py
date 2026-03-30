from custom_payroll.api import get_working_days_sunday_only


def apply_working_days_only(doc, method=None):
    if not doc.start_date or not doc.end_date:
        return

    result = get_working_days_sunday_only(
        start_date=doc.start_date,
        end_date=doc.end_date
    )

    doc.total_working_days = result.get("total_working_days", 0)