/* ============================================================
   SCRIPT — Apple-style Interactions & Animations
   ============================================================ */

// ---- Helper: DOM Ready Guard ----
function runWhenDOMReady(fn) {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', fn);
    } else {
        // DOM ist bereits geladen (z. B. nach dynamischem Skript-Laden) -> sofort ausführen
        fn();
    }
}

// ---- Scroll Animation Observer (Apple Reveal Effect) ----
function initScrollObserver() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    if (!elements.length) return;

    // 1. Bereits sichtbare Elemente (z. B. Hero) sofort als sichtbar markieren
    const viewHeight = window.innerHeight || document.documentElement.clientHeight;
    elements.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.top < viewHeight * 0.95) {
            el.classList.add('visible');
        }
    });

    // 2. Scroll-Animation für noch nicht sichtbare Elemente aktivieren
    document.body.classList.add('scroll-anim-ready');

    // 3. IntersectionObserver zum Einblenden beim Hinabscrollen
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target); // bleibt dauerhaft sichtbar
                }
            });
        }, {
            threshold: 0.06,
            rootMargin: '0px 0px -30px 0px'
        });

        elements.forEach(el => {
            if (!el.classList.contains('visible')) {
                observer.observe(el);
            }
        });
    }

    // 4. Scroll-Listener als Sicherheitsnetz für schnelles Scrollen
    function checkRemaining() {
        const vh = window.innerHeight || document.documentElement.clientHeight;
        elements.forEach(el => {
            if (!el.classList.contains('visible')) {
                const rect = el.getBoundingClientRect();
                if (rect.top < vh - 20) {
                    el.classList.add('visible');
                }
            }
        });
    }

    window.addEventListener('scroll', checkRemaining, { passive: true });
}

runWhenDOMReady(initScrollObserver);

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
    if (e) e.preventDefault();
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

// ---- Datenschutz Modal ----
function showDatenschutz(e) {
    if (e) e.preventDefault();
    const modal = document.getElementById('datenschutzModal');
    if (modal) {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
}

function closeDatenschutz() {
    const modal = document.getElementById('datenschutzModal');
    if (modal) {
        modal.classList.remove('show');
        document.body.style.overflow = '';
    }
}

// Close datenschutz modal on overlay click
document.getElementById('datenschutzModal').addEventListener('click', (e) => {
    if (e.target === e.currentTarget) {
        closeDatenschutz();
    }
});

// Close all modals on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeImpressum();
        closeDatenschutz();
        closeUrlaubModal();
    }
});

// ---- Google Maps 2-Klick Lösung ----
function loadGoogleMaps() {
    const container = document.getElementById('mapContainer');
    if (!container) return;
    
    container.innerHTML = `
        <iframe 
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2555.5!2d11.0035!3d49.5966!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x47a1f8c5c6d2c8d7%3A0x7c2c5b0e05f9b0c0!2sSchlossplatz%201%2C%2091054%20Erlangen!5e0!3m2!1sde!2sde!4v1"
            width="100%" 
            height="100%" 
            style="border:0;" 
            allowfullscreen="" 
            loading="lazy"
            title="Standort der Praxis Dr. med. Rahemi Pour">
        </iframe>
    `;
}

// ---- Form Submissions ----
function submitRezept(e) {
    e.preventDefault();
    if (isPraxisUrlaubAktiv) {
        openUrlaubModal();
        return;
    }
    const form = document.getElementById('rezeptForm');
    const success = document.getElementById('rezeptSuccess');
    const btn = form.querySelector('button[type="submit"]');

    const vorname = document.getElementById('rezeptVorname').value.trim();
    const nachname = document.getElementById('rezeptNachname').value.trim();
    const geburt = document.getElementById('rezeptGeburt').value;
    const telefon = document.getElementById('rezeptTelefon').value.trim();
    const medikament = document.getElementById('rezeptMedikament').value.trim();
    const anmerkung = document.getElementById('rezeptAnmerkung').value.trim();

    if (!document.getElementById('rezeptDatenschutz').checked) {
        alert('Bitte willigen Sie vor dem Absenden in die Datenschutzerklärung ein.');
        return;
    }

    btn.disabled = true;
    btn.innerHTML = '<span style="display:inline-flex;align-items:center;gap:8px;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin"><circle cx="12" cy="12" r="10" stroke-opacity="0.25"/><path d="M12 2a10 10 0 0 1 10 10"/></svg> Anfrage wird übermittelt...</span>';

    // Übermittlung der Rezeptanforderung an praxisdr.rahemi-pour@hotmail.de
    const payload = {
        _subject: `Neue Rezeptbestellung: ${vorname} ${nachname}`,
        _captcha: "false",
        "Patient": `${vorname} ${nachname}`,
        "Geburtsdatum": geburt,
        "Telefonnummer": telefon,
        "Gewünschte Medikamente": medikament,
        "Anmerkungen": anmerkung || "Keine",
        "Einwilligung DSGVO": "Ja (erteilt)"
    };

    fetch('https://formsubmit.co/ajax/praxisdr.rahemi-pour@hotmail.de', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        form.style.display = 'none';
        success.classList.add('show');
    })
    .catch(error => {
        form.style.display = 'none';
        success.classList.add('show');
    });
}

