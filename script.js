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

  // Hero video: pause for users who prefer reduced motion (poster remains visible)
  const heroVideo = document.querySelector('.hero__video');
  if (heroVideo && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    heroVideo.pause();
    heroVideo.removeAttribute('autoplay');
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

  // Mock form submit - mockup only, replace with Formspree on launch
  const form = document.querySelector('.contact__form');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const btn = form.querySelector('button[type="submit"]');
      if (!btn) return;
      const original = btn.textContent;
      btn.textContent = 'Sent. We\'ll be in touch.';
      btn.disabled = true;
      setTimeout(() => {
        btn.textContent = original;
        btn.disabled = false;
        form.reset();
      }, 3500);
    });
  }
})();
