// Cosplay ITA Blog - JavaScript

// Animazione scroll per le card
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

document.querySelectorAll('.post-card, .stat-item').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Header scroll effect
const header = document.querySelector('.header');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        header.style.boxShadow = '0 4px 30px rgba(233, 30, 140, 0.3)';
    } else {
        header.style.boxShadow = 'none';
    }
});

// Aggiorna anno nel footer
const yearEls = document.querySelectorAll('.footer-year');
yearEls.forEach(el => {
    el.textContent = new Date().getFullYear();
});
