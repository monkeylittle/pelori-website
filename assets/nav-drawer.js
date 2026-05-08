// Mobile hamburger nav toggle.
//
// Wired to <button id="nav-burger"> in the page header — adds /
// removes a `.nav-open` class on <body> which the CSS uses to slide
// the drawer in from the right and dim the page behind it. Closing
// is allowed via the close button, the page scrim, the Escape key,
// or tapping any link inside the drawer (so back-navigating to the
// page doesn't leave it stuck open).
(function () {
  'use strict';

  const burger = document.getElementById('nav-burger');
  const drawer = document.getElementById('nav-drawer');
  if (!burger || !drawer) return;

  function setOpen(open) {
    document.body.classList.toggle('nav-open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
  }

  burger.addEventListener('click', () => {
    setOpen(!document.body.classList.contains('nav-open'));
  });

  // Close on any element flagged with [data-nav-close] (the X button
  // and every drawer link).
  drawer.querySelectorAll('[data-nav-close]').forEach((el) => {
    el.addEventListener('click', () => setOpen(false));
  });

  // Tap-on-scrim close. The scrim is the body's ::after pseudo-element
  // generated when .nav-open is on, so we can't bind directly to it —
  // instead, treat any click outside the drawer (and outside the
  // burger button) as a request to close.
  document.addEventListener('click', (e) => {
    if (!document.body.classList.contains('nav-open')) return;
    if (drawer.contains(e.target) || burger.contains(e.target)) return;
    setOpen(false);
  });

  // Escape key.
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && document.body.classList.contains('nav-open')) {
      setOpen(false);
    }
  });
})();
