import os
import uvicorn
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from database import get_db_client

app = FastAPI(title="Agri-Union Homs")

# روابط مجتمعات الواتساب (يرجى وضع الروابط الحقيقية هنا)
COMMUNITY_GROUPS = {
    "السنة الأولى": "https://chat.whatsapp.com/KYFfLhFPC3X19ZHC3VlzL0?mode=gi_t",
    "السنة الثانية": "https://chat.whatsapp.com/KAzCQpPvuTP4FY39Ob5flU?mode=gi_t",
    "السنة الثالثة": "https://chat.whatsapp.com/CfqLCkejcHREknO59FT04S?mode=gi_t",
    "السنة الرابعة": "https://chat.whatsapp.com/HS57aU9zE2ULGwax3zKIEG?mode=gi_t",
    "السنة الخامسة": "https://chat.whatsapp.com/DrihEQImyX4Bzgv36Skggb?mode=gi_t",
}

# --- واجهة المستخدم (HTML + CSS + JS) محسنة، خالية من الأخطاء، مع تصميم رهيب وتفاعلات خرافية، ويتناسب مع الشاشة ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>بوابة التسجيل | جامعة حمص</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/confetti-js@0.1.0/dist/confetti.min.js"></script>
    <style>
        :root {
            --primary-green: #1b5e20;
            --leaf-green: #4caf50;
            --soil-brown: #5d4037;
            --soft-white: #f9fdf9;
            --sun-yellow: #ffd54f;
            --sky-blue: #81d4fa;
            --accent-gold: #f9a825;
            --shadow-color: rgba(0,0,0,0.2);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Tajawal', sans-serif;
            background: linear-gradient(135deg, var(--sky-blue), var(--leaf-green), var(--primary-green));
            background-attachment: fixed;
            display: flex;
            justify-content: center;
            align-items: flex-start; /* تغيير إلى flex-start لمنع الخروج من أعلى الشاشة */
            min-height: 100vh;
            overflow: auto; /* السماح بالتمرير إذا لزم الأمر */
            position: relative;
            padding: 20px 10px; /* زيادة padding للشاشات الصغيرة */
        }

        #particles-js {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: -1;
        }

        .main-card {
            background: rgba(255, 255, 255, 0.97);
            backdrop-filter: blur(20px);
            border-radius: 60px;
            box-shadow: 0 50px 100px var(--shadow-color);
            width: 100%;
            max-width: 550px;
            max-height: 90vh; /* حد أقصى للارتفاع ليتناسب مع الشاشة */
            overflow-y: auto; /* السماح بالتمرير داخل البطاقة إذا تجاوز الارتفاع */
            border: 3px solid rgba(255,255,255,0.8);
            animation: epicEntrance 1.5s ease-out forwards, etherealGlow 3s infinite alternate;
            position: relative;
            z-index: 1;
            padding: 20px;
            margin-top: 20px; /* هامش علوي لمنع الالتصاق بالأعلى */
        }

        @keyframes epicEntrance { 
            0% { opacity: 0; transform: scale(0.5) rotate(-180deg); } 
            100% { opacity: 1; transform: scale(1) rotate(0deg); } 
        }

        @keyframes etherealGlow { 
            0% { box-shadow: 0 0 30px rgba(76, 175, 80, 0.4); } 
            100% { box-shadow: 0 0 60px rgba(76, 175, 80, 0.8); } 
        }

        .header {
            padding: 60px 40px 40px;
            text-align: center;
            background: linear-gradient(to bottom, #c5e1a5, #ffffff);
            position: relative;
            overflow: hidden;
            border-bottom: 2px dashed var(--leaf-green);
        }

        .header::before {
            content: '';
            position: absolute;
            top: -60%;
            left: -60%;
            width: 220%;
            height: 220%;
            background: radial-gradient(circle, rgba(255,213,79,0.4) 0%, transparent 80%);
            animation: radiantSun 8s infinite linear;
        }

        @keyframes radiantSun { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        .logo-frame {
            width: 170px;
            height: 170px;
            background: linear-gradient(135deg, #ffffff, #e8f5e9);
            border-radius: 50%;
            margin: 0 auto 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 20px 45px rgba(27, 94, 32, 0.25);
            border: 6px solid var(--primary-green);
            transition: all 0.8s cubic-bezier(0.68, -0.55, 0.27, 1.55);
            position: relative;
        }

        .logo-frame:hover {
            transform: rotate(720deg) scale(1.15);
            box-shadow: 0 30px 60px rgba(27, 94, 32, 0.5);
            border-color: var(--accent-gold);
        }

        .logo-frame::after {
            content: '';
            position: absolute;
            top: -15px;
            left: -15px;
            width: calc(100% + 30px);
            height: calc(100% + 30px);
            border-radius: 50%;
            border: 4px dotted var(--sun-yellow);
            animation: orbitDash 12s infinite linear;
        }

        @keyframes orbitDash { 0% { transform: rotate(0deg); } 100% { transform: rotate(-360deg); } }

        .logo-frame img { 
            width: 95%; 
            height: 95%; 
            object-fit: contain; 
            animation: vibrantWiggle 2.5s infinite alternate ease-in-out; 
        }

        @keyframes vibrantWiggle { 
            0% { transform: rotate(-8deg) scale(1); } 
            100% { transform: rotate(8deg) scale(1.05); } 
        }

        h1 { 
            color: var(--primary-green); 
            margin: 0; 
            font-size: 34px; 
            font-weight: 900; 
            text-shadow: 0 3px 6px var(--shadow-color); 
            animation: titlePulse 2s infinite alternate; 
        }

        @keyframes titlePulse { 
            0% { transform: scale(1); } 
            100% { transform: scale(1.05); } 
        }

        .uni-info { 
            color: var(--soil-brown); 
            font-size: 18px; 
            font-weight: 700; 
            margin-top: 10px; 
            opacity: 0.98; 
            animation: infoShimmer 2s infinite alternate; 
        }

        @keyframes infoShimmer { 
            0% { text-shadow: 0 0 8px var(--sun-yellow); } 
            100% { text-shadow: 0 0 15px var(--sun-yellow); } 
        }

        form { padding: 0 60px 60px; }

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

        .form-item:focus-within label { color: var(--accent-gold); }

        input, select {
            width: 100%;
            padding: 20px 25px;
            border: 3px solid #c0d8c0;
            border-radius: 30px;
            font-family: 'Tajawal', sans-serif;
            font-size: 17px;
            transition: all 0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55);
            background: linear-gradient(to bottom, #fff, #f0f8f0);
            box-sizing: border-box;
            box-shadow: inset 0 2px 5px var(--shadow-color);
        }

        input:focus, select:focus {
            border-color: var(--leaf-green);
            outline: none;
            box-shadow: 0 12px 30px rgba(76, 175, 80, 0.25);
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
        }

        .form-item:focus-within::before {
            opacity: 1;
            transform: translateY(-50%) scale(1.2) rotate(360deg);
        }

        button {
            width: 100%;
            padding: 22px;
            background: linear-gradient(135deg, var(--primary-green), var(--leaf-green), var(--sun-yellow), var(--accent-gold));
            color: white;
            border: none;
            border-radius: 30px;
            font-size: 22px;
            font-weight: 900;
            cursor: pointer;
            transition: all 0.6s ease;
            margin-top: 25px;
            box-shadow: 0 20px 40px rgba(27, 94, 32, 0.3);
            position: relative;
            overflow: hidden;
            z-index: 1;
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
            transform: translateY(-8px) rotate(5deg);
            box-shadow: 0 30px 50px rgba(27, 94, 32, 0.5);
            filter: brightness(1.3);
        }

        .footer {
            text-align: center;
            padding: 35px;
            font-size: 13px;
            color: #666;
            background: linear-gradient(to top, #f0f8f0, #fcfdfc);
            border-top: 2px solid #d8e8d8;
            position: relative;
        }

        .footer::before {
            content: '🌿 🌱 🍀';
            display: block;
            margin-bottom: 15px;
            font-size: 22px;
            animation: natureDance 4s infinite;
        }

        @keyframes natureDance { 
            0% { transform: translateY(0) rotate(0deg); opacity: 0.8; } 
            50% { transform: translateY(-15px) rotate(180deg); opacity: 1; } 
            100% { transform: translateY(0) rotate(360deg); opacity: 0.8; } 
        }

        /* Responsive adjustments */
        @media (max-width: 600px) {
            body { padding: 10px; align-items: flex-start; }
            .main-card { max-width: 100%; border-radius: 40px; padding: 15px; max-height: none; /* إزالة الحد للشاشات الصغيرة */ overflow: visible; }
            form { padding: 0 30px 40px; }
            .header { padding: 40px 20px 20px; }
            .logo-frame { width: 140px; height: 140px; }
            h1 { font-size: 28px; }
            .uni-info { font-size: 15px; }
            input, select { padding: 15px 20px; font-size: 15px; }
            button { padding: 18px; font-size: 18px; }
            .footer { padding: 25px; font-size: 11px; }
        }
    </style>
</head>
<body>
    <div id="particles-js"></div>
    <div class="main-card">
        <div class="header">
            <div class="logo-frame">
                <img src="/static/0145.png" alt="الهيئة الطلابية">
            </div>
            <h1>اتحاد الطلبة</h1>

            <h1>الهيئة الطلابية</h1>
            <div class="uni-info">جامعة حمص | كلية الهندسة الزراعية</div>
        </div>

        <form id="registration-form" action="/register" method="POST">
            <div class="form-item" data-emoji="✍️">
                <label>الاسم الثلاثي</label>
                <input type="text" name="name" placeholder="أدخل اسمك الكامل" required>
            </div>

            <div class="form-item" data-emoji="🎓">
                <label>الرقم الجامعي</label>
                <input type="text" name="u_id" placeholder="أدخل رقمك الجامعي" required pattern="[0-9]+" title="الرقم الجامعي يجب أن يحتوي على أرقام فقط">
            </div>

            <div class="form-item" data-emoji="📱">
                <label>رقم الواتساب</label>
                <input type="tel" name="whatsapp" placeholder="09xxxxxxxx" required pattern="09[0-9]{8}" title="رقم الواتساب يجب أن يبدأ بـ 09 ويحتوي على 10 أرقام">
            </div>

            <div class="form-item" data-emoji="📅">
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

            <button type="submit">تسجيل وانضمام للمجتمع</button>
        </form>
        <div class="footer">بوابة مكتب التنظيم الرقمي - الهيئة الطلابية © 2026</div>
    </div>

    <script>
        // تهيئة Particles.js لخلفية ديناميكية تعبر عن الحيوية الزراعية
        particlesJS('particles-js', {
            particles: {
                number: { value: 100, density: { enable: true, value_area: 1000 } },
                color: { value: ['#4caf50', '#1b5e20', '#ffd54f', '#f9a825'] },
                shape: { type: ['circle', 'triangle', 'polygon'], stroke: { width: 0, color: '#000000' }, polygon: { nb_sides: 5 } },
                opacity: { value: 0.6, random: true, anim: { enable: true, speed: 1, opacity_min: 0.1 } },
                size: { value: 6, random: true, anim: { enable: true, speed: 2, size_min: 0.1 } },
                line_linked: { enable: true, distance: 180, color: '#81d4fa', opacity: 0.5, width: 1.5 },
                move: { enable: true, speed: 4, direction: 'none', random: true, straight: false, out_mode: 'bounce', bounce: true, attract: { enable: true, rotateX: 600, rotateY: 1200 } }
            },
            interactivity: {
                detect_on: 'window',
                events: { onhover: { enable: true, mode: 'grab' }, onclick: { enable: true, mode: 'push' }, resize: true },
                modes: { grab: { distance: 200, line_linked: { opacity: 0.8 } }, bubble: { distance: 300, size: 50, duration: 2, opacity: 0.8 }, repulse: { distance: 250, duration: 0.5 }, push: { particles_nb: 6 }, remove: { particles_nb: 3 } }
            },
            retina_detect: true
        });

        // تفاعل جديد: تحقق من صحة الإدخال قبل الإرسال باستخدام JS
        const form = document.getElementById('registration-form');
        form.addEventListener('submit', (event) => {
            if (!form.checkValidity()) {
                event.preventDefault();
                alert('يرجى التحقق من صحة البيانات المدخلة!');
                return;
            }
            // إضافة تأثير confetti عند الإرسال الناجح
            const confettiSettings = { target: document.body, max: 200, size: 1.5, animate: true, props: ['circle', 'square', 'triangle'], colors: [[27,94,32], [76,175,80], [255,213,79]], clock: 35 };
            const confetti = new ConfettiGenerator(confettiSettings);
            confetti.render();
            setTimeout(() => confetti.clear(), 5000);
        });

        // تفاعل جديد: تغيير لون الخلفية ديناميكياً بناءً على الوقت (نهار/ليل)
        const hour = new Date().getHours();
        if (hour >= 18 || hour < 6) {
            document.body.style.background = 'linear-gradient(135deg, #0d47a1, #1b5e20, #004d40)';
        }

        // تفاعل جديد: صوت خلفي خفيف (مثل صوت الرياح في الحقول) - يتطلب موافقة المستخدم
        // ملاحظة: استبدل الرابط بصوت حقيقي إذا لزم، لكن هنا نتركه كمثال
    const welcomeVoice = new Audio('/static/sounds/welcome-female.mp3');
welcomeVoice.volume = 0.9;  // صوت واضح للترحيب

// شغّل مرة واحدة عند فتح الصفحة (بعد تفاعل المستخدم)
document.body.addEventListener('click', () => {
    welcomeVoice.play().catch(err => console.log("Autoplay issue:", err));
}, { once: true });  // مرة واحدة فقط

        // تفاعل جديد: هز الزر عند التحريك فوق الزر
        const button = document.querySelector('button');
        button.addEventListener('mouseover', () => {
            button.style.animation = 'buttonShake 0.5s infinite';
        });
        button.addEventListener('mouseout', () => {
            button.style.animation = '';
        });

        // تفاعل جديد: تأثير تدريجي لظهور الحقول عند التحميل
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