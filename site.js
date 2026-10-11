// Menu: mobile sheet blooms from the burger button; desktop dropdown opens under its button
const nav = document.querySelector('.nav'), burger = document.querySelector('.burger');
function setMenu(open) {
  if (open) {
    const r = burger.getBoundingClientRect();
    nav.style.setProperty('--ox', (r.left + r.width / 2) + 'px');
    nav.style.setProperty('--oy', (r.top + r.height / 2) + 'px');
  }
  nav.classList.toggle('open', open);
  burger.setAttribute('aria-expanded', open);
  document.body.style.overflow = open ? 'hidden' : '';
}
burger.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
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
// Ambient video: show sound toggle only when a video actually loads
const vid = document.querySelector('.vslot video'), vbtn = document.querySelector('.vsound');
if (vid && vbtn) {
  // autoplay (muted is allowed everywhere); retry on first touch if the browser blocked it
  const tryPlay = () => vid.play().catch(() => {});
  tryPlay();
  ['click','touchstart','scroll'].forEach(ev => addEventListener(ev, tryPlay, { once: true, passive: true }));
  document.addEventListener('visibilitychange', () => { if (!document.hidden) tryPlay(); });
  vid.addEventListener('loadeddata', () => { vbtn.hidden = false; });
  vbtn.addEventListener('click', () => {
    vid.muted = !vid.muted;
    vbtn.textContent = vid.muted ? '🔇' : '🔊';
    vbtn.setAttribute('aria-label', vid.muted ? 'הפעלת צליל' : 'השתקה');
  });
}
// Header shrinks smoothly with scroll position (--p goes 0 -> 1 over the first 220px)
let ticking = false;
function updateHeader() {
  const p = Math.min(Math.max(scrollY / 220, 0), 1);
  document.documentElement.style.setProperty('--p', p.toFixed(3));
  ticking = false;
}
addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(updateHeader); } }, { passive: true });
updateHeader();
