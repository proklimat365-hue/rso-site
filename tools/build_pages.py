"""Генерирует SEO-страницы «услуга + город» и sitemap.xml.

Запуск из корня репозитория: python3 tools/build_pages.py
Тексты страниц лежат в PAGES ниже; шапка, кнопки и подвал общие.
"""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://xn--b1afk4ade.xn--365-5cd3blhj9c.xn--90ais/"

SHOP = "https://xn--b1abglpdo.xn--365-5cd3blhj9c.xn--90ais/kategorii/kondicionery"
SHOP_LINKS = [
    (f"{SHOP}/kinghome/split-sistema-kinghome-prestige-inverter-kwh09acc-s6dba2a.html", "KingHome Prestige Inverter", "тихий инверторный кондиционер, наш выбор для квартиры"),
    (f"{SHOP}/kinghome/split-sistema-kinghome-kinghome-cosmo-nordic-inverter-r32-wi-fi-kwh09awcxb-k6dna1b.html", "KingHome COSMO NORDIC", "для обогрева зимой, управление по Wi-Fi"),
]

PHONE = "+375296878717"
PHONE_TXT = "+375 29 687-87-17"
VIBER = "viber://chat?number=%2B375447688127"
TG = "https://t.me/+375447688127"

BRANDS = ['Daikin', 'Mitsubishi Heavy', 'Toshiba', 'Panasonic', 'Hitachi', 'LG', 'Haier', 'Gree', 'Midea', 'Hisense', 'Electrolux', 'Ballu', 'Royal Clima', 'NeoClima', 'Energolux', 'Funai', 'MDV', 'Daichi', 'Dahatsu', 'Chigo', 'Green', 'Oasis']

SERVICE_INTRO = 'С 2018 года к нам обратились более 9 000 клиентов, поэтому мы создали отдельный отдел сервиса. Многие компании летом заняты только монтажом и продажей кондиционеров, и до ремонта у них просто не доходят руки. У нас есть отдельный отдел сервиса, поэтому ремонтом и обслуживанием мы занимаемся круглый год, в том числе в разгар сезона.'
SERVICE_ITEMS = ['<b>Руководитель сервиса</b> отвечает за качество и сроки.', '<b>Менеджер заботы</b> принимает заявки, напоминает о плановом обслуживании и остаётся на связи после работы.', '<b>Инженер по обслуживанию</b> занимается только ремонтом и сервисом, его не забирают на монтажи.']

CITIES = {
    "mogilev": {"name": "Могилёв", "in": "в Могилёве", "region": "Могилёвская область",
                "near": "Могилёв и район, а также Бобруйск, Осиповичи, Горки, Кричев по договорённости",
                "badge": "<b>Аварийный выезд</b> в день обращения",
                "speed": [
                    "Срочный ремонт и аварии: выезжаем в день обращения.",
                    "Плановое обслуживание: как правило, на следующий день.",
                    "Область: платный выезд на следующий день или дешевле, групповым выездом, когда собираем несколько заказов в одну поездку.",
                ],
                "overrides": {}},
    "minsk": {"name": "Минск", "in": "в Минске", "region": "Минская область",
              "near": "Минск и Минский район",
              "badge": "<b>Свой мастер</b> в Минске",
              "speed": [
                  "В Минске работает наш мастер, ехать из другого города не нужно.",
                  "Плановые выезды записываем в график: как правило, на 2–4 дня вперёд.",
                  "Срочный случай: позвоните, инженер выслушает и скажет, как быстро сможем приехать.",
              ],
              "overrides": {
                  "obsluzhivanie-kondicionerov": {
                      "desc": "Техническое обслуживание и чистка кондиционеров {in}: от 125 BYN. Свой мастер в Минске, запись на ближайшие дни, гарантия. Климат 365, тел. +375 29 687-87-17.",
                      "lead": "Плановое обслуживание продлевает жизнь кондиционера, возвращает ему мощность охлаждения и убирает неприятный запах. В Минске работает наш мастер, выезды записываем в график на ближайшие дни.",
                  },
                  "remont-kondicionerov": {
                      "desc": "Ремонт кондиционеров {in}: не холодит, течёт, шумит, не включается. Свой мастер в Минске, диагностика от 40 BYN, гарантия 1 год. Тел. +375 29 687-87-17.",
                      "lead": "Ремонтируем бытовые и полупромышленные кондиционеры любых марок. В Минске работает наш мастер. В срочном случае инженер после звонка решает, как быстро можно приехать. На ремонт даём гарантию 1 год.",
                  },
                  "holod-dlya-cvetochnyh-magazinov": {
                      "desc": "Кондиционеры, холодильные камеры и витрины для цветочных магазинов {in}: подбор, монтаж, ремонт и обслуживание. Свой мастер в Минске. Тел. +375 29 687-87-17.",
                      "lead": "Цветы теряют товарный вид за несколько часов без холода. Мы обслуживаем цветочные салоны: подбираем и ставим кондиционеры, ремонтируем холодильные камеры и витрины для цветов. Если камера остановилась, позвоните: инженер оценит ситуацию и скажет, как быстро приедет мастер.",
                  },
              }},
}

