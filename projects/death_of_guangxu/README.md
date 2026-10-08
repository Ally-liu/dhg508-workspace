# The Death of Guangxu (光绪之死)

1908-11-14 光绪帝崩于瀛台涵元殿，次日慈禧亦崩——相隔不足二十四小时，
成为近代中国最著名的悬案之一。本项目把它做成一个**交互式证据探索**：
不是讲一个猎奇故事，而是把散落的记载收进数据库、让体验者阅读互相矛盾的证据、
对最后几天做推测、模型只依据库内证据行追问，最后提交自己的判决。

## 单人项目

DHG508 期末作业。原不发期末 brief 时以 Week 1–5 练习积累的全套
流程（OCR → 带 source 的关系库 → 渐进式 skill → 真 DeepSeek 的 web app）
直接迁移为本项目的技术底座。

## 一句话命题

> 悬案的价值不在"谁是凶手"，而在"我们凭什么相信一件事"。
> 底层事实（是否砒霜中毒）可以有硬结论；上层归因（谁的手）永远开放。

## 结构

- `research/` 设计文档、日志、笔记、参考文献
- `sources/raw/` 原件或原始文本（脉案影印、实录、日记、报刊、检测论文）
- `sources/processed/` 转写与 OCR 结果，每行带 source
- `artifacts/guangxu.db` 由 `code/build_db.py` 生成，不进 Git
- `code/` 数据管线与 web app（Python server + 一页 HTML/JS）
- `skills/` 渐进式 skill：`SKILL.md` 索引 + answering / maintain / principles

## 状态

- [x] 项目 scaffold
- [ ] 设计文档 v1
- [ ] 证据开采第一批：30+ 条带 source 的证据行，二次文献核对
- [ ] schema 定稿（events / evidence / hypotheses / verdicts 等）
- [ ] 三幕交互手绘稿与文案
- [ ] build_db.py 与 records.json
- [ ] skill（索引 + answering/maintain/principles）
- [ ] server + 页面（真 DeepSeek 交叉讯问）
- [ ] 视觉：档案原件视觉化 + 瀛台静帧（Blender 预渲染，可选）
- [ ] 检验题集与改进日志
