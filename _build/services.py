#!/usr/bin/env python3
"""Собирает страницы услуг /uslugi/<slug>/index.html из шапки главной и данных ниже.
Запуск из корня проекта: python3 _build/services.py"""
import html, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://xn--80aaemplaikqwwh.xn--p1ai"
MAX = "https://max.ru/u/f9LHodD0cOJ-I2c5GvvgMV4BQCZMem87lvZ4GcqRK_pRCQoFt9h_9IcK-Cg"
V = "18"

idx = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
v_main = re.search(r"main\.js\?v=(\d+)", idx).group(1)

# шапка: от <body> до <main>, якоря ведут на главную
top = idx[idx.index("<body>") + len("<body>"): idx.index('<main id="main">')]
top = re.sub(r'href="#(?!i-)', 'href="/#', top)
top = top.replace('href="/#top"', 'href="/"').replace('href="/#main"', 'href="#main"')
dock = idx[idx.index('<div class="dock"'): idx.index("</div>", idx.index('<div class="dock"')) + 6]

def pic(name, w, h, alt):
    return (f'<picture><source type="image/webp" srcset="/assets/img/{name}.webp">'
            f'<img src="/assets/img/{name}.jpg" width="{w}" height="{h}" alt="{html.escape(alt)}"></picture>')

