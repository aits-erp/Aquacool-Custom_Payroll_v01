frappe.ui.form.on("Salary Slip", {
    employee(frm) {
        calculate_weekday_working_days(frm);
    },
    company(frm) {
        calculate_weekday_working_days(frm);
    },
    start_date(frm) {
        calculate_weekday_working_days(frm);
    },
    end_date(frm) {
        calculate_weekday_working_days(frm);
    },
    leave_without_pay(frm) {
        calculate_weekday_working_days(frm);
    },
    absent_days(frm) {
        calculate_weekday_working_days(frm);
    },
    refresh(frm) {
        if (frm.doc.start_date && frm.doc.end_date) {
            calculate_weekday_working_days(frm);
        }
    }
});

function calculate_weekday_working_days(frm) {
    if (!frm.doc.start_date || !frm.doc.end_date) return;

    frappe.call({
        method: "custom_payroll.api.get_weekday_working_days",
        args: {
            employee: frm.doc.employee,
            company: frm.doc.company,
            start_date: frm.doc.start_date,
            end_date: frm.doc.end_date,
            leave_without_pay: frm.doc.leave_without_pay || 0,
            absent_days: frm.doc.absent_days || 0
        },
        callback: function (r) {
            if (r.message) {
                frm.set_value("total_working_days", r.message.total_working_days || 0);
                frm.set_value("payment_days", r.message.payment_days || 0);
            }
        }
    });
}