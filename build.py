"""Builds every page of the site from shared pieces (header, footer, hero, image slots, space template).

Edit this file, then run:  python3 build.py
It rewrites the .html files next to it. style.css, site.js and images/ are edited directly.
"""
import os, hashlib
OUT = os.path.dirname(os.path.abspath(__file__))
# cache-buster: changes only when style.css or site.js change
VER = hashlib.md5(b"".join(open(os.path.join(OUT, f), "rb").read() for f in ("style.css", "site.js"))).hexdigest()[:8]
os.makedirs(OUT + "/images", exist_ok=True)

NAV = [("index.html","דף הבית"),("story.html","הסיפור שלי"),("mishkan.html","המשכן"),
       ("spaces","המרחבים שלי"),("events.html","אירועים ומפגשים"),("contact.html","יצירת קשר")]
SPACES = [("kol-hanshama.html","קול הנשמה"),("derech-haahava.html","דרך האהבה"),
          ("bechazara-leahava.html","בחזרה לאהבה"),("veahavat-lach.html","ואהבת לך")]

def slot(name, label, ratio="4/3", cls=""):
    """Image slot: shows images/<name> if the file exists, otherwise a labelled placeholder."""
    if "hero-img" in cls:
        return '<div class="halo">' + slot(name, label, ratio, cls.replace("hero-img","hero-fig")) + '</div>'
    return (f'<figure class="slot {cls}" style="--ratio:{ratio}">'
            f'<div class="slot-ph"><span class="slot-ico">▢</span><b>{label}</b><small>images/{name}</small></div>'
            f'<img src="images/{name}" alt="{label}" loading="lazy" onerror="this.remove()"></figure>')

def page(fn, title, desc, body, active):
    nav = ""
    for idx,(href, t) in enumerate(NAV):
        if href == "spaces":
            sub = "".join('<a href="%s"%s>%s</a>' % (h, ' class="cur"' if h == active else "", n) for h, n in SPACES)
            cur = ' class="cur"' if active in [h for h, _ in SPACES] else ""
            nav += f'<div class="dd" style="--i:{idx}"><button{cur} aria-expanded="false">{t}<i class="caret"></i></button><div class="dd-menu">{sub}</div></div>'
        else:
            cur = ' class="cur"' if href == active else ""
            nav += f'<a href="{href}"{cur} style="--i:{idx}">{t}</a>'
    return f'''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | מירב מאור</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title} | מירב מאור">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="images/og-share.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bellefair&family=Frank+Ruhl+Libre:wght@400;500&family=Amatic+SC:wght@400;700&family=Assistant:wght@300;400;600&display=swap">
<script>try{{var p=sessionStorage.getItem('pt');if(p){{sessionStorage.removeItem('pt');var a=p.split(',');var d=document.documentElement;d.classList.add('pt-in');d.style.setProperty('--px',a[0]+'px');d.style.setProperty('--py',a[1]+'px')}}}}catch(e){{}}</script>
<link rel="stylesheet" href="style.css?v={VER}">
</head>
<body class="{'home' if fn=='index.html' else ''}">
<header class="hdr"><div class="wrap hdr-in">
<a class="logo" href="index.html"><i class="logo-ring"></i><span>מירב מאור<small>אהבה זה כל הסיפור ♡</small></span></a>
<button class="burger" aria-label="תפריט" aria-expanded="false"><span></span><span></span><span></span></button>
<nav class="nav">{nav}</nav>
</div></header>
<main>
{body}
</main>
<footer class="ftr"><div class="wrap ftr-grid">
<div class="ftr-brand"><p class="ftr-t">מירב מאור</p><p>מרחבי ריפוי, חיבור והיזכרות בתדר של אהבה.</p>
<p class="ftr-soc"><a href="https://wa.me/972503854445" target="_blank" rel="noopener">וואטסאפ</a><a href="https://www.instagram.com/meiravmaor/" target="_blank" rel="noopener">אינסטגרם</a><a href="https://www.facebook.com/merimaor" target="_blank" rel="noopener">פייסבוק</a></p>
<p class="ftr-contact"><a href="tel:+972503854445" dir="ltr">050-385-4445</a></p></div>
<nav aria-label="האתר"><h4>האתר</h4><a href="index.html">דף הבית</a><a href="story.html">הסיפור שלי</a><a href="mishkan.html">המשכן</a><a href="events.html">אירועים ומפגשים</a><a href="contact.html">יצירת קשר</a></nav>
<nav aria-label="המרחבים"><h4>המרחבים</h4><a href="kol-hanshama.html">קול הנשמה</a><a href="derech-haahava.html">דרך האהבה</a><a href="bechazara-leahava.html">בחזרה לאהבה</a><a href="veahavat-lach.html">ואהבת לך</a></nav>
</div><div class="wrap ftr-bot"><span>כל הזכויות שמורות למירב מאור</span><a href="privacy.html">מדיניות פרטיות</a></div></footer>
<script src="site.js?v={VER}"></script>
</body>
</html>
'''

