# 茶功能活性 / 影响因素 / 数据库-知识图谱 调研备忘

更新时间：2026-03-31  
主题：围绕“茶、茶提取物、茶成分的功能活性及受什么影响”，评估建立数据库/知识图谱（KG）的研究潜力、创新性、可行性，并给出可执行 idea。

## 1. 结论先行

这个方向有潜力，而且在“数据库/知识图谱”这一层面具有明显创新空间。

原因不是“茶功能活性”本身新，而是：

1. 2022-2025 年关于茶活性、加工影响、提取工艺、肠道菌群、生物利用度的综述和实验研究很多，说明数据源足够丰富。
2. 但截至 2026-03-31，我能确认到的茶领域数据库/KG 论文很少，且现有工作主要集中在“风险物质”或“基因组/转录组”层面，并没有形成一个以“茶成分-加工/品种/环境-功能活性-机制-证据等级”为中心的知识系统。
3. 因此，若项目定位为“Tea Functional Bioactivity Database / Knowledge Graph”，创新点应放在“跨层整合”和“可推理应用”，而不是只做文献汇编。

## 2. 研究目标重述

建议把长期目标定义为：

“构建一个面向茶功能活性研究的结构化知识基础设施，将茶类型、茶提取物、单体成分、加工方式、环境与原料因素、实验模型、功能活性、作用机制、剂量/暴露和证据强度进行统一表示，并支持检索、证据追踪和新假设生成。”

这比“做一个茶数据库”更有研究价值，因为它直接对应：

- 文献检索低效
- 不同茶类与不同成分之间证据碎片化
- 体外 / 动物 / 人群证据难以对齐
- 加工、品种、产地、发酵、提取方式对活性的影响难以系统比较
- 缺少面向下游应用的机器可读知识层

## 3. 2022-2026 关键论文分类

说明：以下按 `综述`、`代表方法/资源`、`最新进展` 分类。  
其中“最新进展”主要是 2024-2025；截至 2026-03-31，没有检索到足够成熟、被广泛引用的 2026 年同主题旗舰论文。

### 3.1 综述类

1. **Luo Q, et al. 2024. _Biological potential and mechanisms of Tea's bioactive compounds: An Updated review._ Journal of Advanced Research. DOI: 10.1016/j.jare.2023.12.004. PMID: 38056775**
   - 核心贡献：系统归纳茶多酚、氨基酸、多糖、生物碱、萜类、矿物质等主要活性成分及其抗癌、抗氧化、抗炎、抗糖尿病、抗肥胖、心血管保护、菌群调节等机制。
   - 局限：以叙述性整合为主，证据等级没有统一量化；没有把“成分-工艺-活性-机制-模型”做成结构化框架。

2. **Raghunath S, et al. 2023. _Processing Technologies for the Extraction of Value-Added Bioactive Compounds from Tea._ Food Engineering Reviews. DOI: 10.1007/s12393-023-09338-2. PMID: 40477896**
   - 核心贡献：总结超声、微波、超临界 CO2、脉冲电场、加压液体等提取技术对茶活性物质回收效率的影响。
   - 局限：重点在工艺综述，不涉及后续生物活性证据整合；不同研究间参数不可直接比较。

3. **Aaqil M, et al. 2023. _Tea Harvesting and Processing Techniques and Its Effect on Phytochemical Profile and Final Quality of Black Tea: A Review._ Foods. DOI: 10.3390/foods12244467. PMID: 38137271**
   - 核心贡献：把采摘、萎凋、揉捻、发酵、干燥、储藏等环节与黑茶/红茶品质和植物化学成分变化联系起来。
   - 局限：偏黑茶工艺；对功能活性终点和机制层面覆盖不深。

4. **Zhao Z, et al. 2024. _Effects of Differently Processed Tea on the Gut Microbiota._ Molecules. DOI: 10.3390/molecules29174020. PMID: 39274868**
   - 核心贡献：明确提出“不同加工类型的茶”会通过差异化成分谱影响肠道菌群，是把“工艺影响因素”与“健康活性”连接起来的重要综述。
   - 局限：多数证据仍来自动物或体外研究；人群证据不足。

