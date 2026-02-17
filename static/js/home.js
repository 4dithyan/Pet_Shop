// ========================================
// HOME PAGE JAVASCRIPT
// Swiper.js, GSAP, and Homepage Animations
// ========================================

// Initialize Swiper for Hero Section
const heroSwiper = new Swiper('.hero-swiper', {
    effect: 'fade',
    loop: true,
    autoplay: {
        delay: 5000,
        disableOnInteraction: false,
    },
    speed: 1500,
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
});

// GSAP Animations for Hero Content
gsap.registerPlugin(ScrollTrigger);

// Hero title animation
gsap.from('.hero-title', {
    duration: 1.2,
    y: 50,
    opacity: 0,
    ease: 'power3.out',
    delay: 0.3
});

// Hero subtitle animation
gsap.from('.hero-subtitle', {
    duration: 1,
    y: 30,
    opacity: 0,
    ease: 'power2.out',
    delay: 0.6
});

// Hero buttons animation
gsap.from('.hero-buttons .btn', {
    duration: 0.8,
    y: 20,
    opacity: 0,
    ease: 'power2.out',
    stagger: 0.2,
    delay: 0.9
});

// Parallax Effect for Background Section
gsap.to('.parallax-section', {
    backgroundPosition: '50% 100%',
    ease: 'none',
    scrollTrigger: {
        trigger: '.parallax-section',
        start: 'top bottom',
        end: 'bottom top',
        scrub: true
    }
});

// Featured Pets Animation on Scroll
gsap.utils.toArray('.pet-card').forEach((card, index) => {
    gsap.from(card, {
        scrollTrigger: {
            trigger: card,
            start: 'top 85%',
            toggleActions: 'play none none reverse'
        },
        y: 60,
        opacity: 0,
        duration: 0.8,
        ease: 'power2.out',
        delay: index * 0.1
    });
});

// Services Section Animation
gsap.utils.toArray('.service-card').forEach((card, index) => {
    gsap.from(card, {
        scrollTrigger: {
            trigger: card,
            start: 'top 85%',
            toggleActions: 'play none none reverse'
        },
        scale: 0.8,
        opacity: 0,
        duration: 0.6,
        ease: 'back.out(1.7)',
        delay: index * 0.15
    });
});

// Gallery Masonry Animation
if (document.querySelector('.gallery')) {
    gsap.utils.toArray('.gallery-item').forEach((item, index) => {
        gsap.from(item, {
            scrollTrigger: {
                trigger: item,
                start: 'top 90%',
                toggleActions: 'play none none reverse'
            },
            scale: 0.9,
            opacity: 0,
            duration: 0.5,
            ease: 'power2.out',
            delay: index * 0.05
        });
    });
}

// Horizontal Scroll Implementation
const horizontalScroll = document.querySelector('.horizontal-scroll');
if (horizontalScroll) {
    let isDown = false;
    let startX;
    let scrollLeft;

    horizontalScroll.addEventListener('mousedown', (e) => {
        isDown = true;
        startX = e.pageX - horizontalScroll.offsetLeft;
        scrollLeft = horizontalScroll.scrollLeft;
        horizontalScroll.style.cursor = 'grabbing';
    });

    horizontalScroll.addEventListener('mouseleave', () => {
        isDown = false;
        horizontalScroll.style.cursor = 'grab';
    });

    horizontalScroll.addEventListener('mouseup', () => {
        isDown = false;
        horizontalScroll.style.cursor = 'grab';
    });

    horizontalScroll.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - horizontalScroll.offsetLeft;
        const walk = (x - startX) * 2;
        horizontalScroll.scrollLeft = scrollLeft - walk;
    });
}

// Testimonials Swiper
const testimonialsSwiper = new Swiper('.testimonials-swiper', {
    slidesPerView: 1,
    spaceBetween: 30,
    loop: true,
    autoplay: {
        delay: 6000,
        disableOnInteraction: false,
    },
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
    breakpoints: {
        768: {
            slidesPerView: 2,
        },
        1024: {
            slidesPerView: 3,
        }
    }
});

// Animated Counters
const animateCounters = () => {
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000; // 2 seconds
        const increment = target / (duration / 16); // 60 FPS
        let current = 0;

        const updateCounter = () => {
            current += increment;
            if (current < target) {
                counter.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };

        // Trigger animation when element is in viewport
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    updateCounter();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        observer.observe(counter);
    });
};

animateCounters();

// Gallery Lightbox
const galleryItems = document.querySelectorAll('.gallery-item');
const lightbox = document.getElementById('lightbox');
const lightboxImg = document.getElementById('lightbox-img');
const lightboxClose = document.getElementById('lightbox-close');

if (galleryItems.length > 0 && lightbox) {
    galleryItems.forEach(item => {
        item.addEventListener('click', function () {
            const imgSrc = this.querySelector('.gallery-img').src;
            lightboxImg.src = imgSrc;
            lightbox.classList.add('active');
            document.body.style.overflow = 'hidden';
        });
    });

    if (lightboxClose) {
        lightboxClose.addEventListener('click', () => {
            lightbox.classList.remove('active');
            document.body.style.overflow = '';
        });
    }

    lightbox.addEventListener('click', (e) => {
        if (e.target === lightbox) {
            lightbox.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
}

// Section Title Reveal Animation
gsap.utils.toArray('.section-title').forEach(title => {
    gsap.from(title, {
        scrollTrigger: {
            trigger: title,
            start: 'top 80%',
            toggleActions: 'play none none reverse'
        },
        y: 40,
        opacity: 0,
        duration: 1,
        ease: 'power3.out'
    });
});

// Floating shapes animation in hero
const createFloatingShapes = () => {
    const hero = document.querySelector('.hero-section');
    if (!hero) return;

    for (let i = 0; i < 5; i++) {
        const shape = document.createElement('div');
        shape.className = 'floating-shape';
        shape.style.cssText = `
            position: absolute;
            width: ${Math.random() * 100 + 50}px;
            height: ${Math.random() * 100 + 50}px;
            background: rgba(46, 196, 182, 0.1);
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            z-index: 1;
        `;
        hero.appendChild(shape);

        gsap.to(shape, {
            y: `${Math.random() * 100 - 50}px`,
            x: `${Math.random() * 100 - 50}px`,
            duration: Math.random() * 3 + 2,
            repeat: -1,
            yoyo: true,
            ease: 'sine.inOut'
        });
    }
};

createFloatingShapes();

console.log('🚀 Homepage animations initialized!');