def hero(h1, sub, imgname, imglabel, kicker=""):
    return f'''<section class="hero"><div class="wrap hero-in">
<div class="hero-txt"><p class="kicker">{kicker}</p><h1>{h1}</h1><p class="lead">{sub}</p>
<p class="cta"><a class="btn" href="contact.html">לפנייה אישית</a> <a class="btn ghost" href="events.html">למפגשים הקרובים</a></p></div>
{slot(imgname, imglabel, "4/5", "hero-img")}
</div></section>'''

def bullets(items): return "<ul class='ticks'>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

def space_page(fn, name, tagline, intro, items, heading, extra, imgs, note=""):
    body = hero(name, f"{tagline}", imgs[0][0], imgs[0][1], "מרחב")
    body += f'''<section class="sec"><div class="wrap two">
<div><h2>על המרחב</h2><p>{intro}</p><h3>{heading}</h3>{bullets(items)}{extra}</div>
{slot(imgs[1][0], imgs[1][1], "4/5")}
</div></section>
<section class="sec alt"><div class="wrap"><h2>גלריה</h2>
<div class="grid3">{slot(imgs[2][0], imgs[2][1], "1/1")}{slot(imgs[3][0], imgs[3][1], "1/1")}{slot(imgs[4][0], imgs[4][1], "1/1")}</div>
<p class="muted">מקום לתמונות ולסרטונים מהמפגשים. תמונות משתתפים יפורסמו רק בהסכמתם.</p></div></section>
<section class="sec"><div class="wrap narrow"><h2>שאלות נפוצות</h2>
<details><summary>למי זה מתאים?</summary><p>[יושלם: למי המרחב מיועד ומה לא צריך להביא איתכם.]</p></details>
<details><summary>מה קורה במפגש?</summary><p>[יושלם: תיאור מפגש טיפוסי.]</p></details>
<details><summary>איך מצטרפים?</summary><p>אפשר לפנות דרך <a href="contact.html">טופס יצירת הקשר</a> או לבחור מפגש קרוב בלוח <a href="events.html">האירועים</a>.</p></details>
{note}
</div></section>
<section class="cta-band"><div class="wrap"><h2>רוצים לשמוע עוד?</h2><p><a class="btn" href="contact.html">בואו ניפגש</a></p></div></section>'''
    return body

pages = {}

# ---------------- HOME ----------------
gates = [("kol-hanshama.html","קול הנשמה","מרחב של צלילים מרפאים, מעגלי שירה, עבודה קולית והקשבה פנימית.","gate-kol.jpg","צלילים וכלי נגינה"),
 ("derech-haahava.html","דרך האהבה","מרחב לפנויים ולפנויות המבקשים להכיר, להתחבר, להתפתח וליצור קשרים אמיתיים.","gate-derech.jpg","מפגש היכרות"),
 ("bechazara-leahava.html","בחזרה לאהבה","מרחב לזוגות המבקשים להתקרב, לפתוח את הלב ולבנות תקשורת ואינטימיות מיטיבות.","gate-bechazara.jpg","זוגיות וחיבור"),
 ("veahavat-lach.html","ואהבת לך","מסע נשי של היזכרות, התעוררות ובחירה.","gate-veahavat.jpg","מסע נשי")]
