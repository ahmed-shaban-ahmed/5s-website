# فايف إس — موقع الشركة

موقع ثابت (HTML / CSS / JS) لشركة فايف إس لحلول تثبيت الرمال والتربة — عربي RTL، خط Readex Pro، مبني وفق دليل تطوير الموقع المقدَّم من العميل (نوفمبر 2026).

## الرابط المباشر

https://ahmed-shaban-ahmed.github.io/5s-website/

## الصفحات

| الصفحة | الرابط |
|--------|--------|
| الرئيسية | [/](https://ahmed-shaban-ahmed.github.io/5s-website/) |
| من نحن | [/about/](https://ahmed-shaban-ahmed.github.io/5s-website/about/) |
| تقنية 5S (الحلول) | [/solutions/](https://ahmed-shaban-ahmed.github.io/5s-website/solutions/) |
| 5S BERM | [/solutions/5s-berm/](https://ahmed-shaban-ahmed.github.io/5s-website/solutions/5s-berm/) |
| 5S ROAD | [/solutions/5s-road/](https://ahmed-shaban-ahmed.github.io/5s-website/solutions/5s-road/) |
| 5S SLOPE | [/solutions/5s-slope/](https://ahmed-shaban-ahmed.github.io/5s-website/solutions/5s-slope/) |
| 5S DUST | [/solutions/5s-dust/](https://ahmed-shaban-ahmed.github.io/5s-website/solutions/5s-dust/) |
| 5S WALK | [/solutions/5s-walk/](https://ahmed-shaban-ahmed.github.io/5s-website/solutions/5s-walk/) |
| القطاعات (9 صفحات) | [/sectors/](https://ahmed-shaban-ahmed.github.io/5s-website/sectors/) |
| المشاريع | [/projects/](https://ahmed-shaban-ahmed.github.io/5s-website/projects/) |
| البيانات الفنية | [/technical-data/](https://ahmed-shaban-ahmed.github.io/5s-website/technical-data/) |
| الشركاء والوكلاء | [/partners/](https://ahmed-shaban-ahmed.github.io/5s-website/partners/) |
| حاسبة المواد | [/calculator/](https://ahmed-shaban-ahmed.github.io/5s-website/calculator/) |
| تواصل معنا | [/contact/](https://ahmed-shaban-ahmed.github.io/5s-website/contact/) |

الروابط القديمة (`about.html`، `solutions.html`، …) تُحوِّل تلقائيًا إلى الروابط الجديدة.

## المحتوى والبيانات المؤقتة

النصوص من دليل العميل والموقع الرسمي [5s-tech.org](https://www.5s-tech.org/). كل بيانات تحتاج اعتماد العميل (الشعارات، الأرقام غير الموثقة، الشهادات، ملفات TDS/SDS، معاملات الحاسبة، بيانات الوكلاء…) معلَّمة في الصفحات بشارة صفراء «⚑ بانتظار…».

## التعديل

الصفحات تُولَّد من `_build/build.py` (القوالب) و`_build/data.py` (المحتوى). بعد أي تعديل:

```bash
python3 _build/build.py
```

معاملات حاسبة المواد في `js/main.js` داخل الثابت `CALC_COEFFICIENTS` ويجب أن يزودها الفريق الفني.

## النشر

GitHub Pages من فرع `main` (المجلد الجذر).
