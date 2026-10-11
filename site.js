// Menu: mobile sheet blooms from the burger button; desktop dropdown opens under its button
const nav = document.querySelector('.nav'), burger = document.querySelector('.burger');
// The sheet blooms from the burger. Keep the origin current at all times (not only on click),
// otherwise the very first open animates from the CSS fallback position.
function placeOrigin() {
  const r = burger.getBoundingClientRect();
  if (!r.width) return;
  nav.style.setProperty('--ox', (r.left + r.width / 2) + 'px');
  nav.style.setProperty('--oy', (r.top + r.height / 2) + 'px');
}
placeOrigin();
addEventListener('resize', placeOrigin);
addEventListener('load', placeOrigin);
if (document.fonts && document.fonts.ready) document.fonts.ready.then(placeOrigin);
function setMenu(open) {
  if (open) placeOrigin();
  nav.classList.toggle('open', open);
  burger.setAttribute('aria-expanded', open);
  document.body.style.overflow = open ? 'hidden' : '';
}
burger.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
// Page transitions: a plum circle blooms from the click point, the next page reveals by shrinking it back
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
function leave(href, x, y, withCurtain) {
  try { sessionStorage.setItem('pt', Math.round(x) + ',' + Math.round(y)); } catch (e) {}
  if (reduceMotion) { location.href = href; return; }
  if (withCurtain) {
    const c = document.createElement('div');
    c.className = 'ptcurtain';
    c.style.setProperty('--px', x + 'px');
    c.style.setProperty('--py', y + 'px');
    document.body.appendChild(c);
    requestAnimationFrame(() => requestAnimationFrame(() => c.classList.add('on')));
  }
  setTimeout(() => { location.href = href; }, withCurtain ? 520 : 220);
}
document.addEventListener('click', e => {
  const a = e.target.closest('a[href]');
  if (!a || e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank' || a.hasAttribute('download')) return;
  const raw = a.getAttribute('href');
  if (!raw || raw === '#') return;
  const u = new URL(a.href, location.href);
  if (u.origin !== location.origin) return;
  const menuOpen = nav.classList.contains('open');
  if (u.pathname === location.pathname && u.hash) {
    if (menuOpen) { e.preventDefault(); setMenu(false); setTimeout(() => { location.hash = u.hash; }, 650); }
    return;
  }
  e.preventDefault();
  let x = e.clientX, y = e.clientY;
  if (menuOpen || !e.detail) {
    const r = (menuOpen ? burger : a).getBoundingClientRect();
    x = r.left + r.width / 2; y = r.top + r.height / 2;
  }
  // with the mobile sheet open, it already covers the screen: keep it, the next page shrinks it toward the burger
  leave(u.href, x, y, !menuOpen);
});
addEventListener('pageshow', e => {
  if (!e.persisted) return;
  document.querySelectorAll('.ptcurtain').forEach(c => c.remove());
  setMenu(false);
});
document.addEventListener('keydown', e => {
  if (e.key !== 'Escape') return;
  setMenu(false);
  document.querySelectorAll('.dd.open').forEach(d => d.classList.remove('open'));
});
window.addEventListener('resize', () => { if (innerWidth > 860) setMenu(false); });
document.querySelectorAll('.dd > button').forEach(b => b.addEventListener('click', e => {
  e.stopPropagation();
  const d = b.parentElement, open = d.classList.toggle('open');
  b.setAttribute('aria-expanded', open);
}));
document.addEventListener('click', () => document.querySelectorAll('.dd.open').forEach(d => d.classList.remove('open')));
// events filter placeholder
document.querySelectorAll('.pill').forEach(p => p.addEventListener('click', () => {
  document.querySelectorAll('.pill').forEach(x => x.classList.remove('on'));
  p.classList.add('on'); // TODO: filter real events by space once events exist
}));
// Placeholders until real links / form endpoint are provided
document.querySelectorAll('a[data-todo]').forEach(a => a.addEventListener('click', e => e.preventDefault()));
const form = document.getElementById('contact-form');
if (form) form.addEventListener('submit', e => {
  e.preventDefault();
  form.querySelector('.form-msg').textContent = 'תודה! (הטופס עדיין לא מחובר לשליחה. יש לחבר שירות טפסים לפני העלייה לאוויר.)';
});
// Ambient video: silent, seamless loop (landscape triptych on wide screens, portrait cut on phones)
const vid = document.querySelector('.vslot video');
if (vid) {
  // autoplay (muted is allowed everywhere); retry on first touch if the browser blocked it
  const tryPlay = () => vid.play().catch(() => {});
  tryPlay();
  ['click','touchstart','scroll'].forEach(ev => addEventListener(ev, tryPlay, { once: true, passive: true }));
  document.addEventListener('visibilitychange', () => { if (!document.hidden) tryPlay(); });
  // the poster image sits behind with identical framing; fade the video in once it is really playing
  const show = () => vid.classList.add('on');
  vid.addEventListener('playing', show, { once: true });
  if (!vid.paused && vid.readyState > 2) show();
}
// Header shrinks smoothly with scroll position (--p goes 0 -> 1 over the first 220px)
let ticking = false;
function updateHeader() {
  const p = Math.min(Math.max(scrollY / 220, 0), 1);
  document.documentElement.style.setProperty('--p', p.toFixed(3));
  placeOrigin();
  ticking = false;
}
addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(updateHeader); } }, { passive: true });
updateHeader();