cards = "".join(f'<a class="card" href="{h}">{slot(img, lab, "4/5")}<h3>{n}</h3><p>{d}</p><span class="more">להיכנס למרחב ←</span></a>' for h,n,d,img,lab in gates)
pages["index.html"] = ("ברוכים הבאים הביתה", "מרחבי ריפוי, חיבור והיזכרות בתדר של אהבה. הבית הדיגיטלי של מירב מאור.", "index.html", f'''
<section class="vhero">
<figure class="vslot"><div class="slot-ph"><span class="slot-ico">▶</span><b>סרטון אווירה (מירב, צלילים, טבע)</b><small>images/hero-video.mp4 · poster: images/hero-poster.jpg</small></div>
<video autoplay muted loop playsinline preload="metadata" poster="images/hero-poster.jpg"><source src="images/hero-video.mp4" type="video/mp4" onerror="this.closest('video').remove()"></video>
<button class="vsound" type="button" aria-label="הפעלת צליל" hidden>🔇</button></figure>
</section>
<section class="intro"><div class="wrap narrow c"><p class="kicker">ברוכים הבאים הביתה</p>
<h1>מירב מאור</h1>
<p class="lead">מרחבי ריפוי, חיבור והיזכרות בתדר של אהבה.</p>
<p>אני מאמינה שהדרך הביתה מתחילה ברגע שבו אנחנו עוצרים להקשיב. להקשיב לגוף, ללב, לקול הפנימי ולמה שמבקש להתעורר בתוכנו. דרך קול וצלילים, תהליכי התפתחות, חיבורים בין לבבות ומפגשים שנוגעים במהות, אני יוצרת מרחבים שבהם אפשר להיזכר, להתרכך, להיפתח ולפגוש את עצמנו מחדש.</p>
<p class="cta"><a class="btn" href="#gates">לגלות את המרחבים שלי</a> <a class="btn ghost" href="story.html">להכיר את הסיפור שלי</a> <a class="btn ghost" href="events.html">להצטרף למפגש קרוב</a></p></div></section>
<section class="sec" id="gates"><div class="wrap"><h2 class="c">ארבעת שערי העשייה</h2><div class="grid4">{cards}</div></div></section>
<section class="quote"><div class="wrap"><p>כשהמילים נחות, הצלילים מדברים</p><small>מרחבי ריפוי, חיבור והיזכרות</small></div></section>
<section class="sec alt"><div class="wrap two">
{slot("mishkan-home.jpg","המרחב החדש ברעננה","4/3")}
<div><p class="kicker">המשכן</p><h2>בית למפגש, לריפוי ולהיזכרות</h2>
<p>המשכן הוא המרחב שאני מבקשת ליצור ברעננה: בית למפגשים, מעגלים, סדנאות ותהליכים המחברים בין גוף, נפש, רוח ולב. מרחב לנשום, להקשיב, לשיר, לנוע, לפגוש אנשים ולתת מקום למה שמבקש להיוולד.</p>
<p><a class="btn" href="mishkan.html">להכיר את המשכן</a></p></div></div></section>
<section class="sec"><div class="wrap two rev">
<div><p class="kicker">הסיפור שלי</p><h2>מגשרת בין עולמות</h2>
<p>הדרך שלי עוברת בין הגוף לרוח, בין המילים לשתיקה, בין הצליל לריפוי ובין האדם לעצמו ולאחר. אני מורת דרך רוחנית, אשת רפואה שמאנית ומאמנת זוגית. מתוך הדרך והמפגשים התגבשה בי השליחות ליצור מרחבים שמאפשרים לאנשים להקשיב, להתחבר ולהיזכר במהות שלהם.</p>
<p><a class="btn ghost" href="story.html">לסיפור המלא</a></p></div>
{slot("story-home.jpg","תמונה אישית של מירב","4/5")}</div></section>
<section class="sec alt"><div class="wrap"><h2 class="c">אירועים קרובים</h2>
<div class="grid3">
<article class="ev">{slot("event-1.jpg","תמונת אירוע","16/10")}<h3>שם האירוע</h3><p class="muted">תאריך ושעה · מיקום</p><a class="btn small" href="events.html">פרטים והרשמה</a></article>
<article class="ev">{slot("event-2.jpg","תמונת אירוע","16/10")}<h3>שם האירוע</h3><p class="muted">תאריך ושעה · מיקום</p><a class="btn small" href="events.html">פרטים והרשמה</a></article>
<article class="ev">{slot("event-3.jpg","תמונת אירוע","16/10")}<h3>שם האירוע</h3><p class="muted">תאריך ושעה · מיקום</p><a class="btn small" href="events.html">פרטים והרשמה</a></article>
</div></div></section>
<section class="cta-band"><div class="wrap"><h2>הקהילה</h2><p>הצטרפו לקהילה של אנשים המבקשים לחיות בחיבור, להעמיק את הקשר עם עצמם ועם אחרים וליצור עוד מרחבים של אהבה בחיים.</p><p><a class="btn" href="contact.html">להצטרף לקהילה</a></p></div></section>
''')