SERVICES = [
  dict(slug="ventvyhody-na-krovlyu", nav="Вентвыходы на кровлю",
    title="Монтаж вентиляционных выходов на кровлю",
    h1="Вентиляционные выходы на кровлю",
    desc="Монтаж вентиляционных выходов и вывод канализационного стояка через кровлю в Свердловской области. Проходные элементы под гибкую черепицу, металлочерепицу, профнастил и плоскую кровлю.",
    lead="Выводим вытяжку и канализационный стояк через кровлю. Проходной элемент подбираем под профиль и цвет покрытия, узел герметизируем, чтобы не было протечек и конденсата под кровлей.",
    image=pic("metal-tile-vent-960", 960, 1280, "Вентиляционный выход с проходным элементом на металлочерепице"),
    when=["На чердаке или под кровлей собирается конденсат, мокнет утеплитель",
          "В доме тянет запахом канализации: стояк не выведен наружу или выведен неправильно",
          "Вытяжка в кухне или санузле работает слабо",
          "Строите дом или перекрываете крышу и нужно вывести новые каналы",
          "Течёт вокруг старого выхода"],
    work=["Смотрим кровлю и каналы, подбираем проходной элемент под ваше покрытие",
          "Ставим проходку и вентвыход, герметизируем примыкание",
          "Выводим фановую трубу канализации, вытяжки кухни и санузлов",
          "Где нужно, ставим утеплённые выходы, чтобы внутри трубы не копился конденсат",
          "Если естественной тяги мало, ставим выход с вентилятором"],
    spec="Гибкая черепица, металлочерепица, профнастил, фальц, плоская кровля",
    faq=[("Зачем утеплённый вентвыход?", "Тёплый влажный воздух из дома остывает в холодной трубе, и на стенках выпадает конденсат. Он стекает обратно или замерзает. Утеплённый выход держит трубу тёплой, и конденсата намного меньше."),
         ("Не будет ли протекать?", "Проходной элемент повторяет профиль кровли, а примыкание мы герметизируем. Именно поэтому элемент подбираем под конкретное покрытие, а не ставим универсальный."),
         ("Можно ли делать зимой?", "Да, среди наших объектов есть смонтированные зимой. Условия обсуждаем после осмотра кровли."),
         ("Сколько стоит?", "Зависит от кровли, высоты и количества выходов. Ориентировочную стоимость назовём по фото, точную после осмотра.")]),
  dict(slug="turbodeflektory", nav="Турбодефлекторы",
    title="Установка турбодефлекторов и дефлекторов",
    h1="Турбодефлекторы и дефлекторы",
    desc="Установка турбодефлекторов и дефлекторов на вентшахты и трубы в Свердловской области. Подбор диаметра и высоты, монтаж на кирпичные шахты.",
    lead="Турбодефлектор усиливает тягу за счёт ветра и закрывает канал от дождя и снега. Ставим на вентшахты и трубы, подбираем диаметр и высоту под ваш канал.",
    image=pic("turbo-deflectors-768", 768, 1024, "Турбодефлекторы на кирпичных вентшахтах плоской кровли"),
    when=["Слабая тяга в вентканалах, в доме душно и влажно",
          "Иногда тянет обратно: запахи с улицы или из шахты",
          "В канал попадает дождь и снег",
          "Старый колпак или дефлектор проржавел"],
    work=["Смотрим шахту или трубу, меряем сечение",
          "Подбираем турбодефлектор или неподвижный дефлектор под задачу",
          "Для кирпичных шахт делаем переходник с шахты на круглый патрубок",
          "Монтируем и проверяем, что ротор вращается свободно"],
    spec="Вентшахты, трубы, нержавеющая и оцинкованная сталь",
    faq=[("Чем турбодефлектор отличается от обычного дефлектора?", "Турбодефлектор вращается от ветра и создаёт разрежение в канале, поэтому тяга сильнее. Обычный дефлектор неподвижен: он защищает канал от осадков и помогает тяге за счёт формы."),
         ("Можно ли поставить турбодефлектор на дымоход?", "Зависит от того, что за отопитель подключён к трубе. Для дымоходов подбираем решение после осмотра, а не ставим турбодефлектор по умолчанию."),
         ("Сколько стоит?", "Зависит от диаметра, материала и количества шахт. Ориентир назовём по фото, точную стоимость после осмотра.")]),
  dict(slug="kozhuhi-dlya-dymohodov", nav="Кожухи для дымоходов",
    title="Кожухи и колпаки для дымоходов и вентшахт",
    h1="Кожухи и колпаки для дымоходов и вентшахт",
    desc="Изготовление и монтаж кожухов и колпаков на дымоходы и вентшахты по размеру трубы, в цвет кровли. Свердловская область.",
    lead="Закрываем трубу от дождя и снега, продлеваем жизнь кладке и придаём кровле законченный вид. Изготавливаем по размеру трубы, в цвет кровли.",
    image=pic("chimney-casing-960", 960, 1280, "Кожух дымохода с зонтом на кровле зимой"),
    when=["Кирпич трубы крошится и намокает",
          "Течёт по трубе или в месте примыкания к кровле",
          "Старая труба портит вид новой кровли",
          "Нужен зонт или оголовок от осадков"],
    work=["Замеряем трубу и примыкание",
          "Изготавливаем кожух по размеру, в цвет кровли",
          "Ставим зонт или жалюзийный оголовок",
          "Монтируем кожух и делаем примыкание к кровле"],
    spec="По размеру трубы, в цвет кровли, зонты и оголовки",
    faq=[("Зачем кожух, если труба целая?", "Кирпичная кладка на крыше постоянно мокнет и промерзает, и со временем разрушается. Кожух защищает её от воды, а заодно выглядит аккуратно."),
         ("Можно ли в цвет кровли?", "Да, кожух делаем в цвет покрытия, чтобы труба смотрелась частью крыши."),
         ("Сколько стоит?", "Зависит от размеров трубы, высоты и оголовка. Ориентир назовём по фото, точную стоимость после замера.")]),
  dict(slug="kiv-125", nav="Приточные клапаны КИВ-125",
    title="Установка приточного клапана КИВ-125",
    h1="Приточные клапаны КИВ-125",
    desc="Установка приточных клапанов КИВ-125 в стену частного дома в Свердловской области. Свежий воздух без открытых окон, меньше конденсата на стёклах.",
    lead="Свежий воздух в комнату при закрытых окнах. Делаем в наружной стене отверстие Ø 125 мм, ставим утеплённый канал с фильтром, снаружи решётку, внутри регулируемый оголовок.",
    image='<img src="/assets/img/kiv-125.svg" width="960" height="1280" alt="Схема приточного клапана КИВ-125 в разрезе стены">',
    image_class="svc-hero__media--scheme",
    when=["Потеют окна, особенно зимой",
          "В спальне душно утром, хотя окна закрыты",
          "В углах появляется плесень, пахнет сыростью",
          "Поставили пластиковые окна, и в доме стало тяжело дышать"],
    work=["Смотрим комнату и вытяжные каналы: приток работает, только когда воздуху есть куда уходить",
          "Выбираем место в наружной стене, обычно рядом с окном или за радиатором",
          "Делаем отверстие Ø 125 мм",
          "Ставим утеплённый канал с фильтром, наружную решётку и внутренний регулируемый оголовок",
          "Убираем за собой и показываем, как регулировать поток"],
    spec="Кирпич, газобетон, брус и каркас, спальни, детские, гостиные",
    faq=[("Не будет ли холодно зимой?", "Поток регулируется оголовком, его можно уменьшить или перекрыть в сильный мороз. Место ставим так, чтобы холодный воздух успевал смешаться с тёплым, например рядом с радиатором."),
         ("Зачем клапан, если можно открыть окно?", "Открытое окно даёт сквозняк и выстуживает комнату, а клапан даёт небольшой постоянный приток без открытой створки. Фильтр задерживает пыль с улицы."),
         ("Будет ли работать без вытяжки?", "Нет. Свежий воздух заходит, когда отработанный уходит через вытяжные каналы. Поэтому сначала проверяем тягу в доме."),
         ("Сколько стоит?", "Зависит от материала и толщины стены и количества клапанов. Ориентир назовём по фото, точную стоимость после осмотра.")]),
  dict(slug="ventilyaciya-pod-klyuch", nav="Вентиляция под ключ",
    title="Вентиляция частного дома под ключ",
    h1="Вентиляция дома под ключ",
    desc="Вентиляция частного дома под ключ в Свердловской области: осмотр, расчёт воздухообмена, схема, подбор оборудования, монтаж и настройка.",
    lead="Смотрим дом, считаем воздухообмен, показываем схему простыми словами, подбираем оборудование и монтируем. После настраиваем и объясняем, как пользоваться.",
    image=pic("shingle-winter-720", 720, 1280, "Вентиляционный выход и аэратор на гибкой черепице зимой"),
    when=["Строите новый дом и хотите заложить вентиляцию сразу",
          "В доме сыро, душно, потеют окна, а точечные меры не помогли",
          "Делаете реконструкцию или утепление, и старая схема перестала работать"],
    work=["Осмотр дома и существующих каналов",
          "Расчёт воздухообмена по комнатам",
          "Схема: где приток, где вытяжка, где выходы на кровлю",
          "Подбор оборудования под бюджет",
          "Монтаж, настройка и объяснение, как пользоваться"],
    spec="Расчёт, схема, подбор оборудования, монтаж, настройка",
    faq=[("С чего начать?", "Позвоните или пришлите в MAX фото дома и коротко опишите проблему. Скажем, что посмотреть на месте и с чего начать."),
         ("Можно делать по частям?", "Да. Часто начинаем с самого нужного, например с вентвыходов или клапанов в спальнях, а остальное делаем по схеме позже."),
         ("Сколько стоит?", "Зависит от площади, количества комнат и оборудования. После осмотра и расчёта назовём стоимость по этапам.")]),
]

