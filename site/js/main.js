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
    iphone_duo: {
      name: 'iPhone Duo (Dual-Screen)',
      width: 164.6,
      height: 117.8,
      penLength: 166.0,
      penName: 'Apple Pencil Pro'
    },
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
        calcStatus.textContent = isEn ? `⚠ VERTICAL QUICK-DRAW · Pen length exceeds height by ${Math.abs(marginY).toFixed(1)} mm` : `⚠ 縱向快拔配置 · 筆總長超出機高 ${Math.abs(marginY).toFixed(1)} mm（投影比較，不代表裝機筆位）`;
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

  // --- 3. Full-Screen Interactive Lightbox Modal (Drafting & Kickstarter Lifestyle) ---
  const GALLERIES = {
    drafting: [
      {
        src: 'assets/renders/sketch-design1.png',
        tag: { zh: 'STAGE 01 / CONCEPT SKETCH', en: 'STAGE 01 / CONCEPT SKETCH' },
        title: { zh: '初探 Ø9 mm 筆徑與 34° 傾角手繪草稿', en: 'Initial Ø9 mm Bore & 34° Diagonal Tilt Draft' },
        desc: {
          zh: '以鉛筆手繪推演斜向收納的可行性，首次定義「免拆保護殼、單手順拔、磁吸導向」的原型架構。',
          en: 'Initial graphite exploration calculating diagonal containment, establishing the core architecture: case-free removal, one-handed draw, and magnetic guidance.'
        }
      },
      {
        src: 'assets/renders/sketch-design2.png',
        tag: { zh: 'STAGE 02 / SECTION STUDY', en: 'STAGE 02 / SECTION STUDY' },
        title: { zh: '側邊按鍵避空槽與 0.8 mm 壁厚剖面手稿', en: 'Side Button Clearance & 0.8 mm Wall Thickness Study' },
        desc: {
          zh: '手繪細部剖面標註下置盲孔與側鍵避空槽，精確計算 PA12 尼龍收縮比，消除插拔干涉。',
          en: 'Hand-drawn section drafts defining blind bottom wells and button clearance channels, tuned for PA12 nylon shrinkage to eliminate insertion friction.'
        }
      },
      {
        src: 'assets/renders/v2-sections.png',
        tag: { zh: 'STAGE 03 / CAD BLUEPRINT', en: 'STAGE 03 / CAD BLUEPRINT' },
        title: { zh: '58.4 mm 磁環槽與 3 顆 N52 磁穴二維藍圖', en: '58.4 mm MagSafe Ring & 3× N52 Magnet Sockets Blueprint' },
        desc: {
          zh: '轉換為 CAD 幾何剖面，驗證 MagSafe 磁吸環與三顆垂直下置強磁的磁通隔絕，確立雙磁力系統。',
          en: 'Translating sketches into 2D CAD profiles to isolate MagSafe magnetic flux from pen retention magnets, establishing the dual-magnetic system.'
        }
      },
      {
        src: 'assets/images/engineering-exploded-view.jpg',
        tag: { zh: 'STAGE 04 / EXPLODED ASSEMBLY', en: 'STAGE 04 / EXPLODED ASSEMBLY' },
        title: { zh: '六層物理裝配分解圖', en: '6-Layer Physical Stack Exploded Diagram' },
        desc: {
          zh: '完整呈現設備背板、引磁環、PA12 尼龍一體外殼、N52 釹鐵硼磁鐵、3D 密封蓋及手寫筆的六層精密層疊。',
          en: 'Full layer explosion detailing device backplate, MagSafe ring, PA12 nylon unibody chassis, N52 magnets, 3D printed seals, and the stylus.'
        }
      }
    ],
    realworld: (window.LIFESTYLE_SCENES || []).map((scene, index) => ({
      src: scene.src,
      tag: {
        zh: `${String(index + 1).padStart(2, '0')} / ${scene.name} · ${scene.device}`,
        en: `${String(index + 1).padStart(2, '0')} / ${scene.name} · ${scene.device}`
      },
      title: scene.title,
      desc: scene.desc
    })),
    labnotes: [
      {
        src: 'assets/lab/boox-85mm-measurement.jpg',
        tag: { zh: 'BENCH EVIDENCE / 01', en: 'BENCH EVIDENCE / 01' },
        title: { zh: '量度更正：磁環距殼底75 mm', en: 'Measurement corrected: 75 mm' },
        desc: {
          zh: '早期照片保留原量度記錄，85 mm讀數已由使用者更正為75 mm。v9採用更正尺寸。',
          en: 'Historical measurement photo: the owner corrected the original 85 mm reading to 75 mm. v9 uses the corrected dimension.'
        }
      },
      {
        src: 'assets/lab/measuring-tape-ribbed-case.jpg',
        tag: { zh: 'BENCH EVIDENCE / 02', en: 'BENCH EVIDENCE / 02' },
        title: { zh: '避開凹凸稜線，確保零晃動貼合', en: 'Ribbed Case Texture & Relief Survey' },
        desc: {
          zh: '使用黃色鋼捲尺橫向與縱向精確複核保護殼 2–15 cm 浮雕紋理間距，保證筆座底座平坦接觸，杜絕按壓翹起。',
          en: 'Physical tape measure survey across ribbed ridges (2–15 cm range) to guarantee a rock-solid, wobble-free puck contact plane.'
        }
      },
      {
        src: 'assets/lab/boox-redline-magsafe-sketch.jpg',
        tag: { zh: 'BENCH EVIDENCE / 03', en: 'BENCH EVIDENCE / 03' },
        title: { zh: '直接在殼體手繪懸臂導槽受力走向', en: 'In-Situ Cantilever & Channel Redlining' },
        desc: {
          zh: '以紅色簽字筆在導磁環與殼體表面手繪力矩支撐點與側邊導流槽，確認手指持握時的貼合手感與防滑邊界。',
          en: 'Red-marker layout directly atop the MagSafe ring, tracing load-bearing cantilevers and ergonomic stylus release bevels.'
        }
      },
      {
        src: 'assets/lab/handwritten-sketch-85-10.png',
        tag: { zh: 'BENCH EVIDENCE / 04', en: 'BENCH EVIDENCE / 04' },
        title: { zh: '85 mm 橫向延伸臂與 Ø10 mm 彈性收容環', en: '#1 Napkin Geometry: 85 mm Arm & Ø10 mm Loop' },
        desc: {
          zh: '設計筆記草圖：推算底座外徑、內凹卡槽與頂部收容環的幾何配比，推導出 10 mm 彈性收容空間與防滑扣位。',
          en: 'Core engineering napkin sketch #1 calculating the horizontal cantilever and 10 mm retention ring profile.'
        }
      }
    ]
  };

  let activeGallery = null;
  let activeIndex = 0;

  const lightboxModal = document.getElementById('image-lightbox');
  const lightboxImg = document.getElementById('lightbox-img');
  const lightboxTag = document.getElementById('lightbox-tag');
  const lightboxCounter = document.getElementById('lightbox-counter');
  const lightboxTitle = document.getElementById('lightbox-title');
  const lightboxDesc = document.getElementById('lightbox-desc');
  const lightboxCloseBtn = document.getElementById('lightbox-close-btn');
  const lightboxPrevBtn = document.getElementById('lightbox-prev-btn');
  const lightboxNextBtn = document.getElementById('lightbox-next-btn');
  const lightboxBackdrop = document.querySelector('.lightbox-backdrop');

  function updateLightboxContent() {
    if (!activeGallery || !GALLERIES[activeGallery]) return;
    const items = GALLERIES[activeGallery];
    const item = items[activeIndex];
    const isEn = window.currentLang === 'en';

    if (lightboxImg) {
      lightboxImg.style.opacity = '0.4';
      lightboxImg.src = item.src;
      lightboxImg.alt = isEn ? item.title.en : item.title.zh;
      lightboxImg.onload = () => {
        lightboxImg.style.opacity = '1';
      };
    }
    if (lightboxTag) lightboxTag.textContent = isEn ? item.tag.en : item.tag.zh;
    if (lightboxCounter) lightboxCounter.textContent = `${activeIndex + 1} / ${items.length}`;
    if (lightboxTitle) lightboxTitle.textContent = isEn ? item.title.en : item.title.zh;
    if (lightboxDesc) lightboxDesc.textContent = isEn ? item.desc.en : item.desc.zh;
  }

  function openLightbox(galleryName, index) {
    if (!GALLERIES[galleryName]) return;
    activeGallery = galleryName;
    activeIndex = Math.max(0, Math.min(index, GALLERIES[galleryName].length - 1));
    updateLightboxContent();

    if (lightboxModal) {
      lightboxModal.classList.add('active');
      lightboxModal.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
      if (lightboxCloseBtn) lightboxCloseBtn.focus();
    }
  }

  function closeLightbox() {
    if (lightboxModal) {
      lightboxModal.classList.remove('active');
      lightboxModal.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }
  }

  function navigateLightbox(dir) {
    if (!activeGallery || !GALLERIES[activeGallery]) return;
    const total = GALLERIES[activeGallery].length;
    activeIndex = (activeIndex + dir + total) % total;
    updateLightboxContent();
  }

  document.querySelectorAll('[data-gallery]').forEach(el => {
    el.addEventListener('click', () => {
      const gallery = el.dataset.gallery;
      const idx = parseInt(el.dataset.index, 10) || 0;
      openLightbox(gallery, idx);
    });
    el.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        const gallery = el.dataset.gallery;
        const idx = parseInt(el.dataset.index, 10) || 0;
        openLightbox(gallery, idx);
      }
    });
  });

  if (lightboxCloseBtn) lightboxCloseBtn.addEventListener('click', closeLightbox);
  if (lightboxBackdrop) lightboxBackdrop.addEventListener('click', closeLightbox);
  if (lightboxPrevBtn) lightboxPrevBtn.addEventListener('click', () => navigateLightbox(-1));
  if (lightboxNextBtn) lightboxNextBtn.addEventListener('click', () => navigateLightbox(1));

  window.addEventListener('keydown', (e) => {
    if (!lightboxModal || !lightboxModal.classList.contains('active')) return;
    if (e.key === 'Escape') {
      closeLightbox();
    } else if (e.key === 'ArrowLeft') {
      navigateLightbox(-1);
    } else if (e.key === 'ArrowRight') {
      navigateLightbox(1);
    }
  });

  // --- 4. Bilingual Language Switcher (ZH / EN) ---
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

      // Translate visitor-facing copy without relying on navigation order.
      document.querySelectorAll('[data-zh][data-en]').forEach(element => {
        element.textContent = isEn ? element.dataset.en : element.dataset.zh;
      });
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

      // Lifestyle copy uses the shared data-zh/data-en language handler.

      // Update Maker's Workbench Lab Notes Section
      const labSec = document.getElementById('lab-notes');
      if (labSec) {
        const lLabel = labSec.querySelector('.section-label');
        if (lLabel) lLabel.textContent = isEn ? "THE MAKER'S WORKBENCH / BENCHTOP MEASUREMENTS & LAB NOTES" : "THE MAKER'S WORKBENCH / 實物測量與工作檯筆記";
        const lH2 = labSec.querySelector('.section-heading h2');
        if (lH2) lH2.innerHTML = isEn ? 'Beyond the CAD screen,<br><span>verifying every millimeter on the physical bench.</span>' : '走出 CAD 螢幕，<br><span>在工作檯上親手驗證每 1 毫米。</span>';
        const lP = labSec.querySelector('.section-heading p');
        if (lP) lP.textContent = isEn ? 'No matter how precise the parametric math, design must ultimately reconcile with physical reality: caliper offsets, ribbed cases, and the first 3D-printed assemblies on our cutting mat.' : '參數再精密，終究要回歸真實物理世界。從游標卡尺的實機取樣、波浪保護殼的公差適配，到首件 3D 打印實體裝機測試——這就是 Mag Holder 在工作室桌面上真實誕生的痕跡。';

        const labCards = labSec.querySelectorAll('.lab-card');
        const labEnData = [
          { scenario: 'Measurement corrected to 75 mm', h3: 'Measurement corrected: 75 mm', p: 'Historical measurement photo: the owner corrected the original 85 mm reading to 75 mm. v9 uses the corrected dimension.' },
          { scenario: 'Tolerance Survey · Ribbed Case Fit', h3: 'Ribbed Case Texture & Relief Survey', p: 'Physical tape measure survey across ribbed ridges (2–15 cm range) to guarantee a rock-solid, wobble-free puck contact plane.' },
          { scenario: 'In-Situ Layout · Redline Skeleton', h3: 'In-Situ Cantilever & Channel Redlining', p: 'Red-marker layout directly atop the MagSafe ring, tracing load-bearing cantilevers and ergonomic stylus release bevels.' },
          { scenario: 'Concept Draft · #1 Napkin Sketch', h3: '#1 Napkin Geometry: 85 mm Arm & Ø10 mm Loop', p: 'Core engineering napkin sketch #1 calculating the horizontal cantilever and 10 mm retention ring profile.' },
          { scenario: 'Bench Assembly · First 3D Prototype', h3: 'First SLA 3D Print on iPad mini', p: 'First SLA resin prototype physically test-fitted onto iPad mini with Apple Pencil on the workbench cutting mat.' }
        ];
        const labZhData = [
          { scenario: '物理測量 · 已更正為75 mm', h3: '量度更正：磁環距殼底75 mm', p: '早期照片保留原量度記錄，85 mm讀數已由使用者更正為75 mm。v9採用更正尺寸。' },
          { scenario: '公差實測 · 保護殼波浪紋避位', h3: '避開凹凸稜線，確保零晃動貼合', p: '使用黃色鋼捲尺橫向與縱向精確複核保護殼 2–15 cm 浮雕紋理間距，保證筆座底座平坦接觸，杜絕按壓翹起。' },
          { scenario: '實體放樣 · 手繪懸臂受力骨架', h3: '直接在殼體手繪懸臂導槽受力走向', p: '以紅色簽字筆在導磁環與殼體表面手繪力矩支撐點與側邊導流槽，確認手指持握時的貼合手感與防滑邊界。' },
          { scenario: '概念草繪 · #1 核心力學手稿', h3: '85 mm 橫向延伸臂與 Ø10 mm 彈性收容環', p: '設計筆記草圖：推算底座外徑、內凹卡槽與頂部收容環的幾何配比，推導出 10 mm 彈性收容空間與防滑扣位。' },
          { scenario: '實物驗證 · 首件 3D 打印試樣', h3: 'iPad mini + Apple Pencil 首個物理打樣', p: '在切割墊上完成首件 SLA 高精度樹脂樣件實裝，Apple Pencil 順暢滑入，驗證側向開槽、快拆手感與懸臂抗扭強度。' }
        ];

        labCards.forEach((c, i) => {
          const d = isEn ? labEnData[i] : labZhData[i];
          if (d) {
            const sc = c.querySelector('.lab-scenario');
            if (sc) sc.textContent = d.scenario;
            const h = c.querySelector('h3');
            if (h) h.textContent = d.h3;
            const p = c.querySelector('p');
            if (p) p.textContent = d.p;
          }
        });
      }

      // Update FAQ Section
      const faqSec = document.getElementById('faq');
      if (faqSec) {
        const fLabel = faqSec.querySelector('.section-label');
        if (fLabel) fLabel.textContent = isEn ? 'FAQ & BACKER GUIDE / ENGINEERING & BACKER FAQ' : 'FAQ & BACKER GUIDE / 工程與贊助常見問答';
        const fH2 = faqSec.querySelector('.section-heading h2');
        if (fH2) fH2.innerHTML = isEn ? 'Engineering in the open,<br><span>answering every detail with honesty.</span>' : '誠實面對工程，<br><span>解答每一個細節疑問。</span>';
        const fP = faqSec.querySelector('.section-heading p');
        if (fP) fP.textContent = isEn ? 'We believe in radical engineering transparency. From magnetic shielding on E-Ink displays and 3D printing materials to iPad mini compatibility, here are honest answers to backer questions.' : '我們堅持透明公開的造物哲學。無論是磁場對 E-Ink 螢幕的潛在影響、3D 打印材料選擇，抑或是對 iPad mini 的支援，所有工程細節在此為你一一解答。';

        const faqItems = faqSec.querySelectorAll('.faq-item');
        const faqEnData = [
          {"q": "Will the 5 x 1 mm N52 magnets interfere with the device?", "a": "<p>Magnetic fields, writing interference and long-term device use have not been tested. No validated magnetic shielding is provided. Test actual pen attraction and retention first.</p>"},
          {"q": "Why use a 75 mm ring position?", "a": "<p>The owner corrected the earlier 85 mm reading to 75 mm from the case bottom. v9 Flow/AERIS is 110 mm long with 3 mm bottom clearance; Facet/VERTEX is 100 mm with 13 mm clearance. K+M has 3.5 mm at the specified pen position.</p>"},
          {"q": "How are the magnets and 3M tape assembled?", "a": "<p>Bottom-loading pockets are 5.3 mm diameter and 4 mm deep. BOOX AERIS & VERTEX use 5 magnets (Y = -48, -38, -12, 0, 12 mm) for enhanced barrel retention; ECLIPSE, ZEPHYR and iPad models use 3 magnets. Bond each 5 x 1 mm magnet to the pocket ceiling using provisionally 0.2 mm tape; secure a 5.05 x 2.7 mm spacer below. Recalculate the spacer for other tape thicknesses. The case ring is separate hardware.</p>"},
          {"q": "What about iPad and printing material?", "a": "<p>iPad geometry remains a fit study; its pockets also change to 5 x 1 mm magnets. No device validation or charging is provided. Quote PA12 prototypes and print fit samples before full bodies.</p>"},
          {"q": "How does AURA DUO support iPhone Duo and Apple Pencil Pro?", "a": "<p>AURA DUO v3 uses a 53.55 mm outboard offset and a parallel pencil axis. Assuming 1.5 mm case edges, sheath clearance is 3 mm. The inherited CAD bore measures 9.6 mm for an 8.9 mm reference barrel. This is mechanical storage; phone writing support, physical fit, retention and hinge sweep are separate checks.</p>"},
          {"q": "Is this a production-ready product?", "a": "<p>This is a v9 digital prototype with eleven STL files: six standard flagships, AURA DUO signature model, three fit samples and one spacer (v9 AERIS & VERTEX feature 5-magnet sockets). Mesh checks do not validate retention, drops or fatigue. Follow the print guide.</p>"}
        ];
        const faqZhData = [
          {"q": "Ø5×1 mm N52磁石會否干擾設備？", "a": "<p>目前未做磁場、壓感干擾或長期裝機測試，也沒有經驗證的磁屏蔽結構。請先測實際筆身能否吸附，再以低處軟墊試裝；不能僅靠N52等級保證保持力。</p>"},
          {"q": "為何改用75 mm磁環位置？", "a": "<p>使用者已確認之前85 mm讀數有誤，正確為距保護殼底75 mm。v9 Flow/AERIS長110 mm，底部留3 mm；Facet/VERTEX長100 mm，留13 mm；K+M指定筆位留3.5 mm。波浪殼黏附與搖晃待實測。</p>"},
          {"q": "磁石與3M雙面膠怎樣裝？", "a": "<p>孔徑5.3 mm、深4 mm，由底面裝入。AERIS 與 VERTEX 旗艦長鞘升級 5 顆 Ø5×1 mm 磁石（Y = -48, -38, -12, 0, 12 mm）強化筆身吸附力，其餘款式配置 3 顆。磁石以暫定0.2 mm膠層貼近孔頂，下方用Ø5.05×2.7 mm墊片承托並另行固定。若膠厚不同，需重算墊片。背殼磁環是另一組硬件。</p>"},
          {"q": "iPad版及打印材料如何選？", "a": "<p>iPad外形暫沿用尺寸研究，磁孔同步改為Ø5×1 mm；未完成實機驗證，也不提供充電。先向打印商詢價PA12試件並打印筆徑試片，核對公差、側鍵及長通道清粉。</p>"},
          {"q": "AURA DUO 如何適配 iPhone Duo 與 Apple Pencil Pro？", "a": "<p>AURA DUO v3 採53.55 mm外側偏置，筆身與手機長邊平行。按每側1.5 mm殼邊估算，鞘至殼邊留3 mm。保留的CAD內孔實測9.6 mm，筆身參考8.9 mm。這是機械收納設計；手機書寫支援、實機配合、保持力與摺疊掃掠須分別確認。</p>"},
          {"q": "現在可以當成量產成品嗎？", "a": "<p>目前是v9數位原型，打樣包包含 10 個 STL（AERIS與VERTEX為5磁孔版本）、AURA DUO 雙屏旗艦款、3 款側滑 STL 與 2 款全新開脊微彈 STL。網格檢查不等於保持力、跌落或疲勞測試。請按打樣指南逐步驗證。</p>"}
        ];

        faqItems.forEach((item, idx) => {
          const d = isEn ? faqEnData[idx] : faqZhData[idx];
          if (d) {
            const titleSpan = item.querySelector('.faq-title');
            if (titleSpan) titleSpan.textContent = d.q;
            const ansDiv = item.querySelector('.faq-answer');
            if (ansDiv) ansDiv.innerHTML = d.a;
          }
        });
      }

      // Update active lightbox if open
      if (lightboxModal && lightboxModal.classList.contains('active')) {
        updateLightboxContent();
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

      // Update Collection Section
      const colSec = document.getElementById('collection');
      if (colSec) {
        const cH2 = colSec.querySelector('.section-heading h2');
        if (cH2) cH2.innerHTML = isEn
          ? 'Ten Flagship Series.<br><span>Axial, Lateral Slide, Open Spine & Dual-Screen.</span>'
          : '十大旗艦系列。<br><span>縱向、側滑、開脊與雙屏四種收納性格。</span>';
        const cP = colSec.querySelector('.section-heading p');
        if (cP) cP.textContent = isEn
          ? 'AERIS, VERTEX, ECLIPSE and ZEPHYR explore axial layouts; AURA DUO stands as our signature flagship for the dual-screen iPhone Duo with Apple Pencil Pro; AURA, NEXUS and AXIS expand lateral slide dimensions; ORBIT and STRATOS introduce open spine flex C-clips.'
          : 'AERIS、VERTEX、ECLIPSE 與 ZEPHYR 探索縱向軸心佈局；AURA DUO 作為旗艦簽名款，專為 iPhone Duo 雙屏與 Apple Pencil Pro 而生；AURA、NEXUS 與 AXIS 側滑系列拓展側翼外擴取筆維度；全新 ORBIT 與 STRATOS 開脊系列以微彈 C 夾與開放式背骨，帶來「微傾即取」的極致靈活。';
        const cCaption = colSec.querySelector('.caption');
        if (cCaption) cCaption.textContent = isEn
          ? 'All views rendered from actual CAD geometry. Material colors are for visual preview; physical surface finish to be confirmed via test prints.'
          : '九款畫面均由實際 CAD 幾何生成，材質顏色僅供視覺預覽；實際表面與手感需以打印樣件確認。';
      }

      // Re-run calculator labels
      updateCalculator();
    });
  }
})();
