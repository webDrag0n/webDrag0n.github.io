/* AI Daily — access panel language toggle + copy buttons */
(function () {
    var LANG_KEY = 'ad-lang';

    function applyLang(lang) {
        var showZh = lang === 'zh';
        document.querySelectorAll('.lang-zh').forEach(function (el) { el.hidden = !showZh; });
        document.querySelectorAll('.lang-en').forEach(function (el) { el.hidden = showZh; });
    }

    function getLang() {
        try { return localStorage.getItem(LANG_KEY) || 'zh'; } catch (e) { return 'zh'; }
    }

    // restore saved preference, default to Chinese
    applyLang(getLang() === 'en' ? 'en' : 'zh');

    // follow the site-wide EN | 中 toggle (dispatched from js/main.js)
    window.addEventListener('langchange', function (e) {
        var lang = (e.detail && e.detail.lang) || 'zh';
        try { localStorage.setItem(LANG_KEY, lang); } catch (err) {}
        applyLang(lang);
    });

    // copy buttons
    document.querySelectorAll('.ad-copy').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var zh = btn.getAttribute('data-copy-zh');
            var en = btn.getAttribute('data-copy-en');
            var fixed = btn.getAttribute('data-copy');
            var lang = getLang();
            var text = fixed || (lang === 'en' ? (en || zh) : (zh || en)) || '';

            function done() {
                var orig = btn.innerHTML;
                btn.textContent = (lang === 'en') ? 'Copied ✓' : '已复制 ✓';
                setTimeout(function () { btn.innerHTML = orig; }, 1500);
            }
            function fallback() {
                var ta = document.createElement('textarea');
                ta.value = text;
                ta.style.position = 'fixed';
                ta.style.opacity = '0';
                document.body.appendChild(ta);
                ta.select();
                try { document.execCommand('copy'); done(); } catch (e) {}
                document.body.removeChild(ta);
            }
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).then(done).catch(fallback);
            } else {
                fallback();
            }
        });
    });
})();