function submitAbsage(e) {
    e.preventDefault();
    const form = document.getElementById('absageForm');
    const success = document.getElementById('absageSuccess');
    const btn = form.querySelector('button[type="submit"]');

    const vorname = document.getElementById('absageVorname').value.trim();
    const nachname = document.getElementById('absageNachname').value.trim();
    const geburt = document.getElementById('absageGeburt').value;
    const termin = document.getElementById('absageTermin').value;
    const uhrzeit = document.getElementById('absageUhrzeit') ? document.getElementById('absageUhrzeit').value : '';
    const grund = document.getElementById('absageGrund').value.trim();

    if (!document.getElementById('absageDatenschutz').checked) {
        alert('Bitte willigen Sie vor dem Absenden in die Datenschutzerklärung ein.');
        return;
    }

    btn.disabled = true;
    btn.innerHTML = '<span style="display:inline-flex;align-items:center;gap:8px;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin"><circle cx="12" cy="12" r="10" stroke-opacity="0.25"/><path d="M12 2a10 10 0 0 1 10 10"/></svg> Absage wird übermittelt...</span>';

    const payload = {
        _subject: uhrzeit 
            ? `Terminabsage: ${vorname} ${nachname} (Termin: ${termin} um ${uhrzeit} Uhr)`
            : `Terminabsage: ${vorname} ${nachname} (Termin: ${termin})`,
        _captcha: "false",
        "Patient": `${vorname} ${nachname}`,
        "Geburtsdatum": geburt,
        "Abzusagender Termin": uhrzeit ? `${termin} um ${uhrzeit} Uhr` : termin,
        "Uhrzeit des Termins": uhrzeit || "Nicht angegeben",
        "Grund der Absage": grund || "Keine Angabe",
        "Einwilligung DSGVO": "Ja (erteilt)"
    };

    fetch('https://formsubmit.co/ajax/praxisdr.rahemi-pour@hotmail.de', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        form.style.display = 'none';
        success.classList.add('show');
    })
    .catch(error => {
        form.style.display = 'none';
        success.classList.add('show');
    });
}

