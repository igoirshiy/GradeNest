document.addEventListener("DOMContentLoaded", () => {
  const levelBtns = document.querySelectorAll('.level-btn');
  const gradeLevelSelect = document.getElementById('gradeLevel');
  const gradeLevelLabel = document.getElementById('gradeLevelLabel');
  const schoolYearSelect = document.getElementById('schoolYear');
  const strandGroup = document.getElementById('strandGroup');
  const strandSelect = document.getElementById('strand');
  const getStartedBtn = document.querySelector('.get-started-btn');
  const educationForm = document.getElementById('educationForm');
  
  const modals = {
    jhs: document.getElementById('jhsModal'),
    shs: document.getElementById('shsModal')
  };
  const modalOverlay = document.getElementById('modalOverlay');
  
  const closeBtns = document.querySelectorAll('.close-btn');
  const cancelBtns = document.querySelectorAll('.btn-cancel');
  const nextBtns = document.querySelectorAll('.btn-next');
  
  let selectedLevel = null;
  let educationData = {};

  const gradeOptions = {
    jhs: [
      { value: '7', text: 'Grade 7' },
      { value: '8', text: 'Grade 8' },
      { value: '9', text: 'Grade 9' },
      { value: '10', text: 'Grade 10' }
    ],
    shs: [
      { value: '11', text: 'Grade 11' },
      { value: '12', text: 'Grade 12' }
    ]
  };

  const schoolYearOptions = [
    { value: '2024-2025', text: '2024-2025' },
    { value: '2025-2026', text: '2025-2026' },
    { value: '2026-2027', text: '2026-2027' }
  ];

  const strandOptions = [
    { value: 'STEM', text: 'STEM' },
    { value: 'GAS', text: 'GAS' },
    { value: 'ABM', text: 'ABM' },
    { value: 'HUMSS', text: 'HUMSS' }
  ];

  init();

  function init() {
    levelBtns.forEach(btn => {
      btn.addEventListener('click', handleLevelSelection);
    });

    closeBtns.forEach(btn => btn.addEventListener('click', closeModal));
    cancelBtns.forEach(btn => btn.addEventListener('click', closeModal));
    nextBtns.forEach(btn => btn.addEventListener('click', handleModalNext));

    modalOverlay.addEventListener('click', closeAllModals);

    gradeLevelSelect.addEventListener('change', validateMainForm);
    schoolYearSelect.addEventListener('change', validateMainForm);
    strandSelect.addEventListener('change', validateMainForm);

    educationForm.addEventListener('submit', handleMainFormSubmit);

    Object.values(modals).forEach(modal => {
      modal.querySelector('.modal-content').addEventListener('click', (e) => e.stopPropagation());
    });
  }

  function handleLevelSelection(e) {
    const level = e.target.dataset.level;
    levelBtns.forEach(btn => btn.classList.remove('active'));
    e.target.classList.add('active');
    selectedLevel = level;
    updateFormForLevel(level);
    showModal(level);
  }

  function updateFormForLevel(level) {
    gradeLevelSelect.innerHTML = '';
    schoolYearSelect.innerHTML = '<option value="">Choose your current school year</option>';
    strandSelect.innerHTML = '<option value="">Select your strand</option>';
    
    if (level === 'jhs') {
      gradeLevelLabel.textContent = 'Grade Level';
      gradeLevelSelect.innerHTML = '<option value="">Choose between 7 - 10</option>';
      gradeOptions.jhs.forEach(opt => addOption(gradeLevelSelect, opt));
      strandGroup.style.display = 'none';
      strandSelect.disabled = true;
    } else if (level === 'shs') {
      gradeLevelLabel.textContent = 'Grade Level';
      gradeLevelSelect.innerHTML = '<option value="">Choose between 11 - 12</option>';
      gradeOptions.shs.forEach(opt => addOption(gradeLevelSelect, opt));
      strandOptions.forEach(opt => addOption(strandSelect, opt));
      strandGroup.style.display = 'block';
      strandSelect.disabled = false;
    }

    schoolYearOptions.forEach(opt => addOption(schoolYearSelect, opt));

    gradeLevelSelect.disabled = false;
    schoolYearSelect.disabled = false;
    
    validateMainForm();
  }

  function addOption(select, option) {
    const el = document.createElement('option');
    el.value = option.value;
    el.textContent = option.text;
    select.appendChild(el);
  }

  function showModal(modalType) {
    closeAllModals();
    modalOverlay.classList.add('show');
    modals[modalType].classList.add('show');
    resetModalForm(modalType);
  }

  function resetModalForm(modalType) {
    const modal = modals[modalType];
    const selects = modal.querySelectorAll('.form-select');
    const errors = modal.querySelectorAll('.error');
    selects.forEach(s => { s.value = ''; s.classList.remove('input-error'); });
    errors.forEach(e => e.classList.remove('show'));
  }

  function closeModal(e) {
    const modalType = e.target.dataset.modal;
    if (modalType) modals[modalType].classList.remove('show');
    closeAllModals();
  }

  function closeAllModals() {
    modalOverlay.classList.remove('show');
    Object.values(modals).forEach(m => m.classList.remove('show'));
  }

  function handleModalNext(e) {
    const modalType = e.target.dataset.modal;
    if (validateModalForm(modalType)) {
      saveModalData(modalType);
      closeAllModals();
      updateMainFormFromModalData();
      setTimeout(() => {
        alert('Education level setup completed! Redirecting to dashboard...');
        window.location.href = '/accounts/dashboard/';
      }, 500);
    }
  }

  function validateModalForm(modalType) {
    let isValid = true;
    if (modalType === 'jhs') {
      const year = document.getElementById('jhsYear');
      const schoolYear = document.getElementById('jhsSchoolYear');
      if (!year.value) { showError('jhsYearError', 'Year level is required'); year.classList.add('input-error'); isValid = false; }
      if (!schoolYear.value) { showError('jhsSchoolYearError', 'School year is required'); schoolYear.classList.add('input-error'); isValid = false; }
    } else if (modalType === 'shs') {
      const strand = document.getElementById('shsStrand');
      const year = document.getElementById('shsYear');
      const schoolYear = document.getElementById('shsSchoolYear');
      if (!strand.value) { showError('shsStrandError', 'Strand is required'); strand.classList.add('input-error'); isValid = false; }
      if (!year.value) { showError('shsYearError', 'Year level is required'); year.classList.add('input-error'); isValid = false; }
      if (!schoolYear.value) { showError('shsSchoolYearError', 'School year is required'); schoolYear.classList.add('input-error'); isValid = false; }
    }
    return isValid;
  }

  function showError(id, msg) {
    const el = document.getElementById(id);
    el.textContent = msg;
    el.classList.add('show');
  }

  function saveModalData(modalType) {
    educationData.level = modalType.toUpperCase();
    if (modalType === 'jhs') {
      educationData.year = document.getElementById('jhsYear').value;
      educationData.schoolYear = document.getElementById('jhsSchoolYear').value;
    } else if (modalType === 'shs') {
      educationData.strand = document.getElementById('shsStrand').value;
      educationData.year = document.getElementById('shsYear').value;
      educationData.schoolYear = document.getElementById('shsSchoolYear').value;
    }
  }

  function updateMainFormFromModalData() {
    if (educationData.year) gradeLevelSelect.value = educationData.year;
    if (educationData.schoolYear) schoolYearSelect.value = educationData.schoolYear;
    if (educationData.strand && selectedLevel === 'shs') strandSelect.value = educationData.strand;
    validateMainForm();
  }

  function validateMainForm() {
    let isValid = false;
    if (selectedLevel === 'jhs') {
      isValid = gradeLevelSelect.value && schoolYearSelect.value;
    } else if (selectedLevel === 'shs') {
      isValid = gradeLevelSelect.value && schoolYearSelect.value && strandSelect.value;
    }
    getStartedBtn.disabled = !isValid;
  }

  function handleMainFormSubmit(e) {
    e.preventDefault();
    if (!selectedLevel) { alert('Please select an education level first.'); return; }
    showModal(selectedLevel);
  }
});