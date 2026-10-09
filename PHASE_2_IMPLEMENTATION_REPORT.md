# PHASE_2_IMPLEMENTATION_REPORT

**项目：** ContextPass Repository A。**范围：** PHASE 2 — Independent Leader / Validator Consensus。
**结论：** 阶段范围实现及离线验收 PASS；原始 Strict 类型检查 FAIL（7 条 SDK 类型诊断：原有 6 条 + 新接入 API 的 1 条）。不代表真实模型准确率、网络多 Validator 共识或部署验收通过。

## 1. 权威基线与版本

已首先完整阅读 architecture-freeze-v1/ 的 9 个权威文件、Canonical Prompt、测试计划、Phase 0/1 报告、现有合约与 PROJECT_CHECKPOINT。再次核验连接账号为 gqzy1（ID 155161534），Phase 1 PR #1 仍 Draft/open/unmerged，HEAD 精确为 6f498abbf1525f304174ed2018509a4445d441c8。

从该 HEAD 创建 phase2-independent-consensus，保留 Phase 1 分支和 main。实现来源仅本项目权威基线与官方锁定 SDK，未使用旧项目代码。

| 项目 | 实际沿用锁定值 |
|---|---|
| Python / GenVM | 3.12.14 / v0.2.16 |
| 合约 SDK py-genlayer runner | 1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6 |
| SDK stdlib runner | 11rhn002yfajawsz7fai6mykznbxkxs6l91iskj5cm82c92qhy3v |
| SDK cloudpickle runner | 1dlk6mnfabi0z7r39635amyfzw8xb6rm8bv4pmgv6ji1bfx9hghd（Phase 0 已锁定传递依赖） |
| genlayer-test / genvm-linter | 0.29.2 / 0.11.0 |
| pytest / pyright | 9.1.1 / 1.1.414 |
| genlayer-py / web3 | 0.16.3 / 8.0.0（测试工具依赖） |
| genlayer-js | 1.1.8 保留为后续客户端锁定；本轮不开发前端 |

requirements.lock.txt 与 Phase 1 完全相同。Direct Mode 未自动导入已锁定 cloudpickle runner，准备脚本从已验证的官方 SDK 包提取原 runner 并用于测试序列化，未安装另一版本。官方 artifact SHA256 仍为 4f0b358ec98ec148be9b95cdfb0f0e1a6cbe64da0194fdfac3fffc6f5d1d93e2。

## 2. 实现与独立性证据

唯一 _semantic_decision 边界现在调用一次真实 SDK custom gl.vm.run_nondet_unsafe。

1. 在确定性上下文中从已持久化原始 scope/requirement 构建冻结 Prompt。七条规则、marker 和措辞逐字保留，仅移除 Markdown 引用前缀。输入按 JSON 字符串安全编码，并转义 marker 终止字符；用户数据中的模板占位符不会二次替换。
2. Leader 通过 _classify(prompt) 独立调用 SDK exec_prompt，完整分类并返回严格一字段 decision 对象。
3. 每个 Validator 首先独立调用 _classify(prompt)，不调用 Leader 函数，不把 Leader 标签或分析送进 Prompt。随后才检验 SDK Return envelope 和 Leader schema，并确定性精确比较两种标签。
4. 回调仅捕获原始输入形成的不可变 Prompt 字符串，不捕获 self、存储或 Leader 结果，实际由锁定 cloudpickle 序列化通过。
5. raw text 模式保留原始 JSON；拒绝重复键、额外/缺失键、非法标签/类型、数组/标量、Markdown 和伪造 envelope。无输出纠正、格式提取或 fallback approval。
6. Validator 异常/模型错误/格式错误投 False；Leader 异常传播；未接受/未决的 SDK 执行不产生业务拒绝或批准。只有 accepted return 后，确定性路径再验证 schema 并保存根绑定决定。双方独立 NOT_ELIGIBLE 是可接受的明确拒绝，与错误/未决严格区分。

结构与运行证据：tests/consensus/ 检验两回调分别独立分类、同一原始 Prompt、没有方便等价封装或回调状态操作；101 个测试 trace 实际记录 183 次离线 mock 模型调用。N09 多 Validator 用例依次记录 leader、validator-1、validator-2、validator-3，四个 Prompt SHA256 相同，三个独立 vote 为 True；另一个用例后续 Validator 改为相反标签，模拟闸门不返回、存储不变。**这些都是离线脚本化调用和票，不是真实网络 Validator 投票。**

证据：evidence/phase2/consensus-traces.json、all-results.xml、protocol-integrity.json、sdk-custom-gate-source.txt。

## 3. 协议完整性

所有 9 个冻结文件、Phase 0/1 报告与原 Phase 1 证据保留。所有既有存储注解、record AST、构造函数及除 _semantic_decision 外的全部方法 AST 与 Phase 1 相同。仍为 5 writes、6 views、0 constructor args；root-only、one-decision-ever、issuer-only revoke 和受保护留言不变。

