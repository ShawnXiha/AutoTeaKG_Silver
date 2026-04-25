# AutoTeaKG-Silver 48 条验证样本标注指南（本科生版）

## 1. 这项标注要做什么

你需要检查模型自动抽取的 48 条证据记录是否基本正确。每条记录来自一篇茶相关论文，Excel 里已经给出标题、摘要、模型抽取的字段，以及需要你填写的判断列。

请注意：你不是在判断“茶有没有效果”，而是在判断“模型有没有把论文里的信息抽对”。

## 2. 每条记录看哪些内容

优先看这几列：

1. `title`：论文标题。
2. `abstract`：论文摘要，是最重要的判断依据。
3. `claim_text_raw`：模型认为最关键的一句话。
4. 以 `_model` 结尾的列：模型抽取结果。
5. 以 `_decision` 结尾的列：你要填写是否正确。
6. 以 `_corrected` 结尾的列：如果模型错了，你填写更正值。

## 3. decision 怎么填

每个字段的 decision 只能填下面四种：

- `correct`：模型抽取基本正确。
- `minor_issue`：方向对，但不够精确。例如机制写得太宽泛，但没有乱编。
- `major_issue`：明显错误。例如动物实验被写成人体研究，或者机制是摘要里没有的。
- `not_applicable`：这篇论文没有报告这个字段，或这个字段不适用。

## 4. overall_record_decision 怎么填

- `accept`：整体可以接受，最多有很小问题。
- `accept_with_correction`：有问题，但通过更正字段可以保留。
- `reject`：这条记录整体不可靠，建议不要进入高质量分析。

## 5. 各字段怎么判断

### activity_category

看这条证据说的是哪类功能。常见类别：

- `anti-inflammatory`：抗炎、降低炎症因子、炎症损伤减轻。
- `antioxidant`：抗氧化、ROS、MDA、GSH、SOD 等。
- `gut microbiota modulation`：肠道菌群、Akkermansia、Lactobacillus、SCFAs 等。
- `anti-obesity`：体重、脂肪、肥胖、产热。
- `metabolic improvement`：血糖、胰岛素抵抗、NAFLD、脂质代谢。
- `neuroprotection`：认知、神经炎症、脑损伤。
- `cardiovascular protection`：心血管风险、动脉粥样硬化、死亡率。
- `other`：不属于上面类别，或模型没法归类。

### study_type

看研究类型：

- `animal study`：小鼠、大鼠等动物实验。
- `in vitro`：细胞或体外实验。
- `randomized controlled trial`：随机对照人体试验。
- `cohort study`：队列或观察性人群研究。
- `meta-analysis`：荟萃分析。
- `systematic review`：系统综述或普通综述。

### evidence_level

通常由 study_type 推出：

- 动物实验：`preclinical_in_vivo`
- 体外实验：`low_preclinical` 或 `in_vitro`
- 人体干预：`human_interventional`
- 人群观察：`human_observational`
- meta-analysis：`evidence_synthesis`
- review：`evidence_synthesis_nonquantitative`

### component_group

看研究对象是什么成分：

- EGCG、catechin：`catechins`
- tea polyphenols：`mixed polyphenols`
- tea polysaccharides、TPS：`tea polysaccharides`
- caffeine：`caffeine`
- theanine：`theanine`
- theaflavins：`theaflavins`
- tea extract：`whole extract`

### processing_step

只在论文明确提到茶材料加工时填写。例如：

- fermentation / fermented tea：发酵
- roasting：烘焙
- drying：干燥
- steaming / fixation：蒸青、杀青

如果摘要只是说 disease aging、middle-aged、freeze-dried sperm 这类不是茶加工，不要算 processing。

### extraction_method

只在论文明确提到提取或制备方法时填写。例如：

- water extract / aqueous extract：水提
- ethanol extraction：乙醇提取
- ultrasound extraction：超声提取
- infusion / brewing：冲泡
- isolation / purification：分离纯化

如果没有提到，就填 `not_applicable` 或留 corrected 空。

### mechanism_label

看模型写的机制是否在摘要里有依据。例如：

- SCFA-mediated JAK2/STAT3 signaling
- gut-liver axis
- barrier function
- NF-kB / MAPK / Nrf2 pathway

如果机制太宽泛但方向对，可以填 `minor_issue`。如果摘要里完全没有这个机制，就是 `major_issue`。

## 6. comments 怎么写

简单写清楚原因即可，例如：

- “摘要明确写了 mice，应为 animal study。”
- “摘要没有提取方法，extraction 应为 not_applicable。”
- “机制方向正确，但 JAK2/STAT3 只在摘要最后一句出现。”

## 7. 工作建议

每条记录建议 2-4 分钟。先看标题和 claim_text_raw，再看摘要中相关句子。不要查太多外部资料，除非摘要确实看不懂。