// ---- Live-Status Öffnungszeiten ----
function updateLiveHoursStatus() {
    const statusEl = document.getElementById('hoursLiveStatus');
    const textEl = document.getElementById('hoursLiveStatusText');
    if (!statusEl || !textEl) return;

    const isEn = (typeof currentLang !== 'undefined' && currentLang === 'en');

    // Wenn Urlaubsmodus aktiv ist
    if (typeof isPraxisUrlaubAktiv !== 'undefined' && isPraxisUrlaubAktiv) {
        statusEl.className = 'hours-live-status status-urlaub';
        const returnText = (typeof urlaubConfig !== 'undefined' && urlaubConfig.wiederDaAb) 
            ? (isEn ? ` (back on ${urlaubConfig.wiederDaAb})` : ` (wieder da ab ${urlaubConfig.wiederDaAb})`) 
            : '';
        textEl.textContent = isEn ? `Practice on vacation${returnText}` : `Praxisurlaub${returnText}`;
        return;
    }

    const now = new Date();
    const day = now.getDay(); // 0 = So, 1 = Mo, 2 = Di, 3 = Mi, 4 = Do, 5 = Fr, 6 = Sa
    const minutesNow = now.getHours() * 60 + now.getMinutes();

    const MORNING_OPEN = 8 * 60; // 08:00 Uhr
    const MORNING_CLOSE = 12 * 60; // 12:00 Uhr
    const AFTERNOON_OPEN = 14 * 60 + 30; // 14:30 Uhr
    const AFTERNOON_CLOSE = 17 * 60 + 30; // 17:30 Uhr

    let isOpen = false;
    let statusMessage = '';

    if (day >= 1 && day <= 5) { // Montag bis Freitag
        const hasAfternoon = (day === 1 || day === 2 || day === 4); // Mo, Di, Do

        if (minutesNow >= MORNING_OPEN && minutesNow < MORNING_CLOSE) {
            isOpen = true;
            statusMessage = isEn ? 'Open now (until 12:00 PM)' : 'Jetzt geöffnet (bis 12:00 Uhr)';
        } else if (hasAfternoon && minutesNow >= MORNING_CLOSE && minutesNow < AFTERNOON_OPEN) {
            isOpen = false;
            statusMessage = isEn ? 'Lunch break (opens 2:30 PM)' : 'Mittagspause (öffnet 14:30 Uhr)';
        } else if (hasAfternoon && minutesNow >= AFTERNOON_OPEN && minutesNow < AFTERNOON_CLOSE) {
            isOpen = true;
            statusMessage = isEn ? 'Open now (until 5:30 PM)' : 'Jetzt geöffnet (bis 17:30 Uhr)';
        } else if (minutesNow < MORNING_OPEN) {
            isOpen = false;
            statusMessage = isEn ? 'Currently closed (opens today 8:00 AM)' : 'Aktuell geschlossen (öffnet heute 08:00 Uhr)';
        } else {
            isOpen = false;
            if (day === 5) {
                statusMessage = isEn ? 'Closed (opens Mon. 8:00 AM)' : 'Geschlossen (öffnet Mo. 08:00 Uhr)';
            } else {
                statusMessage = isEn ? 'Closed (opens tomorrow 8:00 AM)' : 'Geschlossen (öffnet morgen 08:00 Uhr)';
            }
        }
    } else {
        // Wochenende
        isOpen = false;
        statusMessage = isEn ? 'Weekend (opens Mon. 8:00 AM)' : 'Wochenende (öffnet Mo. 08:00 Uhr)';
    }

    if (isOpen) {
        statusEl.className = 'hours-live-status status-open';
    } else {
        statusEl.className = 'hours-live-status status-closed';
    }
    textEl.textContent = statusMessage;
}

// ---- Urlaubsmodus & Vertretungen Logik ----
let isPraxisUrlaubAktiv = false;

function checkUrlaubStatus() {
    if (typeof urlaubConfig === 'undefined') {
        console.warn('[Urlaubs-Check] urlaubConfig nicht definiert.');
        return false;
    }

    console.log('[Urlaubs-Check] Aktuelle Konfiguration:', {
        status: urlaubConfig.status,
        von: urlaubConfig.von,
        bis: urlaubConfig.bis
    });

    if (urlaubConfig.status === 'an') {
        console.log('[Urlaubs-Check] Status ist manuell "an" -> Urlaubsmodus aktiv.');
        return true;
    }
    if (urlaubConfig.status === 'aus') {
        console.log('[Urlaubs-Check] Status ist manuell "aus" -> Urlaubsmodus inaktiv.');
        return false;
    }

    // Automatischer Datumsabgleich bei 'auto'
    if (urlaubConfig.status === 'auto') {
        if (!urlaubConfig.von || !urlaubConfig.bis) {
            console.warn('[Urlaubs-Check] status=auto, aber von/bis fehlt -> Inaktiv.');
            return false;
        }

        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const todayStr = `${year}-${month}-${day}`;

        const von = String(urlaubConfig.von).trim();
        const bis = String(urlaubConfig.bis).trim();
        const istAktiv = (todayStr >= von && todayStr <= bis);

        console.log(`[Urlaubs-Check auto] Heute: "${todayStr}" | Zeitraum: "${von}" bis "${bis}" | Aktiv: ${istAktiv}`);
        return istAktiv;
    }

    return false;
}

function formatDateGerman(isoDate) {
    if (!isoDate) return '';
    const parts = isoDate.split('-');
    if (parts.length !== 3) return isoDate;
    return `${parts[2]}.${parts[1]}.${parts[0]}`;
}

function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag] || tag)
    );
}

function openUrlaubModal() {
    const modal = document.getElementById('urlaubModal');
    if (modal) {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }
}

function closeUrlaubModal() {
    const modal = document.getElementById('urlaubModal');
    if (modal) {
        modal.classList.remove('show');
        document.body.style.overflow = '';
    }
}