合约当前 SHA256：4412035632f586b72c376fb42e618f68ff665063cf356dd727849d76dd7f08ec。完整冻结文件与源码 hash 在 protocol-integrity.json。没有新公开参数、成员 grant、前端结果入口、scope 修改或授权绕过。

## 4. 全部最终测试结果

**163 executed / 163 passed / 0 failed / 0 errors / 0 skipped。**

| 分组 | 执行 / PASS | 性质 |
|---|---|---|
| D01–D24 | 54 / 54 | 全部确定性回归 |
| N01–N10 | 61 / 61 | 实际生产回调的离线脚本模拟 |
| S01–S20 | 40 / 40 | 每 fixture 的独立脚本一致 + 相反标签分歧 |
| 补充检查 | 8 / 8 | 冻结模板/结构、原生 SDK Validator 捕获重跑、5 类错误 text 返回 |
| 总计 | 163 / 163 | 无真实网络/模型调用 |

D20 和 Phase 1 stub 源码 guard 改为检查新共识的未接受安全行为与无 test flag；没有删除 D 要求或测试数量。其余 D 私有边界隔离用例仍只证明确定性核心；新增 N/S 才执行真实生产共识回调。

| N ID | 结果 | 验证 |
|---|---|---|
| N01 | PASS | 独立赞同、保存准确根绑定资格 |
| N02 | PASS | 独立明确拒绝、保存拒绝并禁止留言 |
| N03 | PASS | Leader 允许 / Validator 拒绝，不写状态 |
| N04 | PASS | Leader 拒绝 / Validator 允许，不写状态 |
| N05 | PASS | 19 种 raw 错误与 8 种 envelope 错误 |
| N06 | PASS | 19 种 Validator raw 错误 + timeout + 模型异常 |
| N07 | PASS | 注入/marker/占位符按数据传输，独立脚本拒绝 |
| N08 | PASS | 未决、Leader 异常、未返回 transport failure 不写状态 |
| N09 | PASS | 每个 Validator 完整重跑；相反标签、后续反对票、VM/User error 安全拒绝 |
| N10 | PASS | refusal 无准入，fresh SDK object 读取仍 NO_DECISION |

| S ID | 冻结预期（脚本输入） | 模拟一致 | 模拟分歧 | 真实模型结果 |
|---|---|---|---|---|
| S01 | ELIGIBLE | PASS | PASS | NOT RUN |
| S02 | NOT_ELIGIBLE | PASS | PASS | NOT RUN |
| S03 | NOT_ELIGIBLE | PASS | PASS | NOT RUN |
| S04 | NOT_ELIGIBLE | PASS | PASS | NOT RUN |
| S05 | ELIGIBLE | PASS | PASS | NOT RUN |
| S06 | NOT_ELIGIBLE | PASS | PASS | NOT RUN |
| S07 | NOT_ELIGIBLE | PASS | PASS | NOT RUN |
| S08 | ELIGIBLE | PASS | PASS | NOT RUN |
| S09 | NOT_ELIGIBLE | PASS | PASS | NOT RUN |
| S10 | NOT_ELIGIBLE | PASS | PASS | NOT RUN |
| S11 | ELIGIBLE | PASS | PASS | NOT RUN |
| S12 | NOT_ELIGIBLE | PASS | PASS | NOT RUN |
| S13 | ELIGIBLE | PASS | PASS | NOT RUN |
| S14 | NOT_ELIGIBLE | PASS | PASS | NOT RUN |
| S15 | NOT_ELIGIBLE | PASS | PASS | NOT RUN |
| S16 | NOT_ELIGIBLE | PASS | PASS | NOT RUN |
| S17 | ELIGIBLE | PASS | PASS | NOT RUN |
| S18 | NOT_ELIGIBLE | PASS | PASS | NOT RUN |
| S19 | NOT_ELIGIBLE | PASS | PASS | NOT RUN |
| S20 | NOT_ELIGIBLE | PASS | PASS | NOT RUN |

S 预期标签来自冻结设计，分别作为 Leader/Validator mock 脚本，不是模型预测。**真实模型分类结果：全部 NOT RUN。** 离线 PASS 只证明 Prompt/数据传输、严格解析、独立调用及 exact 比较。不能据此宣称模型能正确处理 S15/S16 注入或真实多 Validator 收敛。

## 5. 实际命令、退出码与日志

工作目录与 UTC 时间记录在 evidence/phase2/command-results.json。typecheck 把原 Phase 0 bin 加入 PATH；combined run 设置 CONTEXTPASS_TRACE_FILE 到证据文件。JUnit 和原始输出同目录，Phase 1 日志未覆盖。

