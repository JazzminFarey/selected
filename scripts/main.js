// Jazz portfolio — interactions
(() => {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Sticky nav border when scrolled
  const nav = document.querySelector('.nav');
  if (nav) {
    const onScroll = () => nav.classList.toggle('is-scrolled', window.scrollY > 8);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Stagger project card reveals so they cascade rather than fire together
  document.querySelectorAll('.showcase .proj.reveal').forEach((el, i) => {
    el.style.transitionDelay = `${60 + i * 80}ms`;
  });

  // Reveal on scroll
  const reveals = document.querySelectorAll('.reveal');
  if (reveals.length && !reduceMotion && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add('is-in');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('is-in'));
  }

  // Outbound page transition.
  // Chrome/Edge with cross-document View Transitions support handle the
  // outbound + inbound crossfade natively via the @view-transition CSS rule.
  // For Safari/Firefox we fall back to a JS-driven leave-fade so the user
  // never sees a hard white flash between pages.
  const supportsCrossDocVT = 'onpageswap' in window;
  if (!reduceMotion && !supportsCrossDocVT) {
    document.addEventListener('click', (e) => {
      // Honor middle-click, modifier keys, and right-click
      if (e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      const a = e.target.closest('a');
      if (!a) return;
      const href = a.getAttribute('href');
      if (!href) return;
      if (href.startsWith('#')) return;
      if (href.startsWith('mailto:') || href.startsWith('tel:')) return;
      if (a.target && a.target !== '_self') return;
      if (a.hasAttribute('download')) return;
      let url;
      try { url = new URL(a.href, window.location.href); } catch (_) { return; }
      if (url.origin !== window.location.origin) return;
      // Same path + same query = treat as in-page (anchor handles itself)
      if (url.pathname === window.location.pathname && url.search === window.location.search) return;

      e.preventDefault();
      document.body.classList.add('is-leaving');
      window.setTimeout(() => { window.location.href = a.href; }, 220);
    });

    // If user navigates back via bfcache, strip the leaving class
    window.addEventListener('pageshow', () => {
      document.body.classList.remove('is-leaving');
    });
  }

  // Update copyright year
  const yr = document.querySelector('[data-year]');
  if (yr) yr.textContent = new Date().getFullYear();
})();