5. **Yang M, Zhang X, Yang CS. 2025. _Bioavailability of Tea Polyphenols: A Key Factor in Understanding Their Mechanisms of Action In Vivo and Health Effects._ Journal of Agricultural and Food Chemistry. DOI: 10.1021/acs.jafc.4c09205. PMID: 39920567**
   - 核心贡献：强调茶多酚体内机制解释必须经过“生物利用度/代谢/组织暴露”这一关，纠正仅凭体外活性推断健康功效的常见问题。
   - 局限：聚焦多酚，不覆盖茶多糖、茶氨酸、挥发性成分等全谱成分。

6. **Rashwan AK, et al. 2025. _Recent advances in chemical characterization, emerging applications, and biological activities of tea polysaccharides and their conjugates from leaves and flowers: A review._ International Journal of Biological Macromolecules. DOI: 10.1016/j.ijbiomac.2025.147540. PMID: 40930359**
   - 核心贡献：把茶多糖/缀合物的化学表征、加工变化、应用场景与生物活性串起来，补足“非多酚成分”维度。
   - 局限：仍然缺少跨茶类、跨提取流程、跨模型的标准化比较。

### 3.2 代表方法 / 资源类

1. **Wang Y, et al. 2023. _TRSRD: a database for research on risky substances in tea using natural language processing and knowledge graph-based techniques._ Database (Oxford). DOI: 10.1093/database/baad031**
   - 核心贡献：这是我目前确认到最接近“茶知识图谱”的工作。作者从 PubMed 文本挖掘出茶风险物质文献，构建了包含 4189 个节点和 9400 条关系的 Neo4j 图数据库。
   - 局限：主题是“风险物质/安全性”，不是“功能活性”；关系类型较粗，更多是文献归档和可视化，而非面向机制和证据推理。

2. **An Y, et al. 2022. _TeaPVs: a comprehensive genomic variation database for tea plant (Camellia sinensis)._ BMC Plant Biology. DOI: 10.1186/s12870-022-03901-5. PMID: 36324064**
   - 核心贡献：整合重测序、转录组和 F1 群体数据，提供茶树基因变异数据库，是茶领域数据平台建设的重要基础。
   - 局限：属于基因组变异资源，不直接回答“哪种茶成分在何种条件下产生何种功能活性”。

3. **Zheng X, et al. 2024. _Comparative transcriptome database for Camellia sinensis reveals genes related to the cold sensitivity and albino mechanism of 'Anji Baicha'._ Physiologia Plantarum. DOI: 10.1111/ppl.14474. PMID: 39139072**
   - 核心贡献：提供 TeaNekT，比对多个茶树品种转录组，支持功能预测和品种差异分析。
   - 局限：仍然主要服务育种/分子机制，不是面向茶功能活性证据整合的数据库。

4. **Wang J, Li Z. 2024. _Effects of processing technology on tea quality analyzed using high-resolution mass spectrometry-based metabolomics._ Food Chemistry. DOI: 10.1016/j.foodchem.2024.138548. PMID: 38277939**
   - 核心贡献：用高分辨质谱代谢组比较不同杀青工艺对成分谱和味觉相关特征的影响，是“加工因素 -> 成分变化”这条边的代表方法。
   - 局限：主要是成分层和感官层，尚未直接外推到健康活性。

5. **Taneja SB, et al. 2023. _Developing a Knowledge Graph for Pharmacokinetic Natural Product-Drug Interactions._ Journal of Biomedical Informatics. DOI: 10.1016/j.jbi.2023.104341. PMID: 36933632**
   - 核心贡献：虽然不是茶领域，但它证明了“天然产物-药代-相互作用”可以用 KG 方式组织，并可作为茶功能活性 KG 的方法学模板。
   - 局限：领域迁移需要重新设计本体和证据规则。

### 3.3 最新进展类

1. **Song Z, Ho CT, Zhang X. 2024. _Gut Microbiota Mediate the Neuroprotective Effect of Oolong Tea Polyphenols in Cognitive Impairment Induced by Circadian Rhythm Disorder._ Journal of Agricultural and Food Chemistry. DOI: 10.1021/acs.jafc.4c01922. PMID: 38745351**
   - 核心贡献：把乌龙茶多酚、肠道菌群和认知保护关联起来，体现“成分-菌群-机制-表型”的链式证据。
   - 局限：仍是特定模型体系，外推到人群需要谨慎。

