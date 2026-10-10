# PHASE 4E FINAL SUBMISSION READINESS REPORT

日期：2026-10-10。账号：gqzy1。结论：**READY FOR REVIEW**。

文档、部署元数据和新只读证据已准备供两个 Draft PR 审查；不能直接标为 READY FOR SUBMISSION。B 存在一条已实际失败的过期测试断言，按本轮范围不修改测试。已知 Python Strict 七条诊断、缺失原截图/原始压缩包、许可未定及部分浏览器覆盖仍需明确接受或处理。

## 1. 当前 main 基线与公开状态

| 仓库 | 审核时 main HEAD | 状态 |
|---|---|---|
| A — gqzy1/context-bound-attestation-genlayer | `c690a2200569977e99e4cde9bfd52bd86aa4a89e` | public；main 已包含 Phase 4D，merge PR #5 |
| B — gqzy1/contextpass-genlayer | `6a6e8d13c6d73e40c6d185b0918a3e11e786cedc` | public；main 已包含 Phase 4D，merge PR #4 |

从各自当前 main 创建 `phase4e-submission-readiness`；审核时没有同名远程分支及未合并 PR，没有覆盖其他人改动。完整审核树保存于各自 `evidence/phase4e/audited-main-tree.txt`。Phase 4E PR 未合并，main 与公开 Pages 不因本轮变更而更新。

## 2. Canonical 源码一致性

| 检查 | 结果 | 证据 |
|---|---|---|
| A 完整生产源码 | PASS，17,514 字节 | A `contracts/context_bound_attestation.py` |
| B 完整源码副本 | PASS，17,514 字节 | B `intelligent-contract/contracts/context_bound_attestation.py` |
| A/B 逐字节一致 | PASS | 两仓库 `evidence/phase4e/source-integrity.json` |
| SHA256 与预期一致 | PASS，`e50cb6703ba63da5095dafc5d9867246888c5151d0773489aed3166033484b3d` | 重新计算，非照抄预期值 |
| Git Blob SHA 一致 | PASS，`10edfd3d23672789b4b600360750f5041c040f6d` | 两份文件实际 git hash-object 与 main tree |
| 部署源码与 A/B 一致 | PASS，重新只读 RPC 获取、base64 解码、逐字节比较 | A `evidence/phase4e/rpc-readonly.json` / `source-integrity.json` |
| 生产前端 canonical 绑定 | PASS | B `src/protocol.ts`、`src/transactions.ts`、`src/transport.ts`、JSON manifest；公开页面显示同一地址 |
| 历史版本区分 | PASS，当前 main / 历史 Phase 2、4B、4C 分开 | 新 SOURCE_PROVENANCE、部署清单；源码自身历史 docstring 保持原样 |

网络：Stable Studionet，61999；RPC `https://studio.genlayer.com/api`。
Canonical：`0xDe9abfBe2E4A61d23e27b552e241f5Bb1d1821b8`。
T01 部署：`0x26282c539033879705d9a8dea18c8676dae46c0cd09df9f91cb20d740f9be994`。
旧地址 `0x97B9003a17A8EDBD1b5E3379AA659753791497d9` 仅是历史记录，不是当前写入目标。

## 3. 提交标准逐项自审

规则依据为用户本轮提供的 Portal Intelligent Contracts / Projects 要求。公开检索未取得这两个分类当前完整表单；按限制未进入 Portal，故**实时官方表单、额外字段与网络受理规则 NOT VERIFIED**。不会把公开 Hackathon 要求当成 Portal 两分类规则，也不推测评分或保证通过。下面是实际产品与用户给定标准的对应审核。

### A — Intelligent Contracts