| 检查 | 实际命令 | Exit | 结果 |
|---|---|---|---|
| prepare-sdk | `/workspace/scratch/114f91cc6678/phase0-env/bin/python scripts/prepare_direct_sdk.py` | 0 | PASS |
| D-regression | `/workspace/scratch/114f91cc6678/phase0-env/bin/python -m pytest tests/direct -q --junitxml=evidence/phase2/d-results.xml` | 0 | PASS |
| N-S-offline | `/workspace/scratch/114f91cc6678/phase0-env/bin/python -m pytest tests/consensus -q --junitxml=evidence/phase2/consensus-results.xml` | 0 | PASS |
| all-tests | `/workspace/scratch/114f91cc6678/phase0-env/bin/python -m pytest tests/direct tests/consensus -q --junitxml=evidence/phase2/all-results.xml` | 0 | PASS |
| static-check | `/workspace/scratch/114f91cc6678/phase0-env/bin/genvm-lint check contracts/context_bound_attestation.py --json` | 0 | PASS |
| default-typecheck | `/workspace/scratch/114f91cc6678/phase0-env/bin/genvm-lint typecheck contracts/context_bound_attestation.py --json` | 0 | PASS |
| strict-typecheck | `/workspace/scratch/114f91cc6678/phase0-env/bin/genvm-lint typecheck contracts/context_bound_attestation.py --strict --json` | 1 | FAIL |
| pip-check | `/workspace/scratch/114f91cc6678/phase0-env/bin/python -m pip check` | 0 | PASS |

静态 lint 3 项 PASS，SDK schema 5 writes / 6 views；默认 typecheck diagnostics=[]；pip check 无冲突。

开发中首次整套运行出现 62 PASS / 101 setup ERROR，原因是 Direct Mode 缺少已锁定 cloudpickle 的导入路径；随后测试 handler 的内部名称和参数顺序错误也被修正。这些是已解决的测试环境/夹具问题。业务实现早期的运行时 guard 类型收窄与 calldata 泛型注解诊断已修正；最终结果以上述保存的实际完整日志为准，没有把失败运行算成 PASS。

## 6. Strict 诊断与风险

**Strict Exit=1 / ok=false / FAIL，7 条 reportUnknownMemberType。**

- 原有 6 条 public.view 无参数/返回类型标注诊断仍存在，位置随代码行数移动。
- 新增 1 条 SDK run_nondet_unsafe 类型签名诊断：上游 Validator Callable 使用未参数化 Result，导致 Return[Unknown]。接口实现和 SDK 原文已复核保留。
- 没有修改 SDK、全局屏蔽规则或过滤输出；业务代码新增诊断已修正。工具 summary.errors=0 与实际列表不一致，以 exit/ok/7 条列表判 FAIL。

默认类型检查、序列化和全部离线运行验证通过，这些上游类型元数据限制不改变本轮已验证的权限和 comparator 行为；Strict 仍是未解决上游问题，不虚报全绿。

Direct Mode 默认 Leader 执行后立即返回、另捕获 Validator，因此持久化失败测试使用仅测试内的同步 executor，在实际回调 vote 接受前不返回且不恢复/伪造存储。此 executor 的配置票必须全部通过；它不是 GenLayer 网络 majority/finality/rotation 的替代实现。原生 SDK 捕获/重跑另有独立 smoke，未保存准入。

genlayer-test 0.29.2 mock 即使 text 模式也自动 JSON 解码；测试 mock 仅将 raw text JSON 包装一次，以确保实际生产 parser 看见原始重复键/格式。该 workaround 不在合约或 SDK 中。

实际网络执行、committee 收敛、轮换、最终性、RPC 额度、真实模型准确率和实际注入抵抗均未验证。F01–F10、T01–T10 NOT RUN。没有发现必须改变冻结架构的硬阻断；不可据此提前部署或承诺真实共识稳定性。

## 7. GitHub 交付

- Repository：[gqzy1/context-bound-attestation-genlayer](https://github.com/gqzy1/context-bound-attestation-genlayer)。
- 新开发分支：phase2-independent-consensus。
- 精确基线：6f498abbf1525f304174ed2018509a4445d441c8。
- 实现及完整离线证据 commit：a1ec692946c787d3abbd329397638dc51365ed45。
- Draft PR：[https://github.com/gqzy1/context-bound-attestation-genlayer/pull/2](https://github.com/gqzy1/context-bound-attestation-genlayer/pull/2)；目标 phase1-deterministic-core，创建已确认 draft=true / open / merged=false，作者 gqzy1。
- 后续只有报告/checkpoint 的链接补充提交；最终 HEAD 在外部交付报告及 PR 中记录。
- Phase 1 PR #1、Phase 1 分支、main 保持原状；不合并任何 PR。

## 8. 成本、范围与停止

新增现金支出 0；没有付费 API/LLM、节点、服务、CI 或链上交易。未创建 Repository B、前端、部署包或执行 Phase 3；未访问其他 GenLayer 网络，未请求/读取/保存钱包私钥或助记词。

下一阶段建议：仅在用户明确批准 Phase 3 后，按冻结文档开发 Repository B 的最小前端；合约真网络收敛与手动签名仍属于后续独立授权阶段。任何架构阻断应 STOP，不改变协议。

**STOP：Phase 2 完成后等待明确 Phase 3 授权。**
