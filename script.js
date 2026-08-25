(() => {
  // Mobile nav toggle
  const toggle = document.querySelector('.nav__toggle');
  const list = document.getElementById('nav-list');
  if (toggle && list) {
    toggle.addEventListener('click', () => {
      const open = list.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    list.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        if (list.classList.contains('is-open')) {
          list.classList.remove('is-open');
          toggle.setAttribute('aria-expanded', 'false');
        }
      });
    });
  }

  // Footer year
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // Hero slideshow: cross-fade through the hero background images.
  // Honours prefers-reduced-motion (stays on the first image).
  const heroShow = document.querySelector('[data-hero-slideshow]');
  if (heroShow) {
    const slides = heroShow.querySelectorAll('img');
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (slides.length > 1 && !reduce) {
      let i = 0;
      setInterval(() => {
        slides[i].classList.remove('is-active');
        i = (i + 1) % slides.length;
        slides[i].classList.add('is-active');
      }, 5000);
    }
  }

  // Mega nav (click-to-toggle on top of hover-to-open)
  const megaItems = document.querySelectorAll('.nav__item--mega');
  megaItems.forEach(item => {
    const trigger = item.querySelector('.nav__trigger');
    if (!trigger) return;
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const isOpen = item.classList.toggle('is-open');
      trigger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      if (isOpen) {
        megaItems.forEach(other => {
          if (other !== item) {
            other.classList.remove('is-open');
            other.querySelector('.nav__trigger')?.setAttribute('aria-expanded', 'false');
          }
        });
      }
    });
  });
  document.addEventListener('click', (e) => {
    megaItems.forEach(item => {
      if (item.classList.contains('is-open') && !item.contains(e.target)) {
        item.classList.remove('is-open');
        item.querySelector('.nav__trigger')?.setAttribute('aria-expanded', 'false');
      }
    });
  });
  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    megaItems.forEach(item => {
      if (item.classList.contains('is-open')) {
        item.classList.remove('is-open');
        item.querySelector('.nav__trigger')?.setAttribute('aria-expanded', 'false');
      }
    });
  });

  // Header: scroll-state styling + hide on scroll-down, reveal on scroll-up
  const header = document.querySelector('[data-site-header]');
  if (header) {
    let lastY = window.scrollY;
    const TOP_BUFFER = 60;
    const HIDE_THRESHOLD = 12;

    const onScroll = () => {
      const y = window.scrollY;

      if (y > TOP_BUFFER) header.classList.add('is-scrolled');
      else header.classList.remove('is-scrolled');

      const delta = y - lastY;
      const navOpen = header.querySelector('.nav__list.is-open')
                   || header.querySelector('.nav__item--mega.is-open');

      if (y <= TOP_BUFFER) {
        header.classList.remove('is-hidden');
      } else if (!navOpen && delta > HIDE_THRESHOLD) {
        header.classList.add('is-hidden');
      } else if (delta < -HIDE_THRESHOLD) {
        header.classList.remove('is-hidden');
      }

      lastY = y;
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Carousel
  document.querySelectorAll('[data-carousel]').forEach((root) => {
    const track = root.querySelector('.carousel__track');
    const slides = root.querySelectorAll('.carousel__slide');
    const prev = root.querySelector('.carousel__arrow--prev');
    const next = root.querySelector('.carousel__arrow--next');
    const dotsList = root.querySelector('.carousel__dots');
    if (!track || slides.length === 0) return;

    let index = 0;
    const count = slides.length;

    const dotButtons = [];
    if (dotsList) {
      slides.forEach((_, i) => {
        const li = document.createElement('li');
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.setAttribute('aria-label', `Go to slide ${i + 1}`);
        btn.addEventListener('click', () => go(i));
        li.appendChild(btn);
        dotsList.appendChild(li);
        dotButtons.push(btn);
      });
    }

    const update = () => {
      track.style.transform = `translateX(-${index * 100}%)`;
      slides.forEach((s, i) => s.setAttribute('aria-hidden', i === index ? 'false' : 'true'));
      dotButtons.forEach((b, i) => {
        if (i === index) b.setAttribute('aria-current', 'true');
        else b.removeAttribute('aria-current');
      });
    };

    const go = (i) => { index = (i + count) % count; update(); };

    if (prev) prev.addEventListener('click', () => go(index - 1));
    if (next) next.addEventListener('click', () => go(index + 1));

    root.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') { go(index - 1); }
      else if (e.key === 'ArrowRight') { go(index + 1); }
    });

    // Touch swipe
    let touchStartX = 0;
    let touchDeltaX = 0;
    track.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; touchDeltaX = 0; }, { passive: true });
    track.addEventListener('touchmove',  (e) => { touchDeltaX = e.touches[0].clientX - touchStartX; }, { passive: true });
    track.addEventListener('touchend',   () => {
      if (Math.abs(touchDeltaX) > 40) go(index + (touchDeltaX < 0 ? 1 : -1));
    });

    update();
  });

  // Booking: reveal indicative pricing when a priced service is selected.
  // A .pricepanel[data-price-for="X"] shows when the trigger select value === X.
  document.querySelectorAll('[data-price-trigger]').forEach((select) => {
    const panels = document.querySelectorAll('.pricepanel[data-price-for]');
    const sync = () => {
      panels.forEach((panel) => {
        panel.hidden = panel.getAttribute('data-price-for') !== select.value;
      });
    };
    select.addEventListener('change', sync);
    sync();
  });

  // Combined contact form: toggle between "Book a job" and "Request a quote".
  // Shows/hides [data-mode] field groups and updates the subject, submit label
  // and heading. Preselects from ?type=quote or #quote (so "Get a quote" links
  // land in quote mode). Booking is the default.
  const reqForm = document.querySelector('[data-request-form]');
  if (reqForm) {
    const radios = reqForm.querySelectorAll('input[name="request_type"]');
    const subject = reqForm.querySelector('input[name="_subject"]');
    const submitBtn = reqForm.querySelector('[data-form-submit]');
    const title = reqForm.querySelector('[data-form-title]');
    const hint = reqForm.querySelector('[data-form-hint]');

    const applyMode = (mode) => {
      const quote = mode === 'quote';
      reqForm.querySelectorAll('[data-mode="quote"]').forEach((el) => { el.hidden = !quote; });
      reqForm.querySelectorAll('[data-mode="booking"]').forEach((el) => { el.hidden = quote; });
      if (subject) subject.value = quote
        ? 'New quote request - hoaddrainage.com.au'
        : 'New booking request - hoaddrainage.com.au';
      if (submitBtn) submitBtn.textContent = quote ? 'Send quote request' : 'Send booking request';
      if (title) title.textContent = quote ? 'Request a quote' : 'Book a job';
      if (hint) hint.textContent = quote
        ? 'Send as much detail as you can, including photos and plans, and we\'ll come back with a price.'
        : 'Booking a CCTV inspection or drain clear? You\'ll see indicative pricing as you choose a service.';
    };

    radios.forEach((r) => r.addEventListener('change', () => {
      if (r.checked) applyMode(r.value === 'Quote' ? 'quote' : 'booking');
    }));

    const params = new URLSearchParams(window.location.search);
    const wantsQuote = params.get('type') === 'quote' || window.location.hash === '#quote';
    const initial = wantsQuote ? 'quote' : 'booking';
    radios.forEach((r) => { r.checked = (initial === 'quote' ? r.value === 'Quote' : r.value === 'Booking'); });
    applyMode(initial);
  }

  // Lead / contact forms. With a real Formspree endpoint wired, submit via
  // fetch and send the visitor to the thank-you page (relative redirect, so
  // it works on any origin). The hidden _next field is the no-JS fallback.
  // While the action is still the placeholder we show a graceful in-page
  // confirmation instead (scaffold build, no backend yet).
  const THANK_YOU_URL = 'thank-you.html';
  document.querySelectorAll('.contact__form').forEach((form) => {
    form.addEventListener('submit', (e) => {
      const action = form.getAttribute('action') || '';
      const isPlaceholder = !action || action.includes('YOUR_FORM_ID');

      if (!isPlaceholder) {
        // Live endpoint: post via fetch, then redirect on success.
        e.preventDefault();
        const btn = form.querySelector('button[type="submit"]');
        const originalText = btn ? btn.textContent : '';
        if (btn) { btn.disabled = true; btn.textContent = 'Sending...'; }
        fetch(action, {
          method: 'POST',
          body: new FormData(form),
          headers: { 'Accept': 'application/json' }
        }).then((res) => {
          if (res.ok) {
            window.location.href = THANK_YOU_URL;
          } else {
            // Let the browser submit natively (Formspree handles _next / errors).
            form.submit();
          }
        }).catch(() => {
          form.submit();
        });
        return;
      }

      e.preventDefault();
      const success = form.querySelector('[data-form-success]');
      const btn = form.querySelector('button[type="submit"]');
      if (success) {
        success.hidden = false;
        success.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      if (!btn) return;
      const original = btn.textContent;
      btn.textContent = 'Sent. We\'ll be in touch.';
      btn.disabled = true;
      setTimeout(() => {
        btn.textContent = original;
        btn.disabled = false;
        form.reset();
        if (success) success.hidden = true;
        document.querySelectorAll('.pricepanel[data-price-for]').forEach((p) => { p.hidden = true; });
      }, 4000);
    });
  });
})();

