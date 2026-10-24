/**
 * 3D STL Interactive Viewer for MagSafe Stylus Holder
 * Uses Three.js r128, OrbitControls, and STLLoader
 */

(function () {
  'use strict';

  let scene, camera, renderer, controls;
  let currentMesh = null;
  let currentModelKey = null;
  let isViewerInitialized = false;
  let floorGrid, ambientLight, dirLight1, dirLight2, pointLight;
  let container, loadingEl, statsEl;
  let isAutoRotating = false;
  let loadRequest = 0;
  let currentMaterialType = 'white'; // 'black', 'white', 'clay', 'wireframe'

  const STL_MODELS = window.MODEL_CATALOG;

  const MATERIALS = {
    black: new THREE.MeshPhysicalMaterial({
      color: 0x303b32,
      metalness: 0.2,
      roughness: 0.7,
      clearcoat: 0.1,
      clearcoatRoughness: 0.8
    }),
    white: new THREE.MeshPhysicalMaterial({
      color: 0x637456,
      metalness: 0.05,
      roughness: 0.5,
      clearcoat: 0.2
    }),
    clay: new THREE.MeshStandardMaterial({
      color: 0xa8a29e,
      roughness: 0.9,
      metalness: 0.0
    }),
    wireframe: new THREE.MeshBasicMaterial({
      color: 0x647e54,
      wireframe: true
    })
  };

  function getRandomModelKey(device, excludeKey) {
    const targetDevice = device || 'boox_v7';
    const keys = Object.keys(STL_MODELS).filter(k => STL_MODELS[k].device === targetDevice);
    if (!keys.length) return 'S_Flow_BOOX_vertical';
    const candidates = excludeKey ? keys.filter(k => k !== excludeKey) : keys;
    const pool = candidates.length > 0 ? candidates : keys;
    return pool[Math.floor(Math.random() * pool.length)];
  }

  function getInitialModelKey() {
    try {
      const urlParams = new URLSearchParams(window.location.search);
      const queryModel = urlParams.get('model') || urlParams.get('inspect');
      if (queryModel && STL_MODELS[queryModel]) {
        return queryModel;
      }
      const hash = window.location.hash;
      if (hash && hash.startsWith('#inspect=')) {
        const hashModel = decodeURIComponent(hash.replace('#inspect=', '').trim());
        if (hashModel && STL_MODELS[hashModel]) {
          return hashModel;
        }
      }
    } catch (e) {
      // ignore URL parsing errors
    }
    return STL_MODELS['AURA_DUO_iPhone'] ? 'AURA_DUO_iPhone' : getRandomModelKey('boox_v7');
  }

  function initViewer() {
    if (isViewerInitialized) return;
    container = document.getElementById('stl-viewer-container');
    if (!container) return;
    isViewerInitialized = true;

    loadingEl = document.getElementById('viewer-loading');
    statsEl = document.getElementById('viewer-stats');

    // Scene setup
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xe0e4d6);

    // Camera setup
    const width = container.clientWidth || 600;
    const height = container.clientHeight || 450;
    camera = new THREE.PerspectiveCamera(40, width / height, 1, 2000);
    camera.up.set(0, 0, 1);
    camera.position.set(90, -125, 110);

    // Renderer setup
    try {
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
    } catch (error) {
      loadingEl.querySelector('.progress-text').textContent = '此瀏覽器未能啟用 3D，請查看下方 CAD 渲染或下載 STL。';
      loadingEl.querySelector('.loader-ring').style.display = 'none';
      return;
    }
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.15;

    container.appendChild(renderer.domElement);
    renderer.domElement.setAttribute('aria-label', '可拖曳旋轉的實際 STL 模型');
    renderer.domElement.setAttribute('role', 'img');

    // Controls setup
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxPolarAngle = Math.PI; // Allow peeking slightly below horizon
    controls.minDistance = 60;
    controls.maxDistance = 500;
    controls.autoRotate = isAutoRotating;
    controls.autoRotateSpeed = 1.2;

    // Lighting
    setupLighting();

    // Subtle Ground Grid
    const grid = new THREE.GridHelper(260, 26, 0xc6cebb, 0xd9dfd0);
    grid.rotation.x = Math.PI / 2;
    grid.position.z = -0.5;
    scene.add(grid);

    // Ground Shadow receiver
    const shadowGeo = new THREE.PlaneGeometry(300, 300);
    const shadowMat = new THREE.ShadowMaterial({ opacity: 0.45 });
    const shadowPlane = new THREE.Mesh(shadowGeo, shadowMat);
    shadowPlane.position.z = -0.6;
    shadowPlane.receiveShadow = true;
    scene.add(shadowPlane);

    // Event listeners
    window.addEventListener('resize', onWindowResize);
    setupControls();

    // Initial Model Load: Randomly select from flagship models (or URL query/hash override)
    const initialModel = getInitialModelKey();
    loadModel(initialModel);

    // Animation Loop
    animate();
  }

  function setupLighting() {
    ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    dirLight1 = new THREE.DirectionalLight(0xffffff, 1.4);
    dirLight1.position.set(100, -120, 220);
    dirLight1.castShadow = true;
    dirLight1.shadow.mapSize.width = 1024;
    dirLight1.shadow.mapSize.height = 1024;
    dirLight1.shadow.camera.near = 10;
    dirLight1.shadow.camera.far = 600;
    dirLight1.shadow.camera.left = -150;
    dirLight1.shadow.camera.right = 150;
    dirLight1.shadow.camera.top = 150;
    dirLight1.shadow.camera.bottom = -150;
    scene.add(dirLight1);

    dirLight2 = new THREE.DirectionalLight(0xc5d8aa, 0.7); // Cool rim light
    dirLight2.position.set(-140, 120, 100);
    scene.add(dirLight2);

    pointLight = new THREE.PointLight(0xffedd5, 0.7, 300); // Warm fill
    pointLight.position.set(0, 120, 90);
    scene.add(pointLight);
  }

  function loadModel(modelKey) {
    const info = STL_MODELS[modelKey];
    if (!info) return;
    currentModelKey = modelKey;
    const request = ++loadRequest;

    // Immediately update UI metadata (hero studio visual, badge tag, title, specs)
    updateModelCard(modelKey, info);

    if (loadingEl) loadingEl.style.display = 'flex';

    const loader = new THREE.STLLoader();
    loader.load(
      info.path,
      function (geometry) {
        if (request !== loadRequest) { geometry.dispose(); return; }
        if (currentMesh) {
          scene.remove(currentMesh);
          currentMesh.geometry.dispose();
          currentMesh.material.dispose();
        }

        geometry.computeVertexNormals();
        geometry.center();

        const mat = MATERIALS[currentMaterialType].clone();
        currentMesh = new THREE.Mesh(geometry, mat);
        currentMesh.castShadow = true;
        currentMesh.receiveShadow = true;

        geometry.computeBoundingBox();
        const bbox = geometry.boundingBox;
        const halfZ = (bbox.max.z - bbox.min.z) / 2;
        currentMesh.position.z = halfZ;

        scene.add(currentMesh);

        resetCamera();

        if (loadingEl) loadingEl.style.display = 'none';
      },
      function (xhr) {
        if (xhr.lengthComputable && loadingEl) {
          const percent = Math.round((xhr.loaded / xhr.total) * 100);
          const pEl = loadingEl.querySelector('.progress-text');
          if (pEl) pEl.textContent = `Loading STL ${percent}%...`;
        }
      },
      function (err) {
        console.error('Error loading STL:', err);
        if (loadingEl) {
          const pEl = loadingEl.querySelector('.progress-text');
          if (pEl) pEl.textContent = 'Error loading 3D model';
        }
      }
    );
  }

  function updateModelCard(key, info) {
    const titleEl = document.getElementById('viewer-model-title');
    const descEl = document.getElementById('viewer-model-desc');
    const extentsEl = document.getElementById('viewer-model-extents');
    const weightEl = document.getElementById('viewer-model-weight');
    const retentionEl = document.getElementById('viewer-model-retention');
    const stageEl = document.getElementById('viewer-model-stage');
    const isEn = window.currentLang === 'en';

    if (titleEl) titleEl.textContent = isEn ? (info.name_en || info.name) : info.name;
    const device = document.getElementById('device-profile');
    if (device && device.value !== info.device) { 
      device.value = info.device; 
      renderModelOptions(info.device); 
    }
    const clearanceEl = document.getElementById('viewer-model-clearance');
    if (clearanceEl) {
      if (info.clearance_text) {
        clearanceEl.textContent = isEn ? (info.clearance_text_en || info.clearance_text) : info.clearance_text;
      } else if (typeof info.bottom === 'number' && typeof info.top === 'number') {
        if (isEn) {
          clearanceEl.textContent = `Bottom Clearance ${info.bottom.toFixed(2)} mm / Top Pen Exposure ${info.top.toFixed(1)} mm (Ring height ${info.ring_height} mm)`;
        } else {
          clearanceEl.textContent = `底端餘量 ${info.bottom.toFixed(2)} mm / 筆尾上露 ${info.top.toFixed(1)} mm（磁環中心距底 ${info.ring_height} mm）`;
        }
      } else {
        clearanceEl.textContent = '';
      }
    }
    const download = document.getElementById('download-stl');
    if (download) download.href = info.path;
    const downloadName = document.getElementById('download-model-name');
    if (downloadName) downloadName.textContent = isEn ? (info.name_en || info.name) : info.name;
    if (descEl) descEl.textContent = isEn ? (info.desc_en || info.desc) : info.desc;
    if (extentsEl) extentsEl.textContent = info.extents;
    if (weightEl) weightEl.textContent = info.weight;
    if (retentionEl) retentionEl.textContent = info.retention;
    if (stageEl) stageEl.textContent = info.stage;

    // Synchronize hero studio visual image and badge
    const heroMainImg = document.getElementById('hero-main-img');
    const heroBadgeTag = document.getElementById('hero-badge-tag');
    if (heroMainImg && info.renderImg) {
      heroMainImg.src = info.renderImg;
      heroMainImg.alt = `${info.name} Studio Render`;
    }
    if (heroBadgeTag) {
      heroBadgeTag.textContent = isEn ? (info.name_en || info.name) : info.name;
    }

    document.querySelectorAll('.model-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.model === key);
    });
  }

  function setMaterial(type) {
    currentMaterialType = type;
    if (!currentMesh) return;

    if (!MATERIALS[type]) return;
    currentMesh.material.dispose();
    currentMesh.material = MATERIALS[type].clone();

    document.querySelectorAll('.mat-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.mat === type);
    });
  }

  function setViewAngle(angle) {
    if (!controls) return;
    controls.autoRotate = false;
    isAutoRotating = false;
    const btnRotate = document.getElementById('btn-autorotate');
    if (btnRotate) { btnRotate.classList.remove('active'); btnRotate.setAttribute('aria-pressed', 'false'); }

    switch (angle) {
      case 'iso':
        camera.up.set(0, 0, 1);
    camera.position.set(90, -125, 110);
        break;
      case 'top':
        camera.position.set(0, -1, 240);
        break;
      case 'bottom': // Underside magnet sockets & MagSafe pocket
        camera.position.set(0, 1, -220);
        break;
      case 'side':
        camera.position.set(-240, 0, 30);
        break;
      case 'front':
        camera.position.set(0, -240, 30);
        break;
    }
    controls.target.set(0, 0, 10);
    controls.update();
  }

  function resetCamera() {
    if (!controls) return;
    camera.up.set(0, 0, 1);
    camera.position.set(90, -125, 110);
    controls.target.set(0, 0, 10);
    controls.update();
  }

  function renderModelOptions(device) {
    const options = document.getElementById('model-options');
    if (!options) return;
    options.replaceChildren();
    const isEn = window.currentLang === 'en';
    const entries = Object.entries(STL_MODELS).filter(([,m]) => m.device === device);

    entries.forEach(([key, info]) => {
      const button = document.createElement('button');
      button.className = 'model-btn';
      button.dataset.model = key;
      if (key === currentModelKey) button.classList.add('active');
      const displayName = isEn ? (info.name_en || info.name) : info.name;
      button.textContent = displayName.split(' · ')[0];
      button.addEventListener('click', () => loadModel(key)); 
      options.appendChild(button);
    });
  }

  function setupControls() {
    const device = document.getElementById('device-profile');
    const initialDevice = device ? device.value : 'iphone_duo';
    renderModelOptions(initialDevice);
    if (device) {
      device.addEventListener('change', () => {
        renderModelOptions(device.value);
        const first = Object.keys(STL_MODELS).find(k => STL_MODELS[k].device === device.value);
        if (first) loadModel(first);
      });
    }
    document.querySelectorAll('.mat-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        setMaterial(btn.dataset.mat);
      });
    });

    document.querySelectorAll('.view-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        setViewAngle(btn.dataset.view);
      });
    });

    const autoRotateBtn = document.getElementById('btn-autorotate');
    if (autoRotateBtn) {
      autoRotateBtn.addEventListener('click', () => {
        isAutoRotating = !isAutoRotating;
        controls.autoRotate = isAutoRotating;
        autoRotateBtn.setAttribute('aria-pressed', String(isAutoRotating));
        autoRotateBtn.classList.toggle('active', isAutoRotating);
      });
    }

    const resetBtn = document.getElementById('btn-reset-view');
    if (resetBtn) {
      resetBtn.addEventListener('click', resetCamera);
    }
  }

  function onWindowResize() {
    if (!container || !renderer || !camera) return;
    const width = container.clientWidth;
    const height = container.clientHeight || 450;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
  }

  function animate() {
    requestAnimationFrame(animate);
    if (controls) controls.update();
    if (renderer && scene && camera) {
      renderer.render(scene, camera);
    }
  }

  if (document.getElementById('stl-viewer-container')) {
    initViewer();
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initViewer);
  } else {
    initViewer();
  }

  window.MagSafeViewer = {
    loadModel,
    getRandomModelKey,
    setMaterial,
    setViewAngle,
    resetCamera,
    renderModelOptions,
    updateModelCard,
    onWindowResize
  };
})();
