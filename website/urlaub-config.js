/**
 * ============================================================
 * URLAUBS- & VERTRETUNGS-KONFIGURATION
 * Hautarztpraxis Dr. med. Rahemi Pour
 * ============================================================
 * 
 * ANLEITUNG:
 * 1. Status festlegen:
 *    - 'auto' : Aktiviert den Urlaubsmodus automatisch zwischen 'von' und 'bis'.
 *    - 'an'   : Urlaubsmodus sofort erzwingen (z. B. für Tests oder kurzfristige Schließungen).
 *    - 'aus'  : Urlaubsmodus komplett ausschalten.
 * 
 * 2. Zeitraum und Wiedereröffnung eintragen (Datum im Format: JJJJ-MM-TT).
 * 3. Vertretungspraxen eintragen (beliebig viele Einträge möglich).
 */

const urlaubConfig = {
    // 'auto' | 'an' | 'aus'
    status: 'auto', // Zum ersten Testen auf 'an' gesetzt, damit Sie das Ergebnis sofort sehen

    // Urlaubszeitraum (Format: JJJJ-MM-TT)
    von: "2026-10-01",
    bis: "2026-10-02",

    // Wann die Praxis wieder regulär erreichbar ist
    wiederDaAb: "Freitag, den 02. Oktober 2026",

    // Kurzer Text für den Announcement-Banner oben
    bannerText: "Praxis geschlossen wegen Kongress",

    // Vertretungspraxen während der Schließzeit
    vertretungen: [
        
        {
            name: "Dermatologisches Zentrum Erlangen",
            fach: "Gemeinschaftspraxis für Hauterkrankungen",
            adresse: "Nürnberger Straße 42, 91052 Erlangen",
            telefon: "09131 987654",
            telefonLink: "+499131987654",
            hinweis: "Akutsprechstunde Mo–Fr von 08:30 bis 10:00 Uhr"
        }
    ],

    // Ärztlicher Bereitschaftsdienst / Notdienst
    notdienst: {
        titel: "Dringende Notfälle & Ärztlicher Bereitschaftsdienst",
        telefon: "116 117",
        hinweis: "Bundesweiter ärztlicher Bereitschaftsdienst bei akuten Beschwerden außerhalb der Öffnungszeiten (kostenfrei, ohne Vorwahl)."
    }
};
