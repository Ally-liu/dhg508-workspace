# maintain.md — 怎么加行/复核

## 加一行（步骤）

1. 找到出处文件在 `sources/raw/` 的位置（或先落先存——**没有核对稿的
   引文不许入行**）。
2. 在 `sources/processed/records.json` 给新行用一个新 id（首字母标记来源
   系，如 E=恽录、D=戴逸/科学、T=十叶野闻、U=外围证言、V=总评、
   G=国闻备乘、X=官方转述），字段：id / source / date_orig / date_iso /
   kind / tier / stance / text / note。**source 字段只能填一个 id**——
   上下游关系写进 note（如"经由 S2 转引，底本 S4"）。
3. 若该行与已有行构成矛盾，登记 `contradict_pairs`（新 pair 编号）。
4. `py code/build_db.py` 重建；`PRAGMA foreign_key_check` 必须空。
5. 在 `research/journal/research_journal.md` 记一行"新行 id + 一句话理由"。

## tier 与 stance 的判级

- **L1**：原件/影印在手（目前全库没有——把握住在手就升）。
- **L2**：可靠出版全文或一手转录在手（恽录、国闻备乘、十叶野闻、
  清稗类钞、戴逸期刊 PDF、CCTV 报道）。
- **L3**：只在二手转述中见过（澄斋日记、起居注、屈桂庭、载沣日记、
  外国报纸）。L3 行加「仅见转述」注。
  升级路径固定：找到原件/原刊 → 换 source 指向 → tier 改 L1/L2 →
  note 记录升级。
- **stance**：official（官方文书/脉案/起居注）/ private（日记、笔记、
  回忆）/ press（报刊）/ science（检测报告）/ foreign（外国使馆、外报）/
  academic（现代史学）。一个人写的东西，立场以"写给谁看、凭什么立足"
  判，不以结论好坏判。

## 复核一件行（抽检制度）

- 每次加批后抽 ≥3 行对照 sources/raw 原文逐字核。
- 错误（日期、人名、字句）当场修正并在 journal 记"发现→修正"。
- 已确认过的错误：D08 日期（1898 非 1908）、D02/D12 复合 source_id、
  U06 date_iso 写错年份（已各自修）。新 Myers出错误照此办理。