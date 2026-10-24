# 朝屏幕水平接駁 v2 / Flat screen-facing v2

NEXUS SCREEN、AURA SCREEN：BOOX Go 6 (Gen II)。
AURA DUO SCREEN：iPhone Duo（收合尺寸包絡；展開與摺疊待驗證）。
三款已修改實際 STL：連接臂上下表面為 Z=0 / 3.4 mm，沒有 L 形或高低落差。
磁環維持機背位置，筆鞘／筆夾以 Z=1.7 mm 反射，向屏幕方向凸出。
筆身仍沿機身長邊；「水平」指連接臂同層，不是把筆轉成橫放。

設備尺寸依據：
- BOOX 官方 Go 6 (Gen II)：149 × 109 × 6.8 mm。
  https://shop.boox.com/products/go6gen2
- Apple 官方 iPhone Duo：收合 117.8 × 84.1 × 11.3 mm；
  展開 117.8 × 164.6 × 5.2 mm。
  https://www.apple.com/iphone-duo/specs/

以上為機身尺寸。每面暫加1.5 mm保護殼包絡，並非已量度的保護殼。
BOOX 檢查包絡為112 × 152 × 9.8 mm；DUO 為87.1 × 120.8 × 14.3 mm。
筆軸偏置：BOOX 66 mm；DUO 53.55 mm，筆鞘內側距假設殼邊3 mm。
磁環在示意殼中央；實際磁環位置須按實機核對。
磁環介面、原筆鞘／夾口尺寸及磁孔保留；筆鞘反射後的磁石極性須重核。

checks.json 記錄封閉網格、單一實體、磁環未改動、水平連接臂高度及包絡交疊檢查。
灰綠色機身為包絡示意，橙色是實際 STL。*_profile.png 是實際 STL 的側視圖。
實體配合、側鍵與接口、磁石裝配、保持力、臂強度及 DUO 鉸鏈掃掠仍待驗證。
請交由列印商審核 PA12 製程、公差與支撐，不能以包絡檢查取代實機打樣。

Rebuild: .venv/bin/python scripts/build-screen-facing.py
The three v2 STL files use a coplanar bridge with zero vertical step.
Holder projection is toward the screen; the pen remains parallel to the long edge.
Device sizes are from the official sources above. Case allowances are provisional.
