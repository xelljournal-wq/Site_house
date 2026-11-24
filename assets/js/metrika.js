/* Яндекс Метрика: счётчик 114652723, цели «Звонок» (автоматически по tel:) и «Написать в MAX» (max_click) */
(function (m, e, t, r, i, k, a) {
  m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments); };
  m[i].l = 1 * new Date();
  for (var j = 0; j < document.scripts.length; j++) { if (document.scripts[j].src === r) { return; } }
  k = e.createElement(t); a = e.getElementsByTagName(t)[0]; k.async = 1; k.src = r; a.parentNode.insertBefore(k, a);
})(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

ym(114652723, "init", { clickmap: true, trackLinks: true, accurateTrackBounce: true, webvisor: true });

document.addEventListener("click", function (ev) {
  var a = ev.target.closest && ev.target.closest('a[href*="max.ru"]');
  if (a) ym(114652723, "reachGoal", "max_click");
});

/* Уведомление о cookie: показывается один раз */
(function () {
  var KEY = "vk-cookie-ok";
  try { if (localStorage.getItem(KEY)) return; } catch (e) {}
  function show() {
    var bar = document.createElement("div");
    bar.className = "cookie";
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", "Уведомление о cookie");
    bar.innerHTML = '<p>Сайт использует cookie и Яндекс Метрику, чтобы понимать, как им пользуются. <a href="privacy.html">Подробнее</a></p><button type="button" class="btn btn--light">Понятно</button>';
    bar.querySelector("button").addEventListener("click", function () {
      try { localStorage.setItem(KEY, "1"); } catch (e) {}
      bar.remove();
    });
    document.body.appendChild(bar);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", show); else show();
})();