2. **Tian B, et al. 2024. _Tea Polyphenols Reduced Obesity by Modulating Gut Microbiota-SCFAs-Barrier and Inflammation in High-Fat Diet-Induced Mice._ Molecular Nutrition & Food Research. DOI: 10.1002/mnfr.202400685. PMID: 39574401**
   - 核心贡献：提供了“多酚 -> 菌群/短链脂肪酸/肠屏障/炎症 -> 肥胖表型”的多跳机制证据。
   - 局限：证据链完整但仍是小鼠研究，剂量与人群暴露匹配问题未完全解决。

3. **Zhang R, et al. 2024. _Harnessing the Power of Fermented Tea to Improve Gut Microbiota and Combat Obesity Epidemic._ Biology. DOI: 10.3390/biology13100779. PMID: 39452088**
   - 核心贡献：把发酵茶作为功能食品/微生态干预对象重新归纳，提示“发酵类型”是数据库中必须建模的关键影响因素。
   - 局限：以综述为主，人群干预数据有限。

4. **Kim Y, Je Y. 2024. _Tea consumption and risk of all-cause, cardiovascular disease, and cancer mortality: a meta-analysis of thirty-eight prospective cohort data sets._ Epidemiology and Health. DOI: 10.4178/epih.e2024056. PMID: 38938012**
   - 核心贡献：提供了较高证据层级的人群结局整合，适合作为 KG 中“证据等级/人群层”节点的来源。
   - 局限：暴露定义多为“饮茶量”，对茶类、提取方式、成分组成分辨率低。

5. **Arce-López B, et al. 2025. _Effect of fiber-modified kombucha tea on gut microbiota in healthy population: A randomized controlled trial (RCT)._ Current Research in Food Science. DOI: 10.1016/j.crfs.2025.101130. PMID: 40689297**
   - 核心贡献：说明“茶基发酵饮品 + 人体菌群干预”已经进入随机对照试验层面，提示未来数据库可扩展到茶衍生功能饮品。
   - 局限：并非传统茶叶单一体系，外源纤维改性会带来混杂。

## 4. 文献综述提纲

题目建议：**茶、茶提取物及茶成分功能活性与影响因素：从证据整合到数据库/知识图谱构建**

### 4.1 研究问题

1. 茶中哪些成分或提取物具有可重复的功能活性证据？
2. 这些功能活性受哪些因素影响？
3. 哪些影响因素作用于“成分丰度”，哪些作用于“生物利用度/机制/终点效应”？
4. 不同证据层级（体外、动物、临床、流行病学）之间是否一致？
5. 现有数据库为什么还不能支持系统回答这些问题？
6. 如何构建一个可扩展、可追踪证据来源、可支持推理的茶功能活性知识图谱？

### 4.2 方法类别

1. **化学成分表征**
   - LC-MS/MS
   - GC-MS
   - 非靶向 / 靶向代谢组
   - 化学计量学

2. **加工与制备研究**
   - 采摘标准、品种、季节、产地
   - 杀青、揉捻、发酵、干燥、储藏
   - 超声、微波、超临界、脉冲电场等提取工艺

3. **功能活性研究**
   - 抗氧化 / 抗炎 / 抗癌 / 抗肥胖 / 代谢调节 / 心血管保护
   - 神经保护
   - 肠道菌群调节

4. **生物利用度与转化研究**
   - 吸收 / 代谢 / 组织分布
   - 肠道菌群转化
   - 结合态 / 聚合态成分活性折损

5. **证据整合与数据建模**
   - 文本挖掘
   - 本体设计
   - 实体标准化
   - 知识图谱与图数据库
   - 文献证据评分

### 4.3 争议点

1. **体外强活性不等于体内有效**
   - 多酚特别明显，生物利用度低、代谢快，导致很多机制推断偏乐观。

2. **“茶”不是单一暴露**
   - 绿茶、红茶、乌龙茶、白茶、黑茶、发酵茶在成分谱上差异很大，不能简单合并。

3. **加工影响与品种影响经常混杂**
   - 同一活性差异到底来自品种、环境、加工还是提取工艺，文献常未完全解耦。

