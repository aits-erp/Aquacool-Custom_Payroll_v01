frappe.ui.form.on("Salary Slip", {
    start_date(frm) {
        update_salary_days(frm);
    },
    end_date(frm) {
        update_salary_days(frm);
    },
    absent_days(frm) {
        update_salary_days(frm);
    },
    leave_without_pay(frm) {
        update_salary_days(frm);
    },
    refresh(frm) {
        if (frm.doc.start_date && frm.doc.end_date) {
            update_salary_days(frm);
        }
    }
});

function update_salary_days(frm) {
    if (!frm.doc.start_date || !frm.doc.end_date) return;

    frappe.call({
        method: "custom_payroll.api.get_salary_days",
        args: {
            start_date: frm.doc.start_date,
            end_date: frm.doc.end_date,
            absent_days: frm.doc.absent_days || 0,
            leave_without_pay: frm.doc.leave_without_pay || 0
        },
        callback: function (r) {
            if (r.message) {
                frm.set_value("total_working_days", r.message.total_working_days || 0);
                frm.set_value("absent_days", r.message.absent_days || 0);
                frm.set_value("payment_days", r.message.payment_days || 0);
            }
        }
    });
}