/* ──────────────────────────────────────────
    darkweb666  ·  MAXIMALIST PROFESSIONAL LEAK JS
   ────────────────────────────────────────── */

// Aktualizacja czasu ostatniej aktualizacji
function updateLastUpdateTime() {
  const el = document.getElementById('last-update');
  if (!el) return;
  el.textContent = new Date().toLocaleString();
}

// Animacje fade-in elementów po załadowaniu
function fadeInElements() {
  const sections = document.querySelectorAll('.section, .gallery-item');
  sections.forEach((el, i) => {
    setTimeout(() => {
      el.classList.add('visible');
    }, i * 120);
  });
}

// Kopiowanie adresu .onion
function copyOnion() {
  const onionElement = document.getElementById('onion');
  if (!onionElement) return;
  navigator.clipboard.writeText(onionElement.innerText)
    .then(() => alert('Adres .onion skopiowany ✅'))
    .catch(() => alert('Błąd kopiowania adresu .onion ❌'));
}

// Logowanie interakcji użytkownika (np. kliknięcia linków)
function logInteraction(event) {
  console.log(`User interaction: ${event.type} on ${event.target}`);
  // Możesz wysłać dane do backendu np. przez fetch()
}

// Dynamiczne dodanie nasłuchiwania na interakcje
function addInteractionListeners() {
  document.body.addEventListener('click', logInteraction);
  document.body.addEventListener('copy', logInteraction);
}

// Inicjalizacja skryptu
function init() {
  document.body.classList.add('page-visible');

  const loader = document.getElementById('loader');
  if (loader) loader.remove();

  updateLastUpdateTime();
  setInterval(updateLastUpdateTime, 60 * 60 * 1000); // co godzinę

  fadeInElements();
  addInteractionListeners();
}

// Dodanie event listenera po załadowaniu DOM
window.addEventListener('DOMContentLoaded', init);

// Eksport funkcji globalnie
window.copyOnion = copyOnion;