4. **终点异质性高**
   - “抗氧化”“改善菌群”“代谢改善”往往用不同指标定义，难直接横向比较。

5. **人群证据分辨率不足**
   - 许多队列/Meta 只有饮茶频率或总量，没有成分和工艺层级信息。

### 4.4 未来方向

1. 从“单成分功效”转向“成分谱 + 加工谱 + 生物利用度 + 菌群转化”的系统研究。
2. 建立统一证据模型，区分体外、动物、临床、流行病学证据强弱。
3. 建立茶领域标准化术语体系和本体。
4. 发展可更新的文献挖掘管线，而非一次性人工汇编。
5. 将知识图谱用于假设生成、实验优先级排序和产品开发。

## 5. 创新性判断

### 5.1 为什么有创新性

如果你做的是下面这个版本，创新性是成立的：

“把茶功能活性相关证据从分散文献中抽取出来，统一成一个可计算的知识层，显式表示成分、加工、品种、环境、提取、活性、机制、证据等级之间的关系，并支持图查询和假设生成。”

创新点主要来自：

1. **问题定义新**：从“茶的活性研究”升级为“茶功能活性知识基础设施”。
2. **对象整合新**：把加工影响因素、生物利用度、菌群转化、人群证据放在一个框架里。
3. **方法组合新**：NLP + 实体标准化 + 本体设计 + KG + 证据评分。
4. **应用价值强**：可直接服务综述写作、课题设计、产品开发、健康声称证据梳理。

### 5.2 哪些做法不够新

1. 只做 Excel 文献汇总。
2. 只收集茶成分，不连接活性与证据。
3. 只做 Neo4j 可视化，不做关系规范和证据约束。
4. 只复刻 TRSRD 的“茶主题 KG”，但没有切换到功能活性和影响因素中心。

## 6. 可行性判断

### 6.1 可行性高的原因

1. 文献量充足，尤其 2022-2025 的综述和实验论文已能支撑 schema 设计。
2. 茶领域实体边界相对明确，适合做本体：
   - 茶类
   - 茶样本
   - 提取物
   - 单体成分
   - 工艺步骤
   - 环境/产地/品种
   - 活性终点
   - 机制通路
   - 证据类型
3. 已有相邻资源可借鉴：
   - TRSRD（茶主题 KG）
   - TeaPVs / TeaNekT（茶领域数据库）
   - NPASS（天然产物活性数据库）
   - 自然产物药代相互作用 KG

### 6.2 真正的难点

1. **命名标准化**
   - 同一成分可能有别名、异构体、不同盐型或缩写。

2. **证据异质性**
   - 同一种活性在不同模型下结论和效应量不同。

3. **影响因素多跳传递**
   - 例如“杀青方式 -> 儿茶素谱变化 -> 生物利用度变化 -> 肠道菌群变化 -> 肥胖改善”，不是简单二元关系。

4. **自动抽取准确率**
   - 全自动 NLP 很难一步到位，需要“规则 + LLM/模型 + 人工校验”混合流程。

## 7. 最值得做的 idea

### Idea 1. TeaBioAct-KG

构建一个面向功能活性的茶知识图谱。

核心实体：

- TeaType
- Cultivar
- Origin / Environment
- ProcessingStep
- ExtractionMethod
- Extract
- Compound
- Bioactivity
- Mechanism
- ModelSystem
- Outcome
- EvidenceLevel
- PMID / DOI

核心关系：

- `contains`
- `enriched_by`
- `altered_by`
- `extracted_by`
- `shows_activity`
- `supported_by`
- `acts_via`
- `validated_in`
- `limited_by`

最适合发论文的点：

- 提出茶功能活性本体
- 构建半自动抽取流程
- 设计证据评分体系
- 展示若干跨文献发现的多跳路径

### Idea 2. Tea Processing-Bioactivity Atlas

重点不做全 KG，而先做“工艺/加工影响 -> 成分变化 -> 活性变化”的专题数据库。

价值：

- 更聚焦
- 数据抽取更容易
- 容易出第一篇方法论文

适合首期范围：

