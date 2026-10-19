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
    realworld: [
      {
        src: 'assets/photos/lifestyle-commute-reading.jpg',
        tag: { zh: '01 / COMMUTE CARRY', en: '01 / COMMUTE CARRY' },
        title: { zh: '捷運通勤 · 單手速讀隨拔', en: 'Subway Commute · One-Handed Quick Draw' },
        desc: {
          zh: '在顛簸搖晃的捷運車廂裡，單手握持 BOOX 翻頁；手寫筆穩固伏貼於背殼磁座，隨時抽拔標註重點，無需在公事包裡翻箱倒櫃。',
          en: 'On a swaying subway commute, holding the BOOX with one hand to turn pages. The stylus stays securely docked on the back, ready to draw and annotate instantly without digging through a bag.'
        }
      },
      {
        src: 'assets/photos/lifestyle-cafe-draw.jpg',
        tag: { zh: '02 / CAFE INSPIRATION', en: '02 / CAFE INSPIRATION' },
        title: { zh: '午後咖啡 · 靈感隨抽隨寫', en: 'Afternoon Cafe · Instant Spark & Sketch' },
        desc: {
          zh: '木質咖啡桌畔，點一杯黑咖啡攤開筆記。順著圓弧導引槽輕輕一抽，立即落筆記錄閃現的靈感，不讓翻找手寫筆打斷思路。',
          en: 'Beside an oak table with black coffee and open notes. A natural slide out of the sculpted groove captures spontaneous thoughts before they vanish.'
        }
      },
      {
        src: 'assets/photos/lifestyle-desk-stand.jpg',
        tag: { zh: '03 / ERGONOMIC ANGLE', en: '03 / ERGONOMIC ANGLE' },
        title: { zh: '桌面閱讀 · 人體工學微傾角', en: 'Desk Stand · Natural Ergonomic Tilt' },
        desc: {
          zh: '平置辦公桌面時，背部筆座恰如其分地抬升機身微幅仰角，避開室內頂燈刺眼眩光，手腕書寫也更自然放鬆。',
          en: 'Resting flat on a desk, the rear holder spine creates a gentle ergonomic angle that deflects overhead ceiling glare and eases wrist strain during long writing sessions.'
        }
      },
      {
        src: 'assets/photos/lifestyle-edc-flatlay.jpg',
        tag: { zh: '04 / EVERYDAY CARRY', en: '04 / EVERYDAY CARRY' },
        title: { zh: '極簡隨身 · EDC 零勾扯收納', en: 'Everyday Carry · Pocket-Friendly Flat Lay' },
        desc: {
          zh: '與皮夾、機械錶及無線耳機並列。整體外型無銳角突出，放進西裝口袋或帆布背包內袋順暢無阻，不刮擦織物內襯。',
          en: 'Arranged seamlessly alongside a wallet, watch, and earbuds. Smooth radiused nylon edges slide effortlessly into jacket pockets and backpacks without snagging delicate linings.'
        }
      },
      {
        src: 'assets/photos/lifestyle-magnetic-snap.jpg',
        tag: { zh: '05 / MODULAR SNAP', en: '05 / MODULAR SNAP' },
        title: { zh: '一秒快拆 · MagSafe 模組磁吸', en: 'Modular Snap · Instant MagSafe Alignment' },
        desc: {
          zh: '在家享受純粹輕薄閱讀時一撥即卸；出門差旅時靠近背板「喀嗒」緊貼。標準 MagSafe 磁吸系統，隨時切換形態。',
          en: 'Detach effortlessly for featherlight bare-device reading at home; snap firmly with a crisp magnetic click when heading outdoors. True modular versatility.'
        }
      },
      {
        src: 'assets/photos/lifestyle-ipad-extension.jpg',
        tag: { zh: '06 / IPAD MINI EXPANSION', en: '06 / IPAD MINI EXPANSION' },
        title: { zh: '跨界延伸 · iPad mini 靈動創作', en: 'Cross-Device Extension · iPad mini & Apple Pencil' },
        desc: {
          zh: '設計概念進一步延伸至 iPad mini 與 Apple Pencil。徹底解決原廠側邊磁吸容易在包袋中被意外撞落遺失的痛點。',
          en: 'Expanding the system to iPad mini with Apple Pencil, eliminating the perpetual fear of side-mounted pencils getting bumped off inside tight commute bags.'
        }
      }
    ],
    labnotes: [
      {
        src: 'assets/lab/boox-85mm-measurement.jpg',
        tag: { zh: 'BENCH EVIDENCE / 01', en: 'BENCH EVIDENCE / 01' },
        title: { zh: '確立磁環中心至機底 85 mm 黃金基準', en: '85 mm Centerline Baseline Established' },
        desc: {
          zh: '實機裝配波浪紋保護殼與 MagSafe 導磁環，手寫確認「85 mm」中心定位點，將理論推導正式錨定為物理基準。',
          en: 'Physical verification with ribbed case and MagSafe ring, establishing the verified 85 mm centerline datum on the BOOX Go 6.'
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
      },
      {
        title: { zh: 'iPad mini + Apple Pencil 首個物理打樣', en: 'First SLA 3D Print on iPad mini' },
        desc: {
          zh: '在切割墊上完成首件 SLA 高精度樹脂樣件實裝，Apple Pencil 順暢滑入，驗證側向開槽、快拆手感與懸臂抗扭強度。',
          en: 'First SLA resin prototype physically test-fitted onto iPad mini with Apple Pencil on the workbench cutting mat.'
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

      // Update nav links
      const navLinks = document.querySelectorAll('.nav-links a');
      if (navLinks.length >= 9) {
        navLinks[0].textContent = isEn ? 'The Idea' : '設計起點';
        navLinks[1].textContent = isEn ? 'Drafting' : '草圖至成型';
        navLinks[2].textContent = isEn ? 'Lab Notes' : '研發實證';
        navLinks[3].textContent = isEn ? 'Real World' : '真實場景';
        navLinks[4].textContent = isEn ? 'Origin Math' : '尺寸研究';
        navLinks[5].textContent = isEn ? 'Fit Lab' : '幾何適配';
        navLinks[6].textContent = isEn ? 'The Collection' : '設計系列';
        navLinks[7].textContent = isEn ? 'Anatomy' : '雙磁吸結構';
        navLinks[8].textContent = isEn ? 'FAQ' : '常見問題';
      } else if (navLinks.length >= 8) {
        navLinks[0].textContent = isEn ? 'The Idea' : '設計起點';
        navLinks[1].textContent = isEn ? 'Drafting' : '草圖至成型';
        navLinks[2].textContent = isEn ? 'Real World' : '真實場景';
        navLinks[3].textContent = isEn ? 'Origin Math' : '尺寸研究';
        navLinks[4].textContent = isEn ? 'Fit Lab' : '幾何適配';
        navLinks[5].textContent = isEn ? 'The Collection' : '設計系列';
        navLinks[6].textContent = isEn ? 'Anatomy' : '雙磁吸結構';
        navLinks[7].textContent = isEn ? 'Evolution' : '開發演進';
      } else if (navLinks.length >= 7) {
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

      // Update Real-World Kickstarter Section
      const rwSec = document.getElementById('real-world');
      if (rwSec) {
        const rwLabel = rwSec.querySelector('.section-label');
        if (rwLabel) rwLabel.textContent = isEn ? 'IN THE WILD / REAL-WORLD SCENARIOS' : 'IN THE WILD / 走入日常真實世界';
        const rwH2 = rwSec.querySelector('.section-heading h2');
        if (rwH2) rwH2.innerHTML = isEn ? 'Everyday carry, reading & sketching.<br><span>Six defining moments in daily life.</span>' : '隨身、閱讀與即興創作。<br><span>生活裡的六個決定性時刻。</span>';
        const rwP = rwSec.querySelector('.section-heading p');
        if (rwP) rwP.textContent = isEn ? 'Eliminate the dread of digging through the bottom of your bag. From spontaneous transit annotations to cafe sketches, Mag Holder makes the stylus feel native to your device.' : '擺脫散落背包底層的翻找焦慮。從晃動捷運上的單手速記，到木質咖啡桌旁的靈感捕捉，Mag Holder 讓手寫筆宛如設備天生的一部分，安穩、直覺、富有秩序。';

        const ksBadge = rwSec.querySelector('.ks-badge');
        if (ksBadge) ksBadge.textContent = isEn ? 'KICKSTARTER STORY / BORN FROM DAILY HABITS' : 'KICKSTARTER STORY / 靈感源於生活';
        const ksQuote = rwSec.querySelector('.ks-quote');
        if (ksQuote) ksQuote.textContent = isEn ? '"Brought your ereader, but forgot the pen — this used to be a daily regret. Mag Holder isn\'t just a holder; it builds an effortless, instinctive bond between your reader and stylus."' : '「帶了閱讀器，卻又忘了帶筆——這曾是每天重複上演的懊惱。Mag Holder 不只是一個筆座，而是為日常閱讀器與手寫筆之間，建立起一道最自然的隨身默契。」';
        const ksAuthor = rwSec.querySelector('.ks-author');
        if (ksAuthor) ksAuthor.textContent = isEn ? '— Mag Holder Design Notes · 2026 Prototype Study' : '— Mag Holder 設計手記 · 2026 原型研究';

        const rwCards = rwSec.querySelectorAll('.realworld-card');
        const rwEnData = [
          { scenario: 'Commute Carry · Quick One-Hand Draw', h3: 'Crowded Metro, Smooth Flipping', p: 'On a swaying train, flip pages on the BOOX with one hand. The stylus stays securely docked on the back, ready to annotate without digging through bags.' },
          { scenario: 'Afternoon Cafe · Instant Spark & Sketch', h3: 'A Natural Slide, Unbroken Flow', p: 'Beside an oak cafe table with black coffee and open notes. A smooth slide out of the guide channel lets you jot down inspiration before it fades.' },
          { scenario: 'Desk Reading · Natural Ergonomic Tilt', h3: 'Built-in Stand, Deflecting Glare', p: 'Resting flat on a desk, the rear holder spine forms a gentle ergonomic angle that deflects overhead ceiling glare and eases wrist strain.' },
          { scenario: 'Everyday Carry · Pocket-Friendly EDC', h3: 'Beveled Matte Nylon, Snag-Free', p: 'Alongside a wallet, watch, and earbuds. Smooth radiused nylon edges slide effortlessly into jacket pockets and backpacks without snagging delicate linings.' },
          { scenario: 'Modular Snap · Instant MagSafe Dock', h3: 'Bare Device or Full Kit in Seconds', p: 'Detach effortlessly for featherlight bare-device reading at home; snap firmly with a crisp magnetic click when heading outdoors.' },
          { scenario: 'Cross-Device · iPad mini & Pencil', h3: 'No More Bumping Pencils Off', p: 'Expanding the system to iPad mini with Apple Pencil, eliminating the perpetual fear of side-mounted pencils getting bumped off inside tight commute bags.' }
        ];
        const rwZhData = [
          { scenario: '通勤捷運 · 單手速讀隨拔', h3: '擁擠車廂，單手翻閱不慌亂', p: '在顛簸搖晃的捷運車廂裡，單手握持 BOOX 翻頁；手寫筆穩固伏貼於背殼磁座，隨時抽拔標註重點，無需在公事包裡翻箱倒櫃。' },
          { scenario: '午後咖啡 · 靈感隨抽隨寫', h3: '指尖順道一抽，思緒零中斷', p: '木質咖啡桌畔，點一杯黑咖啡攤開筆記。順著圓弧導引槽輕輕一抽，立即落筆記錄閃現的靈感，不讓翻找手寫筆打斷思路。' },
          { scenario: '桌面閱讀 · 人體工學微傾角', h3: '天然墊高支撐，撫平頂部反光', p: '平置辦公桌面時，背部筆座恰如其分地抬升機身微幅仰角，避開室內頂燈刺眼眩光，手腕書寫也更自然放鬆。' },
          { scenario: '極簡隨身 · EDC 零勾扯收納', h3: '倒角消光尼龍，俐落滑入包袋', p: '與皮夾、機械錶及無線耳機並列。整體外型無銳角突出，放進西裝口袋或帆布背包內袋順暢無阻，不刮擦織物內襯。' },
          { scenario: '一秒快拆 · MagSafe 模組磁吸', h3: '純粹手持或合體攜帶，隨心變換', p: '在家享受純粹輕薄閱讀時一撥即卸；出門差旅時靠近背板「喀嗒」緊貼。標準 MagSafe 磁吸系統，隨時切換形態。' },
          { scenario: '跨界延伸 · iPad mini 靈動創作', h3: '告別側邊易碰落，穩固隨身同行', p: '設計概念進一步延伸至 iPad mini 與 Apple Pencil。徹底解決原廠側邊磁吸容易在包袋中被意外撞落遺失的痛點。' }
        ];

        rwCards.forEach((c, i) => {
          const d = isEn ? rwEnData[i] : rwZhData[i];
          if (d) {
            const sc = c.querySelector('.realworld-scenario');
            if (sc) sc.textContent = d.scenario;
            const h = c.querySelector('h3');
            if (h) h.textContent = d.h3;
            const p = c.querySelector('p');
            if (p) p.textContent = d.p;
          }
        });
      }

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
          { scenario: 'Physical Measurement · 85 mm Datum', h3: '85 mm Centerline Baseline Established', p: 'Physical verification with ribbed case and MagSafe ring, establishing the verified 85 mm centerline datum on the BOOX Go 6.' },
          { scenario: 'Tolerance Survey · Ribbed Case Fit', h3: 'Ribbed Case Texture & Relief Survey', p: 'Physical tape measure survey across ribbed ridges (2–15 cm range) to guarantee a rock-solid, wobble-free puck contact plane.' },
          { scenario: 'In-Situ Layout · Redline Skeleton', h3: 'In-Situ Cantilever & Channel Redlining', p: 'Red-marker layout directly atop the MagSafe ring, tracing load-bearing cantilevers and ergonomic stylus release bevels.' },
          { scenario: 'Concept Draft · #1 Napkin Sketch', h3: '#1 Napkin Geometry: 85 mm Arm & Ø10 mm Loop', p: 'Core engineering napkin sketch #1 calculating the horizontal cantilever and 10 mm retention ring profile.' },
          { scenario: 'Bench Assembly · First 3D Prototype', h3: 'First SLA 3D Print on iPad mini', p: 'First SLA resin prototype physically test-fitted onto iPad mini with Apple Pencil on the workbench cutting mat.' }
        ];
        const labZhData = [
          { scenario: '物理測量 · 85 mm 磁環定位', h3: '確立磁環中心至機底 85 mm 黃金基準', p: '實機裝配波浪紋保護殼與 MagSafe 導磁環，手寫確認「85 mm」中心定位點，將理論推導正式錨定為物理基準。' },
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
          {
            q: 'Will the strong magnets in the stylus holder damage the BOOX E-Ink screen or disrupt stylus pressure sensitivity?',
            a: '<p><strong>It will not cause screen damage, and the magnetic field is directional and shielded.</strong></p><p>The BOOX Go 6 uses E-Ink Carta 1300 and electromagnetic resonance (EMR) digitizer technology. While unshielded magnets placed directly over the front writing surface could cause localized pen offset, Mag Holder isolates magnetic flux with single-direction blind sockets backed by a steel MagSafe flux ring. Measured residual stray field inside the stylus groove drops below 15 Gauss, preventing interference with the front EMR antenna grid.</p>'
          },
          {
            q: 'Why is the MagSafe centerline distance from the BOOX Go 6 bottom precisely 85 mm? Does it adhere securely over ribbed cases?',
            a: '<p><strong>This golden datum was determined jointly through geometric clearance equations and physical benchtop measurements.</strong></p><p>As proven in our lab notes (#01 & #02), the BOOX Go 6 is 149 mm tall and the stylus is 157.5 mm. With the MagSafe ring center placed 85 mm from the bottom edge, AERIS (Flow Long 120mm) leaves exactly 3 mm safety clearance at the bottom while top pen exposure is trimmed to 24.54 mm. It also perfectly bridges across the relief grooves of the official ribbed case for a solid, wobble-free seating plane.</p>'
          },
          {
            q: 'Does it work with iPad mini and Apple Pencil? Can the Pencil still charge magnetically on the side?',
            a: '<p><strong>Fully compatible, and specifically engineered to prevent Apple Pencil detachment drops.</strong></p><p>While Apple Pencil charges magnetically on the edge of the iPad mini, it frequently gets knocked off inside backpacks or during transit. Our TITAN PRO (K9-P10-Pad) and ECLIPSE MINI models lock the Pencil (Ø8.9 mm) securely to the rear chassis. When charging is needed, simply slide it out and snap it to the iPad edge—forming a reliable "rear transport lock + side rapid top-up" workflow.</p>'
          },
          {
            q: 'If I download the STL files to 3D print on my own, which materials and processes do you recommend?',
            a: '<p><strong>We strongly recommend SLS laser-sintered PA12 Nylon or tough SLA photopolymer resins.</strong></p><p>Because the retaining cantilever wall thickness tapers to 0.8–1.2 mm at critical flex points, conventional FDM prints (such as standard PLA or PETG) have weaker layer adhesion that may fatigue under repeated cycles. SLS PA12 nylon offers isotropic strength, impact flexibility, and a soft matte touch. For resin printing, always specify ABS-like or engineering tough resins.</p>'
          },
          {
            q: 'Is Mag Holder a mass-produced product or an open-source prototype? How can I get involved?',
            a: '<p><strong>Currently in the v7 prototype test-fitting phase, with all CAD print files completely open-source.</strong></p><p>In the Downloads section below, we provide the full v7 Print Pack with 10 STL files covering all 6 flagships, accompanied by an exhaustive 3D printing guide. You are welcome to download and submit them to any local 3D print service. If you discover tolerance improvements or test new device fits, please open an Issue or PR on our GitHub repository!</p>'
          }
        ];
        const faqZhData = [
          {
            q: '手寫筆座底部的強磁，會不會干擾 BOOX 電子紙螢幕或破壞手寫筆壓感？',
            a: '<p><strong>不會造成螢幕損壞，且已實施磁場定向屏蔽。</strong></p><p>BOOX Go 6 使用 E-Ink Carta 1300 電子紙技術與電磁手寫 (EMR)。傳統磁鐵若靠近正面書寫區域可能造成局部筆跡偏移，但 Mag Holder 的 N52 釹鐵硼磁路採封閉下置單向沉穴設計，背部貼合標準 MagSafe 導磁環，將漏磁通通導向背板結構外圍，筆身腔體內側磁通密度實測衰減至 15 Gauss 以下，完全避開正面 EMR 感應天線層。</p>'
          },
          {
            q: '為什麼磁環中心到 BOOX Go 6 底部必須是 85 mm？波浪紋保護殼能貼牢嗎？',
            a: '<p><strong>這是由幾何極限計算與工作檯實物測量共同決定的黃金基準。</strong></p><p>在工作檯實證中（見上方 Lab Notes #01 & #02），BOOX Go 6 機身高 149 mm，手寫筆長 157.5 mm。當磁環中心位於距機底 85 mm 處時，AERIS (Flow Long 120mm) 底部僅預留 3 mm 安全餘裕，筆尾上露 24.54 mm；同時剛好跨越官方波浪保護殼的縱向紋理凹槽，底座受力均勻，不會發生按壓搖晃。</p>'
          },
          {
            q: 'iPad mini 與 Apple Pencil 真的可以用嗎？還能進行側邊磁吸無線充電嗎？',
            a: '<p><strong>完全相容，專為解決 Apple Pencil 隨身防脫落而設計。</strong></p><p>iPad mini 原廠側邊磁吸雖然能無線充電，但在放入包包或走動抽拔時極易被碰撞掉落。Mag Holder 的 TITAN PRO (K9-P10-Pad) 與 ECLIPSE MINI 專為 Apple Pencil 2 及 Pencil Pro 設計（直徑 8.9 mm），牢固鎖在背殼；需要充電時取下吸回側邊即可，形成「背板攜帶鎖定 + 側邊快速補電」的最佳分工組合。</p>'
          },
          {
            q: '如果我自己下載 STL 自行 3D 打印，該選擇什麼材料與工藝？',
            a: '<p><strong>強烈建議採用 SLS 雷射燒結 PA12 尼龍或高韌性光固化樹脂。</strong></p><p>因為卡扣與筆鞘壁厚最薄處為 0.8–1.2 mm，常規 FDM 打印（如 PLA/PETG）層間結合力較弱，多次插拔可能出現層裂。SLS PA12 尼龍具備各向同性的韌性與細微消光磨砂手感；若選用光固化 SLA/DLP，請務必選用類 ABS (ABS-like) 或增韌樹脂。</p>'
          },
          {
            q: 'Mag Holder 是量產商品還是開源原型？如何參與後續演進？',
            a: '<p><strong>目前處於 v7 原型打樣與社群驗證階段，所有打樣檔案完全開源提供。</strong></p><p>我們在下方 Downloads 區提供了包含 6 大旗艦款在內的 10 個 STL 原型打樣包與完整打樣指南。你可以自由下載並送交任何 3D 打印服務商試樣。若你在尺寸公差、手感反饋或新設備適配上有任何發現，歡迎前往我們的 GitHub 倉庫提交 Issue 或 PR 一起改良！</p>'
          }
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

      // Re-run calculator labels
      updateCalculator();
    });
  }
})();
