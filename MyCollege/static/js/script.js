const navLinks = document.querySelectorAll('.nav-link');
const sortDropdown = document.querySelectorAll('.dropdown-item');

  navLinks.forEach(link => {
    link.addEventListener('click', function() {
      // Remove .active from all links
      navLinks.forEach(l => l.classList.remove('active'));
      // Add .active to the clicked one
      this.classList.add('active');
    });
  });

    sortDropdown.forEach(link => {
    link.addEventListener('click', function() {
      // Remove .active from all links
      sortDropdown.forEach(l => l.classList.remove('active'));
      // Add .active to the clicked one
      this.classList.add('active');
    });
  });

  new DataTable('#example');