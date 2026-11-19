/* STEGARC Homepage – kleine, zurückhaltende Interaktionen (kein Framework).
   Navigation: Hintergrund beim Scrollen, aktiver Menüpunkt, mobiles Menü. Abschnitte blenden beim Eintreten sanft ein. */
(function () {
  var top = document.querySelector(".top"), nav = document.getElementById("menu"), btn = document.querySelector(".menu-btn");
  function onScroll() { if (top) top.classList.toggle("scrolled", window.scrollY > 8); }
  onScroll(); window.addEventListener("scroll", onScroll, { passive: true });

  // Mobiles Menü
  function setMenu(open) { if (!btn || !nav) return; btn.setAttribute("aria-expanded", open ? "true" : "false"); nav.classList.toggle("open", open);
    btn.querySelector(".sr").textContent = open ? btn.dataset.close : btn.dataset.open; if (open) { var f = nav.querySelector("a"); if (f) f.focus(); } }
  if (btn) btn.addEventListener("click", function () { setMenu(btn.getAttribute("aria-expanded") !== "true"); });
  if (nav) nav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && btn && btn.getAttribute("aria-expanded") === "true") { setMenu(false); btn.focus(); } });

  // Aktiver Menüpunkt (nur Anker auf derselben Seite)
  var links = Array.prototype.slice.call(document.querySelectorAll(".nav a.link")).filter(function (a) { var h = a.getAttribute("href") || ""; return h.indexOf("#") >= 0 && document.getElementById(h.split("#")[1]); });
  if ("IntersectionObserver" in window && links.length) {
    var byId = {}; links.forEach(function (a) { byId[a.getAttribute("href").split("#")[1]] = a; });
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { links.forEach(function (a) { a.removeAttribute("aria-current"); }); byId[e.target.id].setAttribute("aria-current", "true"); } }); }, { rootMargin: "-45% 0px -50% 0px" });
    Object.keys(byId).forEach(function (id) { io.observe(document.getElementById(id)); });
  }

  // Sanftes Einblenden
  var rv = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var ro = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); ro.unobserve(e.target); } }); }, { rootMargin: "0px 0px -8% 0px", threshold: .08 });
    rv.forEach(function (el) { ro.observe(el); });
  } else rv.forEach(function (el) { el.classList.add("in"); });
})();