function initUrlaub() {
    isPraxisUrlaubAktiv = checkUrlaubStatus();

    const banner = document.getElementById('urlaubBanner');
    const rezeptForm = document.getElementById('rezeptForm');
    const rezeptNotice = document.getElementById('rezeptUrlaubNotice');
    const rezeptSectionDesc = document.getElementById('rezeptSectionDesc');

    if (!isPraxisUrlaubAktiv) {
        // Urlaub inaktiv: Sämtliche Urlaubselemente entfernen / Normalzustand herstellen
        document.body.classList.remove('urlaub-aktiv');
        if (banner) banner.style.display = 'none';
        if (rezeptForm) rezeptForm.style.display = '';
        if (rezeptNotice) rezeptNotice.style.display = 'none';
        if (rezeptSectionDesc) {
            rezeptSectionDesc.textContent = 'Nur für bestehende Patienten. Bitte füllen Sie das Formular vollständig aus.';
        }
        console.log('[Urlaubs-Init] Praxisurlaub ist aktuell INAKTIV. Normaler Praxisbetrieb angezeigt.');
        return;
    }

    // Urlaub aktiv
    console.log('[Urlaubs-Init] Praxisurlaub ist AKTIV. Urlaubs-Banner & Vertretungen eingeblendet.');
    document.body.classList.add('urlaub-aktiv');

    // Banner aktivieren & beschriften
    const bannerText = document.getElementById('urlaubBannerText');
    if (banner && bannerText && urlaubConfig.bannerText) {
        bannerText.textContent = urlaubConfig.bannerText;
        banner.style.display = 'flex';
    }

    // Modal-Header befüllen
    const modalPeriod = document.getElementById('modalUrlaubPeriod');
    if (modalPeriod && urlaubConfig.von && urlaubConfig.bis) {
        modalPeriod.textContent = `Geschlossen vom ${formatDateGerman(urlaubConfig.von)} bis ${formatDateGerman(urlaubConfig.bis)}`;
    }

    const modalReturn = document.getElementById('modalUrlaubReturn');
    if (modalReturn && urlaubConfig.wiederDaAb) {
        modalReturn.textContent = urlaubConfig.wiederDaAb;
    }

    // Vertretungsliste dynamisch aufbauen
    const vertretungenList = document.getElementById('modalVertretungenList');
    if (vertretungenList && Array.isArray(urlaubConfig.vertretungen)) {
        vertretungenList.innerHTML = urlaubConfig.vertretungen.map(v => {
            const mapsQuery = encodeURIComponent(`${v.name}, ${v.adresse}`);
            const telLink = v.telefonLink || (v.telefon ? v.telefon.replace(/[\s\/\(\)-]/g, '') : '');
            return `
                <div class="vertretung-card">
                    <div class="vertretung-info">
                        <h4>${escapeHtml(v.name)}</h4>
                        <div class="vertretung-fach">${escapeHtml(v.fach || 'Facharzt für Dermatologie')}</div>
                        <div class="vertretung-meta">
                            <div class="vertretung-meta-item">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                                <a href="https://maps.google.com/?q=${mapsQuery}" target="_blank" rel="noopener noreferrer">${escapeHtml(v.adresse)}</a>
                            </div>
                            <div class="vertretung-meta-item">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                                <a href="tel:${telLink}">${escapeHtml(v.telefon)}</a>
                            </div>
                            ${v.hinweis ? `<div class="vertretung-hinweis">ℹ️ ${escapeHtml(v.hinweis)}</div>` : ''}
                        </div>
                    </div>
                    <div class="vertretung-actions">
                        <a href="tel:${telLink}" class="vertretung-call-btn">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                            Anrufen
                        </a>
                    </div>
                </div>
            `;
        }).join('');
    }

    // Notdienst befüllen
    if (urlaubConfig.notdienst) {
        const titleEl = document.getElementById('modalNotdienstTitle');
        const textEl = document.getElementById('modalNotdienstText');
        const btnTextEl = document.getElementById('modalNotdienstBtnText');
        if (titleEl && urlaubConfig.notdienst.titel) titleEl.textContent = urlaubConfig.notdienst.titel;
        if (textEl && urlaubConfig.notdienst.hinweis) textEl.textContent = urlaubConfig.notdienst.hinweis;
        if (btnTextEl && urlaubConfig.notdienst.telefon) btnTextEl.textContent = urlaubConfig.notdienst.telefon;
    }

    // Rezeptbestellung sperren
    const rezeptReturn = document.getElementById('rezeptUrlaubReturn');

    if (rezeptForm) rezeptForm.style.display = 'none';
    if (rezeptNotice) rezeptNotice.style.display = 'block';
    if (rezeptReturn && urlaubConfig.wiederDaAb) {
        rezeptReturn.textContent = urlaubConfig.wiederDaAb;
    }
    if (rezeptSectionDesc) {
        rezeptSectionDesc.textContent = 'Aufgrund unseres Praxisurlaubs ist die Online-Rezeptbestellung derzeit pausiert.';
    }
}

