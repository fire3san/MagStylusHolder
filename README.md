# Mag Holder (MAG / HOLDER) — 磁吸手寫筆座

> **讓筆，有自己的位置。**  
> 一道俐落的輪廓，一個可拆卸的連接點。為閱讀、書寫與收納之間，留出剛剛好的秩序。

🌐 **線上產品展示頁 (Live Product Showcase)**:  
👉 **[https://fire3san.github.io/MagStylusHolder/](https://fire3san.github.io/MagStylusHolder/)**

---

## 📖 設計理念與起點 (The Origin & Concept)

### 帶了閱讀器，卻又忘了帶筆。
這個設計，起於一位 BOOX 使用者的真實困擾：有筆、有保護殼，卻沒有一個順手的位置放筆。分開攜帶容易遺忘，隨手放下又可能滑落、撞傷。

我們想把「記得帶筆」變成一個更自然的動作：收好閱讀器時，筆也有自己的位置。因此，從保護殼背面的磁環出發，設計可拆卸的磁吸筆座。

### 尺寸悖論挑戰 (The Length Challenge)
- **BOOX Go 6**: $149 \times 109 \times 6.8\text{ mm}$
- **InkSense Plus 手寫筆**: $157.5\text{ mm} \cdot \varnothing 9\text{ mm}$
- **長度衝突**: $157.5 - 149 = +8.5\text{ mm}$ (筆比機身長)
- **幾何演進**: 從早期 $34^\circ$ 對角斜向投影幾何探索，到 v7 縱向取筆配置，以底部不超出機身為優先，精準平衡筆身包覆與握取空間。
- **跨平台延伸**: 進一步適配 **iPad mini 6 / A17 Pro** 與 Apple Pencil。

---

## 🏆 旗艦產品系列 (The Collection)

| 型號 | 代號 | 設計特點 | 適配設備 |
## 🏆 旗艦產品系列 (The Collection)

Mag Holder 目前涵蓋 **四大架構體系、共十款旗艦設計**，外加 iPad mini 專屬款式與歷代工程里程碑：

0. **★ AURA DUO v3**: 筆軸53.55 mm外側偏置，鞘至殼邊3 mm（每側1.5 mm殼邊假設），筆與手機長邊及背板平行。實機配合與摺疊掃掠待驗證。
1. **縱向軸心系列 (Axial Sheaths & Clamps)**: 沿機身背板軸向收納，強調沈浸式包覆與極限防護。
2. **側翼外擴側滑系列 (Lateral Slide Rails)**: 筆軸向外側延伸 60.3 mm，解放後背握持空間，支援側向滑入。
3. **開脊微彈快拆系列 (Open Spine Quick-Release)**: 開放式背骨與雙側開 C 夾，實現「微傾即取」的極致靈活性。

---

## 🗺️ 產品名稱與 STL 檔案對照表 (Product Name to STL Mapping Guide for AI / Dev)

> **重要提示（致後續維護之 AI Agent 與開發者）**：  
> 網頁前端使用 `window.MODEL_CATALOG`（位於 [js/models.js](C:/SRC/MagStylusHolder/js/models.js) 與 [site/js/models.js](C:/SRC/MagStylusHolder/site/js/models.js)）驅動 Three.js 3D 檢視器、按鈕資料繫結 (`data-inspect`)、型號規格卡片與下載連結。所有路徑在專案根目錄與 `site/` 保持 1:1 鏡像對應。

### 0. ★ 旗艦簽名款：iPhone Duo 雙屏專用 (Flagship Signature)

| 編號 | 產品中文名稱 | 產品英文名稱 | Catalog Key (`data-inspect`) | 主要 STL 檔案路徑 | 產品渲染圖路徑 | 尺寸 (W×H×D mm) | 磁石配置 | 架構特色與展開動態學 |
|:---:|:---|:---|:---|:---|:---|:---:|:---:|:---|
| **00** | **★ AURA DUO · 雙屏磁吸智筆座** | AURA DUO v3 | `AURA_DUO_iPhone` | `assets/stl/side/AURA_DUO_iPhone_v3.stl` | `assets/renders/side/AURA_DUO_v3_unfolded.png` | $93.05 \times 114.54 \times 14.9$ | 5個保留磁孔 | 53.55 mm外側偏置；鞘至殼邊3 mm（每側1.5 mm殼邊假設）；筆與手機長邊及背板平行；實機與摺疊掃掠待驗證 |

---

### 1. BOOX Go 6 九大旗艦模型 (The Nine Flagships)

| 編號 | 產品中文名稱 | 產品英文名稱 | Catalog Key (`data-inspect`) | 主要 STL 檔案路徑 | 產品渲染圖路徑 | 尺寸 (W×H×D mm) | 磁石配置 | 架構特色 |
|:---:|:---|:---|:---|:---|:---|:---:|:---:|:---|
| **01** | **AERIS · 全包覆流光長鞘** | AERIS · Monolithic Sheath | `S_Flow_BOOX_vertical` | `assets/stl/v9/S_Flow_BOOX_vertical.stl` | `assets/renders/v9/AERIS_fit_checked_mounted.png` | $68.0 \times 110.0 \times 16.0$ | 5 顆 $\varnothing 5\times 1$ mm | 110mm 縱向長鞘，底端餘 3mm，高於152mm假設殼頂21.54mm，5 磁梯次保持 |
| **02** | **VERTEX · 幾何稜角精雕鞘** | VERTEX · Architectural Facet | `S_Facet_BOOX_vertical` | `assets/stl/v9/S_Facet_BOOX_vertical.stl` | `assets/renders/v9/S_Facet_BOOX_vertical_mounted.png` | $68.0 \times 100.0 \times 16.1$ | 5 顆 $\varnothing 5\times 1$ mm | 100mm 建築稜角，底端餘 13mm，頂部露 34.54mm，5 磁梯次保持 |
| **03** | **ECLIPSE · 圓融雙磁快取環** | ECLIPSE · Radial Magnetic Collar | `KM_Arc_BOOX_vertical` | `assets/stl/v9/KM_Arc_BOOX_vertical.stl` | `assets/renders/v9/KM_Arc_BOOX_vertical_mounted.png` | $68.0 \times 68.0 \times 16.05$ | 3 顆 $\varnothing 5\times 1$ mm | 68mm 圓弧微彈鎖定環，中央同心底座，底端餘 3.5mm，瞬拔快取 |
| **04** | **ZEPHYR · 疾風羽翼流線夾** | ZEPHYR · Aerodynamic Wing Clamp | `KM_Ribbon_BOOX_vertical` | `assets/stl/v9/KM_Ribbon_BOOX_vertical.stl` | `assets/renders/v9/KM_Ribbon_BOOX_vertical_mounted.png` | $68.0 \times 68.0 \times 15.85$ | 3 顆 $\varnothing 5\times 1$ mm | 68mm 空氣動力流線雙翼肋夾，底端餘 3.5mm，極致輕盈導流 |
| **05** | **AURA · 流光側滑長鞘** | AURA · Lateral Flow Sheath | `Side_Scabbard_v3` | `assets/stl/side/01_Side_Scabbard_PROVISIONAL.stl` | `assets/renders/side/01_Side_Scabbard_mounted.png` | $99.8 \times 114.54 \times 14.9$ | 5 顆 $\varnothing 5\times 1$ mm | 94mm 側滑導軌長鞘（側向外擴 60.3mm），18mm 劍梢導角，防誤觸避鍵槽 |
| **06** | **NEXUS · 側翼瞬取雙夾** | NEXUS · Dual-Wing Quick Clip | `Side_QuickClip_v3` | `assets/stl/side/02_Side_QuickClip_PROVISIONAL.stl` | `assets/renders/side/02_Side_QuickClip_mounted.png` | $99.8 \times 65.0 \times 12.45$ | 3 顆 $\varnothing 5\times 1$ mm | 65mm 雙 C 翼快拆夾（跨距 26mm，側向外擴 60.3mm），一秒瞬插盲拔 |
| **07** | **AXIS · 極簡導軌滑夾** | AXIS · Precision Rail Slide Clip | `Apple_Pencil_Clip_v3` | `assets/stl/side/03_Apple_Pencil_Original_5x1_NoText_PROVISIONAL.stl` | `assets/renders/side/03_Apple_Pencil_Original_mounted.png` | $14.0 \times 67.5 \times 9.18$ | 3 顆 $\varnothing 5\times 1$ mm | 14×67.5mm 極致修長窄軌直夾，無刻字極簡表面，羽量級精準貼合 |
| **08** | **ORBIT · 脊光開放快拆座** | ORBIT · Open Spine Compact | `A_Open_Spine_Compact` | `assets/stl/open_spine/A_Open_Spine_Compact.stl` | `assets/renders/open_spine/A_Open_Spine_Compact_mounted.png` | $68.0 \times 106.0 \times 16.1$ | 5 顆 $\varnothing 5\times 1$ mm | 106mm 開放背骨 + 雙側開微彈 C 夾（夾中距 -27/+22mm）+ 底部筆尖保護杯 |
| **09** | **STRATOS · 凌霄開脊長座** | STRATOS · Extended Rear Spine | `B_Rear_Spine_Extended` | `assets/stl/open_spine/B_Rear_Spine_Extended.stl` | `assets/renders/open_spine/B_Rear_Spine_Extended_mounted.png` | $68.0 \times 129.0 \times 16.1$ | 5 顆 $\varnothing 5\times 1$ mm | 129mm 加長脊骨（延伸至 +57mm）+ 擴展雙 C 夾（-19/+27mm）+ 底部筆尖保護杯 |

---

### 2. iPad mini 專用旗艦款 (iPad mini Series)

| 產品中文名稱 | 產品英文名稱 | Catalog Key | 主要 STL 檔案路徑 | 產品渲染圖路徑 | 尺寸 (W×H×D mm) | 磁石配置 | 特點說明 |
|:---|:---|:---|:---|:---|:---:|:---:|:---|
| **TITAN PRO · 旗艦雙模工作座** | TITAN PRO · Studio Sheath | `S_Flow_iPad_Pencil89` | `assets/stl/v9/S_Flow_iPad_Pencil89.stl` | `assets/renders/v9/S_Flow_iPad_Pencil89_mounted.png` | $68.0 \times 130.54 \times 16.0$ | 3 顆 $\varnothing 5\times 1$ mm | $\varnothing 9.3$ mm Apple Pencil 內徑，130.54mm 高度實現 0mm 頂部外露全包覆 |
| **ECLIPSE MINI · 快拆雙磁環扣** | ECLIPSE MINI · Quick-Draw Puck | `KM_Arc_iPad_Pencil89` | `assets/stl/v9/KM_Arc_iPad_Pencil89.stl` | `assets/renders/v9/KM_Arc_iPad_Pencil89_mounted.png` | $68.0 \times 68.0 \times 16.05$ | 3 顆 $\varnothing 5\times 1$ mm | $\varnothing 9.3$ mm 內徑，底端留 14.7mm，隨行快取，背部防丟與側吸充電互不干擾 |

---

### 3. 歷代工程演進樣件 (Historical Milestones)

| 代數 / 階段 | 產品中文名稱 | Catalog Key | STL 檔案路徑 | 設計工程定位 |
|:---|:---|:---|:---|:---|
| **Gen 5** | v5 Shield / 空氣動力筆鞘 | `Shield_scabbard` | `assets/stl/Shield_scabbard.stl` | 144.2mm 超長全包覆筆鞘，驗證筆尖全包覆保護，但促使後續 v6/v7 縮減尾端以避免下超出 |
| **Gen 4** | v4 Fused Collar / 一體項圈夾 | `KM_fused_collar_under_magnets` | `assets/stl/KM_fused_collar_under_magnets.stl` | 取消分離式 TPU 軟膠，首次將剛性尼龍筆圈與 68mm 磁環底座融合，磁石移至底面隱藏 |
| **Gen 3** | v3 Scabbard / 雙隧道分段筆鞘 | `S_scabbard_v3` | `assets/stl/S_scabbard_v3.stl` | 雙導向環分段進筆測試，探索入口環與底鞘的導引同心度 |
| **Gen 2** | v2 Compact Puck / 緊湊磁扣圓盤 | `M_compact_puck_v2` | `assets/stl/M_compact_puck_v2.stl` | 68mm 極簡圓盤構型，首次驗證 MagSafe 磁吸環與內部三點磁吸筆身力學可行性 |

---

### 4. 3D 打印打包下載檔案結構 (Download Packages Mapping)

使用者可在頁面底部 `#downloads` 下載打包好的驗證資源包：

| 下載包檔案名稱 | 對應路徑 | 包含內容 (STL / Docs) |
|:---|:---|:---|
| **v9 旗艦打樣包** | `assets/downloads/BOOX_iPad_v9_print_pack.zip` | 6 款主件 (AERIS, VERTEX, ECLIPSE, ZEPHYR, TITAN PRO, ECLIPSE MINI) + 3 款筆徑試片 ($\varnothing 9.3/\varnothing 9.4/\varnothing 9.6$) + $\varnothing 5.05\times 2.70$ 磁石墊片 |
| **側滑外擴打樣包** | `assets/downloads/three_holder_designs_v3.zip` | 3 款側滑主件 (AURA, NEXUS, AXIS) + 墊片 STL |
| **開脊微彈雙款打樣包** | `assets/downloads/BOOX_Open_Spine_Duo_Five_Magnets.zip` | 2 款開脊主件 (ORBIT, STRATOS) + 3 款側夾彈性試片 ($\varnothing 9.4/\varnothing 9.6/\varnothing 9.8$) + $\varnothing 5.05\times 2.70$ 墊片 (單件需 5 顆) |
| **繁體中文打樣指南** | `assets/downloads/PRINT_GUIDE_ZH.md` | 詳細材料規格 (PA12)、公差配合、磁石裝配順序、3M 背膠厚度與驗證清單 |

---

## ⚡ 核心工程特點 (Engineering Architecture)

- **雙磁吸系統 (Dual-Magnetic System)**:
  - 外部基底：$\varnothing 58.4\text{ mm}$ 標準 MagSafe 磁吸環槽，牢固吸附於保護殼引磁片。
  - 內部筆座：3 ~ 5 顆下置 N52 釹鐵硼微型強磁（v9 AERIS/VERTEX 與 AURA DUO 配備 5 顆梯次分佈強磁），精準吸附手寫筆內部鐵芯，行進不脫落、單手直覺拔出。
- **雙屏鉸鏈中軸防干涉動態學 (Dual-Screen Fold Kinematics Clearance)**:
  - 專為 iPhone Duo 開發：中央折疊鉸鏈（$X=0$）與右背板 MagSafe 中心距離 $38.2\text{ mm}$。
  - AURA DUO 筆鞘長鞘（Scabbard）朝外側延伸至 $X = +60.3\text{ mm}$，筆身完全收納於外緣，底座內緣預留 $6\text{ mm}$ 軸心切角。
  - 徹底杜絕向內側干涉導致的「卡中軸」問題，無論是 $180^\circ$ 完全展開雙屏、折疊單屏使用，或任意角度懸停皆順暢無阻。
- **3D 互動 CAD 實驗室 (Interactive 3D WebGL Viewer)**:
  - 採用 Three.js 與真實工程 STL 網格渲染。
  - 支援石白 (Alabaster White)、墨黑 (Ink Black)、岩灰 (Clay Gray) 與工程線框 (Wireframe) 四種材質模式。
  - 自由旋轉、縮放與立體/頂面/底面視角切換。
- **幾何適配計算機 (Fit Lab)**:
  - 動態滑桿即時計算 $0^\circ \sim 45^\circ$ 傾角下的垂直與水平尺寸投影。

---

## 📁 倉庫目錄結構 (Project Structure)

```text
├── index.html          # 產品頁入口 (GitHub Pages 主頁)
├── css/
│   └── style.css       # 響應式排版與美學樣式
├── js/
│   ├── main.js         # 互動邏輯、中英雙語切換、幾何計算機
│   ├── viewer.js       # Three.js 3D STL 互動檢視器
│   ├── models.js       # 旗艦型號數據庫與 STL 配置
│   └── vendor/         # Three.js 與 OrbitControls 庫
├── assets/
│   ├── renders/        # 4K 高解析度 Studio 產品渲染圖
│   ├── stl/            # 旗艦系列真實 3D 打印 STL 檔案
│   ├── images/         # 六層裝配爆炸圖等工程圖紙
│   └── downloads/      # 3D 打印打包下載檔案
├── output/             # 歷代工程版本 (v2 ~ v7)、淘寶 3D 打印需求單
└── README.md           # 專案說明文件
```

---

## 🖨️ 3D 列印打樣建議 (3D Printing Spec)

- **製程工藝**: SLS (選擇性激光燒結) 或 MJF (多射流熔融)
- **建議材質**: PA12 尼龍 (耐磨損、耐衝擊、韌性極佳)
- **層厚精度**: 0.08 mm ~ 0.1 mm
- **外觀處理**: 噴砂化學平滑 (Vapor Smoothing) + 黑色或象牙白染色
- **強磁規格**: N52 釹鐵硼 $\varnothing 5\text{ mm} \times 1\text{ mm}$ 圓形強磁（孔徑 $5.3\text{ mm}$、深 $4.0\text{ mm}$，底面裝入；搭配 $\varnothing 5.05 \times 2.70\text{ mm}$ PA12 尼龍承托墊片與暫定 $0.2\text{ mm}$ 背膠層）
- **打樣順序**: 請務必先打樣筆徑試片 ($\varnothing 9.3/\varnothing 9.4/\varnothing 9.6\text{ mm}$) 檢視實機配合公差，再進行主件列印。

---

## 📜 聲明 (Disclaimer)

*本專案為開源設計研究與打樣原型，旨在探討極簡收納與人體工學體驗。MagSafe 為 Apple Inc. 之註冊商標，此處僅作為幾何接口與磁吸規格之技術參考。*

## Frontend maintenance

The repository root is the canonical product-page source. See
[the maintenance guide](docs/maintaining-product-page.md) for the CSS component
map and editing workflow. Run `python3 scripts/sync-site.py` after frontend edits
to update the portable `site/` mirror; `--check` verifies that it is current.

## AURA DUO v3 correction

See [geometry and rendering notes](docs/AURA_DUO_V3.md). Rebuild with `.venv/bin/python scripts/aura_duo/build.py`; the product page and downloads use the revised STL.

Lifestyle scene sources, device references and generation prompts: [docs/LIFESTYLE_GALLERY.md](docs/LIFESTYLE_GALLERY.md).

## 朝屏幕側置款（SCREEN 概念打樣）

NEXUS、AURA 與 AURA DUO（使用者稱 AURA PRO）各新增一款朝顯示屏版本，原款保留。
v2 已更新實際 STL：連接臂為水平同層直臂，落差0 mm；筆夾／筆鞘朝屏幕。
NEXUS、AURA 對應 BOOX Go 6 Gen II；AURA DUO 對應 iPhone Duo 收合尺寸。
按官方機身尺寸，每面暫加1.5 mm保護殼作包絡檢查，鞘至假設殼邊3 mm。
尺寸來源與實機驗證限制詳見 `assets/stl/screen-facing/README.md`。

- 網頁：`#screen-facing`，3D 型號：`NEXUS_SCREEN`、`AURA_SCREEN`、`AURA_DUO_SCREEN`。
- STL、驗證結果與說明：`assets/stl/screen-facing/`。
- 打樣包：`assets/downloads/Screen_Facing_Flat_v2.zip`。
- 重新生成：`.venv/bin/python scripts/build-screen-facing.py`。
- 三款均檢查封閉網格、單一實體、磁環區域不變及與假設機殼包絡無交疊。
- 實機、側鍵、磁石裝配、保持力、直臂強度與 DUO 摺疊須後續打樣確認。