# ---------------- STORY ----------------
pages["story.html"] = ("הסיפור שלי", "הדרך האישית והמקצועית של מירב מאור: מורת דרך רוחנית, אשת רפואה שמאנית ומאמנת זוגית.", "story.html", f'''
{hero("הסיפור שלי","אני מאמינה שאהבה היא לא רק דבר שאנחנו מחפשים. היא גם הדרך שבה אנחנו פוגשים את עצמנו, את האחר ואת החיים.","story-hero.jpg","פורטרט טבעי של מירב","הכירו אותי")}
<section class="sec"><div class="wrap two">
<div><h2>מגשרת בין עולמות</h2>
<p>הדרך שלי עוברת בין הגוף לרוח, בין המילים לשתיקה, בין הצליל לריפוי ובין האדם לעצמו ולאחר. אני מורת דרך רוחנית, אשת רפואה שמאנית ומאמנת זוגית.</p>
<p class="draft">[כאן יבוא הנוסח הסופי של הסיפור האישי, בגוף ראשון, בקול אישי, כן ונוגע.]</p>
<h3>על מה אספר</h3>
{bullets(["הדרך האישית וההתפתחותית","החיבור בין רוח, גוף, נפש, קול ואהבה","היותי מורת דרך רוחנית ואשת רפואה שמאנית","העבודה עם קול, שירה, תנועה וצלילים מרפאים","הליווי האישי והזוגי","ליווי מעברי חיים ויצירת טקסים משמעותיים, לרבות טקסי לידה","החזון ליצור מרחבי ריפוי, חיבור והיזכרות"])}
</div>
<div class="stack">{slot("story-1.jpg","תמונה מהדרך","4/5")}{slot("story-2.jpg","תמונה עם כלי נגינה","4/3")}</div>
</div></section>
<section class="sec alt"><div class="wrap"><h2>רגעים מהדרך</h2><div class="grid3">{slot("story-3.jpg","תמונה","1/1")}{slot("story-4.jpg","תמונה","1/1")}{slot("story-5.jpg","תמונה","1/1")}</div></div></section>
<section class="cta-band"><div class="wrap"><h2>נשמח להכיר</h2><p><a class="btn" href="contact.html">בואו ניפגש</a></p></div></section>
''')