# Города, куда ездим групповыми выездами (5–7 клиентов за поездку).
GROUP_PAGES = ["obsluzhivanie-kondicionerov", "remont-kondicionerov", "zapravka-kondicionerov", "montazh-kondicionerov", "holod-dlya-cvetochnyh-magazinov"]


def group_city(name, in_, region, near, clients, intro):
    speed = [
        f"{name} обслуживаем групповыми выездами: собираем 5–7 заявок и приезжаем в один день.",
        "Если в поездку набирается 4 и больше клиентов, дорога для вас бесплатная.",
        "Нужно срочно или отдельно от группы: выезд стоит 0,30 BYN за километр в одну сторону, обратная дорога не оплачивается.",
        f"Оставьте заявку заранее, и менеджер заботы скажет дату ближайшего выезда {in_}.",
    ]
    return {"name": name, "in": in_, "region": region, "near": near,
            "badge": "<b>Дорога бесплатно</b> при групповом выезде",
            "speed": speed, "pages": GROUP_PAGES,
            "intro": (f"Климат 365 {in_}", f"{intro} Сейчас {in_} у нас {clients}. Наш офис находится в Могилёве, поэтому мы приезжаем по графику групповых выездов: так обслуживание обходится вам без доплаты за дорогу."),
            "overrides": {
                "obsluzhivanie-kondicionerov": {
                    "desc": "Обслуживание и чистка кондиционеров {in}: от 125 BYN. Групповые выезды, дорога бесплатно от 4 клиентов. Климат 365, тел. +375 29 687-87-17.",
                    "lead": f"Плановое обслуживание продлевает жизнь кондиционера, возвращает ему мощность охлаждения и убирает неприятный запах. {in_[0].upper() + in_[1:]} мы работаем групповыми выездами, поэтому дорога для вас обычно бесплатная.",
                },
                "remont-kondicionerov": {
                    "desc": "Ремонт кондиционеров {in}: не холодит, течёт, шумит, не включается. Диагностика от 40 BYN, гарантия 1 год. Тел. +375 29 687-87-17.",
                    "lead": "Ремонтируем бытовые и полупромышленные кондиционеры любых марок. Несрочный ремонт делаем во время группового выезда, срочный можно заказать отдельным выездом. На ремонт даём гарантию 1 год.",
                },
                "zapravka-kondicionerov": {
                    "desc": "Заправка кондиционеров фреоном {in}: поиск утечки, проверка давления. Диагностика от 40 BYN, групповые выезды. Тел. +375 29 687-87-17.",
                },
                "holod-dlya-cvetochnyh-magazinov": {
                    "desc": "Кондиционеры, холодильные камеры и витрины для цветочных магазинов {in}: ремонт и обслуживание по договору. Тел. +375 29 687-87-17.",
                    "lead": "Цветы теряют товарный вид за несколько часов без холода. Мы обслуживаем цветочные салоны: ремонтируем холодильные камеры и витрины для цветов, обслуживаем кондиционеры. Плановые работы делаем во время групповых выездов, при аварии можно вызвать мастера отдельно.",
                },
            }}