| 标准 | 判定 | 对应源码 / 文件及理由 |
|---|---|---|
| 独立成立的 Intelligent Contract Primitive | PASS | A SPEC.md / 合约 NonTransitiveContextAdmissionV1：原始背书、上下文准入、撤销与发帖权限，独立于前端 |
| 真实有意义的 GenLayer 共识 | PASS | apply_and_join → _semantic_decision → run_nondet_unsafe；T04/T07 真实 FINALIZED 共识证据 |
| Leader/Validator 职责明确 | PASS | CONSENSUS.md / _semantic_decision：各自独立执行同一完整原始输入分类 |
| Equivalence 不仅检查 JSON 格式 | PASS | Validator 先独立 _classify，再比较实际 ELIGIBLE/NOT_ELIGIBLE 标签；形状正确但标签相反会拒绝；consensus tests |
| 状态与授权清晰 | PASS | SPEC.md / create_space、issue、revoke、apply、post、is_active_member；发行人/持有人/撤销/唯一决定检查 |
| 可复用、可解释、超越单次演示 | PARTIAL | generic 原始 scope/target、5 写 6 读、多个空间独立评估；机制可复用，但没有明确 LICENSE，法律许可待定 |
| 完整源码、测试、使用说明 | PASS | contracts、tests/direct + tests/consensus、README/SPEC/CONSENSUS/TESTING；本轮 240/240；Strict 已知失败另列 |

### B — Projects

| 标准 | 判定 | 对应源码 / 文件及理由 |
|---|---|---|
| 解决具体信任问题 | PASS | SUBMISSION_PROJECTS.md / DEMO.md：窄技能背书不能扩张为不相关角色权限 |
| 核心流程依赖 GenLayer | PASS | apply_and_join 的语义裁决在合约共识内；前端不决定资格 |
| 使用真实链上状态 | PASS | src/transport.ts real readContract/getTransaction；本轮 Pages/SDK 读取撤销、决定、Space #3、计数及公开 notes |
| 独立可访问完整前端 | PASS | 公开 Pages 页面实际加载；4 个产品区；Vite project base；非纯静态图 |
| 实际合约读写及钱包交互 | PARTIAL | 实现 5 写 6 读、注入钱包、双重 canonical guards；用户已完成桌面连接和一次真实 Pages create_space；其余 4 写及拒签/切链/恢复/移动签名 NOT RUN live |
| 完整应用源码 | PASS | src、tests、package/lock、vite/tsconfig、工作流均公开；安装与构建本轮成功 |
| Projects 内完整 Intelligent Contract 源码 | PASS | intelligent-contract/contracts/context_bound_attestation.py 完整并与 A/部署一致；不是 wrapper |
| 清晰部署、演示、使用及审核证据 | PARTIAL | 现行清单与只读收据/状态已补；缺失原 PNG/压缩包已公开标注；本轮 B 1 条 stale 测试失败 |
| 非基础模板、非 Thin LLM Wrapper | PASS | 原始发行人选择、不可转移原始 root、空间绑定、唯一决定、语义覆盖和即时撤销链上 gate；界面不能绕过合约授权 |

PASS 为当前证据满足所列项，不等于所有浏览器场景或实时 Portal 审核已通过。

## 4. 明显问题、严重程度与处置

严重度定义：P0 为源码/部署/授权错配或产品核心不可用；P1 为本轮正式提交门槛未完成；P2 为可复核性/许可/展示限制；P3 为非致命性能警告。

| 问题 | 严重度 | 结果 |
|---|---|---|
| B 两份 provenance 仍把 Phase 2/候选当 canonical，旧 SHA、bootstrap/unmerged 状态误导 | P1 | 修复：当前 main HEAD/hash/blob/部署来源置顶，原文 Historical/Superseded 保留 |
| A/B 三份部署清单仍写未部署/未发布、地址 null、钱包 NOT RUN | P1 | 修复：当前部署、Pages、单次前端真实测试和覆盖边界置顶 |
| JSON false / NOT RUN / pagesPublished=false 与 Phase 4D 冲突 | P1 | 修复为真实值，新增按方法/异常测试范围；不把一次测试扩大为全通过 |
| B packaging.test.ts 要求 frontendRealWalletTested=false | P1 | **未修复**：本轮实际 144/145，唯一失败。测试更改超出授权，保留失败日志；不把错误 JSON 改回 false 来制造 PASS |
| README/清单/提交说明仍有未合并旧描述 | P1 | 新当前摘要、结果和审核导航；历史原文保留、明确 superseded |
| A evidence index 链到 B main/Phase4C 不存在的原截图、gzip 包和脚本 | P2 | 修正归档声明，标注不存在；已有 JSON 收据摘要/日志保留；未伪造/补造缺失文件 |
| Python Strict 七条 SDK 类型诊断 | P2 | 本轮再次 FAIL (exit 1)，7 reportUnknownMemberType；没有 SDK patch/规则屏蔽 |
| 两仓库均无 LICENSE | P2 | 未添加；用户单独决定许可；public 可读不等于有明确再利用许可 |
| 其余网站真实写入/拒签/换链换账户/恢复/移动签名覆盖有限 | P2 | 明确 NOT RUN live；Studio E2E 与离线 mocks 不能代替 |
| Overview raw publicHistory.notes 显示 `[{}]` | P2 | 当前浏览器观察到；独立 SDK jsonSafeReturn=true 能读出完整历史 note。src/protocol.ts printable 不转换嵌套 Map，而 room history 专用列表使用 record。仅记录展示问题，不修改任何前端代码 |
| SDK bundle 781.88 kB minified / 191.73 kB gzip | P3 | 构建通过，保留 >500 kB 警告，不重构/升级依赖 |
| Explorer /transactions 被怀疑错误 | 非问题 | 11 笔全部真实访问并跳转有效 /tx 页面；不能以跳转为由认定旧链接错误，未批量替换 |