# ---------------- MISHKAN ----------------
pages["mishkan.html"] = ("המשכן", "המשכן: המרחב הפיזי והקהילתי החדש ברעננה. בית למפגשים, מעגלים, סדנאות ותהליכים.", "mishkan.html", f'''
{hero("המשכן","בית למפגש, לריפוי ולהיזכרות. המרחב שאני מבקשת ליצור ברעננה.","mishkan-hero.jpg","המרחב החדש (או הדמיה)","ברעננה")}
<section class="sec"><div class="wrap two">
<div><h2>בית שמאפשר לעצור</h2><p>המשכן הוא בית למפגשים שמאפשרים לעצור את מרוץ היומיום ולהתחבר מחדש למהות. כאן עתידים להתקיים:</p>
{bullets(["מעגלי שירה וצלילים מרפאים","מפגשי קול ותנועה","סדנאות התפתחות ורוח","מפגשים לפנויים ולפנויות","מרחבים ותהליכים לנשים","מפגשים לזוגות","טקסים, מפגשים מיוחדים ואירועים קהילתיים"])}</div>
{slot("mishkan-1.jpg","תמונה של המרחב","4/5")}</div></section>
<section class="sec alt"><div class="wrap"><h2>גלריית המרחב</h2><div class="grid3">{slot("mishkan-2.jpg","תמונה","4/3")}{slot("mishkan-3.jpg","תמונה","4/3")}{slot("mishkan-4.jpg","תמונה","4/3")}{slot("mishkan-5.jpg","תמונה","4/3")}{slot("mishkan-6.jpg","תמונה","4/3")}{slot("mishkan-7.jpg","תמונה","4/3")}</div>
<p class="muted">התמונות יתווספו לאחר שהמרחב יתגבש.</p></div></section>
<section class="sec"><div class="wrap narrow"><h2>לוח מפגשים</h2><p>המפגשים הקרובים במשכן יפורסמו ב<a href="events.html">עמוד האירועים</a>.</p>
<h2>פרטי הגעה</h2><p class="draft">[פרטי המיקום יפורסמו בהתאם להחלטה.]</p>
<h2>שאלות נפוצות</h2>
<details><summary>איפה נמצא המשכן?</summary><p>ברעננה. הכתובת המדויקת תפורסם בהמשך.</p></details>
<details><summary>איך נרשמים למפגש?</summary><p>דרך <a href="events.html">לוח האירועים</a> או <a href="contact.html">טופס ההתעניינות</a>.</p></details>
</div></section>
<section class="cta-band"><div class="wrap"><h2>מתעניינים במשכן?</h2><p><a class="btn" href="contact.html">השאירו פרטים</a></p></div></section>
''')

# ---------------- SPACES ----------------
pages["kol-hanshama.html"] = ("קול הנשמה", "קול הנשמה: סאונד הילינג, מעגלי שירה, קערות קריסטל וגונג. כשהמילים נחות, הצלילים מדברים.", "kol-hanshama.html",
 space_page("", "קול הנשמה", "כשהמילים נחות, הצלילים מדברים",
 "יש דברים שהמילים לא תמיד יודעות לומר. דרך הצליל, הנשימה, הקול והשקט, אנחנו יכולים להקשיב פנימה ולפגוש מקומות בתוכנו שמבקשים תשומת לב. קול הנשמה הוא מרחב של צלילים מרפאים, מעגלי שירה, עבודה קולית ומסעות חווייתיים המשלבים הקשבה, נוכחות וחיבור פנימי.",
 ["סאונד הילינג","מעגלי שירה ושירה שמאנית","עבודה קולית וביטוי דרך הקול","קערות קריסטל, קערות טיבטיות, גונג וכלי נגינה נוספים","מסעות בצלילים ובתדרים","מפגשים קבוצתיים ואישיים, בהתאם לשירותים המוצעים"], "מה כולל המרחב", "",
 [("kol-hero.jpg","מירב עם קערות/גונג"),("kol-1.jpg","כלי נגינה"),("kol-2.jpg","מעגל שירה"),("kol-3.jpg","קערות קריסטל"),("kol-4.jpg","גונג")]))

