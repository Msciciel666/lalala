/*  ──────────────────────────────────────────
    darkweb666  ·  minimal vanilla-JS bundle
    ────────────────────────────────────────── */

    function updateLastUpdateTime() {
      const el = document.getElementById('last-update');
      if (!el) return;
      el.textContent = new Date().toLocaleString();
    }
    
    /* A) Fade-in oraz inicjalizacja */
document.addEventListener('DOMContentLoaded', () => {
  document.body.classList.add('page-visible');
  document.getElementById('loader')?.remove();
  updateLastUpdateTime();
  setInterval(updateLastUpdateTime, 12 * 60 * 60 * 1000);
});

/* B) Kopiowanie adresu .onion do schowka */
function copyOnion() {
  navigator.clipboard
           .writeText(document.getElementById('onion').innerText)
           .then(() => alert('Skopiowano .onion ✅'),
                 () => alert('Kopiowanie nieudane ❌'));
}

/* C) Eksport funkcji dla HTML */
window.copyOnion = copyOnion;