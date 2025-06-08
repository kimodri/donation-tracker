
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
	document.getElementById(formId).classList.add("active");
}

// FOR STAR RTING
const score = document.querySelector(".score");
const ratings = document.querySelectorAll(".rating input");

ratings.forEach((rating) => {
	rating.addEventListener("change", () => {
		const selectedRating = rating.value;
		const text = selectedRating == 1 ? "star" : "stars";
		score.textContent = `${selectedRating}`;
	});
});

// FEEDBACK PUP UP

const feedbackButtons = document.querySelectorAll(".feedback-bttn");
const modal = document.querySelector(".feedback-modal");
const closeBtn = document.querySelector(".feedback-modal-close");
const cancelBtn = document.querySelector(".cancel-bttn");
const organizerNameField = document.querySelector(
	".feedback-modal-form .organizer-name"
);

feedbackButtons.forEach((button) => {
	button.addEventListener("click", () => {
		const organizerName = button.previousElementSibling.textContent;
		organizerNameField.textContent = organizerName;
		modal.classList.add("active");
	});
});

closeBtn.addEventListener("click", () => {
	modal.classList.remove("active");
});

cancelBtn.addEventListener("click", () => {
	modal.classList.remove("active");
});

// Optional: Close modal when clicking outside content
document
	.querySelector(".feedback-modal-overlay")
	.addEventListener("click", () => {
		modal.classList.remove("active");
	});
