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

        /* Summary card button — sits to the right of h1 */
        .title-row { display: flex; align-items: flex-start; gap: 1rem; }
        .title-row h1 { flex: 1; }
        .card-mode-btn {
          flex-shrink: 0; margin-top: .6rem;
          background: var(--surface); border: 1px solid var(--border); border-radius: 6px;
          padding: .32rem .7rem; font-size: .78rem; font-weight: 600; letter-spacing: .01em;
          color: var(--text-muted); cursor: pointer; transition: all .2s;
          font-family: var(--font-sans, system-ui); white-space: nowrap;
        }
        .card-mode-btn:hover { background: var(--primary-light); color: var(--primary); border-color: var(--primary); }

        /* Summary card overlay */
        .sc-overlay {
          display: none; position: fixed; inset: 0; z-index: 500;
          background: rgba(0,0,0,.5); backdrop-filter: blur(6px);
          align-items: center; justify-content: center; padding: 2rem;
        }
        body.card-mode .sc-overlay { display: flex; }
        body.card-mode .main-with-toc,
        body.card-mode .toc-toggle,
        body.card-mode .toc-sidebar { visibility: hidden; }
        body.card-mode .sc-overlay { visibility: visible; }

        /* The card itself */
        .sc-card {
          position: relative; width: 420px; max-width: 100%;
          background: #f5f3ed; border-radius: 14px; overflow: hidden;
          box-shadow: 0 32px 96px rgba(0,0,0,.4);
        }
        /* Paper noise texture */
        .sc-card::before {
          content: ''; position: absolute; inset: 0; pointer-events: none; opacity: .04;
          background-image:
            radial-gradient(circle at 20% 20%, rgba(0,0,0,.8) .5px, transparent .8px),
            radial-gradient(circle at 80% 40%, rgba(0,0,0,.7) .4px, transparent .7px);
          background-size: 8px 8px, 11px 11px;
        }
        .sc-inner { padding: 2.2rem 2rem; display: flex; flex-direction: column; gap: 1rem; }
        .sc-meta { font-size: .68rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: #888; }
        .sc-title { font-size: 1.85rem; font-weight: 800; color: #111; line-height: 1.1; letter-spacing: -.02em; }
        .sc-bar { width: 48px; height: 4px; background: var(--primary, #1A56DB); border-radius: 2px; }
        .sc-abstract { font-size: .88rem; line-height: 1.65; color: #444; }
        .sc-kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(88px,1fr)); gap: .5rem; margin-top: .2rem; }
        .sc-kpi { background: rgba(0,0,0,.05); border-radius: 7px; padding: .55rem .7rem; }
        .sc-kpi-v { font-size: 1.35rem; font-weight: 800; color: #111; line-height: 1.1; }
        .sc-kpi-l { font-size: .65rem; color: #777; text-transform: uppercase; letter-spacing: .06em; margin-top: .18rem; }
        .sc-kpi-t { font-size: .7rem; color: #10B981; margin-top: .1rem; }
        .sc-sections { display: flex; flex-wrap: wrap; gap: .35rem; }
        .sc-chip { font-size: .68rem; background: rgba(0,0,0,.07); border-radius: 99px; padding: .18rem .55rem; color: #555; }
        .sc-footer { font-size: .68rem; color: #aaa; text-align: center; padding: .8rem 2rem; border-top: 1px solid rgba(0,0,0,.07); }
        .sc-close {
          position: absolute; top: .85rem; right: .85rem;
          background: rgba(0,0,0,.09); border: none; border-radius: 50%;
          width: 26px; height: 26px; cursor: pointer; color: #666;
          display: flex; align-items: center; justify-content: center; font-size: .85rem;
          transition: background .2s;
        }
        .sc-close:hover { background: rgba(0,0,0,.18); }
        @media print { .sc-overlay, .card-mode-btn { display: none !important; } }
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
          <!-- lang:en card button label: "⊞ Summary" | lang:zh: "⊞ 摘要卡" -->
          <div class="title-row">
            <h1>[title]</h1>
            <button class="card-mode-btn" id="card-mode-btn" title="[Summary card|摘要卡片]">[⊞ Summary|⊞ 摘要卡]</button>
          </div>
          [if author or date: <p class="report-meta">[author] · [date]</p>]

          <!-- Summary card overlay (always present) — populated from #report-summary JSON -->
          <div class="sc-overlay" id="sc-overlay">
            <div class="sc-card" id="sc-card">
              <button class="sc-close" id="sc-close" aria-label="Close">✕</button>
              <div class="sc-inner" id="sc-inner"><!-- filled by JS --></div>
              <div class="sc-footer" id="sc-footer"></div>
            </div>
          </div>

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
        // Scroll-triggered animations
        if (!document.body.classList.contains('no-animations')) {
          // Generic fade-in-up
          const fadeObserver = new IntersectionObserver(
            entries => entries.forEach(e => {
              if (e.isIntersecting) { e.target.classList.add('visible'); fadeObserver.unobserve(e.target); }
            }),
            { threshold: 0.08 }
          );
          document.querySelectorAll('.fade-in-up').forEach(el => fadeObserver.observe(el));

          // Stagger helper: observe parent, animate children one by one
          function staggerGroup(parentSel, childSel, delay) {
            document.querySelectorAll(parentSel).forEach(parent => {
              new IntersectionObserver((entries, obs) => {
                if (!entries[0].isIntersecting) return;
                obs.disconnect();
                parent.classList.add('stagger-ready');
                parent.querySelectorAll(childSel).forEach((el, i) =>
                  setTimeout(() => el.classList.add('visible'), i * delay)
                );
              }, { threshold: 0.1 }).observe(parent);
            });
          }
          staggerGroup('.kpi-grid', '.kpi-card', 100);   // KPI cards: spring bounce stagger
          staggerGroup('.timeline', '.timeline-item', 130); // Timeline items: slide-in stagger

          // KPI counter animation (CountUp)
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

      <script>
        // Summary card mode — reads #report-summary JSON, renders inline card, toggles body.card-mode
        (function() {
          const btn     = document.getElementById('card-mode-btn');
          const overlay = document.getElementById('sc-overlay');
          const inner   = document.getElementById('sc-inner');
          const footer  = document.getElementById('sc-footer');
          const closeBtn= document.getElementById('sc-close');
          if (!btn || !overlay || !inner) return;

          function buildCard() {
            try {
              const d = JSON.parse(document.getElementById('report-summary').textContent);

              const metaParts = [d.author, d.date].filter(Boolean);
              const kpisHtml = (d.kpis || []).slice(0, 6).map(k => `
                <div class="sc-kpi">
                  <div class="sc-kpi-v">${k.value || ''}</div>
                  <div class="sc-kpi-l">${k.label || ''}</div>
                  ${k.trend ? `<div class="sc-kpi-t">${k.trend}</div>` : ''}
                </div>`).join('');
              const chipsHtml = (d.sections || []).map(s =>
                `<span class="sc-chip">${s}</span>`).join('');

              inner.innerHTML = [
                metaParts.length ? `<div class="sc-meta">${metaParts.join(' · ')}</div>` : '',
                `<div class="sc-title">${d.title || ''}</div>`,
                `<div class="sc-bar"></div>`,
                d.abstract  ? `<div class="sc-abstract">${d.abstract}</div>` : '',
                kpisHtml    ? `<div class="sc-kpis">${kpisHtml}</div>` : '',
                chipsHtml   ? `<div class="sc-sections">${chipsHtml}</div>` : '',
              ].filter(Boolean).join('');

              if (footer) footer.textContent = window.location.pathname.split('/').pop() || 'report.html';
            } catch(e) {
              inner.textContent = 'Summary unavailable.';
            }
          }

          let built = false;
          function open() {
            if (!built) { buildCard(); built = true; }
            document.body.classList.add('card-mode');
            overlay.setAttribute('aria-hidden', 'false');
          }
          function close() {
            document.body.classList.remove('card-mode');
            overlay.setAttribute('aria-hidden', 'true');
          }

          btn.addEventListener('click', open);
          closeBtn && closeBtn.addEventListener('click', close);
          overlay.addEventListener('click', e => { if (e.target === overlay) close(); });
          document.addEventListener('keydown', e => {
            if (e.key === 'Escape' && document.body.classList.contains('card-mode')) close();
          });
        })();
      </script>

    </body>
    </html>