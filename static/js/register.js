document.addEventListener('DOMContentLoaded', function() {
    const firstNameInput = document.getElementById('id_first_name');
    const lastNameInput = document.getElementById('id_last_name');
    const birthdateInput = document.getElementById('id_birth_date');
    const usernameInput = document.getElementById('username');
  
    firstNameInput.addEventListener('input', updateUsername);
    lastNameInput.addEventListener('input', updateUsername);
    birthdateInput.addEventListener('change', updateUsername);
  
    function updateUsername() {
      const firstName = firstNameInput.value.trim().toLowerCase().replace(/\s/g, '');
      const lastName = lastNameInput.value.trim().toLowerCase().replace(/\s/g, ''); 
      const birthdate = new Date(birthdateInput.value).getFullYear();
  
      const username = firstName + lastName + birthdate;
  
      usernameInput.value = username;
    }
  });