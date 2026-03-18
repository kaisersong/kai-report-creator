# HTML Shell Template

When generating the final HTML report, produce a complete self-contained HTML file using this structure. Replace all `[...]` placeholders with actual content.

    <!DOCTYPE html>
    <html lang="[lang]">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>[title]</title>

      <!-- CDN libraries (add only what's needed; omit if --bundle, inline instead) -->
      <!-- If any :::chart blocks present AND using Chart.js: -->
      <!-- <script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script> -->
      <!-- If any :::chart blocks present AND using ECharts: -->
      <!-- <script src="https://cdn.jsdelivr.net/npm/echarts@5/dist/echarts.min.js"></script> -->
      <!-- If any :::code blocks present: -->
      <!-- <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/highlight.js@11/styles/github.min.css"> -->
      <!-- (use github-dark.min.css for dark-tech theme) -->
      <!-- <script src="https://cdn.jsdelivr.net/npm/highlight.js@11/lib/highlight.min.js"></script> -->
      <!-- <script>document.addEventListener('DOMContentLoaded', () => hljs.highlightAll());</script> -->

      <style>
        /* [Paste the selected theme CSS here, e.g., the corporate-blue block] */

        /* [Paste the shared component CSS here] */

        /* Floating TOC overlay — default collapsed on all screen sizes */
        .toc-sidebar {
          position: fixed; top: 0; left: 0; width: 240px; height: 100vh;
          overflow-y: auto; padding: 3rem 1rem 1.5rem; background: var(--surface);
          border-right: 1px solid var(--border); font-size: .83rem; z-index: 100;
          transform: translateX(-100%); transition: transform .28s ease;
        }
        .toc-sidebar.open {
          transform: translateX(0); box-shadow: 4px 0 24px rgba(0,0,0,.18);
        }
        .toc-sidebar h4 {
          font-size: .72rem; text-transform: uppercase; letter-spacing: .08em;
          color: var(--text-muted); margin: 0 0 .75rem; font-weight: 600;
        }
        .toc-sidebar a {
          display: block; color: var(--text-muted); text-decoration: none;
          padding: .28rem .5rem; border-radius: 4px; margin-bottom: 1px; transition: all .18s;
          white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
        }
        .toc-sidebar a:hover, .toc-sidebar a.active { color: var(--primary); background: var(--primary-light); }
        .toc-sidebar a.toc-h3 { padding-left: 1.1rem; font-size: .78rem; opacity: .85; }
        .main-with-toc { margin-left: 0; }
        .toc-toggle {
          position: fixed; top: .75rem; left: .75rem; z-index: 200;
          background: var(--primary); color: #fff; border: none; border-radius: 6px;
          padding: .45rem .7rem; cursor: pointer; font-size: 1rem; line-height: 1;
          box-shadow: 0 2px 8px rgba(0,0,0,.2);
        }
        .toc-toggle.locked { box-shadow: 0 0 0 2px #fff, 0 2px 8px rgba(0,0,0,.2); }
        @media (max-width: 768px) {
          .report-wrapper { padding: 1.5rem 1rem; }
        }
        body.no-toc .toc-sidebar, body.no-toc .toc-toggle { display: none; }
        body.no-toc .main-with-toc { margin-left: 0; }
      </style>
    </head>
    <body class="[add 'no-toc' if toc:false] [add 'no-animations' if animations:false]">

      <!-- AI Readability Layer 1: Report Summary JSON -->
      <!-- Always present, even if not visible to humans -->
      <script type="application/json" id="report-summary">
      {
        "title": "[title]",
        "author": "[author or empty string]",
        "date": "[date]",
        "abstract": "[abstract from frontmatter, or auto-generate a 1-sentence summary of the report content]",
        "sections": ["[heading of section 1]", "[heading of section 2]", "..."],
        "kpis": [
          {"label": "[label]", "value": "[display value]", "trend": "[trend text or empty]"}
        ]
      }
      </script>

      <!-- Edit mode (always present) -->
      <div class="edit-hotzone" id="edit-hotzone"></div>
      <button class="edit-toggle" id="edit-toggle" title="Edit mode (E)">✏ Edit</button>

      <!-- Export (always present) -->
      <!-- lang:en labels: "↓ Export" / "🖨 Print / PDF" / "🖥 Save PNG (Desktop)" / "📱 Save PNG (Mobile)" / "💬 IM Image" -->
      <!-- lang:zh labels: "↓ 导出"  / "🖨 打印 / PDF"  / "🖥 保存图片（桌面）"    / "📱 保存图片（手机）"  / "💬 IM 分享长图"   -->
      <div class="export-menu" id="export-menu">
        <button class="export-item" onclick="window.print()">[🖨 Print / PDF|🖨 打印 / PDF]</button>
        <button class="export-item" id="export-png-desktop">[🖥 Save PNG (Desktop)|🖥 保存图片（桌面）]</button>
        <button class="export-item" id="export-png-mobile">[📱 Save PNG (Mobile)|📱 保存图片（手机）]</button>
        <button class="export-item" id="export-im-share">[💬 IM Image|💬 IM 长图]</button>
      </div>
      <button class="export-btn" id="export-btn" title="Export">[↓ Export|↓ 导出]</button>

      <!-- Floating TOC (omit entirely if toc:false) -->
      <!-- TOC label localization: lang:en → aria-label="Contents" / "Table of Contents" / <h4>Contents</h4> -->
      <!--                         lang:zh → aria-label="目录" / "报告目录" / <h4>目录</h4> -->
      <button class="toc-toggle" id="toc-toggle-btn" aria-label="[Contents|目录]" aria-expanded="false">☰</button>
      <nav class="toc-sidebar" id="toc-sidebar" aria-label="[Table of Contents|报告目录]">
        <h4>[Contents|目录]</h4>
        <!-- Generate one <a> per ## heading and one per ### heading in the report -->
        <!-- Example (lang:en): <a href="#section-core-metrics" data-section="Core Metrics">Core Metrics</a> -->
        <!-- For ### heading: add class="toc-h3" -->
        [TOC links generated from all ## and ### headings in the IR]
      </nav>

      <div class="main-with-toc">
        <div class="report-wrapper">

          <!-- Report title and meta -->
          <h1>[title]</h1>
          [if author or date: <p class="report-meta">[author] · [date]</p>]

          <!-- AI Readability Layer 2: Section annotations are on each <section> element -->
          <!-- Rendered sections — each ## becomes: -->
          <!-- <section data-section="[heading]" data-summary="[1-sentence summary]"> -->
          <!--   <h2 id="section-[slug]">[heading]</h2> -->
          <!--   [section content] -->
          <!-- </section> -->

          [All rendered section content here]

        </div>
      </div>

      <script>
        // Scroll-triggered fade-in animations
        if (!document.body.classList.contains('no-animations')) {
          const fadeObserver = new IntersectionObserver(
            entries => entries.forEach(e => {
              if (e.isIntersecting) { e.target.classList.add('visible'); fadeObserver.unobserve(e.target); }
            }),
            { threshold: 0.08 }
          );
          document.querySelectorAll('.fade-in-up').forEach(el => fadeObserver.observe(el));

          // KPI counter animation
          const kpiObserver = new IntersectionObserver(entries => {
            entries.forEach(e => {
              if (!e.isIntersecting) return;
              const el = e.target;
              const target = parseFloat(el.dataset.targetValue);
              if (isNaN(target)) return;
              const prefix = el.dataset.prefix || '';
              const suffix = el.dataset.suffix || '';
              const isFloat = String(target).includes('.');
              const decimals = isFloat ? String(target).split('.')[1].length : 0;
              let startTime = null;
              const duration = 1200;
              const animate = ts => {
                if (!startTime) startTime = ts;
                const progress = Math.min((ts - startTime) / duration, 1);
                const ease = 1 - Math.pow(1 - progress, 3);
                const current = isFloat
                  ? (ease * target).toFixed(decimals)
                  : Math.floor(ease * target).toLocaleString();
                el.textContent = prefix + current + suffix;
                if (progress < 1) requestAnimationFrame(animate);
                else el.textContent = prefix + (isFloat ? target.toFixed(decimals) : target.toLocaleString()) + suffix;
              };
              requestAnimationFrame(animate);
              kpiObserver.unobserve(el);
            });
          }, { threshold: 0.3 });
          document.querySelectorAll('.kpi-value[data-target-value]').forEach(el => kpiObserver.observe(el));
        }

        // TOC: hover to open, click to lock, no backdrop
        const tocBtn = document.getElementById('toc-toggle-btn');
        const tocSidebar = document.getElementById('toc-sidebar');
        if (tocBtn && tocSidebar) {
          let locked = false, closeTimer;
          function openToc() {
            clearTimeout(closeTimer);
            tocSidebar.classList.add('open');
            tocBtn.setAttribute('aria-expanded', 'true');
          }
          function scheduleClose() {
            closeTimer = setTimeout(() => {
              if (!locked) {
                tocSidebar.classList.remove('open');
                tocBtn.setAttribute('aria-expanded', 'false');
              }
            }, 150);
          }
          tocBtn.addEventListener('mouseenter', openToc);
          tocSidebar.addEventListener('mouseenter', openToc);
          tocBtn.addEventListener('mouseleave', scheduleClose);
          tocSidebar.addEventListener('mouseleave', scheduleClose);
          tocBtn.addEventListener('click', () => {
            locked = !locked;
            tocBtn.classList.toggle('locked', locked);
            if (locked) openToc(); else scheduleClose();
          });
          document.querySelectorAll('.toc-sidebar a').forEach(a => a.addEventListener('click', () => {
            if (!locked) scheduleClose();
          }));
        }

        // TOC active state tracking
        const tocLinks = document.querySelectorAll('.toc-sidebar a[data-section]');
        if (tocLinks.length) {
          const sectionObserver = new IntersectionObserver(entries => {
            entries.forEach(e => {
              const id = e.target.dataset.section;
              const link = document.querySelector(`.toc-sidebar a[data-section="${CSS.escape(id)}"]`);
              if (link) link.classList.toggle('active', e.isIntersecting);
            });
          }, { rootMargin: '-10% 0px -60% 0px' });
          document.querySelectorAll('section[data-section]').forEach(s => sectionObserver.observe(s));
        }
      </script>

      <script>
        // Edit mode: hover bottom-left hotzone to reveal button, click to toggle
        (function() {
          const hotzone = document.getElementById('edit-hotzone');
          const toggle  = document.getElementById('edit-toggle');
          if (!hotzone || !toggle) return;
          let active = false, hideTimer;
          function showBtn() { clearTimeout(hideTimer); toggle.classList.add('show'); }
          function schedHide() { hideTimer = setTimeout(() => { if (!active) toggle.classList.remove('show'); }, 400); }
          hotzone.addEventListener('mouseenter', showBtn);
          hotzone.addEventListener('mouseleave', schedHide);
          toggle.addEventListener('mouseenter', showBtn);
          toggle.addEventListener('mouseleave', schedHide);
          function enterEdit() {
            active = true; toggle.classList.add('active', 'show'); toggle.textContent = '✓ Done';
            document.body.classList.add('edit-mode');
            document.querySelectorAll('h1,h2,h3,p,li,td,th,figcaption').forEach(el => el.setAttribute('contenteditable', 'true'));
          }
          function exitEdit() {
            active = false; toggle.classList.remove('active'); toggle.textContent = '✏ Edit';
            document.body.classList.remove('edit-mode');
            document.querySelectorAll('[contenteditable]').forEach(el => el.removeAttribute('contenteditable'));
            schedHide();
          }
          hotzone.addEventListener('click', () => active ? exitEdit() : enterEdit());
          toggle.addEventListener('click', () => active ? exitEdit() : enterEdit());
          document.addEventListener('keydown', e => {
            if ((e.key === 'e' || e.key === 'E') && !document.activeElement.getAttribute('contenteditable')) {
              active ? exitEdit() : enterEdit();
            }
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
              e.preventDefault();
              const html = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;
              const a = Object.assign(document.createElement('a'), {
                href: URL.createObjectURL(new Blob([html], {type: 'text/html'})),
                download: location.pathname.split('/').pop() || 'report.html'
              });
              a.click(); URL.revokeObjectURL(a.href);
            }
          });
        })();
      </script>

      <script>
        // Export: Print/PDF via window.print(); images via html2canvas (preloaded on page open)
        // Desktop PNG : full-page, adaptive scale (2× short / 1.5× long pages), PNG
        // Mobile PNG  : .report-wrapper 750px wide (iPhone 2× Retina), JPEG 92%
        // IM Share    : .report-wrapper 800px wide (WeChat/Feishu/DingTalk), JPEG 92%
        (function() {
          const exportBtn  = document.getElementById('export-btn');
          const exportMenu = document.getElementById('export-menu');
          const pngDesktop = document.getElementById('export-png-desktop');
          const pngMobile  = document.getElementById('export-png-mobile');
          const pngIM      = document.getElementById('export-im-share');
          if (!exportBtn || !exportMenu) return;
          const LABEL = exportBtn.textContent;

          exportBtn.addEventListener('click', e => { e.stopPropagation(); exportMenu.classList.toggle('open'); });
          document.addEventListener('click', e => {
            if (!exportBtn.contains(e.target) && !exportMenu.contains(e.target))
              exportMenu.classList.remove('open');
          });

          /* Preload html2canvas immediately — ready before first click */
          let libPromise = null;
          function loadLib() {
            if (libPromise) return libPromise;
            libPromise = new Promise(resolve => {
              if (window.html2canvas) { resolve(); return; }
              const s = document.createElement('script');
              s.src = 'https://cdn.jsdelivr.net/npm/html2canvas@1/dist/html2canvas.min.js';
              s.onload = resolve; document.head.appendChild(s);
            });
            return libPromise;
          }
          loadLib(); /* fire immediately */

          function restore() { exportBtn.style.visibility = ''; exportBtn.textContent = LABEL; }
          function filename(suffix, ext) {
            const d = new Date(), pad = n => String(n).padStart(2,'0');
            const date = `${d.getFullYear()}${pad(d.getMonth()+1)}${pad(d.getDate())}`;
            return (document.title||'report').replace(/[/\\:*?"<>|]/g,'_') + `_${date}${suffix}.${ext}`;
          }
          function saveBlob(canvas, fname, jpeg) {
            canvas.toBlob(blob => {
              const a = Object.assign(document.createElement('a'), { href: URL.createObjectURL(blob), download: fname });
              a.click(); URL.revokeObjectURL(a.href); restore();
            }, jpeg ? 'image/jpeg' : 'image/png', jpeg ? 0.92 : 1);
          }
          function capture(el, cfg, fname, jpeg) {
            exportMenu.classList.remove('open');
            exportBtn.style.visibility = 'hidden';
            exportBtn.textContent = '…';
            // Hide TOC toggle button if sidebar is not open (don't pollute screenshot)
            const tocSidebar = document.getElementById('toc-sidebar');
            const tocToggle = document.getElementById('toc-toggle-btn');
            const tocIsOpen = tocSidebar && tocSidebar.classList.contains('open');
            if (tocToggle && !tocIsOpen) tocToggle.style.visibility = 'hidden';
            document.querySelectorAll('.fade-in-up').forEach(e => e.classList.add('visible'));
            loadLib().then(() => html2canvas(el, cfg).then(c => {
              if (tocToggle && !tocIsOpen) tocToggle.style.visibility = '';
              saveBlob(c, fname, jpeg);
            }));
          }

          pngDesktop && pngDesktop.addEventListener('click', () => {
            const H = document.documentElement.scrollHeight;
            capture(document.documentElement, {
              scale: H > 4000 ? 2.5 : 3, useCORS: true, allowTaint: true,
              scrollX: 0, scrollY: 0,
              width: document.documentElement.scrollWidth, height: H,
              windowWidth: document.documentElement.scrollWidth, windowHeight: H
            }, filename('', 'png'), false);
          });

          pngMobile && pngMobile.addEventListener('click', () => {
            const el = document.querySelector('.report-wrapper') || document.documentElement;
            const bg = getComputedStyle(document.body).backgroundColor;
            capture(el, {
              scale: (750 / el.offsetWidth) * 2, useCORS: true, allowTaint: true,
              backgroundColor: bg,
              scrollX: 0, scrollY: 0, width: el.scrollWidth, height: el.scrollHeight
            }, filename('-mobile', 'jpg'), true);
          });

          pngIM && pngIM.addEventListener('click', () => {
            const el = document.querySelector('.report-wrapper') || document.documentElement;
            const bg = getComputedStyle(document.body).backgroundColor;
            capture(el, {
              scale: (800 / el.offsetWidth) * 2, useCORS: true, allowTaint: true,
              backgroundColor: bg,
              scrollX: 0, scrollY: 0, width: el.scrollWidth, height: el.scrollHeight
            }, filename('-im', 'jpg'), true);
          });
        })();
      </script>

    </body>
    </html>