pages["derech-haahava.html"] = ("דרך האהבה", "דרך האהבה: מפגשי היכרות, סדנאות ותהליכי התפתחות לפנויים ולפנויות.", "derech-haahava.html",
 space_page("", "דרך האהבה", "הדרך לחיבור מתחילה בתוכנו",
 "דרך האהבה היא מרחב לפנויים ולפנויות המבקשים להכיר, להתפתח, לפתוח את הלב וליצור חיבורים משמעותיים. הוא משלב בין היכרות עם אחרים לבין היכרות עמוקה יותר עם עצמנו. המרחב אינו רק שירות היכרויות אלא גם מרחב של התפתחות וקהילה.",
 ["מפגשי היכרות לפנויים ולפנויות","יצירת חיבורים והיכרויות","סדנאות בנושא אהבה, קשר ותקשורת","תהליכי התפתחות אישית בהקשר של זוגיות","מפגשי קהילה וחוויות משותפות","תוכן מעשי על גבולות, תקשורת והיכרות עצמית"], "מה כולל המרחב", "",
 [("derech-hero.jpg","מפגש חם של אנשים"),("derech-1.jpg","חיבור וקשר"),("derech-2.jpg","סדנה"),("derech-3.jpg","מעגל"),("derech-4.jpg","קהילה")]))

pages["bechazara-leahava.html"] = ("בחזרה לאהבה", "בחזרה לאהבה: ליווי ואימון זוגי, תקשורת, אינטימיות וסדנאות לזוגות.", "bechazara-leahava.html",
 space_page("", "בחזרה לאהבה", "למצוא מחדש את הדרך זה אל זו",
 "מרחב לזוגות המבקשים להעמיק את הקשר, לפתח תקשורת מיטיבה, לחזק אינטימיות ולבנות מערכת יחסים שיש בה יותר הקשבה, בחירה וקרבה.",
 ["ליווי ואימון זוגי","תקשורת והקשבה בתוך קשר","זיהוי דפוסים שמרחיקים בין בני זוג","חיזוק הקרבה והאינטימיות","תהליכים וסדנאות לזוגות","כלים מעשיים להתנהלות זוגית מיטיבה"], "מה כולל המרחב",
 '<p class="muted">הפנייה דיסקרטית, ואפשר לתאם שיחת היכרות דרך <a href="contact.html">טופס יצירת הקשר</a>.</p>',
 [("bechazara-hero.jpg","זוג בקרבה (צילום מכבד)"),("bechazara-1.jpg","תמונה"),("bechazara-2.jpg","תמונה"),("bechazara-3.jpg","תמונה"),("bechazara-4.jpg","תמונה")]))

pages["veahavat-lach.html"] = ("ואהבת לך", "ואהבת לך: מסע נשי של היזכרות, התעוררות ובחירה. המסע הביתה אל האישה שאת.", "veahavat-lach.html",
 space_page("", "ואהבת לך", "המסע הביתה אל האישה שאת",
 "מרחב נשי לתהליך חווייתי של חיבור לגוף, לנפש, לרוח ולמהות הנשית. מסע שמזמין להיזכר, להתעורר ולבחור מתוך מפגש אמיתי עם מי שאת.",
 ["<b>נזכרת</b> — חיבור פנימה, הקשבה וזיהוי הקול האישי","<b>מתעוררת</b> — מפגש עם הגוף, הנשיות, הרצון והכוחות הפנימיים","<b>בוחרת</b> — אינטגרציה, בחירה ויצירת דרך אישית להמשך"], "מבנה המסע",
 '<p>ארבעה חוטים שזורים לאורך התהליך: גוף ונשיות; נפש ועולם רגשי; נשמה ורוח; הנשיות השמאנית.</p><p class="muted">פרטי המחזור הקרוב (מועדים, מספר משתתפות ומחיר) יפורסמו לאחר אישור סופי.</p>',
 [("veahavat-hero.jpg","תמונה נשית רגישה ומכובדת"),("veahavat-1.jpg","תמונה"),("veahavat-2.jpg","תמונה"),("veahavat-3.jpg","תמונה"),("veahavat-4.jpg","תמונה")]))

