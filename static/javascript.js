document.addEventListener("DOMContentLoaded", function () {
    const roleSelect = document.getElementById("role");
    const repFields = document.getElementById("representative-extra-fields");

    roleSelect.addEventListener("change", function () {
        if (roleSelect.value === "representative") {
            repFields.style.display = "block";
        } else {
            repFields.style.display = "none";
        }
    });
});

function showForm(formId) {
	document.querySelectorAll(".form-box").forEach((form) => form.classList.remove("active"));
	document.getElementById(formId).classList.add("active");
}
