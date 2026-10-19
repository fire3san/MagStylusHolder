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
|:---|:---|:---|:---|
| **AERIS** | S_Flow | 全包覆流光長鞘，外殼沿筆身流線延伸，底部餘量 3mm，最高防護 | BOOX Go 6 |
| **VERTEX** | S_Facet | 幾何折面極速座，立體切角與微斜切拔槽，極速單手拔插 | BOOX Go 6 |
| **ECLIPSE** | KM_Ring | 日蝕包覆防脫環，閉環鎖定與圓形磁底一體成型，防顛簸掉落 | BOOX Go 6 |
| **ZEPHYR** | KM_Ribbon | 疾風羽翼夾，微弧側翼緊湊收束於 68mm 中央磁盤，極致輕盈 | BOOX Go 6 |
| **TITAN PRO** | iPad_Titan | 鈦盾全裝甲加固座，專為 iPad mini 6 / A17 Pro 及 Apple Pencil 量身定製 | iPad mini 6 / A17 Pro |
| **ECLIPSE MINI** | iPad_Eclipse | 日蝕迷你快取環，簡潔環形鎖定，輕巧便攜 | iPad mini 6 / A17 Pro |

---

## ⚡ 核心工程特點 (Engineering Architecture)

- **雙磁吸系統 (Dual-Magnetic System)**:
  - 外部基底：$\varnothing 58.4\text{ mm}$ 標準 MagSafe 磁吸環槽，牢固吸附於保護殼引磁片。
  - 內部筆座：3 顆下置 N52 釹鐵硼微型強磁，精準吸附手寫筆內部鐵芯，行進不脫落、單手直覺拔出。
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
- **強磁規格**: N52 釹鐵硼直徑 3mm × 厚度 2mm 沉頭磁鐵

---

## 📜 聲明 (Disclaimer)

*本專案為開源設計研究與打樣原型，旨在探討極簡收納與人體工學體驗。MagSafe 為 Apple Inc. 之註冊商標，此處僅作為幾何接口與磁吸規格之技術參考。*