CITIES.update({
    "gomel": group_city("Гомель", "в Гомеле", "Гомельская область",
                        "Гомель и Гомельский район, а также Речица, Жлобин и Светлогорск",
                        "более 800 клиентов",
                        "В Гомель и Гомельскую область мы ездим регулярно: обслуживаем кондиционеры в квартирах, домах, офисах и магазинах."),
    "vitebsk": group_city("Витебск", "в Витебске", "Витебская область",
                          "Витебск и Витебский район",
                          "более 700 клиентов",
                          "В Витебске нам доверяют частные клиенты и бизнес, и каждый сезон мы приезжаем обслужить их кондиционеры."),
    "orsha": group_city("Орша", "в Орше", "Витебская область",
                        "Орша и Оршанский район, а также Дубровно и Новолукомль",
                        "около 600 клиентов",
                        "Орша ближе всего к Могилёву из городов Витебской области, поэтому группы сюда собираются быстро."),
    "polotsk": group_city("Полоцк", "в Полоцке и Новополоцке", "Витебская область",
                          "Полоцк, Новополоцк и Полоцкий район",
                          "более 400 клиентов",
                          "Полоцк и Новополоцк мы обслуживаем вместе, одной поездкой: это удобно и вам, и нам."),
})

PAGES = [
    {
        "slug": "obsluzhivanie-kondicionerov",
        "videos": [("5D4iwPBhh-w", "Обслуживание кондиционера")],
        "title": "Обслуживание кондиционеров {in}",
        "desc": "Техническое обслуживание и чистка кондиционеров {in}: от 125 BYN. Выезд на следующий день, гарантия. Климат 365, тел. +375 29 687-87-17.",
        "lead": "Плановое обслуживание продлевает жизнь кондиционера, возвращает ему мощность охлаждения и убирает неприятный запах. Приезжаем, как правило, на следующий день после звонка.",
        "sections": [
            ("Что входит в обслуживание", [
                "Чистка фильтров и теплообменника внутреннего блока",
                "Дезинфекция от бактерий и плесени",
                "Проверка давления фреона и дозаправка при необходимости",
                "Проверка дренажа, чтобы кондиционер не капал",
                "Проверка работы во всех режимах",
            ]),
            ("Когда пора обслужить", [
                "Кондиционер стал хуже охлаждать",
                "Появился запах при включении",
                "Капает вода из внутреннего блока",
                "Последнее обслуживание было больше года назад",
            ]),
        ],
        "prices": [("Обслуживание «Стандарт»", "125 BYN"), ("Обслуживание «Стандарт Плюс»", "150 BYN")],
        "faq": [
            ("Как часто нужно обслуживать кондиционер?", "Для дома достаточно одного раза в год, лучше весной перед сезоном. Для магазинов, кафе и цветочных салонов, где кондиционер работает каждый день, раз в полгода."),
            ("Сколько длится обслуживание?", "Обычно 1–2 часа на один кондиционер."),
        ],
    },
    {
        "slug": "zapravka-kondicionerov",
        "title": "Заправка кондиционеров фреоном {in}",
        "desc": "Заправка и дозаправка кондиционеров фреоном {in}. Поиск и устранение утечки, проверка давления. Диагностика от 40 BYN. Тел. +375 29 687-87-17.",
        "lead": "Если кондиционер дует, но не холодит, чаще всего ему не хватает фреона. Мы не просто доливаем фреон, а находим, куда он ушёл, иначе через месяц всё повторится.",
        "sections": [
            ("Как проходит заправка", [
                "Проверяем давление в системе",
                "Ищем и устраняем место утечки",
                "Заправляем фреоном нужной марки",
                "Проверяем, что кондиционер выходит на рабочий режим",
            ]),
            ("Признаки нехватки фреона", [
                "Кондиционер дует тёплым или едва прохладным воздухом",
                "На штуцерах наружного блока появляется иней",
                "Кондиционер работает без остановки, а в комнате жарко",
            ]),
        ],
        "prices": [("Диагностика", "от 40 BYN"), ("Обслуживание с дозаправкой «Стандарт»", "125 BYN")],
        "faq": [
            ("Нужно ли заправлять кондиционер каждый год?", "Нет. Исправный кондиционер не теряет фреон. Если его приходится доливать каждый сезон, значит есть утечка, и её нужно устранить."),
        ],
    },
    {
        "slug": "remont-kondicionerov",
        "title": "Ремонт кондиционеров {in}",
        "desc": "Ремонт кондиционеров {in}: не холодит, течёт, шумит, не включается. Аварийный выезд в день обращения, диагностика от 40 BYN, гарантия 1 год. Тел. +375 29 687-87-17.",
        "lead": "Ремонтируем бытовые и полупромышленные кондиционеры любых марок. При аварии выезжаем в день обращения. На ремонт даём гарантию 1 год.",
        "sections": [
            ("С чем к нам обращаются", [
                "Кондиционер не холодит или не греет",
                "Течёт вода из внутреннего блока",
                "Шумит или вибрирует наружный блок",
                "Не включается, мигают лампочки или ошибка на дисплее",
                "Не реагирует на пульт",
            ]),
        ],
        "prices": [("Диагностика и ремонт", "от 40 BYN")],
        "faq": [
            ("Сколько стоит ремонт?", "Точную цену называем после диагностики, она стоит от 40 BYN. Ориентировочную стоимость часто можем подсказать по телефону, если описать, что происходит."),
            ("Какая гарантия на ремонт?", "1 год, выдаём гарантийный талон."),
        ],
    },
    {
        "slug": "montazh-kondicionerov",
        "shop": True,
        "videos": [("bYHBgKCmuSY", "Монтаж кондиционера"), ("KMqF0kp1l1Y", "Монтаж кондиционера, ещё один объект")],
        "title": "Установка и монтаж кондиционеров {in}",
        "desc": "Установка кондиционеров {in}: монтаж от 450 BYN, гарантия на монтаж 3 года. Бытовые и полупромышленные сплит-системы. Тел. +375 29 687-87-17.",
        "lead": "Устанавливаем бытовые и полупромышленные кондиционеры в квартирах, домах, офисах и магазинах. Даём гарантию на монтаж 3 года.",
        "sections": [
            ("Что важно при монтаже", [
                "Правильное место для внутреннего блока, чтобы не дуло на людей",
                "Надёжное крепление наружного блока",
                "Аккуратная трасса в декоративном коробе",
                "Вакуумирование системы перед запуском",
            ]),
        ],
        "prices": [("Монтаж «Стандарт»", "450 BYN"), ("Монтаж «Стандарт Плюс»", "500 BYN"),
                   ("Монтаж полупромышленного кондиционера", "600 BYN"), ("Демонтаж", "100 BYN")],
        "faq": [
            ("Какая гарантия на монтаж?", "3 года. После работы выдаём гарантийный талон ООО «Климат 365»."),
        ],
    },
    {
        "slug": "holod-dlya-cvetochnyh-magazinov",
        "brands": False,
        "title": "Холодильное оборудование для цветочных магазинов {in}",
        "desc": "Кондиционеры, холодильные камеры и витрины для цветочных магазинов {in}: подбор, монтаж, ремонт и обслуживание. Аварийный выезд в день обращения. Тел. +375 29 687-87-17.",
        "lead": "Цветы теряют товарный вид за несколько часов без холода. Мы обслуживаем цветочные салоны: подбираем и ставим кондиционеры, ремонтируем холодильные камеры и витрины для цветов. При поломке выезжаем в день обращения.",
        "sections": [
            ("Что делаем для цветочных магазинов", [
                "Подбор и монтаж кондиционера под площадь салона",
                "Ремонт и обслуживание холодильных камер для цветов",
                "Ремонт цветочных холодильных витрин",
                "Плановое обслуживание по договору",
            ]),
            ("Почему это важно", [
                "Стабильная температура продлевает жизнь букетов",
                "Регулярное обслуживание снижает риск аварии в праздники, когда загрузка максимальная",
            ]),
        ],
        "prices": [],
        "faq": [
            ("Можно ли заключить договор на обслуживание?", "Да, работаем с организациями: договор, документы и регулярные выезды по графику."),
        ],
    },
]


