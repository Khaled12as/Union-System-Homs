import os
import uvicorn
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from database import get_db_client

app = FastAPI(title="Agri-Union Homs")

# روابط مجتمعات الواتساب (يرجى وضع الروابط الحقيقية هنا)
COMMUNITY_GROUPS = {
    "السنة الأولى": "https://chat.whatsapp.com/DLYZGtkr5ZMA40EBAn0xkg?mode=gi_t",
    "السنة الثانية": "https://chat.whatsapp.com/Hs359jGCUAw9w1O9jXIXVC?mode=gi_t",
    "السنة الثالثة": "https://chat.whatsapp.com/JV7DryJiqgD7MgNIxsA5Uy?mode=gi_t",
    "السنة الرابعة": "https://chat.whatsapp.com/EXOpeeaEDfO2qvvtldCZrb?mode=gi_t",
    "السنة الخامسة": "https://chat.whatsapp.com/DrihEQImyX4Bzgv36Skggb?mode=gi_t",
}
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>بوابة الانضمام للمجتمع | مكتب التنظيم - تهنئة عيد الفطر</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/confetti-js@0.1.0/dist/confetti.min.js"></script>
    <style>
        :root {
            /* الألوان الأصلية مع إضافة ألوان العيد */
            --primary-green: #1b5e20;
            --leaf-green: #4caf50;
            --soil-brown: #5d4037;
            --soft-white: #f9fdf9;
            --sun-yellow: #ffd54f;
            --sky-blue: #81d4fa;
            /* ألوان العيد الجديدة (فخمة) */
            --eid-gold: #f9a825; /* الذهبي الملكي */
            --eid-night: #1a237e; /* الأزرق الليلي */
            --eid-purple: #4a148c; /* الأرجواني العميق */
            --accent-gold: #ffd700;
            --shadow-color: rgba(0,0,0,0.3);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Tajawal', sans-serif;
            /* خلفية متدرجة احتفالية تدمج الهوية الزراعية مع سحر ليلة العيد */
            background: linear-gradient(135deg, var(--eid-night), var(--primary-green), var(--eid-purple));
            background-attachment: fixed;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
            overflow: auto;
            position: relative;
            padding: 20px 10px;
        }

        #particles-js {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: -1;
        }

        /* إضافة زخارف فوانيس وأهلة تتدلى خارج الكارت */
        body::before {
            content: '🌕'; /* هلال */
            position: fixed;
            top: 50px;
            left: 10%;
            font-size: 40px;
            color: var(--accent-gold);
            opacity: 0.7;
            animation: floating 4s infinite ease-in-out;
            z-index: 0;
        }
        
        body::after {
            content: '🏮'; /* فانوس */
            position: fixed;
            top: 100px;
            right: 10%;
            font-size: 40px;
            color: var(--eid-gold);
            opacity: 0.7;
            animation: floating 4s infinite ease-in-out 2s;
            z-index: 0;
        }

        @keyframes floating {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(10deg); }
        }

        .main-card {
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            border-radius: 60px;
            box-shadow: 0 50px 100px var(--shadow-color);
            width: 100%;
            max-width: 550px;
            max-height: 90vh;
            overflow-y: auto;
            /* حدود ذهبية مضيئة */
            border: 4px solid var(--accent-gold);
            animation: epicEntrance 1.5s ease-out forwards, etherealGlow 3s infinite alternate;
            position: relative;
            z-index: 1;
            padding: 20px;
            margin-top: 20px;
        }

        /* تأثير لمعان يمر فوق الكارت */
        .main-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 50%;
            height: 100%;
            background: linear-gradient(to right, rgba(255,255,255,0) 0%, rgba(255,215,0,0.3) 50%, rgba(255,255,255,0) 100%);
            transform: skewX(-25deg);
            animation: shine 6s infinite;
            z-index: 2;
        }

        @keyframes shine {
            0% { left: -100%; }
            20% { left: 100%; }
            100% { left: 100%; }
        }

        @keyframes epicEntrance { 
            0% { opacity: 0; transform: scale(0.5) rotate(-180deg); } 
            100% { opacity: 1; transform: scale(1) rotate(0deg); } 
        }

        @keyframes etherealGlow { 
            0% { box-shadow: 0 0 30px rgba(255, 215, 0, 0.4); } 
            100% { box-shadow: 0 0 60px rgba(255, 215, 0, 0.8); } 
        }

        .header {
            padding: 60px 40px 40px;
            text-align: center;
            /* خلفية متدرجة ذهبية بيضاء مع نمط زخرفي إسلامي باهت */
            background: linear-gradient(to bottom, #fff9c4, #ffffff);
            background-image: url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgdmlld0JveD0iMCAwIDQwIDQwIj48ZyBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZGQ1NGYiIGZpbGwtb3BhY2l0eT0iMC4xNSI+PHBhdGggZD0iTTAgMGg0MHY0MEgwVjB6bTIwIDIwaDIwdjIwSDIWMjB6TTAgMjBoMjB2MjBIMFYyMHoyMCAwaDIwdjIwSDIwVjB6Ii8+PC9nPjwvZz48L3N2Zz4=');
            position: relative;
            overflow: hidden;
            border-bottom: 3px dashed var(--accent-gold);
        }

        /* تهنئة العيد المتحركة في الهيدر */
        .eid-greeting {
            font-size: 20px;
            color: var(--eid-purple);
            font-weight: bold;
            margin-bottom: 15px;
            display: block;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            animation: vibe 1s infinite alternate;
        }
        
        @keyframes vibe {
            0% { transform: translateY(0); }
            100% { transform: translateY(-5px); }
        }

        .logo-frame {
            width: 170px;
            height: 170px;
            background: linear-gradient(135deg, #ffffff, #fffde7);
            border-radius: 50%;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            /* ظل ذهبي للشعار */
            box-shadow: 0 20px 45px rgba(255, 215, 0, 0.4);
            border: 6px solid var(--accent-gold);
            transition: all 0.8s cubic-bezier(0.68, -0.55, 0.27, 1.55);
            position: relative;
            z-index: 3;
        }

        /* هالة نورانية خلف الشعار */
        .logo-frame::before {
            content: '';
            position: absolute;
            width: 120%;
            height: 120%;
            background: radial-gradient(circle, rgba(255,215,0,0.5) 0%, transparent 70%);
            border-radius: 50%;
            animation: pulseHolo 2s infinite;
            z-index: -1;
        }

        @keyframes pulseHolo {
            0% { transform: scale(1); opacity: 0.5; }
            50% { transform: scale(1.1); opacity: 1; }
            100% { transform: scale(1); opacity: 0.5; }
        }

.logo-frame img { 
    width: 80%;       /* تقليل العرض قليلاً ليظهر الشعار كاملاً */
    height: 80%;      /* تقليل الارتفاع لترك مساحة بيضاء "تنفس" للشعار */
    object-fit: contain; 
    animation: vibrantWiggle 2.5s infinite alternate ease-in-out; 
    border-radius: 0;  /* تأكد أن الصورة نفسها ليست مدورة إذا كانت شفافة */
}
        h1 { 
            color: var(--primary-green); 
            margin: 0; 
            font-size: 30px; 
            font-weight: 900; 
            text-shadow: 0 3px 6px var(--shadow-color); 
        }

        /* تمييز كلمة "الهيئة الطلابية" بلون العيد */
        .header h1:last-of-type {
            color: var(--eid-purple);
            font-size: 34px;
            background: linear-gradient(to right, var(--primary-green), var(--eid-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .uni-info { 
            color: var(--soil-brown); 
            font-size: 18px; 
            font-weight: 700; 
            margin-top: 10px; 
            opacity: 0.98; 
        }

        form { padding: 30px 60px 60px; }

        .form-item { 
            margin-bottom: 30px; 
            text-align: right; 
            position: relative; 
            transition: all 0.3s ease; 
        }

        .form-item:hover { transform: translateX(-5px); }

        label { 
            display: block; 
            margin-bottom: 12px; 
            color: var(--primary-green); 
            font-weight: 800; 
            font-size: 16px; 
            transition: color 0.3s; 
        }

        /* تغيير اللون عند التركيز للون الأرجواني للاحتفال */
        .form-item:focus-within label { color: var(--eid-purple); }

        input, select {
            width: 100%;
            padding: 20px 25px;
            border: 3px solid #c0d8c0;
            border-radius: 30px;
            font-family: 'Tajawal', sans-serif;
            font-size: 17px;
            transition: all 0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55);
            background: linear-gradient(to bottom, #fff, #f9fdf9);
            box-sizing: border-box;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.05);
        }

        input:focus, select:focus {
            border-color: var(--accent-gold);
            outline: none;
            /* ظل ذهبي عند التركيز */
            box-shadow: 0 12px 30px rgba(255, 215, 0, 0.3);
            transform: scale(1.03) translateX(-15px);
            background: #fff;
        }

        .form-item::before {
            content: attr(data-emoji);
            position: absolute;
            right: 25px;
            top: 50%;
            transform: translateY(-50%);
            opacity: 0.5;
            transition: all 0.4s;
            font-size: 24px;
            z-index: 2; /* تأكد من ظهورها فوق الخلفية */
        }

        .form-item:focus-within::before {
            opacity: 1;
            transform: translateY(-50%) scale(1.2) rotate(360deg);
        }

        button {
            width: 100%;
            padding: 22px;
            /* خلفية متدرجة فخمة تدمج الذهب والأرجواني والأخضر */
            background: linear-gradient(135deg, var(--eid-purple), var(--primary-green), var(--accent-gold), var(--eid-gold));
            background-size: 300% 300%;
            color: white;
            border: none;
            border-radius: 30px;
            font-size: 22px;
            font-weight: 900;
            cursor: pointer;
            transition: all 0.6s ease;
            margin-top: 25px;
            box-shadow: 0 20px 40px rgba(74, 20, 140, 0.3);
            position: relative;
            overflow: hidden;
            z-index: 1;
            animation: gradientBG 5s infinite;
        }
        
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -120%;
            width: 120%;
            height: 100%;
            background: rgba(255,255,255,0.4);
            transition: left 0.6s;
            z-index: -1;
        }

        button:hover::before { left: 0; }

        button:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 30px 50px rgba(255, 215, 0, 0.5);
            filter: brightness(1.1);
        }

        .footer {
            text-align: center;
            padding: 35px;
            font-size: 13px;
            color: #555;
            background: linear-gradient(to top, #fffde7, #fcfdfc);
            border-top: 2px solid var(--accent-gold);
            position: relative;
        }

        /* تحديث إيموجي الفوتر لتكون احتفالية */
        .footer::before {
            content: '🌙 🌸 🍬 ☕';
            display: block;
            margin-bottom: 15px;
            font-size: 24px;
            animation: natureDance 4s infinite;
        }

        @keyframes natureDance { 
            0% { transform: translateY(0) rotate(0deg); opacity: 0.8; } 
            50% { transform: translateY(-10px) rotate(10deg); opacity: 1; } 
            100% { transform: translateY(0) rotate(-10deg); opacity: 0.8; } 
        }

        /* Responsive adjustments */
        @media (max-width: 600px) {
            body { padding: 10px; align-items: flex-start; }
            .main-card { max-width: 100%; border-radius: 40px; padding: 10px; max-height: none; overflow: visible; border-width: 3px;}
            form { padding: 20px 20px 40px; }
            .header { padding: 40px 20px 20px; }
            .logo-frame { width: 130px; height: 130px; border-width: 4px;}
            h1 { font-size: 24px; }
            .header h1:last-of-type { font-size: 28px; }
            .uni-info { font-size: 14px; }
            .eid-greeting { font-size: 16px; }
            input, select { padding: 15px 18px; font-size: 15px; }
            .form-item::before { font-size: 20px; right: 15px; }
            button { padding: 18px; font-size: 18px; }
            .footer { padding: 25px; font-size: 11px; }
        }
    </style>
</head>
<body>
    <div id="particles-js"></div>
    <div class="main-card">
        <div class="header">
            <span class="eid-greeting">🌟 عيدكم مبارك وكل عام وأنتم بخير 🌟</span>
            <div class="logo-frame">
                <img src="/static/0145.png" alt="الهيئة الطلابية">
            </div>
            <h1>اتحاد الطلبة</h1>
            <h1>الهيئة الطلابية</h1>
            <div class="uni-info">جامعة حمص | كلية الهندسة الزراعية</div>
        </div>

        <form id="registration-form" action="/register" method="POST">
            <div class="form-item" data-emoji="🎁">
                <label>الاسم الثلاثي</label>
                <input type="text" name="name" placeholder="أدخل اسمك الكامل" required>
            </div>

            <div class="form-item" data-emoji="🆔">
                <label>الرقم الجامعي</label>
                <input type="text" name="u_id" placeholder="أدخل رقمك الجامعي" required pattern="[0-9]+" title="الرقم الجامعي يجب أن يحتوي على أرقام فقط">
            </div>

            <div class="form-item" data-emoji="📞">
                <label>رقم الواتساب</label>
                <input type="tel" name="whatsapp" placeholder="09xxxxxxxx" required pattern="09[0-9]{8}" title="رقم الواتساب يجب أن يبدأ بـ 09 ويحتوي على 10 أرقام">
            </div>

            <div class="form-item" data-emoji="🏫">
                <label>السنة الدراسية</label>
                <select name="year" required>
                    <option value="" disabled selected>اختر سنتك الدراسية</option>
                    <option>السنة الأولى</option>
                    <option>السنة الثانية</option>
                    <option>السنة الثالثة</option>
                    <option>السنة الرابعة</option>
                    <option>السنة الخامسة</option>
                </select>
            </div>

            <button type="submit">تسجيل وانضمام للمجتمع ✨</button>
        </form>
        <div class="footer">بوابة مكتب التنظيم الرقمي - الهيئة الطلابية © 2026<br>تقبل الله طاعاتكم</div>
    </div>

    <script>
        // --- الحفاظ على كافة تفاعلات JS الأصلية مع تعديلات بصرية بسيطة ---

        // تهيئة Particles.js: تغيير الأشكال لنجوم وأهلة لجو العيد
        particlesJS('particles-js', {
            particles: {
                number: { value: 120, density: { enable: true, value_area: 1000 } },
                // ألوان الجسيمات: ذهبي، أبيض، أخضر، أرجواني
                color: { value: ['#ffd700', '#ffffff', '#4caf50', '#ea80fc'] },
                // تغيير الشكل إلى نجوم (star) بشكل أساسي
                shape: { type: ['star', 'circle'], stroke: { width: 0, color: '#000000' } },
                opacity: { value: 0.7, random: true, anim: { enable: true, speed: 1, opacity_min: 0.1 } },
                size: { value: 5, random: true, anim: { enable: true, speed: 2, size_min: 0.1 } },
                line_linked: { enable: true, distance: 150, color: '#ffd700', opacity: 0.4, width: 1 },
                move: { enable: true, speed: 3, direction: 'none', random: true, straight: false, out_mode: 'out', bounce: false, attract: { enable: false, rotateX: 600, rotateY: 1200 } }
            },
            interactivity: {
                detect_on: 'canvas',
                events: { onhover: { enable: true, mode: 'grab' }, onclick: { enable: true, mode: 'push' }, resize: true },
                modes: { grab: { distance: 200, line_linked: { opacity: 0.8 } }, bubble: { distance: 400, size: 40, duration: 2, opacity: 8, speed: 3 }, repulse: { distance: 200, duration: 0.4 }, push: { particles_nb: 4 }, remove: { particles_nb: 2 } }
            },
            retina_detect: true
        });

        const form = document.getElementById('registration-form');
        form.addEventListener('submit', (event) => {
            if (!form.checkValidity()) {
                event.preventDefault();
                alert('يرجى التحقق من صحة البيانات المدخلة!');
                return;
            }
            // إضافة تأثير confetti عند الإرسال الناجح: تحديث الألوان لتركيبة العيد
            const confettiSettings = { target: document.body, max: 250, size: 1.8, animate: true, props: ['circle', 'square', 'triangle', 'star'], colors: [[255,215,0], [74,14,140], [27,94,32], [255,255,255]], clock: 40 };
            const confetti = new ConfettiGenerator(confettiSettings);
            confetti.render();
            // تمديد الوقت قليلاً للاحتفال
            setTimeout(() => confetti.clear(), 6000);
        });

        // تغيير لون الخلفية ديناميكياً: الحفاظ على الميزة مع ألوان ليلية أعمق
        const hour = new Date().getHours();
        if (hour >= 18 || hour < 6) {
            document.body.style.background = 'linear-gradient(135deg, #050b2e, #1b5e20, #2e0b57)';
        }

        // الصوت الخلفي: الحفاظ عليه كما هو
        const welcomeVoice = new Audio('/static/sounds/welcome-female.mp3');
        welcomeVoice.volume = 0.9;

        document.body.addEventListener('click', () => {
            welcomeVoice.play().catch(err => console.log("Autoplay issue:", err));
        }, { once: true });

        const button = document.querySelector('button');
        button.addEventListener('mouseover', () => {
            button.style.animation = 'buttonShake 0.5s infinite, gradientBG 1s infinite'; // دمج الأنماط
        });
        button.addEventListener('mouseout', () => {
            button.style.animation = 'gradientBG 5s infinite'; // العودة للنمط الافتراضي
        });

        const formItems = document.querySelectorAll('.form-item');
        formItems.forEach((item, index) => {
            item.style.opacity = 0;
            item.style.transform = 'translateY(20px)';
            setTimeout(() => {
                item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                item.style.opacity = 1;
                item.style.transform = 'translateY(0)';
            }, index * 200);
        });

        // نمط الهز للأزرار (الحفاظ عليه كما هو)
        const style = document.createElement('style');
        style.innerHTML = `
            @keyframes buttonShake {
                0% { transform: translate(1px, 1px) rotate(0deg); }
                10% { transform: translate(-1px, -2px) rotate(-1deg); }
                20% { transform: translate(-3px, 0px) rotate(1deg); }
                30% { transform: translate(3px, 2px) rotate(0deg); }
                40% { transform: translate(1px, -1px) rotate(1deg); }
                50% { transform: translate(-1px, 2px) rotate(-1deg); }
                60% { transform: translate(-3px, 1px) rotate(0deg); }
                70% { transform: translate(3px, 1px) rotate(-1deg); }
                80% { transform: translate(-1px, -1px) rotate(1deg); }
                90% { transform: translate(1px, 2px) rotate(0deg); }
                100% { transform: translate(1px, -2px) rotate(-1deg); }
            }
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
"""
# --- إعدادات FastAPI مع تحسينات للأداء ---

from fastapi.staticfiles import StaticFiles

# جبل مجلد static للصور والملفات الثابتة
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    return HTML_TEMPLATE

@app.post("/register")
async def register_student(
    name: str = Form(...),
    u_id: str = Form(...),
    whatsapp: str = Form(...),
    year: str = Form(...)
):
    try:
        db = get_db_client()
        student_data = {
            "full_name": name.strip(),
            "university_id": u_id.strip(),
            "whatsapp_number": whatsapp.strip(),
            "study_year": year
        }
        
        # حفظ البيانات في Supabase مع التحقق من عدم التكرار (افتراضياً)
        db.table("students").insert(student_data).execute()
        
        # التوجيه لمجموعة الواتساب المناسبة
        redirect_link = COMMUNITY_GROUPS.get(year, "https://chat.whatsapp.com/General")
        return RedirectResponse(url=redirect_link, status_code=303)
        
    except Exception as e:
        print(f"DEBUG DB ERROR: {str(e)}")
        raise HTTPException(status_code=400, detail="فشل في عملية التسجيل. يرجى المحاولة لاحقاً.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, workers=2)