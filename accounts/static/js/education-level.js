document.addEventListener("DOMContentLoaded", () => {
  const levelBtns = document.querySelectorAll('.level-btn');
  const gradeLevelSelect = document.getElementById('gradeLevel');
  const schoolYearSelect = document.getElementById('schoolYear');
  const strandGroup = document.getElementById('strandGroup');
  const strandSelect = document.getElementById('strand');
  const getStartedBtn = document.querySelector('.get-started-btn');
  const educationForm = document.getElementById('educationForm');

  const hiddenEducationLevel = document.getElementById('hiddenEducationLevel');
  const hiddenGradeLevel = document.getElementById('hiddenGradeLevel');
  const hiddenSchoolYear = document.getElementById('hiddenSchoolYear');
  const hiddenStrand = document.getElementById('hiddenStrand');

  const selectionText = document.getElementById('selectionText');

  let selectedLevel = null;

  const gradeOptions = {
    jhs: ['6','7','8','9','10'],
    shs: ['11','12']
  };

  const schoolYearOptions = ['2024-2025','2025-2026','2026-2027'];
  const strandOptions = ['STEM','GAS','ABM','HUMSS'];

  // Initialize
  levelBtns.forEach(btn => btn.addEventListener('click', handleLevelSelection));
  gradeLevelSelect.addEventListener('change', validateForm);
  schoolYearSelect.addEventListener('change', validateForm);
  strandSelect.addEventListener('change', validateForm);
  educationForm.addEventListener('submit', handleFormSubmit);

  function handleLevelSelection(e) {
    selectedLevel = e.target.dataset.level;

    // Highlight active button
    levelBtns.forEach(b => b.classList.remove('active'));
    e.target.classList.add('active');

    // Show reminder text
    selectionText.textContent = `You selected: ${selectedLevel === 'jhs' ? 'Junior High School' : 'Senior High School'}`;

    // Reset dropdowns
    gradeLevelSelect.innerHTML = '<option value="">Select your grade</option>';
    schoolYearSelect.innerHTML = '<option value="">Select your school year</option>';
    strandSelect.innerHTML = '<option value="">Select your strand</option>';

    // Populate grades
    gradeOptions[selectedLevel].forEach(g => gradeLevelSelect.add(new Option(`Grade ${g}`, g)));
    gradeLevelSelect.disabled = false;

    // Populate school years
    schoolYearOptions.forEach(s => schoolYearSelect.add(new Option(s, s)));
    schoolYearSelect.disabled = false;

    // Handle SHS strand
    if (selectedLevel === 'shs') {
      strandGroup.style.display = 'block';
      strandOptions.forEach(s => strandSelect.add(new Option(s, s)));
      strandSelect.disabled = false;
    } else {
      strandGroup.style.display = 'none';
      strandSelect.disabled = true;
    }

    // Reset hidden values
    hiddenEducationLevel.value = '';
    hiddenGradeLevel.value = '';
    hiddenSchoolYear.value = '';
    hiddenStrand.value = '';

    validateForm();
  }

  function validateForm() {
    let valid = gradeLevelSelect.value && schoolYearSelect.value;
    if (selectedLevel === 'shs') valid = valid && strandSelect.value;
    getStartedBtn.disabled = !valid;
  }

  function handleFormSubmit(e) {
    if (!selectedLevel) { 
      e.preventDefault(); 
      alert('Please select a level'); 
      return; 
    }

    // Fill hidden inputs
    hiddenEducationLevel.value = selectedLevel.toUpperCase();
    hiddenGradeLevel.value = gradeLevelSelect.value;
    hiddenSchoolYear.value = schoolYearSelect.value;
    hiddenStrand.value = selectedLevel === 'shs' ? strandSelect.value : '';
  }
});
