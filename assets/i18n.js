// Pelori marketing site i18n.
//
// JS-driven translation for a small (3 page) static site. Element
// content is swapped client-side on DOM ready based on, in order:
// 1. ?lang= query param (link-shareable),
// 2. localStorage('pelori-lang') (sticky across visits),
// 3. navigator.language (browser preference),
// 4. English fallback.
//
// Per-language URLs would give better SEO but bloat the source from
// 3 files to 15. The site's primary funnel is App Store / TestFlight,
// not search, so the trade-off favours simplicity.

(function () {
  'use strict';

  const SUPPORTED = ['en', 'nl', 'fr', 'es', 'it'];
  const NATIVE_NAMES = {
    en: 'English',
    nl: 'Nederlands',
    fr: 'Français',
    es: 'Español',
    it: 'Italiano',
  };

  const T = {
    en: {
      'meta.title': 'Pelori — Group cycling, planned together',
      'meta.description': 'Pelori rounds up your crew before the ride: plan group rides, RSVP per week, chat with everyone in one place, and find new rides nearby.',
      'nav.features': 'Features',
      'nav.screens': 'Screens',
      'nav.beta': 'Beta',
      'nav.faq': 'FAQ',
      'lang.aria': 'Language',
      'hero.headline_html': 'Ride <span class="accent">together</span>.<br>We\'ve got the rest.',
      'hero.sub': 'Pelori rounds up your crew before the ride. Sorts the RSVPs. Keeps the conversation in one place. So you can actually ride.',
      'hero.cta_primary': 'Join the open beta',
      'hero.cta_secondary': 'See what\'s in it',
      'features.eyebrow': 'What it does',
      'features.title': 'The bits a group ride actually needs.',
      'features.sub': 'No cockpit dashboards, no leaderboards, no "you\'re 0.4 km behind last Tuesday\'s split." Just the four things you message friends about before every ride.',
      'features.plan.title': 'Plan the ride',
      'features.plan.body': 'Date, time, meeting pin, recurring or one-off. "Every Tuesday at 7pm" is one tap. Invite your crew and the ride lives somewhere everyone can find.',
      'features.rsvp.title': 'Know who\'s coming',
      'features.rsvp.body': 'Per-occurrence RSVPs — going, not going, or maybe. Tap the count to see riders\' faces. Resets every week so the regulars don\'t have to rebook the same ride.',
      'features.chat.title': 'One thread per ride',
      'features.chat.body': 'Group chat right next to the ride it belongs to. Replaces five overlapping group chats with the conversation organised the same way the rides are.',
      'features.discover.title': 'Find rides nearby',
      'features.discover.body': 'Public rides from cycling clubs, bike shops, and weekend crews. Browse the route and meeting point before you commit — one tap to join.',
      'shots.eyebrow': 'In the app',
      'shots.title': 'What it looks like.',
      'shots.alt.myrides': 'My Rides screen with three ride cards and a notification bell',
      'shots.alt.where': 'Ride settings — Where tab with meeting-point map',
      'shots.alt.chat': 'Per-ride group chat with messages from the crew',
      'shots.alt.discover': 'Discover screen showing public rides',
      'cta.title': 'Ride together. Starting now.',
      'cta.sub': 'Pelori is in open beta on iOS and Android via TestFlight and Google Play. Join in with your crew — feedback shapes what ships next.',
      'cta.ios_button': 'Join the iOS beta',
      'cta.android_button': 'Get on Google Play',
      'footer.copyright': '© {year} Pelori. Made for riders who roll out together.',
      'footer.faq': 'FAQ',
      'footer.whatsNew': "What's new",
      'footer.privacy': 'Privacy',
      'footer.terms': 'Terms',
      'footer.contact': 'Contact',
      'legal.back': '← Back to home',
      'legal.en_only': 'This page is available in English only — the app itself is fully localised.',
    },
    nl: {
      'meta.title': 'Pelori — Groepswielrennen, samen gepland',
      'meta.description': 'Pelori brengt je crew samen voor de rit: plan groepsritten, RSVP per week, chat met iedereen op één plek en vind nieuwe ritten in de buurt.',
      'nav.features': 'Functies',
      'nav.screens': 'Schermen',
      'nav.beta': 'Bèta',
      'nav.faq': 'FAQ',
      'lang.aria': 'Taal',
      'hero.headline_html': 'Rijd <span class="accent">samen</span>.<br>De rest doen wij.',
      'hero.sub': 'Pelori brengt je crew bij elkaar voordat je vertrekt. Houdt de aanmeldingen bij. Verzamelt het gesprek op één plek. Zodat jij gewoon kunt rijden.',
      'hero.cta_primary': 'Doe mee aan de open bèta',
      'hero.cta_secondary': 'Bekijk wat erin zit',
      'features.eyebrow': 'Wat het doet',
      'features.title': 'De dingen die een groepsrit echt nodig heeft.',
      'features.sub': 'Geen dashboards, geen ranglijsten, geen "je loopt 0,4 km achter op afgelopen dinsdag." Gewoon de vier dingen waar je voor elke rit met je vrienden over appt.',
      'features.plan.title': 'Plan de rit',
      'features.plan.body': 'Datum, tijd, verzamelpunt, terugkerend of eenmalig. "Elke dinsdag om 19:00" is één tik. Nodig je crew uit en de rit staat ergens waar iedereen hem kan vinden.',
      'features.rsvp.title': 'Weet wie er komt',
      'features.rsvp.body': 'RSVP per rit — gaat mee, niet mee, of misschien. Tik op het aantal om de rijders te zien. Reset elke week, zodat vaste deelnemers niet steeds opnieuw hoeven te bevestigen.',
      'features.chat.title': 'Eén gesprek per rit',
      'features.chat.body': 'Groepschat direct naast de rit waar hij bij hoort. Vervangt vijf overlappende appgroepen met een gesprek dat net zo georganiseerd is als de ritten.',
      'features.discover.title': 'Vind ritten in de buurt',
      'features.discover.body': 'Openbare ritten van wielerclubs, fietswinkels en weekendploegen. Bekijk route en verzamelpunt voordat je je aanmeldt — meedoen is één tik.',
      'shots.eyebrow': 'In de app',
      'shots.title': 'Hoe het eruitziet.',
      'shots.alt.myrides': 'Scherm Mijn ritten met drie ritkaarten en een meldingenbel',
      'shots.alt.where': 'Ritinstellingen — tabblad Waar met verzamelpuntkaart',
      'shots.alt.chat': 'Groepschat per rit met berichten van de crew',
      'shots.alt.discover': 'Ontdek-scherm met openbare ritten',
      'cta.title': 'Rij samen. Vanaf nu.',
      'cta.sub': 'Pelori is in open bèta op iOS en Android via TestFlight en Google Play. Doe mee met je crew — jullie feedback bepaalt wat er volgt.',
      'cta.ios_button': 'Doe mee aan de iOS-bèta',
      'cta.android_button': 'Download op Google Play',
      'footer.copyright': '© {year} Pelori. Gemaakt voor rijders die samen vertrekken.',
      'footer.faq': 'FAQ',
      'footer.whatsNew': 'Wat is nieuw',
      'footer.privacy': 'Privacy',
      'footer.terms': 'Voorwaarden',
      'footer.contact': 'Contact',
      'legal.back': '← Terug naar home',
      'legal.en_only': 'Deze pagina is alleen in het Engels beschikbaar — de app zelf is volledig vertaald.',
    },
    fr: {
      'meta.title': 'Pelori — Le cyclisme en groupe, planifié ensemble',
      'meta.description': 'Pelori rassemble ta team avant la sortie : planifie les sorties de groupe, réponds chaque semaine, discute en un seul endroit et trouve de nouvelles sorties à proximité.',
      'nav.features': 'Fonctions',
      'nav.screens': 'Écrans',
      'nav.beta': 'Bêta',
      'nav.faq': 'FAQ',
      'lang.aria': 'Langue',
      'hero.headline_html': 'Roule <span class="accent">ensemble</span>.<br>On s\'occupe du reste.',
      'hero.sub': 'Pelori rassemble ta team avant le départ. Gère les réponses. Garde la conversation au même endroit. Pour que tu puisses simplement rouler.',
      'hero.cta_primary': 'Rejoindre la bêta ouverte',
      'hero.cta_secondary': 'Voir ce qu\'il y a dedans',
      'features.eyebrow': 'Ce que ça fait',
      'features.title': 'Les vrais essentiels d\'une sortie de groupe.',
      'features.sub': 'Pas de tableau de bord, pas de classement, pas de "tu as 0,4 km de retard sur mardi dernier". Juste les quatre choses dont tu parles à tes potes avant chaque sortie.',
      'features.plan.title': 'Planifie la sortie',
      'features.plan.body': 'Date, heure, point de rendez-vous, récurrente ou ponctuelle. "Tous les mardis à 19h" en un tap. Invite ta team et la sortie est rangée là où tout le monde la retrouve.',
      'features.rsvp.title': 'Sache qui vient',
      'features.rsvp.body': 'Réponses par sortie — présent, absent ou peut-être. Tape le compteur pour voir les visages. Se remet à zéro chaque semaine, donc les habitués n\'ont pas à reconfirmer.',
      'features.chat.title': 'Un seul fil par sortie',
      'features.chat.body': 'Conversation de groupe juste à côté de la sortie correspondante. Remplace cinq groupes WhatsApp qui se chevauchent par une discussion organisée comme les sorties.',
      'features.discover.title': 'Trouve des sorties à côté',
      'features.discover.body': 'Sorties publiques de clubs cyclistes, magasins de vélo et groupes du week-end. Regarde le parcours et le point de rendez-vous avant de t\'engager — un tap pour rejoindre.',
      'shots.eyebrow': 'Dans l\'app',
      'shots.title': 'À quoi ça ressemble.',
      'shots.alt.myrides': 'Écran Mes sorties avec trois cartes de sortie et une cloche de notifications',
      'shots.alt.where': 'Réglages de la sortie — onglet Où avec la carte du point de rendez-vous',
      'shots.alt.chat': 'Conversation de groupe par sortie avec messages de la team',
      'shots.alt.discover': 'Écran Découvrir affichant des sorties publiques',
      'cta.title': 'Roule ensemble. Dès maintenant.',
      'cta.sub': 'Pelori est en bêta ouverte sur iOS et Android via TestFlight et Google Play. Rejoins-nous avec ta team — vos retours façonnent la suite.',
      'cta.ios_button': 'Rejoindre la bêta iOS',
      'cta.android_button': 'Disponible sur Google Play',
      'footer.copyright': '© {year} Pelori. Conçu pour les cyclistes qui roulent ensemble.',
      'footer.faq': 'FAQ',
      'footer.whatsNew': 'Nouveautés',
      'footer.privacy': 'Confidentialité',
      'footer.terms': 'Conditions',
      'footer.contact': 'Contact',
      'legal.back': '← Retour à l\'accueil',
      'legal.en_only': 'Cette page n\'est disponible qu\'en anglais — l\'app elle-même est entièrement traduite.',
    },
    es: {
      'meta.title': 'Pelori — Ciclismo en grupo, planificado juntos',
      'meta.description': 'Pelori reúne a tu grupo antes de la ruta: planifica rutas, responde cada semana, chatea con todos en un mismo lugar y descubre nuevas rutas cerca.',
      'nav.features': 'Características',
      'nav.screens': 'Pantallas',
      'nav.beta': 'Beta',
      'nav.faq': 'FAQ',
      'lang.aria': 'Idioma',
      'hero.headline_html': 'Rueda con <span class="accent">los tuyos</span>.<br>Nosotros ponemos el resto.',
      'hero.sub': 'Pelori reúne a tu grupo antes de la ruta. Organiza las respuestas. Mantiene la conversación en un solo lugar. Para que puedas pedalear sin más.',
      'hero.cta_primary': 'Unirse a la beta abierta',
      'hero.cta_secondary': 'Ver qué tiene',
      'features.eyebrow': 'Qué hace',
      'features.title': 'Lo que de verdad necesita una ruta en grupo.',
      'features.sub': 'Sin paneles de mando, sin clasificaciones, sin "vas 0,4 km por detrás del martes pasado". Solo las cuatro cosas de las que hablas con tu grupo antes de cada salida.',
      'features.plan.title': 'Planifica la ruta',
      'features.plan.body': 'Fecha, hora, punto de encuentro, recurrente o única. "Todos los martes a las 19:00" en un toque. Invita a tu grupo y la ruta queda donde todos pueden encontrarla.',
      'features.rsvp.title': 'Sabe quién viene',
      'features.rsvp.body': 'Confirmación por salida — voy, no voy o quizás. Toca el contador para ver las caras. Se reinicia cada semana, así los habituales no tienen que volver a apuntarse.',
      'features.chat.title': 'Un hilo por ruta',
      'features.chat.body': 'Chat de grupo justo al lado de la ruta a la que pertenece. Sustituye cinco grupos solapados por una conversación organizada igual que las rutas.',
      'features.discover.title': 'Encuentra rutas cerca',
      'features.discover.body': 'Rutas públicas de clubs ciclistas, tiendas de bici y grupos de fin de semana. Mira la ruta y el punto de encuentro antes de apuntarte — un toque para unirte.',
      'shots.eyebrow': 'En la app',
      'shots.title': 'Así se ve.',
      'shots.alt.myrides': 'Pantalla Mis rutas con tres tarjetas de ruta y una campana de notificaciones',
      'shots.alt.where': 'Ajustes de la ruta — pestaña Dónde con mapa del punto de encuentro',
      'shots.alt.chat': 'Chat de grupo por ruta con mensajes del grupo',
      'shots.alt.discover': 'Pantalla Descubrir mostrando rutas públicas',
      'cta.title': 'Rueda con los tuyos. Empezando ya.',
      'cta.sub': 'Pelori está en beta abierta en iOS y Android vía TestFlight y Google Play. Únete con tu grupo — vuestros comentarios moldean lo que viene.',
      'cta.ios_button': 'Unirse a la beta iOS',
      'cta.android_button': 'Disponible en Google Play',
      'footer.copyright': '© {year} Pelori. Hecho para ciclistas que salen juntos.',
      'footer.faq': 'FAQ',
      'footer.whatsNew': 'Novedades',
      'footer.privacy': 'Privacidad',
      'footer.terms': 'Términos',
      'footer.contact': 'Contacto',
      'legal.back': '← Volver al inicio',
      'legal.en_only': 'Esta página solo está disponible en inglés — la app está totalmente traducida.',
    },
    it: {
      'meta.title': 'Pelori — Il ciclismo di gruppo, pianificato insieme',
      'meta.description': 'Pelori raduna la tua squadra prima dell\'uscita: pianifica uscite di gruppo, conferma ogni settimana, chatta con tutti in un solo posto e scopri nuove uscite vicino a te.',
      'nav.features': 'Funzioni',
      'nav.screens': 'Schermate',
      'nav.beta': 'Beta',
      'nav.faq': 'FAQ',
      'lang.aria': 'Lingua',
      'hero.headline_html': 'Pedala <span class="accent">insieme</span>.<br>Al resto pensiamo noi.',
      'hero.sub': 'Pelori raduna la tua squadra prima dell\'uscita. Gestisce le risposte. Tiene la conversazione in un unico posto. Così puoi semplicemente pedalare.',
      'hero.cta_primary': 'Entra nella beta aperta',
      'hero.cta_secondary': 'Scopri cosa c\'è dentro',
      'features.eyebrow': 'Cosa fa',
      'features.title': 'Quello che a un\'uscita di gruppo serve davvero.',
      'features.sub': 'Niente cruscotti, niente classifiche, niente "sei 0,4 km dietro al martedì scorso". Solo le quattro cose di cui parli con gli amici prima di ogni uscita.',
      'features.plan.title': 'Pianifica l\'uscita',
      'features.plan.body': 'Data, ora, punto di ritrovo, ricorrente o una tantum. "Ogni martedì alle 19" in un tap. Invita la squadra e l\'uscita resta dove tutti la possono trovare.',
      'features.rsvp.title': 'Sai chi viene',
      'features.rsvp.body': 'Conferme per ogni uscita — ci sono, non vengo o forse. Tocca il contatore per vedere i volti. Si azzera ogni settimana, così gli abituali non devono confermare di nuovo.',
      'features.chat.title': 'Un filo per ogni uscita',
      'features.chat.body': 'Chat di gruppo proprio accanto all\'uscita a cui appartiene. Sostituisce cinque chat sovrapposte con una conversazione organizzata come le uscite.',
      'features.discover.title': 'Trova uscite vicino a te',
      'features.discover.body': 'Uscite pubbliche di club ciclistici, negozi di bici e gruppi del weekend. Guarda il percorso e il ritrovo prima di impegnarti — un tap per partecipare.',
      'shots.eyebrow': 'Nell\'app',
      'shots.title': 'Com\'è fatta.',
      'shots.alt.myrides': 'Schermata Le mie uscite con tre carte uscita e una campana di notifiche',
      'shots.alt.where': 'Impostazioni uscita — scheda Dove con la mappa del ritrovo',
      'shots.alt.chat': 'Chat di gruppo per uscita con i messaggi della squadra',
      'shots.alt.discover': 'Schermata Scopri con uscite pubbliche',
      'cta.title': 'Pedala insieme. A partire da ora.',
      'cta.sub': 'Pelori è in beta aperta su iOS e Android tramite TestFlight e Google Play. Unisciti con la tua squadra — i vostri feedback plasmano i prossimi passi.',
      'cta.ios_button': 'Entra nella beta iOS',
      'cta.android_button': 'Disponibile su Google Play',
      'footer.copyright': '© {year} Pelori. Pensato per chi pedala insieme.',
      'footer.faq': 'FAQ',
      'footer.whatsNew': 'Novità',
      'footer.privacy': 'Privacy',
      'footer.terms': 'Termini',
      'footer.contact': 'Contatti',
      'legal.back': '← Torna alla home',
      'legal.en_only': 'Questa pagina è disponibile solo in inglese — l\'app è completamente tradotta.',
    },
  };

  function pickLang() {
    const params = new URLSearchParams(window.location.search);
    const fromUrl = params.get('lang');
    if (fromUrl && SUPPORTED.includes(fromUrl)) return fromUrl;
    try {
      const stored = localStorage.getItem('pelori-lang');
      if (stored && SUPPORTED.includes(stored)) return stored;
    } catch (e) {
      // localStorage may be denied (private browsing); fall through.
    }
    const browser = (navigator.language || 'en').slice(0, 2).toLowerCase();
    if (SUPPORTED.includes(browser)) return browser;
    return 'en';
  }

  function lookup(t, key) {
    return t[key] !== undefined ? t[key] : T.en[key];
  }

  function applyLang(lang) {
    const t = T[lang] || T.en;
    const year = new Date().getFullYear();
    document.documentElement.lang = lang;

    // Document head
    const title = lookup(t, 'meta.title');
    if (title) document.title = title;
    const desc = document.querySelector('meta[name="description"]');
    if (desc) {
      const v = lookup(t, 'meta.description');
      if (v) desc.setAttribute('content', v);
    }
    const ogTitle = document.querySelector('meta[property="og:title"]');
    if (ogTitle && title) ogTitle.setAttribute('content', title);
    const ogDesc = document.querySelector('meta[property="og:description"]');
    if (ogDesc) {
      const v = lookup(t, 'meta.description');
      if (v) ogDesc.setAttribute('content', v);
    }

    // Body — three flavours of marker:
    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      const key = el.getAttribute('data-i18n');
      const v = lookup(t, key);
      if (v !== undefined) {
        el.textContent = v.replace('{year}', year);
      }
    });
    document.querySelectorAll('[data-i18n-html]').forEach(function (el) {
      const key = el.getAttribute('data-i18n-html');
      const v = lookup(t, key);
      if (v !== undefined) el.innerHTML = v;
    });
    document.querySelectorAll('[data-i18n-alt]').forEach(function (el) {
      const key = el.getAttribute('data-i18n-alt');
      const v = lookup(t, key);
      if (v !== undefined) el.setAttribute('alt', v);
    });
    // Locale-keyed image sources — the attribute holds the full src
    // path with `{lang}` as a placeholder, e.g.
    //   <img data-i18n-src="assets/screenshots/{lang}/02-my-rides.png">
    // The JS substitutes the active locale on apply. Used by the
    // marketing screenshots on the home page so each language sees
    // its own captured + composed set.
    document.querySelectorAll('[data-i18n-src]').forEach(function (el) {
      const tpl = el.getAttribute('data-i18n-src');
      if (tpl) el.setAttribute('src', tpl.replace('{lang}', lang));
    });

    // Reflect on the picker button + menu + persist.
    const flag = document.getElementById('lang-flag');
    if (flag) flag.className = 'lang-flag lang-' + lang;
    const nameEl = document.getElementById('lang-name');
    if (nameEl) nameEl.textContent = NATIVE_NAMES[lang] || NATIVE_NAMES.en;
    const menu = document.getElementById('lang-menu');
    if (menu) {
      menu.querySelectorAll('li').forEach(function (li) {
        const active = li.dataset.value === lang;
        li.setAttribute('aria-selected', active ? 'true' : 'false');
      });
    }
    try {
      localStorage.setItem('pelori-lang', lang);
    } catch (e) {
      // ignore
    }

    // Show the "available in English only" banner on legal pages when
    // we're rendering a non-English chrome. Hidden on English so it
    // doesn't shout the obvious.
    const banner = document.querySelector('[data-legal-en-only]');
    if (banner) banner.hidden = lang === 'en';
  }

  function setupPicker() {
    const picker = document.getElementById('lang-picker');
    const btn = document.getElementById('lang-btn');
    const menu = document.getElementById('lang-menu');
    if (!picker || !btn || !menu) return;

    // Populate the menu once. Each item carries the language's flag
    // chip + native name, plus a data-value used by the click handler.
    menu.innerHTML = SUPPORTED.map(function (code) {
      return (
        '<li role="option" data-value="' + code + '" tabindex="-1">' +
          '<span class="lang-flag lang-' + code + '" aria-hidden="true"></span>' +
          '<span>' + NATIVE_NAMES[code] + '</span>' +
        '</li>'
      );
    }).join('');

    function open() {
      menu.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
      // Move focus into the menu so arrow keys work straight away.
      const active = menu.querySelector('li[aria-selected="true"]')
        || menu.querySelector('li');
      if (active) active.focus();
    }
    function close() {
      menu.hidden = true;
      btn.setAttribute('aria-expanded', 'false');
    }
    function toggle() {
      if (menu.hidden) open(); else close();
    }

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      toggle();
    });

    menu.addEventListener('click', function (e) {
      const li = e.target.closest('li[data-value]');
      if (!li) return;
      applyLang(li.dataset.value);
      close();
      btn.focus();
    });

    // Keyboard nav — arrow keys move between options, Enter/Space
    // selects, Escape closes and returns focus to the button.
    menu.addEventListener('keydown', function (e) {
      const items = Array.from(menu.querySelectorAll('li'));
      const idx = items.indexOf(document.activeElement);
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        const next = items[(idx + 1 + items.length) % items.length];
        if (next) next.focus();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        const prev = items[(idx - 1 + items.length) % items.length];
        if (prev) prev.focus();
      } else if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        const li = document.activeElement;
        if (li && li.dataset && li.dataset.value) {
          applyLang(li.dataset.value);
          close();
          btn.focus();
        }
      } else if (e.key === 'Escape') {
        e.preventDefault();
        close();
        btn.focus();
      }
    });

    // Click outside the picker closes it.
    document.addEventListener('click', function (e) {
      if (!picker.contains(e.target)) close();
    });
    // Escape on the trigger itself also closes (covers the case where
    // focus is on the button rather than inside the menu).
    btn.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        close();
      } else if (e.key === 'ArrowDown' || e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        open();
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    setupPicker();
    applyLang(pickLang());
  });
})();