- 绿茶、乌龙茶、红茶
- 只覆盖多酚、茶氨酸、咖啡因、多糖
- 只覆盖抗氧化、抗炎、菌群调节、代谢改善四类活性

### Idea 3. Evidence-Graded Tea Health Claims Database

按证据等级组织“茶或茶成分是否支持某健康作用”。

层级示例：

- `in vitro`
- `animal`
- `RCT`
- `cohort`
- `meta-analysis`

这个方向更偏转化和产业应用，适合服务功能食品、保健品、健康声称梳理。

### Idea 4. Tea-GutMicrobiome Mechanism Graph

围绕“茶成分-菌群-代谢物-SCFAs-屏障-炎症-代谢疾病/认知”做专题 KG。

优点：

- 2024-2025 文献增长快
- 机制链条清晰
- 适合做图推理和假设生成

## 8. 建议的研究路线

### Phase 1. 缩范围

第一版不要覆盖“所有茶 + 所有活性 + 所有证据”。

建议先选：

- 茶类：绿茶、乌龙茶、红茶
- 成分：儿茶素、茶黄素、茶氨酸、咖啡因、茶多糖
- 活性：抗炎、抗氧化、抗肥胖/代谢、肠道菌群调节
- 影响因素：品种、产地、季节、加工、提取方法

### Phase 2. 建 schema

先设计最小可用 schema，而不是先爬所有文献。

### Phase 3. 小样本人工标注

选 100-200 篇高价值文献建立 gold set，用于：

- 定义实体边界
- 统一关系类型
- 制定证据评分规则

### Phase 4. 半自动扩展

用 PubMed + Crossref + 全文摘要抽取，人工抽检。

### Phase 5. 输出形式

至少产出：

1. 一个结构化数据库
2. 一个图数据库接口
3. 一篇方法/资源论文
4. 一个案例研究，例如“发酵茶-菌群-肥胖”或“加工方式-儿茶素谱-抗氧化”

## 9. 我对选题的判断

### 值得做

值得做，前提是你把项目定位成“茶功能活性知识基础设施”而不是普通综述或资料库。

### 创新性

中高。  
“茶活性研究”不新；“茶功能活性 + 影响因素 + 证据等级 + KG”这个组合是新的，而且当前茶领域空位明显。

### 可行性

中高。  
第一阶段完全可做；真正风险不在数据有没有，而在于 scope 是否收得住、schema 是否设计得好。

### 最推荐的切入方式

优先推荐：`Idea 2 -> Idea 1`

即：

1. 先做 `Tea Processing-Bioactivity Atlas`
2. 再扩展成 `TeaBioAct-KG`

这样最稳，因为第一步更容易形成高质量数据和首篇论文。

## 10. 参考来源链接

- TRSRD: https://academic.oup.com/database/article/doi/10.1093/database/baad031/7158386
- TeaPVs: https://pubmed.ncbi.nlm.nih.gov/36324064/
- TeaNekT paper: https://pubmed.ncbi.nlm.nih.gov/39139072/
- Updated review: https://pubmed.ncbi.nlm.nih.gov/38056775/
- Extraction review: https://pubmed.ncbi.nlm.nih.gov/40477896/
- Black tea processing review: https://pubmed.ncbi.nlm.nih.gov/38137271/
- Processed tea and gut microbiota review: https://pubmed.ncbi.nlm.nih.gov/39274868/
- Bioavailability review: https://pubmed.ncbi.nlm.nih.gov/39920567/
- Tea polysaccharide review: https://pubmed.ncbi.nlm.nih.gov/40930359/
- HRMS metabolomics processing study: https://pubmed.ncbi.nlm.nih.gov/38277939/
- Oolong tea polyphenol neuroprotection study: https://pubmed.ncbi.nlm.nih.gov/38745351/
- Obesity / microbiota mechanistic study: https://pubmed.ncbi.nlm.nih.gov/39574401/
- Fermented tea and gut microbiota review: https://pubmed.ncbi.nlm.nih.gov/39452088/
- Mortality meta-analysis: https://pubmed.ncbi.nlm.nih.gov/38938012/
- Natural product-drug interaction KG: https://pubmed.ncbi.nlm.nih.gov/36933632/
- NPASS 2023 update: https://pubmed.ncbi.nlm.nih.gov/36624664/
