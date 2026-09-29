// Native controls always allow pausing. Respect reduced motion and visibility.
(() => {
  const video = document.querySelector('.home-motion video');
  if (!video) return;
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  if (!preference.matches) video.play().catch(() => {});
  preference.addEventListener('change', () => { if (preference.matches) video.pause(); });
  document.addEventListener('visibilitychange', () => { if (document.hidden) video.pause(); });
})();
