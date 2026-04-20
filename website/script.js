/* ============================================================
   SCRIPT — Apple-style Interactions & Animations
   ============================================================ */

// ---- Scroll Animation Observer ----
document.addEventListener('DOMContentLoaded', () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.08,
        rootMargin: '0px 0px -60px 0px'
    });

    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
});

// ---- Navigation Scroll Behavior ----
(() => {
    const nav = document.getElementById('nav');
    let lastScroll = 0;

    function updateNav() {
        const scrollY = window.scrollY;
        const heroHeight = document.getElementById('hero').offsetHeight;

        // Toggle dark nav when past hero
        if (scrollY > heroHeight * 0.8) {
            nav.classList.remove('nav-dark');
        } else {
            nav.classList.add('nav-dark');
        }

        lastScroll = scrollY;
    }

    // Initialize as dark (over hero)
    nav.classList.add('nav-dark');
    window.addEventListener('scroll', updateNav, { passive: true });
    updateNav();
})();

// ---- Mobile Menu Toggle ----
(() => {
    const toggle = document.getElementById('navToggle');
    const menu = document.getElementById('mobileMenu');
    const links = menu.querySelectorAll('.mobile-link, .mobile-cta');
    let isOpen = false;

    toggle.addEventListener('click', () => {
        isOpen = !isOpen;
        toggle.classList.toggle('active', isOpen);
        menu.classList.toggle('active', isOpen);
        document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    links.forEach(link => {
        link.addEventListener('click', () => {
            isOpen = false;
            toggle.classList.remove('active');
            menu.classList.remove('active');
            document.body.style.overflow = '';
        });
    });
})();

// ---- Smooth Scroll for Anchor Links ----
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#' || targetId === '#impressum' || targetId === '#datenschutz') return;
        
        e.preventDefault();
        const target = document.querySelector(targetId);
        if (target) {
            const navHeight = document.getElementById('nav').offsetHeight;
            const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navHeight;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// ---- Treatment Accordion ----
function toggleTreatment(id) {
    const body = document.getElementById(`body-${id}`);
    const chevron = document.getElementById(`chevron-${id}`);
    
    body.classList.toggle('show');
    chevron.classList.toggle('rotated');
}

// ---- Memberships Toggle ----
function toggleMemberships() {
    const list = document.getElementById('membershipsList');
    const btn = document.getElementById('toggleMemberships');
    
    list.classList.toggle('show');
    
    if (list.classList.contains('show')) {
        btn.innerHTML = 'Mitgliedschaften ausblenden <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="18 15 12 9 6 15"/></svg>';
    } else {
        btn.innerHTML = 'Mitgliedschaften anzeigen <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>';
    }
}

// ---- Impressum Modal ----
function showImpressum(e) {
    e.preventDefault();
    document.getElementById('impressumModal').classList.add('show');
    document.body.style.overflow = 'hidden';
}

function closeImpressum() {
    document.getElementById('impressumModal').classList.remove('show');
    document.body.style.overflow = '';
}

// Close modal on overlay click
document.getElementById('impressumModal').addEventListener('click', (e) => {
    if (e.target === e.currentTarget) {
        closeImpressum();
    }
});

// Close modal on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeImpressum();
    }
});

// ---- Form Submissions ----
function submitRezept(e) {
    e.preventDefault();
    const form = document.getElementById('rezeptForm');
    const success = document.getElementById('rezeptSuccess');
    
    // Simulate form submission
    form.style.display = 'none';
    success.classList.add('show');
    
    // In production, replace with actual form submission:
    // const formData = new FormData(form);
    // fetch('/api/rezept', { method: 'POST', body: formData })
}

function submitAbsage(e) {
    e.preventDefault();
    const form = document.getElementById('absageForm');
    const success = document.getElementById('absageSuccess');
    
    form.style.display = 'none';
    success.classList.add('show');
}

// ---- Parallax-like Hero Effect ----
(() => {
    const heroImg = document.querySelector('.hero-img');
    if (!heroImg) return;
    
    let ticking = false;
    
    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(() => {
                const scrollY = window.scrollY;
                const heroHeight = document.getElementById('hero').offsetHeight;
                
                if (scrollY < heroHeight) {
                    const progress = scrollY / heroHeight;
                    heroImg.style.transform = `scale(${1 + progress * 0.1}) translateY(${scrollY * 0.3}px)`;
                    heroImg.style.opacity = 1 - progress * 0.4;
                }
                
                ticking = false;
            });
            ticking = true;
        }
    }, { passive: true });
})();

// ---- Active Nav Link Highlighting ----
(() => {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    function updateActiveLink() {
        const scrollY = window.scrollY + 100;
        
        sections.forEach(section => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');
            
            if (scrollY >= top && scrollY < top + height) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }
    
    window.addEventListener('scroll', updateActiveLink, { passive: true });
})();
