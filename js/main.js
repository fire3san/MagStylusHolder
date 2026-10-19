(() => {
  'use strict';

  // --- 0. Dual-Mode Hero View Switcher (Studio Visual vs 3D CAD Lab) ---
  const viewModeRenderBtn = document.getElementById('view-mode-render');
  const viewMode3dBtn = document.getElementById('view-mode-3d');
  const heroRenderView = document.getElementById('hero-render-view');
  const hero3dView = document.getElementById('hero-3d-view');
  const btnHeroLaunch3d = document.getElementById('btn-hero-launch-3d');

  function setHeroMode(mode) {
    const is3d = mode === '3d';
    if (viewModeRenderBtn) {
      viewModeRenderBtn.classList.toggle('active', !is3d);
      viewModeRenderBtn.setAttribute('aria-selected', String(!is3d));
    }
    if (viewMode3dBtn) {
      viewMode3dBtn.classList.toggle('active', is3d);
      viewMode3dBtn.setAttribute('aria-selected', String(is3d));
    }
    if (heroRenderView) heroRenderView.classList.toggle('active', !is3d);
    if (hero3dView) hero3dView.classList.toggle('active', is3d);

    if (is3d) {
      setTimeout(() => {
        if (window.MagSafeViewer && window.MagSafeViewer.onWindowResize) {
          window.MagSafeViewer.onWindowResize();
        } else {
          window.dispatchEvent(new Event('resize'));
        }
      }, 50);
    }
  }

  if (viewModeRenderBtn) {
    viewModeRenderBtn.addEventListener('click', () => setHeroMode('render'));
  }
  if (viewMode3dBtn) {
    viewMode3dBtn.addEventListener('click', () => setHeroMode('3d'));
  }
  if (btnHeroLaunch3d) {
    btnHeroLaunch3d.addEventListener('click', () => setHeroMode('3d'));
  }

  // --- 1. Interactive Fit Lab & Clearance Calculator ---
  const DEVICE_CONFIGS = {
    boox: {
      name: 'BOOX Go 6',
      width: 109.0,
      height: 149.0,
      penLength: 157.5,
      penName: 'InkSense Plus'
    },
    ipad: {
      name: 'iPad mini 6 / A17 Pro',
      width: 134.8,
      height: 195.4,
      penLength: 166.0,
      penName: 'Apple Pencil Pro / 2'
    }
  };

  const calcDeviceSelect = document.getElementById('calc-device');
  const calcAngleInput = document.getElementById('calc-angle');
  const calcAngleValue = document.getElementById('calc-angle-value');
  const calcStatus = document.getElementById('calc-status');
  const calcY = document.getElementById('calc-y');
  const calcYMargin = document.getElementById('calc-y-margin');
  const calcX = document.getElementById('calc-x');
  const calcXMargin = document.getElementById('calc-x-margin');
  const calcDeviceOutline = document.getElementById('calc-device-outline');
  const calcPenLine = document.getElementById('calc-pen-line');

  function updateCalculator() {
    if (!calcDeviceSelect || !calcAngleInput) return;
    const devKey = calcDeviceSelect.value || 'boox';
    const cfg = DEVICE_CONFIGS[devKey] || DEVICE_CONFIGS.boox;
    const angleDeg = parseFloat(calcAngleInput.value) || 0;
    const angleRad = (angleDeg * Math.PI) / 180;

    if (calcAngleValue) calcAngleValue.textContent = `${angleDeg}°`;

    const projY = cfg.penLength * Math.cos(angleRad);
    const projX = cfg.penLength * Math.sin(angleRad);

    const marginY = cfg.height - projY;
    const marginX = cfg.width - projX;

    const isEn = window.currentLang === 'en';

    if (calcY) calcY.textContent = `${projY.toFixed(1)} mm`;
    if (calcX) calcX.textContent = `${projX.toFixed(1)} mm`;

    if (calcYMargin) {
      if (marginY >= 0) {
        calcYMargin.textContent = isEn ? `Height margin: +${marginY.toFixed(1)} mm (contained)` : `高度餘量: +${marginY.toFixed(1)} mm (未超出)`;
        calcYMargin.style.color = '#355222';
      } else {
        calcYMargin.textContent = isEn ? `Height overhang: ${marginY.toFixed(1)} mm (exceeds)` : `高度溢出: ${marginY.toFixed(1)} mm (超出機身)`;
        calcYMargin.style.color = '#8b3a2a';
      }
    }

    if (calcXMargin) {
      if (marginX >= 0) {
        calcXMargin.textContent = isEn ? `Width margin: +${marginX.toFixed(1)} mm` : `寬度餘量: +${marginX.toFixed(1)} mm`;
        calcXMargin.style.color = '#355222';
      } else {
        calcXMargin.textContent = isEn ? `Width overhang: ${marginX.toFixed(1)} mm` : `寬度溢出: ${marginX.toFixed(1)} mm`;
        calcXMargin.style.color = '#8b3a2a';
      }
    }

    if (calcStatus) {
      calcStatus.className = 'calc-status-badge';
      if (marginY >= 0 && marginX >= 0) {
        calcStatus.classList.add('ok');
        calcStatus.textContent = isEn ? `✓ ZERO OVERHANG · Fully inside ${cfg.name}` : `✓ 完全包絡 · 筆身 100% 收容於 ${cfg.name} 邊界內`;
      } else if (angleDeg === 0 && marginY < 0 && marginX >= 0) {
        calcStatus.classList.add('warn');
        calcStatus.textContent = isEn ? `⚠ VERTICAL QUICK-DRAW · Pen tail exposed by ${Math.abs(marginY).toFixed(1)} mm` : `⚠ 縱向快拔配置 · 筆尾安全上露 ${Math.abs(marginY).toFixed(1)} mm（筆尖向下入鞘）`;
      } else {
        calcStatus.classList.add('error');
        calcStatus.textContent = isEn ? `✕ EXCEEDS CHASSIS · Overhang by ${Math.abs(Math.min(marginY, marginX)).toFixed(1)} mm` : `✕ 超出機身範圍 · 溢出 ${Math.abs(Math.min(marginY, marginX)).toFixed(1)} mm`;
      }
    }

    // Update 2D SVG preview
    if (calcDeviceOutline && calcPenLine) {
      const svgW = 260;
      const svgH = 220;
      const scale = 0.85 * Math.min(svgW / cfg.width, svgH / cfg.height);
      const dw = cfg.width * scale;
      const dh = cfg.height * scale;
      const dx = (svgW - dw) / 2;
      const dy = (svgH - dh) / 2;

      calcDeviceOutline.setAttribute('x', dx);
      calcDeviceOutline.setAttribute('y', dy);
      calcDeviceOutline.setAttribute('width', dw);
      calcDeviceOutline.setAttribute('height', dh);

      const cx = svgW / 2;
      const cy = svgH / 2;
      const halfLen = (cfg.penLength * scale) / 2;
      const p1x = cx - halfLen * Math.sin(angleRad);
      const p1y = cy + halfLen * Math.cos(angleRad);
      const p2x = cx + halfLen * Math.sin(angleRad);
      const p2y = cy - halfLen * Math.cos(angleRad);

      calcPenLine.setAttribute('x1', p1x);
      calcPenLine.setAttribute('y1', p1y);
      calcPenLine.setAttribute('x2', p2x);
      calcPenLine.setAttribute('y2', p2y);

      if (marginY >= 0 && marginX >= 0) {
        calcPenLine.setAttribute('stroke', '#355222');
      } else if (angleDeg === 0) {
        calcPenLine.setAttribute('stroke', '#7a4409');
      } else {
        calcPenLine.setAttribute('stroke', '#8b3a2a');
      }
    }
  }

  if (calcDeviceSelect) {
    calcDeviceSelect.addEventListener('change', updateCalculator);
  }
  if (calcAngleInput) {
    calcAngleInput.addEventListener('input', updateCalculator);
  }

  document.querySelectorAll('.preset-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const ang = btn.dataset.angle;
      if (calcAngleInput) {
        calcAngleInput.value = ang;
        updateCalculator();
      }
    });
  });

  updateCalculator();

  // --- 2. 3D Inspection Triggers ---
  document.querySelectorAll('[data-inspect]').forEach(button => {
    button.addEventListener('click', () => {
      setHeroMode('3d');
      if (window.MagSafeViewer && window.MagSafeViewer.loadModel) {
        window.MagSafeViewer.loadModel(button.dataset.inspect);
      }
      const viewerSec = document.getElementById('viewer');
      if (viewerSec) viewerSec.scrollIntoView({ behavior: 'smooth' });
    });
  });

  const inspectUnderside = document.getElementById('inspect-underside');
  if (inspectUnderside) {
    inspectUnderside.addEventListener('click', () => {
      setHeroMode('3d');
      if (window.MagSafeViewer && window.MagSafeViewer.setViewAngle) {
        window.MagSafeViewer.setViewAngle('bottom');
      }
      const viewerSec = document.getElementById('viewer');
      if (viewerSec) viewerSec.scrollIntoView({ behavior: 'smooth' });
    });
  }

  // --- 3. Bilingual Language Switcher (ZH / EN) ---
  window.currentLang = 'zh';

  const langToggleBtn = document.getElementById('lang-toggle');
  if (langToggleBtn) {
    langToggleBtn.addEventListener('click', () => {
      window.currentLang = window.currentLang === 'zh' ? 'en' : 'zh';
      const isEn = window.currentLang === 'en';
      document.documentElement.lang = isEn ? 'en' : 'zh-Hant';

      document.querySelectorAll('.lang-opt').forEach(opt => {
        opt.classList.toggle('active', opt.dataset.lang === window.currentLang);
      });

      document.title = isEn ? 'Mag Holder — MagSafe Stylus System' : 'Mag Holder — 磁吸手寫筆座';
      const footerP = document.querySelector('footer p');
      if (footerP) footerP.textContent = isEn ? 'MagSafe Stylus Holder · Design Study & Prototype' : '磁吸手寫筆座 · 設計研究與打樣原型';

      // Update nav links
      const navLinks = document.querySelectorAll('.nav-links a');
      if (navLinks.length >= 7) {
        navLinks[0].textContent = isEn ? 'The Idea' : '設計起點';
        navLinks[1].textContent = isEn ? 'Drafting' : '草圖至成型';
        navLinks[2].textContent = isEn ? 'Origin Math' : '尺寸研究';
        navLinks[3].textContent = isEn ? 'Fit Lab' : '幾何適配';
        navLinks[4].textContent = isEn ? 'The Collection' : '設計系列';
        navLinks[5].textContent = isEn ? 'Anatomy' : '雙磁吸結構';
        navLinks[6].textContent = isEn ? 'Evolution' : '開發演進';
      } else if (navLinks.length >= 6) {
        navLinks[0].textContent = isEn ? 'The Idea' : '設計起點';
        navLinks[1].textContent = isEn ? 'Drafting' : '草圖至成型';
        navLinks[2].textContent = isEn ? 'Fit Lab' : '幾何適配';
        navLinks[3].textContent = isEn ? 'The Collection' : '設計系列';
        navLinks[4].textContent = isEn ? 'Anatomy' : '雙磁吸結構';
        navLinks[5].textContent = isEn ? 'Evolution' : '開發演進';
      }
      const navCta = document.querySelector('.nav-cta');
      if (navCta) navCta.innerHTML = isEn ? 'Download CAD <span>↗</span>' : '取得打樣檔案 <span>↗</span>';

      // Update hero view switcher buttons
      if (viewModeRenderBtn) {
        viewModeRenderBtn.innerHTML = isEn
          ? '<span class="view-dot"></span> Studio Visual'
          : '<span class="view-dot"></span> 實體渲染 · Studio Visual';
      }
      if (viewMode3dBtn) {
        viewMode3dBtn.innerHTML = isEn
          ? '<span>🔬</span> 3D CAD Lab'
          : '<span>🔬</span> 3D 互動 · CAD Lab';
      }
      if (btnHeroLaunch3d) {
        btnHeroLaunch3d.textContent = isEn
          ? 'Enter 3D CAD Orbit ↗'
          : '進入 3D CAD 旋轉檢視 ↗';
      }

      // Update hero
      const heroH1 = document.querySelector('.hero h1');
      if (heroH1) heroH1.innerHTML = isEn ? 'Giving the pen<br>a place of its<br><em>own.</em>' : '讓筆，<br>有自己的<br><em>位置。</em>';
      const heroDesc = document.querySelector('.hero-description');
      if (heroDesc) heroDesc.innerHTML = isEn ? 'A crisp silhouette, a detachable snap point.<br>Bringing quiet order between reading, writing, and transit carry.' : '一道俐落的輪廓，一個可拆卸的連接點。<br>為閱讀、書寫與收納之間，留出剛剛好的秩序。';

      // Update Drafting Table Section
      const draftSec = document.getElementById('drafting');
      if (draftSec) {
        const dLabel = draftSec.querySelector('.section-label');
        if (dLabel) dLabel.textContent = isEn ? 'THE DRAFTING TABLE / FROM FIRST SKETCH TO PHYSICAL FORM' : 'THE DRAFTING TABLE / 從第一筆草圖到實體成型';
        const dH2 = draftSec.querySelector('.section-heading h2');
        if (dH2) dH2.innerHTML = isEn ? 'Every curve began<br><span>with a graphite line on paper.</span>' : '每一道弧度，<br><span>都始於紙上的第一筆鉛痕。</span>';
        const dP = draftSec.querySelector('.section-heading p');
        if (dP) dP.textContent = isEn ? 'Thoughtful design is never born from thin air. We systematically translated real constraints, geometric tolerances, and magnetic circuits from hand-drawn drafts into 3D reality.' : '好的設計絕非憑空生成，而是將使用限制、幾何公差與磁路工程，一步步從手繪線條推演至 3D 物理實體。在此見證設計誕生的四個決定性時刻。';

        const draftCards = draftSec.querySelectorAll('.draft-card');
        if (draftCards.length >= 4) {
          const c0 = draftCards[0];
          c0.querySelector('.draft-step').textContent = isEn ? 'STAGE 01 / CONCEPT SKETCH' : 'STAGE 01 / 手繪構思';
          c0.querySelector('h3').textContent = isEn ? 'Exploring Ø9 mm Bore & 34° Diagonal Tilt' : '初探 Ø9 mm 筆徑與 34° 傾角';
          c0.querySelector('p').textContent = isEn ? 'Initial graphite studies calculating diagonal containment, defining the core architecture: case-free removal, one-handed draw, and magnetic guidance.' : '以鉛筆手繪推演斜向收納的可行性，首次定義「免拆保護殼、單手順拔、磁吸導向」的原型架構。';

          const c1 = draftCards[1];
          c1.querySelector('.draft-step').textContent = isEn ? 'STAGE 02 / SECTION STUDY' : 'STAGE 02 / 剖面手稿';
          c1.querySelector('h3').textContent = isEn ? 'Side Button Clearance & 0.8 mm Wall Specs' : '側邊按鍵避空槽與 0.8 mm 壁厚';
          c1.querySelector('p').textContent = isEn ? 'Hand-drawn section drafts defining blind bottom wells and button clearance channels, tuned for PA12 nylon shrinkage to eliminate insertion friction.' : '手繪細部剖面標註下置盲孔與側鍵避空槽，精確計算 PA12 尼龍收縮比，消除插拔干涉。';

          const c2 = draftCards[2];
          c2.querySelector('.draft-step').textContent = isEn ? 'STAGE 03 / CAD BLUEPRINT' : 'STAGE 03 / 工程藍圖';
          c2.querySelector('h3').textContent = isEn ? '58.4 mm MagSafe Ring & 3× N52 Sockets' : '58.4 mm 磁環槽與 3 顆 N52 磁穴';
          c2.querySelector('p').textContent = isEn ? 'Translating sketches into 2D CAD profiles to isolate MagSafe magnetic flux from pen retention magnets, establishing the dual-magnetic system.' : '轉換為 CAD 幾何剖面，驗證 MagSafe 磁吸環與三顆垂直下置強磁的磁通隔絕，確立雙磁力系統。';

          const c3 = draftCards[3];
          c3.querySelector('.draft-step').textContent = isEn ? 'STAGE 04 / EXPLODED ASSEMBLY' : 'STAGE 04 / 精密爆炸圖';
          c3.querySelector('h3').textContent = isEn ? '6-Layer Physical Stack Breakdown' : '六層物理裝配分解圖';
          c3.querySelector('p').textContent = isEn ? 'Full layer explosion detailing device backplate, MagSafe ring, PA12 nylon unibody chassis, N52 magnets, 3D printed seals, and the stylus.' : '完整呈現設備背板、引磁環、PA12 尼龍一體外殼、N52 釹鐵硼磁鐵、3D 密封蓋及手寫筆的六層精密層疊。';
        }
      }

      // Refresh viewer card and options
      if (window.MagSafeViewer) {
        const deviceProfile = document.getElementById('device-profile');
        if (deviceProfile && window.MagSafeViewer.renderModelOptions) {
          window.MagSafeViewer.renderModelOptions(deviceProfile.value);
        }
        const activeBtn = document.querySelector('.model-btn.active');
        if (activeBtn && window.MagSafeViewer.loadModel) {
          window.MagSafeViewer.loadModel(activeBtn.dataset.model);
        }
      }

      // Re-run calculator labels
      updateCalculator();
    });
  }
})();