# ---------------- EVENTS ----------------
spaces_filter = ["הכול","קול הנשמה","המשכן","דרך האהבה","בחזרה לאהבה","ואהבת לך","ריטריטים וטקסים"]
pills = "".join(f'<button class="pill{" on" if i==0 else ""}">{s}</button>' for i,s in enumerate(spaces_filter))
evs = "".join(f'''<article class="ev">{slot(f"event-{i}.jpg","תמונת אירוע","16/10")}<p class="tag">{spaces_filter[1+(i%6)] if False else "מרחב"}</p><h3>שם האירוע</h3><p class="muted">תאריך · שעה · מיקום · מחיר</p><p>תיאור קצר של האירוע.</p><a class="btn small" href="contact.html">הרשמה / פנייה</a></article>''' for i in range(1,7))
pages["events.html"] = ("אירועים ומפגשים", "לוח האירועים והמפגשים: סדנאות, מעגלי שירה, מפגשי היכרות, תהליכים לנשים וזוגות וריטריטים.", "events.html", f'''
<section class="page-hd"><div class="wrap"><h1>אירועים ומפגשים</h1><p class="lead">כל הפעילויות הפתוחות להרשמה, במקום אחד.</p></div></section>
<section class="sec"><div class="wrap"><div class="pills">{pills}</div>
<div class="grid3">{evs}</div>
<p class="muted c">אירועים אמיתיים יתווספו כאן. כל אירוע יכלול תמונה, תאריך, מיקום, מחיר לפי הצורך, כפתור הרשמה ואפשרות לרשימת המתנה.</p></div></section>
''')

# ---------------- CONTACT ----------------
pages["contact.html"] = ("יצירת קשר", "בואו ניפגש: טופס פנייה, וואטסאפ ורשתות חברתיות.", "contact.html", f'''
<section class="page-hd"><div class="wrap"><h1>בואו ניפגש</h1><p class="lead">אשמח לשמוע ממך. השאירו פרטים ואחזור אליכם.</p></div></section>
<section class="sec"><div class="wrap two">
<form class="form" id="contact-form" method="post" action="#" data-todo="form-endpoint">
<label>שם<input name="name" required autocomplete="name"></label>
<label>דוא״ל או טלפון<input name="contact" required autocomplete="email"></label>
<label>נושא הפנייה<select name="topic"><option>קול הנשמה</option><option>דרך האהבה</option><option>בחזרה לאהבה</option><option>ואהבת לך</option><option>המשכן</option><option>אחר</option></select></label>
<label>הודעה<textarea name="message" rows="5"></textarea></label>
<label class="chk"><input type="checkbox" required><span>אני מסכים/ה לשימוש בפרטיי ליצירת קשר, בהתאם ל<a href="privacy.html">מדיניות הפרטיות</a>.</span></label>
<button class="btn" type="submit">שליחה</button>
<p class="form-msg" role="status"></p>
</form>
<div>{slot("contact.jpg","תמונה חמה של מירב","4/5")}
</div></div></section>
''')

pages["privacy.html"] = ("מדיניות פרטיות", "מדיניות הפרטיות של האתר.", "privacy.html", '''
<section class="page-hd"><div class="wrap"><h1>מדיניות פרטיות</h1></div></section>
<section class="sec"><div class="wrap narrow"><p class="draft">[נוסח מדיניות הפרטיות, ביטולים ותנאי הרשמה יושלם בהתאם לאופן שבו המידע נאסף ונשמר.]</p></div></section>''')

for fn,(t,d,act,body) in pages.items():
    open(f"{OUT}/{fn}","w",encoding="utf-8").write(page(fn,t,d,body,act))
print(len(pages),"pages")
