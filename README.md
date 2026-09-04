# 数学奥林匹克学术视觉与数字化系统工坊 (Mathematics Olympiad Visual Suite)

> 汇聚全国及区域数学奥林匹克竞赛的顶尖数字化设计、学术聘书与品牌视觉系统。  
> Academic visual identity, digital credentials, and industrial vector systems for Mathematical Olympiads.

---

## 📁 核心项目导航 (Repository Projects)

| 项目名称 | 核心主题 | 访问入口 | 交付成果 |
| :--- | :--- | :--- | :--- |
| **01. 北方奥赛命题专家聘任证书** | 第二十一届北方数学奥林匹克命题专家聘任证书交互重构版 | [`./index.html`](./index.html) | 全浅色羊皮白、3D 物理翻转、冷烫金流光、矢量朱砂印鉴、A4 矢量打印 |
| **02. 高中数学奥林匹克启航联盟** | 启航联盟「拓扑之帆 · 莫比乌斯无限」全套 VI 与工程落地 | [`./qihang-alliance-logo/index.html`](./qihang-alliance-logo/index.html) | 纯净母标系统、72×24mm 官方金属胸牌、25mm 纪念徽章、6 大实拍画廊、生产级 SVG 包 |

---

## 💎 项目一：高中数学奥林匹克启航联盟视觉系统 (`qihang-alliance-logo/`)

- **设计理念**：以**莫比乌斯曲面拓扑环**与**领航之帆**为图腾，融入欧拉常数香槟金与高维极光电紫，彻底摒弃多余虚线与行业陈词滥调。
- **实物落地保障**：包含西装翻领实物金属胸牌、官方深紫天鹅绒授牌礼盒、全国奥赛纯金珐琅奖章、全国统考试卷与精装论文集、学术峰会万人大礼堂钛合金发光大屏、国家集训营刺绣卫衣。所有场景 100% 吻合矢量母标。
- **生产级工程矢量**：
  - `qihang-alliance-logo/vector_exports/HSMO_Logo_Clean_Primary.svg` (全彩母标)
  - `qihang-alliance-logo/vector_exports/HSMO_Logo_Monochrome.svg` (单色试卷)
  - `qihang-alliance-logo/vector_exports/HSMO_Lapel_Nameplate_72x24.svg` (72×24mm 金属胸牌)
  - `qihang-alliance-logo/vector_exports/HSMO_Round_Lapel_Pin_25mm.svg` (25mm 圆形徽章)
- **子目录详情**：详见 [`qihang-alliance-logo/README.md`](./qihang-alliance-logo/README.md)。

---

## 📜 项目二：第二十一届北方数学奥林匹克专家聘任证书 (`./`)

- **设计规范**：采用温润纯棉羊皮白底色，结合斐波那契对数螺旋防伪底纹与专属正多面体晶体桂冠金徽。
- **交互与功能**：支持正反双面拟真 3D 翻转、冷烫金漫反射流光、实时在线编辑专家档案与一键导出 A4 印刷标准 PDF。

---

## 🚀 运行方式 (Quick Start)

双击直接在任意浏览器中打开对应网页即可流畅体验：
```bash
# 体验项目一：高中数学奥林匹克启航联盟视觉门户
open qihang-alliance-logo/index.html

# 体验项目二：第二十一届北方奥林匹克命题专家聘书
open index.html
```

---

## 🛠️ 技术与实现 (Tech Stack)

- **图形与排版**：原生标准 HTML5 + 纯矢量 SVG，零第三方外部库依赖
- **视觉引擎**：CSS3 3D Matrix, Perspective Flip, Specular Reflection Lighting, Backdrop Filters
- **工程标准**：满足印刷制版（Pantone 专色）、激光线切割、五轴 CNC 雕刻与金属冲压模具要求
