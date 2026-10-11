// Mobile menu, dropdown, events filter, contact form
const nav = document.querySelector('.nav'), burger = document.querySelector('.burger');
burger.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  burger.setAttribute('aria-expanded', open);
});
document.querySelectorAll('.dd > button').forEach(b => b.addEventListener('click', () => b.parentElement.classList.toggle('open')));
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