/* --- Ad attribution ------------------------------------------------------
   Captures the Google Ads click id (and utm_* if present) on the first page
   of the visit, keeps it for the session, and stamps it into every lead form
   as hidden fields. Without this a paid lead arrives in the inbox looking
   identical to an organic one, and the Formspree poller logs it as organic
   (it reads `source`). Runs at load, not at submit, so the values are already
   in the form when FormData is built.
-------------------------------------------------------------------------- */
(function () {
  var KEY = 'hoad_attr';

  function read() {
    try { return JSON.parse(sessionStorage.getItem(KEY) || 'null'); } catch (e) { return null; }
  }

  function capture() {
    var stored = read();
    if (stored) return stored;                       // first touch wins

    var p = new URLSearchParams(window.location.search);
    var clickId = p.get('gclid') || p.get('gbraid') || p.get('wbraid') || '';
    var utmSource = p.get('utm_source') || '';
    if (!clickId && !utmSource) return null;         // organic visit, nothing to stamp

    var attr = {
      source: clickId ? 'google-ads' : utmSource,
      gclid: clickId,
      campaign: p.get('utm_campaign') || '',
      term: p.get('utm_term') || '',
      landing_page: window.location.pathname
    };
    try { sessionStorage.setItem(KEY, JSON.stringify(attr)); } catch (e) {}
    return attr;
  }

  function stamp(attr) {
    if (!attr) return;
    document.querySelectorAll('form[data-lead-form], .contact__form').forEach(function (form) {
      Object.keys(attr).forEach(function (name) {
        if (!attr[name] || form.querySelector('input[name="' + name + '"]')) return;
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = name;
        input.value = attr[name];
        form.appendChild(input);
      });
    });
  }

  stamp(capture());
})();
