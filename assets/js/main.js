(() => {
  "use strict";

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const cfg = window.SITE_CONFIG || {};
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const isDesktop = () => window.matchMedia("(min-width: 1025px)").matches;

  /* ------------------------------------------------------------------
     Contacts from config
     ------------------------------------------------------------------ */
  function applyContacts() {
    $$("[data-contact]").forEach((el) => {
      switch (el.dataset.contact) {
        case "phone":
          if (cfg.phone) { el.href = `tel:${cfg.phone}`; el.textContent = cfg.phoneDisplay || cfg.phone; }
          break;
        case "phone-action":
          if (cfg.phone) el.href = `tel:${cfg.phone}`;
          break;
        case "max":
          if (cfg.max) { el.href = cfg.max; el.target = "_blank"; el.rel = "noopener"; }
          break;
        case "hours":
          if (cfg.hours) el.textContent = cfg.hours;
          break;
        case "area":
          if (cfg.area) el.textContent = cfg.area;
          break;
        case "avito":
          if (cfg.avito) el.href = cfg.avito;
          break;
      }
    });

    const rating = $("[data-rating]");
    if (rating && cfg.avitoRating) {
      $("[data-rating-value]", rating).textContent = cfg.avitoRating;
      rating.hidden = false;
    }
  }

  /* ------------------------------------------------------------------
     Page-load sequence
     ------------------------------------------------------------------ */
  function initLoad() {
    const go = () => requestAnimationFrame(() => document.documentElement.classList.add("is-loaded"));
    if (document.fonts && document.fonts.ready) {
      Promise.race([document.fonts.ready, new Promise((r) => setTimeout(r, 600))]).then(go);
    } else go();
  }

  /* ------------------------------------------------------------------
     Scroll: active nav + mobile dock
     ------------------------------------------------------------------ */
  function initScroll() {
    const links = $$(".nav__link");
    const map = new Map(links.map((l) => [l.getAttribute("href").slice(1), l]));
    const sections = [...map.keys()].map((id) => document.getElementById(id)).filter(Boolean);
    const dock = $("#dock");
    const hero = $(".hero");
    const call = $("#call");
    const contacts = $("#contacts");
    let ticking = false;

    const update = () => {
      const vh = window.innerHeight;
      const mid = vh * 0.4;
      const current = sections.find((s) => {
        const r = s.getBoundingClientRect();
        return r.top <= mid && r.bottom > mid;
      });
      links.forEach((l) => l.classList.toggle("is-active", !!current && map.get(current.id) === l));

      if (dock) {
        const pastHero = hero ? hero.getBoundingClientRect().bottom < vh * 0.4 : true;
        const overCta = [call, contacts].some((s) => {
          if (!s) return false;
          const r = s.getBoundingClientRect();
          return r.top < vh * 0.75 && r.bottom > vh * 0.25;
        });
        const menuOpen = document.body.classList.contains("menu-open");
        dock.classList.toggle("is-visible", pastHero && !overCta && !menuOpen);
      }
      ticking = false;
    };

    window.addEventListener("scroll", () => {
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  /* ------------------------------------------------------------------
     Mobile menu
     ------------------------------------------------------------------ */
  function initMenu() {
    const burger = $(".burger");
    const menu = $("#menu");
    if (!burger || !menu) return;

    const setOpen = (open) => {
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? "Закрыть меню" : "Открыть меню");
      menu.classList.toggle("is-open", open);
      document.body.classList.toggle("menu-open", open);
      document.body.style.overflow = open ? "hidden" : "";
      $("#dock")?.classList.remove("is-visible");
    };

    burger.addEventListener("click", () => setOpen(burger.getAttribute("aria-expanded") !== "true"));
    $$("a", menu).forEach((a) => a.addEventListener("click", () => setOpen(false)));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && menu.classList.contains("is-open")) { setOpen(false); burger.focus(); }
    });
    window.addEventListener("resize", () => {
      if (window.matchMedia("(min-width: 1241px)").matches && menu.classList.contains("is-open")) setOpen(false);
    });
  }

  /* ------------------------------------------------------------------
     Services: swap sticky photo
     ------------------------------------------------------------------ */
  function initServices() {
    const services = $$(".service");
    const pics = $$(".services__visual picture");
    if (!services.length || !pics.length) return;

    const activate = (i) => {
      services.forEach((s, j) => s.classList.toggle("is-active", i === j));
      pics.forEach((p) => p.classList.toggle("is-active", Number(p.dataset.service) === i));
    };

    services.forEach((s) => {
      const i = Number(s.dataset.serviceIndex);
      s.addEventListener("mouseenter", () => isDesktop() && activate(i));
      s.addEventListener("focus", () => activate(i));
    });

    if ("IntersectionObserver" in window) {
      const io = new IntersectionObserver((entries) => {
        if (!isDesktop()) return;
        entries.forEach((en) => { if (en.isIntersecting) activate(Number(en.target.dataset.serviceIndex)); });
      }, { rootMargin: "-40% 0px -55% 0px" });
      services.forEach((s) => io.observe(s));
    }
  }

  /* ------------------------------------------------------------------
     Reviews carousel
     ------------------------------------------------------------------ */
  function initReviews() {
    const track = $("[data-reviews]");
    const tpl = $("#review-template");
    if (!track || !tpl) return;

    const placeholders = [
      { ph: true, name: "Имя клиента", date: "Дата отзыва", service: "Услуга", text: "Здесь будет реальный отзыв из профиля на Авито — перенесём его без изменений." },
      { ph: true, name: "Имя клиента", date: "Дата отзыва", service: "Услуга", text: "Здесь будет реальный отзыв из профиля на Авито — перенесём его без изменений." },
      { ph: true, name: "Имя клиента", date: "Дата отзыва", service: "Услуга", text: "Здесь будет реальный отзыв из профиля на Авито — перенесём его без изменений." },
    ];
    const items = Array.isArray(cfg.reviews) && cfg.reviews.length ? cfg.reviews : placeholders;

    items.forEach((r) => {
      let card;
      if (r.image) {
        card = document.createElement("article");
        card.className = "review review--image";
        const img = document.createElement("img");
        img.src = r.image;
        img.alt = r.name ? `Отзыв с Авито: ${r.name}` : "Отзыв с Авито";
        img.loading = "lazy";
        card.appendChild(img);
      } else {
        card = tpl.content.firstElementChild.cloneNode(true);
        if (r.ph) card.classList.add("review--ph");
        const rating = Math.max(1, Math.min(5, Number(r.rating) || 5));
        const stars = $(".review__stars", card);
        stars.setAttribute("aria-label", `Оценка ${rating} из 5`);
        $$("svg", stars).forEach((s, i) => { if (i >= rating) s.style.opacity = "0.2"; });
        $(".review__avatar", card).textContent = r.ph ? "" : (r.name || "?").trim().charAt(0).toUpperCase();
        $(".review__name", card).textContent = r.name || "Клиент";
        $(".review__meta", card).textContent = [r.date, r.service].filter(Boolean).join(", ");
        $(".review__text", card).textContent = r.text || "";
      }
      track.appendChild(card);
    });

    const cards = $$(".review", track);
    const dots = $("[data-dots]");
    const prev = $("[data-prev]");
    const next = $("[data-next]");

    const perView = () => {
      const first = cards[0];
      if (!first) return 1;
      return Math.max(1, Math.round(track.clientWidth / first.getBoundingClientRect().width));
    };
    const pages = () => Math.max(1, cards.length - perView() + 1);
    const step = () => (cards[1] ? cards[1].offsetLeft - cards[0].offsetLeft : track.clientWidth);
    const current = () => Math.round(track.scrollLeft / step());

    const renderDots = () => {
      dots.innerHTML = "";
      const n = pages();
      if (n <= 1) { prev.hidden = next.hidden = true; return; }
      prev.hidden = next.hidden = false;
      for (let i = 0; i < n; i++) {
        const b = document.createElement("button");
        b.type = "button";
        b.setAttribute("aria-label", `Отзыв ${i + 1}`);
        b.addEventListener("click", () => track.scrollTo({ left: i * step() }));
        dots.appendChild(b);
      }
      sync();
    };
    const sync = () => {
      const i = Math.min(current(), pages() - 1);
      $$("button", dots).forEach((b, j) => b.setAttribute("aria-current", String(i === j)));
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 2;
    };

    prev.addEventListener("click", () => track.scrollBy({ left: -step() }));
    next.addEventListener("click", () => track.scrollBy({ left: step() }));
    track.addEventListener("scroll", () => requestAnimationFrame(sync), { passive: true });
    track.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") { e.preventDefault(); track.scrollBy({ left: step() }); }
      if (e.key === "ArrowLeft") { e.preventDefault(); track.scrollBy({ left: -step() }); }
    });
    window.addEventListener("resize", renderDots);
    renderDots();
  }

  /* ------------------------------------------------------------------
     Lightbox
     ------------------------------------------------------------------ */
  function initLightbox() {
    const dlg = $("#lightbox");
    const triggers = $$(".work__btn");
    if (!dlg || !triggers.length || typeof dlg.showModal !== "function") return;

    const img = $("[data-lb-img]", dlg);
    const cap = $("[data-lb-caption]", dlg);
    const count = $("[data-lb-count]", dlg);
    let index = 0;
    let lastFocus = null;

    const show = (i) => {
      index = (i + triggers.length) % triggers.length;
      const t = triggers[index];
      img.src = t.dataset.full;
      img.alt = $("img", t)?.alt || "";
      cap.textContent = t.dataset.caption || "";
      count.textContent = `${index + 1} / ${triggers.length}`;
    };

    triggers.forEach((t, i) => t.addEventListener("click", () => {
      lastFocus = t;
      show(i);
      dlg.showModal();
      document.body.style.overflow = "hidden";
    }));

    dlg.addEventListener("close", () => {
      document.body.style.overflow = "";
      lastFocus?.focus({ preventScroll: true });
    });
    $("[data-lb-close]", dlg).addEventListener("click", () => dlg.close());
    $("[data-lb-prev]", dlg).addEventListener("click", () => show(index - 1));
    $("[data-lb-next]", dlg).addEventListener("click", () => show(index + 1));
    dlg.addEventListener("click", (e) => { if (e.target === dlg || e.target.classList.contains("lightbox__stage")) dlg.close(); });
    dlg.addEventListener("keydown", (e) => {
      if (e.key === "ArrowLeft") show(index - 1);
      if (e.key === "ArrowRight") show(index + 1);
    });

    let startX = null;
    dlg.addEventListener("touchstart", (e) => { startX = e.touches[0].clientX; }, { passive: true });
    dlg.addEventListener("touchend", (e) => {
      if (startX === null) return;
      const dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 50) show(index + (dx < 0 ? 1 : -1));
      startX = null;
    });
  }

  /* ------------------------------------------------------------------
     Calculator form
     ------------------------------------------------------------------ */
  function initForm() {
    const form = $("#calc-form");
    const section = $("#calc");
    if (!form || !section) return;

    const fieldOf = (el) => el.closest(".field");
    const validators = {
      area: (el) => Number(el.value) >= 10,
      phone: (el) => el.value.replace(/\D/g, "").length >= 10,
      consent: (el) => el.checked,
    };

    const validate = () => {
      let firstInvalid = null;
      Object.entries(validators).forEach(([name, fn]) => {
        const el = form.elements[name];
        const ok = fn(el);
        fieldOf(el)?.classList.toggle("has-error", !ok);
        if (!ok && !firstInvalid) firstInvalid = el;
      });
      const houseOk = $$('input[name="house"]', form).some((r) => r.checked);
      $("#f-type").classList.toggle("has-error", !houseOk);
      if (!houseOk && !firstInvalid) firstInvalid = $('input[name="house"]', form);
      return firstInvalid;
    };

    form.addEventListener("input", (e) => {
      const f = fieldOf(e.target);
      const fn = validators[e.target.name];
      if (f?.classList.contains("has-error") && (!fn || fn(e.target))) f.classList.remove("has-error");
      if (e.target.name === "house") $("#f-type").classList.remove("has-error");
    });

    const collect = () => {
      const fd = new FormData(form);
      return {
        area: fd.get("area"),
        house: fd.get("house"),
        needs: fd.getAll("need"),
        city: String(fd.get("city") || "").trim(),
        name: String(fd.get("name") || "").trim(),
        phone: String(fd.get("phone") || "").trim(),
        page: location.href,
        sentAt: new Date().toISOString(),
      };
    };

    const toText = (d) => [
      "Заявка на расчёт — векторклимата.рф",
      `Площадь: ${d.area} м²`,
      `Тип дома: ${d.house}`,
      d.needs.length ? `Что нужно: ${d.needs.join(", ")}` : "",
      d.city ? `Город: ${d.city}` : "",
      d.name ? `Имя: ${d.name}` : "",
      `Телефон: ${d.phone}`,
    ].filter(Boolean).join("\n");

    const showSuccess = (data, sentToServer) => {
      section.classList.add("is-sent");
      const actions = $("[data-success-actions]", section);
      actions.innerHTML = "";
      if (!sentToServer) {
        if (cfg.max) {
          const msg = $("[data-success-text]", section);
          msg.textContent = "Продублируйте заявку в MAX, так мы ответим быстрее.";
          const a = document.createElement("a");
          a.className = "btn btn--max";
          a.href = cfg.max;
          a.target = "_blank";
          a.rel = "noopener";
          a.textContent = "Открыть MAX";
          actions.appendChild(a);
          navigator.clipboard?.writeText(toText(data))
            .then(() => { msg.textContent += " Текст заявки скопирован, просто вставьте его в чат."; })
            .catch(() => {});
        }
        console.info("[Вектор климата] formEndpoint не настроен — заявка не отправлена на сервер.\n" + toText(data));
      }
      $(".form__success", section).focus({ preventScroll: true });
      section.scrollIntoView({ behavior: reducedMotion ? "auto" : "smooth", block: "start" });
    };

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const invalid = validate();
      if (invalid) { invalid.focus(); return; }
      const data = collect();
      if (!cfg.formEndpoint) { showSuccess(data, false); return; }

      const btn = $('button[type="submit"]', form);
      const label = btn.textContent;
      btn.disabled = true;
      btn.textContent = "Отправляем…";
      try {
        const res = await fetch(cfg.formEndpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        showSuccess(data, true);
      } catch (err) {
        console.error(err);
        btn.textContent = label;
        btn.disabled = false;
        showSuccess(data, false);
      }
    });
  }

  function initYear() {
    $$("[data-year]").forEach((el) => { el.textContent = new Date().getFullYear(); });
  }

  applyContacts();
  initLoad();
  initScroll();
  initMenu();
  initServices();
  initReviews();
  initLightbox();
  initForm();
  initYear();
})();