// Initialization nach DOM-Ready
runWhenDOMReady(() => {
    initUrlaub();
    updateLiveHoursStatus();
    setInterval(updateLiveHoursStatus, 60000);

    const urlaubModal = document.getElementById('urlaubModal');
    if (urlaubModal) {
        urlaubModal.addEventListener('click', (e) => {
            if (e.target === e.currentTarget) {
                closeUrlaubModal();
            }
        });
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeUrlaubModal();
        }
    });
});

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

// ---- Active Nav Link Highlighting (ScrollSpy) ----
(() => {
    const navLinks = document.querySelectorAll('.nav-link, .mobile-link');
    const sectionIds = [
        'kontakt',
        'anfahrt',
        'arzt',
        'besondere',
        'leistungen',
        'terminabsage',
        'rezept',
        'schnellauswahl'
    ];

    function updateActiveLink() {
        // Offset für fixed Nav (ca. 60px) + Puffer
        const scrollPos = window.scrollY + 130;
        let activeId = '';

        // Am Seitenende immer den letzten Abschnitt (Kontakt) aktivieren
        if ((window.innerHeight + window.scrollY) >= (document.documentElement.scrollHeight - 60)) {
            activeId = 'kontakt';
        } else {
            // Von unten nach oben den ersten sichtbaren Abschnitt finden
            for (const id of sectionIds) {
                const el = document.getElementById(id);
                if (el && el.offsetTop <= scrollPos) {
                    activeId = id;
                    break;
                }
            }
        }

        const targetHref = (activeId === 'terminabsage') ? '#rezept' : `#${activeId}`;

        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (activeId && href === targetHref) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    window.addEventListener('scroll', updateActiveLink, { passive: true });
    window.addEventListener('resize', updateActiveLink, { passive: true });
    runWhenDOMReady(updateActiveLink);
})();

// ---- Services Category Filter ----
function initServiceFilter() {
    const tabs = document.querySelectorAll('.service-tab');
    const cards = document.querySelectorAll('.service-card');
    if (!tabs.length || !cards.length) return;

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const filter = tab.getAttribute('data-filter');
            tabs.forEach(t => {
                t.classList.remove('active');
                t.setAttribute('aria-selected', 'false');
            });
            tab.classList.add('active');
            tab.setAttribute('aria-selected', 'true');

            cards.forEach(card => {
                const category = card.getAttribute('data-category');
                if (filter === 'all' || category === filter) {
                    card.classList.remove('is-filtered-out');
                } else {
                    card.classList.add('is-filtered-out');
                }
            });
        });
    });
}
runWhenDOMReady(initServiceFilter);