不存在证据表明当前 canonical 源码或部署不一致。未发现 P0；P1 过期测试断言仍妨碍将本轮补丁升级为正式提交状态。

## 5. 真实证据与复核路径

- A `evidence/phase4c/t01-t10.json`：原 T01–T10 逐轮 Leader/Validator、输入、结果。旧测试和链上记录未改。
- A `evidence/phase4e/rpc-readonly.json`：本次 eth_chainId、eth_getTransactionByHash（Phase 4D）、gen_getContractCode 的实际 HTTP/JSON 记录。61999 与部署来源重新核验。
- 两仓库 `evidence/phase4e/frontend-tx-summary.json`：锁定 genlayer-js 1.1.8 对实际 calldata/Leader return 离线解码。hash、sender、canonical recipient、create_space args 与 Return 3 相符。
- B `evidence/phase4e/sdk-current-readback.json`：最新最终态 get_counts、get_space(3)、get_room_notes(1,0,20) 实际结果。spaces=3 / attestations=1 / decisions=2 / notes=1；Space #3 owner/trusted issuer Wallet A、标题 ContextPass Frontend QA、精确 requirement 相符。
- 两仓库 `evidence/phase4e/explorer-link-audit.json`：浏览器逐笔检查 T01–T10 + Phase 4D 跳转、hash、地址和 FINALIZED；记录为网页观察，不冒充新 raw RPC 的 T01–T10 收据。
- 本次 hosted read-only refresh 返回 Root #1 revoked=true，Space #1 historical ELIGIBLE / active=false，Space #2 NOT_ELIGIBLE / active=false。这个结果和历史 T09/T10 相符，不能据历史资格授予当前权限。
- T07 首轮 parse error/Leader Rotation 与反对票保留，最终 rotation 1；不是首次即成功或五票一致。
- T08/T10 是共识接受的 ACTIVE_MEMBER_ONLY Rollback，不是成功业务写入。失败之后 notes=1，历史 note 保留。
- Phase 4D transaction `0x85c5037d3ac249faca70336a6760d4538dc26407181bf71d79da091e6457d02d` 本次独立 raw RPC 核验：FINALIZED、MAJORITY_AGREE、Leader SUCCESS、Return 3、NORMAL、rotation 0、initial validators 5、3 agree / 2 idle；没有制造 Validator 票。
- 两仓库原树中没有原 PNG 截图或引用 gzip 包。本轮未创建截图，未宣称用户旧图已归档。已有归档 hash metadata 不等于对应文件真实存在。
- 公开 Demo 地址 `https://gqzy1.github.io/contextpass-genlayer/` 本次 HTTP 200 且浏览器加载/只读使用成功。页面已含 Phase 4D 说明。本轮未连接钱包、触发签名或发布。

## 6. 本轮实际命令与结果

环境 Python 3.12.14、Node 24.19.0、npm 11.9.0；原锁定版本安装，未更新依赖。命令参数、cwd、UTC 起止、exit 和完整输出在各自 `evidence/phase4e/command-results.json` / logs。

