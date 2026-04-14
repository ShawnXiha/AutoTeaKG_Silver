---
title: "AutoTeaKG-Silver 项目汇报"
subtitle: "茶功能活性文献的自动化证据图谱、论文产出与下一步计划"
author: "项目内部汇报"
date: "2026-04-14"
---

# AutoTeaKG-Silver 项目汇报

# 一、项目一句话

AutoTeaKG-Silver 是一个围绕茶、茶提取物、茶成分及其功能活性的自动化证据图谱项目。它的核心目标不是直接证明“茶有什么神奇功效”，而是把分散在 PubMed 文献中的研究证据整理成可查询、可追溯、可更新、带不确定性标注的证据地图。

换句话说，这个项目把问题从“茶有没有某种作用”推进到更科学的问题：

- 哪些论文支持这个说法？
- 这些证据来自动物实验、人体研究还是综述？
- 研究用的是哪类茶、哪类成分、哪种提取物？
- 是否报告了加工、发酵、提取等关键上下文？
- 这个证据路径的不确定性有多高？

# 二、这个项目有什么用

## 2.1 支撑资源型论文和数据库论文

茶功能活性研究很多，但目前缺少一个围绕“功能活性证据”的结构化资源。已有茶数据库更多集中在基因组、转录组、品种资源或风险物质层面，而不是系统整理“茶类型—成分—加工/提取—功能活性—证据等级—机制”的证据链。

AutoTeaKG-Silver 可以作为资源型数据库论文的主体，重点贡献不是某一个单独算法，而是一个可复现的证据基础设施：

- 自动检索和整理 PubMed 茶功能活性文献；
- 将论文转成标准化 evidence records；
- 明确区分证据等级；
- 加入加工和提取上下文；
- 形成可查询的知识图谱；
- 保留每条关系的来源和不确定性。

## 2.2 支撑综述写作和课题设计

传统综述依赖人工阅读和手工归纳，效率低、更新慢，而且容易把不同证据层级混在一起。AutoTeaKG-Silver 可以快速回答：

- 哪些方向主要是动物实验，哪些方向已经有人群证据？
- 哪些茶成分和肠道菌群机制联系更密集？
- 哪些研究缺少加工或提取信息？
- 哪些主题适合做后续实验或项目申请？

这对综述、开题、基金申请和实验选题都有直接帮助。

## 2.3 支撑产品或健康声称证据梳理

如果后续涉及茶相关功能食品、提取物或产品开发，这类图谱可以帮助做初步证据梳理。它不能替代临床证据，也不能直接作为健康声称依据，但可以帮助团队快速判断：

- 某个成分或茶类型已有多少相关证据；
- 证据主要集中在哪些终点；
- 是否有人体研究；
- 机制证据是否集中在肠道菌群、炎症、氧化应激或代谢通路；
- 哪些说法仍然证据不足。

# 三、当前已经完成了什么

当前项目已经从 ideation 走到完整原型阶段，主要产物包括数据、图谱、论文、前端和汇报材料。

| 类别 | 当前状态 |
|---|---|
| PubMed 检索 | 已固定检索式、检索日期和检索结果归档 |
| 自动标注 | 已完成 GLM5 自动抽取和后处理 |
| KG v3 | 已完成最终方法级归一化图谱 |
| 前端展示 | 已完成静态 KG explorer |
| 论文草稿 | 已完成 Database-oriented v6 |
| PPT | 已完成普通观众版和老板汇报版 |
| GitHub | 已推送至 `git@github.com:ShawnXiha/AutoTeaKG_Silver.git` |

当前核心数据规模如下：

| 指标 | 数量 |
|---|---:|
| Silver evidence records | 635 |
| KG nodes | 1,989 |
| KG edges | 8,195 |
| Microbiome-relevant records | 190 |
| Records with processing context | 183 |
| Records with extraction context | 185 |
| Low-uncertainty records | 100 |
| Moderate-uncertainty records | 470 |
| High-uncertainty records | 65 |
| Residual missing-context records | 303 |

# 四、创新点

## 4.1 不是普通文献汇总，而是 evidence graph

普通综述或 Excel 表通常只记录论文题目、结论和关键词。AutoTeaKG-Silver 把每篇文献拆成结构化 evidence records，并把证据连接到活动类别、成分、茶类型、研究类型、证据等级、机制和不确定性。

这使得文献综述从“人工读后总结”变成“可查询证据结构”。

## 4.2 显式区分证据等级，避免过度解读

茶功能活性研究中，动物实验、细胞实验、人群观察、随机试验、综述常被混在一起讨论。AutoTeaKG-Silver 将 evidence level 作为图谱属性保留，使研究者可以筛选：

- 只看人群证据；
- 只看动物机制；
- 区分综述总结和原始实验；
- 避免把 preclinical 结果过度解释为人体结论。

## 4.3 把加工/提取上下文作为核心问题

茶不是单一对象。绿茶、红茶、黑茶、乌龙茶、发酵茶、提取物、EGCG、茶多酚、茶多糖等对象差异很大。加工、发酵、提取方法会影响成分和活性解释。

本项目发现加工/提取上下文是当前文献的最大缺口之一：

- processing context 从 146 条提升到 183 条；
- extraction context 从 154 条提升到 185 条；
- 但仍有 303 条记录缺少加工或提取上下文。

这本身就是一个重要科学发现：很多茶功能活性文献的摘要或开放全文没有提供足够工艺信息。

## 4.4 不隐藏不确定性，而是把不确定性建模

自动抽取一定存在不确定性。项目没有假装所有关系都完全正确，而是将不确定性作为图谱的一部分。