// ---- Bilingual Internationalization (DE / EN) ----
const translations = {
    de: {
        // Navigation
        nav_quick: "Schnellzugriff",
        nav_online: "Rezept &amp; Absage",
        nav_services: "Leistungen",
        nav_special: "Spezialbehandlungen",
        nav_doctor: "Über mich",
        nav_anfahrt: "Anfahrt",
        nav_contact: "Kontakt",
        btn_book: "Termin buchen",
        btn_book_short: "Termin buchen",

        // Hero
        hero_eyebrow: "Hautarztpraxis Erlangen",
        hero_subtitle: "Facharzt für Dermatologie · Allergologie · Ambulante Operationen · Dermatohistologie",
        hero_btn_book: "Termin vereinbaren",
        hero_btn_more: "Mehr erfahren",

        // Schnellzugriff
        insurance_pill: "Alle gesetzlichen Kassen (GKV) &amp; Privatversicherte (PKV)",
        quick_eyebrow: "SCHNELLZUGRIFF",
        quick_title: "ALLES, WAS SIE BRAUCHEN",
        quick_desc: "Die wichtigsten Funktionen für unsere Patienten – schnell und unkompliziert.",
        quick_card_termin_title: "Termin vereinbaren",
        quick_card_termin_desc: "Online Terminbuchung über Doctolib – einfach, schnell und jederzeit verfügbar.",
        quick_card_rezept_title: "Rezept bestellen",
        quick_card_rezept_desc: "Folgerezepte bequem online bestellen – nur für bestehende Patienten.",
        quick_card_absage_title: "Termin absagen",
        quick_card_absage_desc: "Können Sie Ihren Termin nicht wahrnehmen? Sagen Sie einfach online ab.",
        card_urlaub_badge: "Urlaubspause",

        // Öffnungszeiten
        hours_title: "Unsere Öffnungszeiten",
        hours_note: "Termine nach Vereinbarung · Notfälle jederzeit",
        day_mon: "Montag",
        day_tue: "Dienstag",
        day_wed: "Mittwoch",
        day_thu: "Donnerstag",
        day_fri: "Freitag",

        // Rezeptbestellung
        rezept_title: "Rezeptbestellung",
        rezept_desc: "Nur für bestehende Patienten. Bitte füllen Sie das Formular vollständig aus.",
        rezept_label_vorname: "Vorname",
        rezept_label_nachname: "Nachname",
        rezept_label_geburt: "Geburtsdatum",
        rezept_label_telefon: "Telefonnummer",
        rezept_label_medikament: "Gewünschte(s) Medikament(e)",
        rezept_label_anmerkung: "Anmerkungen (optional)",
        rezept_consent: "Ich willige ein, dass meine Angaben (einschließlich sensibler Gesundheitsdaten) zur Bearbeitung der Rezeptanforderung verarbeitet werden. Weitere Hinweise in der <a href=\"#datenschutz\" onclick=\"showDatenschutz(event)\">Datenschutzerklärung</a>.*",
        rezept_btn_submit: "Rezept anfordern",
        rezept_success_title: "Anfrage gesendet!",
        rezept_success_desc: "Wir melden uns schnellstmöglich bei Ihnen.",

        // Terminabsage
        absage_title: "Terminabsage",
        absage_desc: "Sie können Ihren Termin nicht wahrnehmen? Bitte sagen Sie rechtzeitig ab.",
        absage_doctolib_hint: "Über Doctolib gebucht? Sie können Termine auch direkt mit 1 Klick in Ihrem <a href=\"https://www.doctolib.de\" target=\"_blank\" rel=\"noopener\">Doctolib-Konto</a> stornieren.",
        label_vorname: "Vorname",
        label_nachname: "Nachname",
        label_geburt: "Geburtsdatum",
        label_termin: "Termin (Datum)",
        label_uhrzeit: "Uhrzeit des Termins",
        label_grund: "Grund der Absage (optional)",
        absage_consent: "Ich willige in die Verarbeitung meiner Daten zur Terminabsage gemäß der <a href=\"#datenschutz\" onclick=\"showDatenschutz(event)\">Datenschutzerklärung</a> ein.*",
        btn_submit_absage: "Termin absagen",
        absage_success_title: "Absage gesendet!",
        absage_success_desc: "Vielen Dank, wir haben Ihre Absage erhalten.",

        // Leistungen
        services_eyebrow: "Unsere Leistungen",
        services_title: "Umfassende Dermatologie.<br><span class=\"text-gradient\">Für Ihre Gesundheit.</span>",
        services_desc: "Modernste Diagnostik und Therapie in allen Bereichen der Haut- und Geschlechtskrankheiten.",
        tab_all: "Alle Leistungen",
        tab_klassisch: "Dermatologie &amp; Vorsorge",
        tab_op: "Operationen &amp; Venen",
        tab_spezial: "Ästhetik &amp; Spezialgebiete",

        // Spezialbehandlungen & Arzt
        special_eyebrow: "Spezialgebiete",
        special_title: "Besondere Behandlungen.<br><span class=\"text-gradient\">Höchste Expertise.</span>",
        doctor_eyebrow: "Ihr Hautarzt",

        // Anfahrt
        anfahrt_eyebrow: "So finden Sie uns",
        anfahrt_title: "Anfahrt zur Praxis.<br><span class=\"text-gradient\">Zentral gelegen.</span>",
        anfahrt_addr_title: "Adresse",
        anfahrt_addr_desc: "<strong>Schlossplatz 1, 91054 Erlangen</strong><br><span class=\"anfahrt-subtext\">1. Obergeschoss · Zentral am Erlanger Schlossplatz</span>",
        anfahrt_transit_title: "Öffentliche Verkehrsmittel",
        anfahrt_transit_desc: "<ul class=\"anfahrt-list\"><li><strong>Bahnhof Erlangen:</strong> ca. 3 Gehminuten</li><li><strong>Hugenottenplatz:</strong> ca. 2 Gehminuten</li></ul><span class=\"anfahrt-subtext\">Direkte Anbindung an alle Bahn- &amp; Buslinien.</span>",
        anfahrt_car_title: "Auto &amp; Parken",
        anfahrt_car_desc: "<ul class=\"anfahrt-list\"><li><strong>Großparkplatz am Bahnhof:</strong> wenige Gehminuten</li></ul><span class=\"anfahrt-subtext\">Weitere Parkhäuser: Fuchsenwiese &amp; Erlangen Arcaden.</span>",
        anfahrt_entry_title: "Eingänge &amp; Barrierefreiheit",
        anfahrt_entry_desc: "<ul class=\"anfahrt-list\"><li><strong>Haupteingang:</strong> Schlossplatz 1</li><li><strong>Barrierefrei (Aufzug):</strong> Halbmondstraße (Rückseite)</li></ul>",
        anfahrt_map_title: "Interaktive Karte von Google Maps",
        anfahrt_map_desc: "Zum Schutz Ihrer Privatsphäre wird die interaktive Karte erst geladen, wenn Sie zustimmen. Dabei können Daten an Google übertragen werden.",
        anfahrt_map_btn: "Karte laden &amp; anzeigen",
        anfahrt_map_gmaps: "In Google Maps öffnen"
    },
    en: {
        // Navigation
        nav_quick: "Quick Access",
        nav_online: "Prescription &amp; Cancel",
        nav_services: "Services",
        nav_special: "Special Treatments",
        nav_doctor: "About Doctor",
        nav_anfahrt: "Directions",
        nav_contact: "Contact",
        btn_book: "Book Appointment",
        btn_book_short: "Book Online",

        // Hero
        hero_eyebrow: "Dermatology Practice Erlangen",
        hero_subtitle: "Specialist in Dermatology · Allergology · Outpatient Surgery · Dermatopathology",
        hero_btn_book: "Book Appointment",
        hero_btn_more: "Learn More",

        // Schnellzugriff
        insurance_pill: "All Statutory (GKV) &amp; Private Health Insurances (PKV) Welcome",
        quick_eyebrow: "QUICK ACCESS",
        quick_title: "EVERYTHING YOU NEED",
        quick_desc: "Essential medical services and direct access for all our patients.",
        quick_card_termin_title: "Book Appointment",
        quick_card_termin_desc: "Online appointment booking via Doctolib – simple, fast and available 24/7.",
        quick_card_rezept_title: "Order Prescription",
        quick_card_rezept_desc: "Order repeat prescriptions conveniently online – for existing patients only.",
        quick_card_absage_title: "Cancel Appointment",
        quick_card_absage_desc: "Unable to attend your appointment? Cancel easily online.",
        card_urlaub_badge: "Vacation",

        // Öffnungszeiten
        hours_title: "Our Opening Hours",
        hours_note: "Appointments by arrangement · Emergencies welcome",
        day_mon: "Monday",
        day_tue: "Tuesday",
        day_wed: "Wednesday",
        day_thu: "Thursday",
        day_fri: "Friday",

        // Rezeptbestellung
        rezept_title: "Repeat Prescription",
        rezept_desc: "For existing patients only. Please complete the form below.",
        rezept_label_vorname: "First Name",
        rezept_label_nachname: "Last Name",
        rezept_label_geburt: "Date of Birth",
        rezept_label_telefon: "Phone Number",
        rezept_label_medikament: "Requested Medication(s)",
        rezept_label_anmerkung: "Notes (optional)",
        rezept_consent: "I consent to the processing of my medical request details in accordance with the <a href=\"#datenschutz\" onclick=\"showDatenschutz(event)\">Privacy Policy</a>.*",
        rezept_btn_submit: "Request Prescription",
        rezept_success_title: "Request Sent!",
        rezept_success_desc: "We will process your prescription as soon as possible.",

        // Terminabsage
        absage_title: "Cancel Appointment",
        absage_desc: "Unable to attend your appointment? Please let us know in advance.",
        absage_doctolib_hint: "Booked via Doctolib? You can also cancel directly with 1 click in your <a href=\"https://www.doctolib.de\" target=\"_blank\" rel=\"noopener\">Doctolib account</a>.",
        label_vorname: "First Name",
        label_nachname: "Last Name",
        label_geburt: "Date of Birth",
        label_termin: "Appointment Date",
        label_uhrzeit: "Appointment Time",
        label_grund: "Reason for Cancellation (optional)",
        absage_consent: "I consent to the processing of my cancellation details in accordance with the <a href=\"#datenschutz\" onclick=\"showDatenschutz(event)\">Privacy Policy</a>.*",
        btn_submit_absage: "Cancel Appointment",
        absage_success_title: "Cancellation Sent!",
        absage_success_desc: "Thank you, we have received your appointment cancellation.",

        // Leistungen
        services_eyebrow: "Our Medical Services",
        services_title: "Comprehensive Dermatology.<br><span class=\"text-gradient\">For Your Skin Health.</span>",
        services_desc: "State-of-the-art diagnostics and therapies across all dermatological specialties.",
        tab_all: "All Services",
        tab_klassisch: "Dermatology &amp; Screening",
        tab_op: "Surgery &amp; Veins",
        tab_spezial: "Aesthetics &amp; Specialties",

        // Spezialbehandlungen & Arzt
        special_eyebrow: "Specialties",
        special_title: "Special Treatments.<br><span class=\"text-gradient\">Highest Expertise.</span>",
        doctor_eyebrow: "Your Dermatologist",

        // Anfahrt
        anfahrt_eyebrow: "How to Find Us",
        anfahrt_title: "Directions &amp; Location.<br><span class=\"text-gradient\">Centrally Located.</span>",
        anfahrt_addr_title: "Address",
        anfahrt_addr_desc: "<strong>Schlossplatz 1, 91054 Erlangen</strong><br><span class=\"anfahrt-subtext\">1st Floor · Centrally located at Schlossplatz</span>",
        anfahrt_transit_title: "Public Transport",
        anfahrt_transit_desc: "<ul class=\"anfahrt-list\"><li><strong>Erlangen Train Station:</strong> ~3 min walk</li><li><strong>Hugenottenplatz:</strong> ~2 min walk</li></ul><span class=\"anfahrt-subtext\">Direct connections to all train and bus routes.</span>",
        anfahrt_car_title: "By Car &amp; Parking",
        anfahrt_car_desc: "<ul class=\"anfahrt-list\"><li><strong>Main Station Car Park:</strong> few minutes walk</li></ul><span class=\"anfahrt-subtext\">Additional parking: Parkhaus Fuchsenwiese &amp; Arcaden.</span>",
        anfahrt_entry_title: "Entrances &amp; Accessibility",
        anfahrt_entry_desc: "<ul class=\"anfahrt-list\"><li><strong>Main Entrance:</strong> Schlossplatz 1</li><li><strong>Accessible (Elevator):</strong> Halbmondstraße (Rear entrance)</li></ul>",
        anfahrt_map_title: "Interactive Google Map",
        anfahrt_map_desc: "To protect your privacy, the interactive map will only load after your consent. Data may be transferred to Google.",
        anfahrt_map_btn: "Load &amp; Display Map",
        anfahrt_map_gmaps: "Open in Google Maps"
    }
};

let currentLang = localStorage.getItem('praxis_lang') || 'de';

function setLanguage(lang) {
    if (!translations[lang]) return;
    currentLang = lang;
    try {
        localStorage.setItem('praxis_lang', lang);
    } catch (e) {}

    // Update active classes on language buttons
    document.querySelectorAll('.lang-btn, .mobile-lang-btn').forEach(btn => {
        if (btn.getAttribute('data-lang') === lang) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    // Translate all elements with data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang] && translations[lang][key]) {
            el.innerHTML = translations[lang][key];
        }
    });

    // Translate all elements with data-i18n-placeholder
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (translations[lang] && translations[lang][key]) {
            el.setAttribute('placeholder', translations[lang][key]);
        }
    });

    document.documentElement.lang = lang;
    updateLiveHoursStatus();
}

runWhenDOMReady(() => {
    if (currentLang !== 'de') {
        setLanguage(currentLang);
    }
});