def page_html(city_key, city, p):
    p = {**p, **city["overrides"].get(p["slug"], {})}
    t = lambda s: s.format(**{"in": city["in"]})
    title = t(p["title"])
    lis = lambda items: "\n".join(f"        <li>{escape(i)}</li>" for i in items)
    sections = "\n".join(f"""  <section class="wrap">
    <h2>{escape(h)}</h2>
    <ul class="why">
{lis(items)}
    </ul>
  </section>""" for h, items in p["sections"])
    if city.get("intro"):
        ih, it = city["intro"]
        sections = f"""  <section class="wrap">
    <h2>{escape(ih)}</h2>
    <p>{escape(it)}</p>
  </section>

""" + sections
    prices = ""
    if p["prices"]:
        rows = "\n".join(f"      <tr><td>{escape(a)}</td><td>{escape(b)}</td></tr>" for a, b in p["prices"])
        prices = f"""  <section class="wrap">
    <h2>Цены</h2>
    <table class="prices">
{rows}
    </table>
  </section>"""
    if p.get("shop"):
        sl = "\n".join(f'      <li><a href="{u}">{escape(n)}</a>: {escape(d)}</li>' for u, n, d in SHOP_LINKS)
        prices += f"""

  <section class="wrap">
    <h2>Ещё нет кондиционера?</h2>
    <p>Кондиционеры мы продаём в нашем магазине на сайте могилев.климат365.бел. Купите у нас и сразу закажите монтаж: поможем подобрать модель под площадь помещения и установим её.</p>
    <ul class="why">
{sl}
    </ul>
    <p><a href="{SHOP}.html">Все кондиционеры в каталоге Климат 365</a></p>
  </section>"""
    brands = ""
    if p.get("brands", True):
        bl = "\n".join(f"      <li>{escape(b)}</li>" for b in BRANDS)
        brands = f"""  <section class="wrap">
    <h2>Работаем со всеми марками</h2>
    <ul class="brands">
{bl}
    </ul>
  </section>"""
    videos = ""
    if p.get("videos"):
        vl = "\n".join(f'      <iframe src="https://www.youtube-nocookie.com/embed/{v}" title="{escape(vt)}: видео Климат 365" loading="lazy" allow="encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>' for v, vt in p["videos"])
        videos = f"""  <section class="wrap">
    <h2>Как мы работаем: видео</h2>
    <div class="videos">
{vl}
    </div>
  </section>"""
    faq = "\n".join(f"""    <h3>{escape(q)}</h3>
    <p>{escape(a)}</p>""" for q, a in p["faq"])
    others = "\n".join(
        f'      <li><a href="{o["slug"]}.html">{escape(t(o["title"]))}</a></li>'
        for o in PAGES if o["slug"] != p["slug"] and o["slug"] in city.get("pages", [x["slug"] for x in PAGES]))
    url = f"{BASE}{city_key}/{p['slug']}.html"
    ld = [
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Главная", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": title, "item": url}]},
        {"@context": "https://schema.org", "@type": "Service", "name": title, "areaServed": city["name"],
         "provider": {"@type": "HVACBusiness", "name": "Климат 365", "telephone": PHONE, "url": BASE}},
    ]
    ld_html = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    og = f"""<meta property="og:type" content="website">
<meta property="og:title" content="{escape(title)} | Климат 365">
<meta property="og:description" content="{escape(t(p["desc"]))}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}img/team/team-2.jpg">
<meta property="og:locale" content="ru_BY">"""
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | Климат 365</title>
<meta name="description" content="{escape(t(p["desc"]))}">
<link rel="canonical" href="{url}">
{og}
{ld_html}
<link rel="icon" href="../img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap">
<link rel="stylesheet" href="../style.css?v=7">
</head>
<body>

