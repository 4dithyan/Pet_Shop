/* ========================================
   PREMIUM PET SHOP - MAIN JAVASCRIPT
======================================== */

document.addEventListener('DOMContentLoaded', function () {

    /* -------------------------------------------------------------------
       1. Navbar Scroll Effect (Glassmorphism)
    ------------------------------------------------------------------- */
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', function () {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    /* -------------------------------------------------------------------
       2. Initialize Tooltips (Bootstrap)
    ------------------------------------------------------------------- */
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    /* -------------------------------------------------------------------
       3. Smooth Scroll for Anchor Links
    ------------------------------------------------------------------- */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    /* -------------------------------------------------------------------
       4. Horizontal Drag Scroll for Categories
    ------------------------------------------------------------------- */
    const scrollContainer = document.querySelector('.horizontal-scroll-wrapper');
    if (scrollContainer) {
        let isDown = false;
        let startX;
        let scrollLeft;

        scrollContainer.addEventListener('mousedown', (e) => {
            isDown = true;
            scrollContainer.classList.add('active');
            startX = e.pageX - scrollContainer.offsetLeft;
            scrollLeft = scrollContainer.scrollLeft;
        });
        scrollContainer.addEventListener('mouseleave', () => {
            isDown = false;
            scrollContainer.classList.remove('active');
        });
        scrollContainer.addEventListener('mouseup', () => {
            isDown = false;
            scrollContainer.classList.remove('active');
        });
        scrollContainer.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - scrollContainer.offsetLeft;
            const walk = (x - startX) * 2; // Scroll-fast
            scrollContainer.scrollLeft = scrollLeft - walk;
        });
    }
});
