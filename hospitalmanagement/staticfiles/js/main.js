// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript loaded successfully');
    
    // Basic form submission handling
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            console.log('Form submitted');
            // Add any pre-submission logic here
        });
    });
    
    // Add active class to current navigation link
    const currentPath = window.location.pathname;
    document.querySelectorAll('nav a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});
document.addEventListener('DOMContentLoaded', function() {
    const dobField = document.getElementById('id_date_of_birth');
    if (dobField) {
        dobField.addEventListener('change', function() {
            // Convert MM/DD/YYYY to YYYY-MM-DD if needed
            const parts = this.value.split('/');
            if (parts.length === 3) {
                this.value = `${parts[2]}-${parts[0]}-${parts[1]}`;
            }
        });
    }
});