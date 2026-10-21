# Project Design Document

## Project Title

圆明园大水法重建：有据图像 vs 凭空图像，并转 3D
(Yuanmingyuan Dashuifa: a sourced image vs. a guess, then 3D)

## Project Files

- [Research Journal](../journal/research_journal.md)
- [Source Manifest](../../sources/processed/source-manifest.md)

## Background and Context

圆明园西洋楼（European-style "Western Mansions", 谐奇趣、海晏堂、大水法、远瀛观一带）
由清廷在乾隆年间（18 世纪）营造，设计参与者的欧洲传教士（如郎世宁 Castiglione、
王致诚 Attiret、蒋友仁 Benoist 掌管喷泉机械）留下图版与记述。1860 年英法联军焚园，
大水法一带此后长期是废墟，今以残迹闻名。因此它天然有"有历史"的两端：**建成时的样子**
与**毁后的样子**——本作业取**毁前（1860 前）**。

## Research Questions

1. 大水法（及其背景远瀛观）在 1860 年前的形式、材料、比例是什么？
2. 哪些资料足以把这些细节做对？哪些细节资料不足、只能靠推测？
3. 有据图像与"仅凭文字描述"的图像，差异具体在哪几处？
4. 生成器在两种做法里分别**编造**了什么？

## Scope

- **In scope:** 大水法本体（石制大水法/喷水池）+ 远瀛观立面 + 周边台阶与平台；
  毁前状态。
- **Out of scope:** 整座西洋楼群、园林植物细部（除非作为背景）、1860 后废墟状态。

## Methodology

1. **收集资料**：图版（西洋楼铜版画）、老照片（如汤姆森、奥尔末）、文字记述。
   每份留原件 + 完整引用，登记到 source-manifest。
2. **做对照图**：
   - A 图：把资料里的形式、构件、比例写成结构化提示词后生成。
   - B 图：只写一句"圆明园的一座欧式喷泉"，模拟无资料者。
   - 并排，逐项回答设计问题 1–3。
3. **转 3D**：路线待定（Blender agent / image-to-3D 服务，如 Tripo）。
   细节构件（券口、栏杆、水盘）单独做再拼装。
4. **第 4 步用途**：待定（短片/动画/场景嵌入）。

## Sources

见 [source-manifest.md](../../sources/processed/source-manifest.md)。优先一手图版，
老照片作辅助（注意其多为废墟状态，不能直接当"毁前"证据）。

## Expected Outputs

- `research/outputs/`：A/B 两张对照图 + 说明文字。
- `artifacts/`：3D 模型文件、渲染截图/录屏（git 忽略）。
- 工具日志（prompt、输入、输出、花费）。

## Working Hypotheses

- 图版能让 A 图在**立面构成、拱券、栏杆层次**上明显更准。
- B 图会给出泛化的"欧式喷泉"，缺少大水法特有的阶梯式水法与远瀛观背景。
- 两张图都会在**纹理、植被、比例**上编造。

## Risks and Open Questions

- 铜版画是线描（无摄影），颜色与材质仍属推断——需在答案里标注。
- 老照片多为 1860 后废墟，不能混作"毁前"依据，须区分。
- 若无法运行 Blender：改用 image-to-3D（Tripo/Hunyuan3D）即可，满足要求。
- 服务收费未知，使用前先查价并留收据。

## Action Items

- [x] 收集西洋楼铜版画中"大水法/远瀛观"图版（第 14/15/16 幅），存 `sources/raw/` 并引用。
- [x] 收集相关老照片（Ohlmer 约1873"远瀛观南面"），标注拍摄者/年代/馆藏。
- [x] 写 source-manifest（区分毁前证据 / 废墟证据）。
- [ ] 生成 A 图（有据）与 B 图（凭空），并排导出到 `research/outputs/`。
- [ ] 回答三个对照问题。
- [ ] 选 image-to-3D 路线，产出 3D 模型。
- [ ] 第 4 步用途。
- [ ] 工具日志 + 至少一个真实困难。
