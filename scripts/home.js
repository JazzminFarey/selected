// Play the Flex preview only on deliberate desktop hover or keyboard focus.
(() => {
 const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
 const hover = matchMedia('(hover: hover) and (pointer: fine)');
 document.querySelectorAll('.tile-loop').forEach(video => {
   const card = video.closest('.proj');
   const stop = () => { video.pause(); card.classList.remove('is-playing'); };
   const start = async () => {
     if (reduceMotion.matches || !hover.matches) return;
     if (!video.getAttribute('src')) video.src = video.dataset.src;
     try { await video.play(); if (!video.paused) card.classList.add('is-playing'); } catch (_) { stop(); }
   };
   card.addEventListener('mouseenter', start);
   card.addEventListener('mouseleave', stop);
   card.addEventListener('focus', start);
   card.addEventListener('blur', stop);
   document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
   reduceMotion.addEventListener('change', stop);
 });
})();
