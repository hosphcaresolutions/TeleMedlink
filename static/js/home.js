// static/js/home.js

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle functionality
    //const mobileMenuToggle = document.createElement('button');
    //mobileMenuToggle.className = 'mobile-menu-toggle';
    //mobileMenuToggle.innerHTML = '<i class="fas fa-bars"></i>';
    //document.querySelector('nav').prepend(mobileMenuToggle);
    
    const navLinks = document.querySelector('.nav-links');
    
    mobileMenuToggle.addEventListener('click', function() {
        navLinks.classList.toggle('active');
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Testimonial slider functionality
    let currentTestimonial = 0;
    const testimonials = document.querySelectorAll('.testimonial-card');
    
    function showTestimonial(index) {
        testimonials.forEach((testimonial, i) => {
            testimonial.style.display = i === index ? 'block' : 'none';
        });
    }
    
    // Only initialize slider if there are testimonials
    if (testimonials.length > 1) {
        showTestimonial(0);
        
        setInterval(() => {
            currentTestimonial = (currentTestimonial + 1) % testimonials.length;
            showTestimonial(currentTestimonial);
        }, 5000);
    }
});