| 仓库 | 实际命令（在该仓库运行） | exit | 真实结果 |
|---|---|---|---|
| A | python3.12 -m venv .venv；.venv/bin/python -m pip install -r requirements.lock.txt | 0 | 原 lock 环境创建及安装成功；安装操作详见独立 setup 日志 |
| A | .venv/bin/genvm-lint download --version v0.2.16 | 0 | 官方 pinned SDK 获取，无 SDK 修改 |
| A | .venv/bin/python scripts/prepare_direct_sdk.py | 0 | pinned SDK digest 验证和 callback runner 准备成功 |
| A | .venv/bin/python -m pytest tests/direct tests/consensus -q --junitxml=evidence/phase4e/all-results.xml | 0 | **240 passed**，无改测试 |
| A | .venv/bin/genvm-lint check contracts/context_bound_attestation.py --json | 0 | schema/static PASS：5 write、6 view、0 constructor args |
| A | .venv/bin/genvm-lint typecheck contracts/context_bound_attestation.py --json | 0 | default PASS，0 diagnostics |
| A | .venv/bin/genvm-lint typecheck contracts/context_bound_attestation.py --strict --json | 1 | **FAIL：7 reportUnknownMemberType**；6 public.view + 1 run_nondet_unsafe。JSON summary.errors=0 与 diagnostics 矛盾，以 exit/ok/diagnostics 判失败 |
| A | .venv/bin/python -m pip check | 0 | No broken requirements found |
| B | npm ci | 0 | 316 packages；锁文件未改 |
| B | npm test | 1 | **144 passed / 1 failed，7 files**；packaging stale false assertion，其他测试通过 |
| B | npm run typecheck | 0 | TypeScript strict PASS |
| B | npm run verify:source | 0 | canonical SHA256 PASS |
| B | npm run build | 0 | 472 modules；dist 生成；781.88 kB bundle 警告保留 |
| A/B | git diff --cached --check -- *.md public/deployment-manifest.json | 0 | 文档与元数据无 whitespace 错误 |
| A/B | SHA256、git hash-object、A/B/deployed bytes 比较 | 0 | 源码完整一致 |
| B | git diff --cached --check（包括新增 raw logs） | 2 | 原始 build.log 保留工具输出尾空格；tests.log 保留末尾空行。不清洗原日志。A 同检查 exit 0 |

Python 类型工具使用 PATH 中的 `.venv/bin`。离线测试没有真实 LLM 预测、交易或链上 writes。历史 240/145 PASS 不冒充本轮结果。本轮 B 失败明确保留，未升级依赖、改业务或改测试来获得 PASS。

本次浏览器 QA 不含完整异常钱包测试、全移动端测试、全控制台/网络审计；标为 NOT RUN/部分覆盖，不宣称所有 QA PASS。

## 7. 变更范围与交付

A：README、CONSENSUS、DEPLOYMENT_STUDIONET、ONCHAIN_EVIDENCE_INDEX、RELEASE_READINESS_CHECKLIST、TESTING、PHASE_4E_SUBMISSION_AUDIT 与新的 evidence/phase4e。

B：README、DEMO、SUBMISSION_PROJECTS、两份 SOURCE_PROVENANCE、两份 DEPLOYMENT_MANIFEST_STUDIONET、TESTING、public/deployment-manifest.json、PHASE_4E_SUBMISSION_AUDIT 与新的 evidence/phase4e。

生产 Python 源码、副本、所有 src、测试、原证据、冻结设计、SDK、依赖锁和工作流 **无修改**。合约 ABI、Prompt、状态机及授权语义均不变。没有任何新链上交易/部署/升级/Portal 提交/PR merge/Pages 发布；不会自动触发 Pages（工作流仅 main 的自身文件变更或手工 dispatch 才发布，本轮未改工作流）。

各自独立 Draft PR 的真实 URL 见最终交付报告；仓库内这份审计材料随 Draft 分支提交，避免预造 URL。

## 8. 提交建议与停止条件

**READY FOR REVIEW**。两仓库核心机制、完整源代码和已部署产品有真实证据，未发现 P0。但 B 本次测试失败仍然存在，补丁尚未审查/合并，许可与 QA 风险未单独确认；本轮不建议直接进入任一 Portal 正式提交，尤其不能把 Projects 标为所有检查已通过。

下一步仅可由用户另行授权：修正 B 那条过期测试，围绕单次 create_space 和未测范围建立事实对应的元数据断言；重新执行 B 检查；独立决定 LICENSE 与是否接受已知 Strict/覆盖限制。Overview raw nested Map 展示问题涉及前端代码，亦需单独授权后才修复。无须为本次证据修正新增链上交易。

到此 STOP；两个 Draft PR 不合并，不发布，不交易，不提交 Portal。
