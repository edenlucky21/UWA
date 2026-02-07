document.addEventListener("DOMContentLoaded", () => {

  const categorySelect = document.getElementById("categorySelect");
  const touristForm = document.getElementById("touristForm");
  const transitForm = document.getElementById("transitForm");
  const studentForm = document.getElementById("studentForm");

  // ---------- CATEGORY SWITCH ----------
  if (categorySelect) {
    categorySelect.addEventListener("change", () => {
      [touristForm, transitForm, studentForm].forEach(f => {
        if (f) f.classList.remove("active");
      });

      if (categorySelect.value === "tourist") touristForm.classList.add("active");
      if (categorySelect.value === "transit") transitForm.classList.add("active");
      if (categorySelect.value === "student") studentForm.classList.add("active");
    });
  }

  // ---------- COUNTRIES LIST ----------
  const countries = [
    "Uganda","Kenya","Tanzania","Rwanda","South Sudan",
    "United States","United Kingdom","Canada","Germany","France",
    "India","China","Japan","Australia","Brazil"
  ];

  // ---------- POPULATE NATIONALITY ----------
  function populateCountries(selectElement) {
    selectElement.innerHTML = '<option value="">--Select Nationality--</option>';
    countries.forEach(country => {
      const option = document.createElement("option");
      option.value = country;
      option.textContent = country;
      selectElement.appendChild(option);
    });
  }

  // Fill all nationality dropdowns
  document.querySelectorAll(".nationality-dropdown")
    .forEach(drop => populateCountries(drop));

});