def page(s):
    url = f"{DOMAIN}/uslugi/{s['slug']}/"
    faq_html = "\n".join(
        f'''          <details class="qa">
            <summary>{html.escape(q)}<span class="qa__toggle" aria-hidden="true"></span></summary>
            <div class="qa__body"><p>{html.escape(a)}</p></div>
          </details>''' for q, a in s["faq"])
    when = "\n".join(f"            <li>{html.escape(x)}</li>" for x in s["when"])
    work = "\n".join(f"            <li>{html.escape(x)}</li>" for x in s["work"])
    others = "\n".join(
        f'          <li><a href="/uslugi/{o["slug"]}/">{html.escape(o["nav"])}</a></li>'
        for o in SERVICES if o is not s)
    ld = [
      {"@context": "https://schema.org", "@type": "Service", "name": s["h1"], "description": s["desc"],
       "areaServed": "Свердловская область", "url": url,
       "provider": {"@type": "HomeAndConstructionBusiness", "name": "Вектор климата", "url": DOMAIN + "/", "telephone": "+7 963 855-50-08"}},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Главная", "item": DOMAIN + "/"},
        {"@type": "ListItem", "position": 2, "name": "Услуги", "item": DOMAIN + "/#services"},
        {"@type": "ListItem", "position": 3, "name": s["h1"], "item": url}]},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faq"]]},
    ]
    title = f'{s["title"]} в Свердловской области — Вектор климата'
    return f'''<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(s["desc"])}">
  <meta name="theme-color" content="#33393d">
  <link rel="canonical" href="{url}">
  <link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="ru_RU">
  <meta property="og:site_name" content="Вектор климата">
  <meta property="og:title" content="{html.escape(s["h1"])} — Вектор климата">
  <meta property="og:description" content="{html.escape(s["desc"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{DOMAIN}/assets/img/og.jpg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Golos+Text:wght@400;500;600&family=Tenor+Sans&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/style.css?v={V}">
  <script>document.documentElement.classList.add('js')</script>
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
  <script src="/assets/js/metrika.js?v={V}" async></script>
</head>
<body class="page-service">
{top.replace('src="assets/', 'src="/assets/').replace('href="assets/', 'href="/assets/')}  <main id="main">
    <section class="svc-hero">
      <div class="container svc-hero__grid">
        <div class="svc-hero__text">
          <nav class="crumbs" aria-label="Навигация"><a href="/">Главная</a><span aria-hidden="true">/</span><a href="/#services">Услуги</a><span aria-hidden="true">/</span><span aria-current="page">{html.escape(s["nav"])}</span></nav>
          <h1 class="svc-hero__title">{html.escape(s["h1"])}</h1>
          <p class="svc-hero__lead">{html.escape(s["lead"])}</p>
          <p class="service__spec">{html.escape(s["spec"])}</p>
          <div class="call__actions">
            <a class="btn btn--dark" href="tel:+79638555008" data-contact="phone-action"><svg class="btn__icon" aria-hidden="true"><use href="#i-phone"/></svg>+7 (963) 855-50-08</a>
            <a class="btn btn--max" href="{MAX}" target="_blank" rel="noopener" data-contact="max"><svg class="btn__icon" aria-hidden="true"><use href="#i-chat"/></svg>Написать в MAX</a>
          </div>
        </div>
        <figure class="svc-hero__media {s.get("image_class", "")}">{s["image"]}</figure>
      </div>
    </section>

    <section class="section svc-body">
      <div class="container svc-cols">
        <div>
          <h2 class="h2">Когда это нужно</h2>
          <ul class="svc-list">
{when}
          </ul>
        </div>
        <div>
          <h2 class="h2">Что делаем</h2>
          <ol class="svc-list svc-list--steps">
{work}
          </ol>
        </div>
      </div>
    </section>

    <section class="section faq" aria-labelledby="faq-title">
      <div class="container faq__grid">
        <h2 class="h2" id="faq-title">Частые вопросы</h2>
        <div class="faq__list">
{faq_html}
        </div>
      </div>
    </section>

    <section class="section call" id="call" aria-labelledby="call-title">
      <div class="container call__grid">
        <div class="call__intro">
          <h2 class="h2" id="call-title">Позвоните, расскажем, что подойдёт вашему дому</h2>
          <p class="head__lead">Ильяс ответит, уточнит детали и назовёт ориентировочную стоимость. Можно сразу прислать фото в MAX.</p>
          <h3 class="svc-more__title">Другие услуги</h3>
          <ul class="svc-more">
{others}
          </ul>
        </div>
        <div class="call__phone">
          <span class="call__label">Телефон, <span data-contact="hours">Пн–Пт</span></span>
          <a class="call__number" href="tel:+79638555008" data-contact="phone">+7 (963) 855-50-08</a>
          <div class="call__actions">
            <a class="btn btn--dark" href="tel:+79638555008" data-contact="phone-action"><svg class="btn__icon" aria-hidden="true"><use href="#i-phone"/></svg>Позвонить</a>
            <a class="btn btn--max" href="{MAX}" target="_blank" rel="noopener" data-contact="max"><svg class="btn__icon" aria-hidden="true"><use href="#i-chat"/></svg>Написать в MAX</a>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer" style="background: var(--graphite)">
    <div class="container footer__inner">
      <a class="logo" href="/"><svg class="logo__mark" aria-hidden="true"><use href="#i-logo"/></svg><span class="logo__word">Вектор климата</span></a>
      <nav class="footer__nav" aria-label="Навигация в подвале">
        <a href="/#services">Услуги</a>
        <a href="/#works">Работы</a>
        <a href="/#reviews">Отзывы</a>
        <a href="/privacy.html">Политика конфиденциальности</a>
      </nav>
      <span>© 2026 Вектор климата, векторклимата.рф</span>
    </div>
  </footer>

  {dock}

  <script src="/assets/js/config.js?v={V}"></script>
  <script src="/assets/js/main.js?v={V}" defer></script>
</body>
</html>
'''

for s in SERVICES:
    d = os.path.join(ROOT, "uslugi", s["slug"])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(s))
    print("ok", s["slug"])

# sitemap
urls = [("/", "1.0")] + [(f"/uslugi/{s['slug']}/", "0.8") for s in SERVICES] + [("/privacy.html", "0.2")]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += "".join(f"  <url><loc>{DOMAIN}{u}</loc><priority>{p}</priority></url>\n" for u, p in urls)
sm += "</urlset>\n"
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(sm)
print("sitemap ok")
