frappe.ui.form.on("Salary Slip", {
    start_date(frm) {
        update_working_days(frm);
    },
    end_date(frm) {
        update_working_days(frm);
    },
    refresh(frm) {
        if (frm.doc.start_date && frm.doc.end_date) {
            update_working_days(frm);
        }
    }
});

function update_working_days(frm) {
    frappe.call({
        method: "custom_payroll.api.get_working_days_sunday_only",
        args: {
            start_date: frm.doc.start_date,
            end_date: frm.doc.end_date
        },
        callback: function(r) {
            if (r.message) {
                frm.set_value("total_working_days", r.message.total_working_days || 0);
            }
        }
    });
}