<header class="top">
  <div class="wrap top-in">
    <a href="../" class="logo"><img src="../img/logo.png" alt="Климат 365" width="160" height="73"></a>
    <nav class="menu" aria-label="Меню"><a href="../#uslugi">Услуги</a><a href="../#prices">Цены</a><a href="../#reviews">Отзывы</a><a href="../#minsk">Минск</a><a href="../#contacts">Контакты</a></nav>
    <div class="top-contact"><a class="phone" href="tel:{PHONE}">{PHONE_TXT}</a><span>ежедневно 9:00–20:00</span></div>
  </div>
</header>

<main>
  <section class="hero">
    <div class="wrap">
      <p class="crumbs"><a href="../">Главная</a> → {escape(title)}</p>
      <h1>{escape(title)}</h1>
      <p class="lead">{escape(p["lead"])}</p>
      <ul class="badges">
        <li><b>Работаем с 2018 года</b></li>
        <li><b>Более 9 000 клиентов</b></li>
        <li><b>Сервис круглый год</b></li>
        <li><b>5,0 ★</b> на Яндекс Картах</li>
        <li>{city["badge"]}</li>
      </ul>
      <div class="cta">
        <a class="btn btn-main" href="tel:{PHONE}">Позвонить</a>
        <a class="btn btn-viber" href="{VIBER}">Viber</a>
        <a class="btn btn-tg" href="{TG}">Telegram</a>
      </div>
    </div>
  </section>