当前不确定性分布为：

- low uncertainty：100 条；
- moderate uncertainty：470 条；
- high uncertainty：65 条。

这使得用户可以根据任务需要筛选不同可信度的证据。

## 4.5 支持机制路径查询

图谱不仅能统计数量，还能查询机制路径。例如当前已经做出一个 case study：

茶多糖 → 肠道菌群/SCFAs → 丁酸/短链脂肪酸 → 肝脏炎症、脂质沉积、肠屏障完整性。

这类查询比关键词搜索更有价值，因为它同时保留：

- 成分类别；
- 微生物机制；
- 代谢物；
- 宿主表型；
- 证据等级；
- 不确定性等级；
- PMID 来源。

# 五、能发表什么论文

## 5.1 第一篇：资源/数据库论文

最适合的第一篇论文定位是资源型或数据库型论文，而不是算法论文。

建议题目方向：

> AutoTeaKG-Silver: An Uncertainty-Aware Evidence Graph for Tea Functional Activity Literature

可投方向：

- Database: The Journal of Biological Databases and Curation；
- Scientific Data（需要更像 Data Descriptor）；
- Journal of Biomedical Informatics（需要增强验证和图谱应用）；
- 食品信息学、天然产物信息学或知识图谱相关 workshop。

目前最匹配的是 Database 类型期刊，因为它接受数据库、注释、biocuration、自动/半自动知识组织这类工作。

## 5.2 第二篇：加工/成分上下文抽取方法论文

本项目发现加工/提取上下文是茶文献中的明显缺口。后续可以把 processing/component extractor 单独发展成方法论文或短文。

可能主题：

- 面向食品/天然产物文献的加工过程信息抽取；
- 摘要 vs methods section 中工艺信息可获得性的系统比较；
- LLM + vocabulary normalization 的食品加工上下文抽取框架。

## 5.3 第三篇：茶—肠道菌群机制图谱论文

KG 中已有 190 条 microbiome-relevant records，可以进一步发展成 C06 方向。

可能主题：

- 茶成分—肠道菌群—代谢物—宿主表型机制图谱；
- 茶多糖、茶多酚、发酵茶的微生物机制路径比较；
- 面向实验假设生成的茶微生物机制图谱。

这篇更偏机制发现和生物学解释，适合在第一篇资源论文基础上推进。

# 六、当前论文状态

当前论文已经推进到 Database-oriented v6。

已经具备：

- Abstract；
- Introduction；
- Related Work / prior work and resource gap；
- Materials and Methods；
- Results；
- Discussion；
- Limitations；
- Data and Code Availability；
- LLM Usage Statement；
- Ethics Statement；
- Supplementary Data；
- 图表和 query tables；
- 前端展示。

已经完成的合规项包括：

- 数据和代码可用性声明；
- LLM 使用声明；
- 伦理声明；
- 不确定性模型表格化；
- stage-wise ablation / QC 表；
- graph query case study；
- computational related work 文献扩展。

# 七、主要风险

## 7.1 最大风险：LLM 抽取准确性需要验证

当前图谱是 silver-standard，不是 gold-standard。虽然每条记录都有置信度和不确定性标记，但投稿时审稿人仍然会问：

> 自动抽取到底准不准？

目前已经准备好 48 条分层验证样本：

- low uncertainty：14 条；
- moderate uncertainty：24 条；
- high uncertainty：10 条。

但还需要人工填写 validation worksheet，才能报告字段级准确率。

## 7.2 第二风险：被认为只是工程流水线

应对方式已经部分完成：

- 加入 uncertainty model；
- 加入 stage-wise QC table；
- 加入 graph query case study；
- 加入 computational related work；
- 明确 silver-standard 定位。

但后续仍建议补一张更强的“图谱查询案例”或“验证结果表”。

## 7.3 第三风险：投稿模板和版面

当前 v6 是 Database-oriented 草案，但还不是目标期刊官方模板。后续需要根据目标期刊要求调整：

- 版面；
- supplementary materials；
- 数据可用性格式；
- 图表位置；
- 引用格式；
- 是否需要 cover letter。

# 八、下一步建议

## 8.1 立即完成验证样本

最优先任务是让 1-2 人填写 48 条 validation worksheet。完成后可以生成：

- 字段级准确率；
- accept / accept with correction / reject 比例；
- 低/中/高不确定性分层质量；
- 哪些字段最容易错。

这会显著提高论文可信度。

## 8.2 确定目标期刊

建议优先选择 Database 方向。如果选择 Scientific Data，则需要把论文改写成 Data Descriptor 风格，弱化方法论和讨论部分。

## 8.3 做投稿版 v7

v7 应该围绕目标期刊进行：

- 模板转换；
- supplement 拆分；
- 表格版面精修；
- cover letter；
- data/code availability 按期刊格式重写。

# 九、需要老板支持的事项

1. 确认论文定位：优先资源/数据库论文，而不是算法论文。
2. 安排 1-2 人完成 48 条抽样验证。
3. 确定目标期刊或会议方向。
4. 决定是否继续扩大 full-text extraction 和人工验证规模。
5. 决定是否将前端做成正式在线展示页面。

# 十、结论

AutoTeaKG-Silver 已经具备四类成果：

- 数据和知识图谱；
- 可复现代码；
- 前端展示；
- 论文和汇报材料。

项目当前已经从探索阶段进入投稿前打磨阶段。最关键的下一步不是再扩更多数据，而是补齐字段级验证结果，并围绕目标期刊完成投稿版定稿。
