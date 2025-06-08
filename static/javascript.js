
// FOR LOGIN / SIGNUP
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
	document
		.querySelectorAll(".form-box")
		.forEach((form) => form.classList.remove("active"));
	document.getElementById(formId)?.classList.add("active");
}

// FOR STAR RATING
const score = document.querySelector(".score");
const ratings = document.querySelectorAll(".rating input");

ratings.forEach((rating) => {
	rating.addEventListener("change", () => {
		const selectedRating = rating.value;
		const text = selectedRating == 1 ? "star" : "stars";
		if (score) score.textContent = `${selectedRating}`;
	});
});

// FEEDBACK POP-UP
const feedbackButtons = document.querySelectorAll(".feedback-bttn");
const modal = document.querySelector(".feedback-modal");
const closeBtn = document.querySelector(".feedback-modal-close");
const cancelBtn = document.querySelector(".cancel-bttn");
const organizerNameField = document.querySelector(
	".feedback-modal-form .organizer-name"
);

feedbackButtons.forEach((button) => {
	button.addEventListener("click", () => {
		const organizerName =
			button.previousElementSibling?.textContent || "Organizer";
		if (organizerNameField) organizerNameField.textContent = organizerName;
		modal?.classList.add("active");
	});
});

closeBtn?.addEventListener("click", () => {
	modal?.classList.remove("active");
});

cancelBtn?.addEventListener("click", () => {
	modal?.classList.remove("active");
});

document
	.querySelector(".feedback-modal-overlay")
	?.addEventListener("click", () => {
		modal?.classList.remove("active");
	});

// FOR CHECKBOX IN REQUEST FORM
document
	.querySelectorAll('.request-item input[type="checkbox"]')
	.forEach((cb) => {
		cb.addEventListener("change", function () {
			const numberInput = this.closest(".request-item")?.querySelector(
				'input[type="number"]'
			);
			if (numberInput) {
				numberInput.disabled = !this.checked;
				if (!this.checked) numberInput.value = "";
			}
			console.log(
				`${this.id} toggled. Number input is now ${
					numberInput?.disabled ? "disabled" : "enabled"
				}`
			);
		});
	});