{sections}

  <section class="wrap">
    <h2>Свой отдел сервиса</h2>
    <p>{escape(SERVICE_INTRO)}</p>
    <ul class="why">
{chr(10).join(f"      <li>{i}</li>" for i in SERVICE_ITEMS)}
    </ul>
  </section>

{videos}

{brands}

{prices}

  <section class="wrap">
    <h2>Как быстро приедем</h2>
    <ul class="why">
{lis(city["speed"])}
    </ul>
    <h2>Где работаем</h2>
    <p>{escape(city["near"])}.</p>
  </section>

  <section class="wrap">
    <h2>Вопросы и ответы</h2>
{faq}
  </section>

  <section class="wrap">
    <h2>Другие услуги {escape(city["in"])}</h2>
    <ul>
{others}
    </ul>
  </section>

  <section class="contacts" id="contacts">
    <div class="wrap">
      <h2>Оставьте заявку</h2>
      <p>Позвоните или напишите, расскажите, что случилось, и мы подскажем стоимость и время выезда.</p>
      <p class="big"><a href="tel:{PHONE}">{PHONE_TXT}</a> <span>(A1)</span></p>
      <p>Viber и Telegram: <a href="{VIBER}">+375 44 768-81-27</a></p>
      <p>Офис: г. Могилёв, ул. Калужская, 15/1, офис 3<br>Работаем ежедневно с 9:00 до 20:00<br>Почта: <a href="mailto:klimat365.pro@yandex.ru">klimat365.pro@yandex.ru</a></p>
    </div>
  </section>
</main>

<footer class="wrap foot">
  <p>ООО «Климат 365» · Обслуживание кондиционеров и холодильного оборудования в Беларуси</p>
  <p>УНП 791308488 · г. Могилёв, ул. Калужская, 15/1, офис 3 · ежедневно 9:00–20:00</p>
</footer>

<nav class="callbar" aria-label="Связаться">
  <a class="cb-call" href="tel:{PHONE}">Позвонить</a>
  <a class="cb-viber" href="{VIBER}">Viber</a>
  <a class="cb-tg" href="{TG}">Telegram</a>
</nav>

</body>
</html>
"""



def shell(title, desc, url, ld, crumbs, main_html, og_type="website"):
    """Общая обёртка страницы (шапка, заявка, подвал) для статей и раздела «Полезное»."""
    ld_html = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} | Климат 365</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{escape(title)} | Климат 365">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}img/team/team-2.jpg">
<meta property="og:locale" content="ru_BY">
{ld_html}
<link rel="icon" href="../img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap">
<link rel="stylesheet" href="../style.css?v=7">
</head>
<body>

<header class="top">
  <div class="wrap top-in">
    <a href="../" class="logo"><img src="../img/logo.png" alt="Климат 365" width="160" height="73"></a>
    <nav class="menu" aria-label="Меню"><a href="../#uslugi">Услуги</a><a href="../#prices">Цены</a><a href="../#reviews">Отзывы</a><a href="./">Полезное</a><a href="../#contacts">Контакты</a></nav>
    <div class="top-contact"><a class="phone" href="tel:{PHONE}">{PHONE_TXT}</a><span>ежедневно 9:00–20:00</span></div>
  </div>
</header>

<main>
  <section class="hero hero-article">
    <div class="wrap">
      <p class="crumbs">{crumbs}</p>
      <h1>{escape(title)}</h1>
    </div>
  </section>

{main_html}

  <section class="contacts" id="contacts">
    <div class="wrap">
      <h2>Нужен мастер?</h2>
      <p>Позвоните или напишите, расскажите, что случилось, и мы подскажем стоимость и время выезда. Работаем в Могилёве, Минске, Гомеле, Витебске, Орше и Полоцке.</p>
      <p class="big"><a href="tel:{PHONE}">{PHONE_TXT}</a> <span>(A1)</span></p>
      <p>Viber и Telegram: <a href="{VIBER}">+375 44 768-81-27</a></p>
      <p>Офис: г. Могилёв, ул. Калужская, 15/1, офис 3<br>Работаем ежедневно с 9:00 до 20:00<br>Почта: <a href="mailto:klimat365.pro@yandex.ru">klimat365.pro@yandex.ru</a></p>
    </div>
  </section>
</main>

<footer class="wrap foot">
  <p>ООО «Климат 365» · Обслуживание кондиционеров и холодильного оборудования в Беларуси</p>
  <p>УНП 791308488 · г. Могилёв, ул. Калужская, 15/1, офис 3 · ежедневно 9:00–20:00</p>
</footer>

<nav class="callbar" aria-label="Связаться">
  <a class="cb-call" href="tel:{PHONE}">Позвонить</a>
  <a class="cb-viber" href="{VIBER}">Viber</a>
  <a class="cb-tg" href="{TG}">Telegram</a>
</nav>

</body>
</html>
"""


MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]


def ru_date(d):
    y, m, dd = d.split("-")
    return f"{int(dd)} {MONTHS[int(m) - 1]} {y}"


def article_html(a):
    url = f"{BASE}poleznoe/{a['slug']}.html"
    faq = "\n".join(f"""    <h3>{escape(q)}</h3>
    <p>{escape(ans)}</p>""" for q, ans in a["faq"])
    main_html = f"""  <article class="wrap article">
    <p class="answer"><b>Короткий ответ:</b> {escape(a["lead"])}</p>
{a["body"]}
    <h2>Вопросы и ответы</h2>
{faq}
    <p class="byline">Статью проверил главный инженер «Климат 365» Андрей Эдуардович · {ru_date(a["date"])}</p>
  </article>"""
    ld = [
        {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"],
         "datePublished": a["date"], "mainEntityOfPage": url, "image": f"{BASE}img/team/team-2.jpg",
         "author": {"@type": "Person", "name": "Андрей Эдуардович", "jobTitle": "Главный инженер"},
         "publisher": {"@type": "Organization", "name": "Климат 365", "logo": {"@type": "ImageObject", "url": f"{BASE}img/logo.png"}}},
        {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in a["faq"]]},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Главная", "item": BASE},
            {"@type": "ListItem", "position": 2, "name": "Полезное", "item": f"{BASE}poleznoe/"},
            {"@type": "ListItem", "position": 3, "name": a["title"], "item": url}]},
    ]
    crumbs = f'<a href="../">Главная</a> → <a href="./">Полезное</a> → {escape(a["title"])}'
    return shell(a["title"], a["desc"], url, ld, crumbs, main_html, og_type="article")


def articles_index_html(items):
    url = f"{BASE}poleznoe/"
    lis = "\n".join(f'      <li><a href="{a["slug"]}.html"><b>{escape(a["title"])}</b></a><br>{escape(a["desc"])}</li>' for a in items)
    main_html = f"""  <section class="wrap">
    <p>Советы инженеров «Климат 365» по кондиционерам и холодильному оборудованию для цветочных магазинов.</p>
    <ul class="why">
{lis}
    </ul>
  </section>"""
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Главная", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": "Полезное", "item": url}]}]
    return shell("Полезное о кондиционерах", "Статьи инженеров Климат 365: обслуживание и ремонт кондиционеров, обогрев зимой, холодильное оборудование для цветочных магазинов.",
                 url, ld, '<a href="../">Главная</a> → Полезное', main_html)


def build_articles(urls):
    from articles import ARTICLES
    items = sorted((a for a in ARTICLES if not a.get("draft")), key=lambda a: a["date"], reverse=True)
    if not items:
        return
    out = ROOT / "poleznoe"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(articles_index_html(items), encoding="utf-8")
    urls.append(f"{BASE}poleznoe/")
    for a in items:
        (out / f'{a["slug"]}.html').write_text(article_html(a), encoding="utf-8")
        urls.append(f'{BASE}poleznoe/{a["slug"]}.html')


def main():
    urls = [BASE]
    for key, city in CITIES.items():
        out = ROOT / key
        out.mkdir(exist_ok=True)
        for p in PAGES:
            if p["slug"] not in city.get("pages", [x["slug"] for x in PAGES]):
                continue
            (out / f'{p["slug"]}.html').write_text(page_html(key, city, p), encoding="utf-8")
            urls.append(f'{BASE}{key}/{p["slug"]}.html')
    build_articles(urls)
    sitemap = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap}\n</urlset>\n',
        encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
    print(f"{len(urls) - 1} страниц")


if __name__ == "__main__":
    main()
