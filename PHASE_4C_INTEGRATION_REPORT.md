# PHASE_4C_INTEGRATION_REPORT

**2026-10-10 — 范围结论：证据归档与前端集成完成，离线验收 PASS；发布验收尚未完成。** Python Strict FAIL（原有七条 SDK 诊断），真实前端钱包/桌面移动浏览器 QA NOT RUN。不能宣布全部验收全绿或已发布。

## 1. 权威基线及完整性

重新阅读 A/B 全部冻结九文件、Canonical Prompt、D/N/S/F/T 测试计划、Phase0–3和4A/4B报告、合约、TESTING、checkpoint、provenance/manifest，以及原定 FRONTEND_ACTIVATION_PLAN。历史 Phase4A 计划的旧 SHA 被用户授权的 Phase4B 修补 SHA 取代；激活流程与安全要求继续沿用，未重设计。

GitHub 连接实际 login=gqzy1 / ID155161534，再次核验。仅使用该连接。A 基线 phase4b-address-compatibility HEAD c7c6e50620602d03ad4e3c116ad1532097feab8a；B 同名基线 HEAD 3eeb4ff52359ffe39e146cce4ac402def612d503。独立分支 A phase4c-evidence-closure，B phase4c-frontend-activation。A main 仍 bootstrap，不作为 canonical；原五个 Draft PR/head、main 不变。

Canonical contract `0xDe9abfBe2E4A61d23e27b552e241f5Bb1d1821b8` / Stable Studionet61999 / https://studio.genlayer.com/api。A源路径 contracts/context_bound_attestation.py，B完整副本 intelligent-contract/contracts/context_bound_attestation.py，实际部署源码三者 **17514 bytes，逐字节一致**，SHA256 **e50cb6703ba63da5095dafc5d9867246888c5151d0773489aed3166033484b3d**。源码 blob10edfd3d23672789b4b600360750f5041c040f6d。源码、冻结文件、所有依赖 lock、五写六读/零构造参数、权限/状态/Prompt/Leader/Validator/Equivalence Principle 均未修改。

沿用 GenVM v0.2.16/原 Depends runner、Python3.12.14、genlayer-test0.29.2、linter0.11.0、pytest9.1.1、pyright1.1.414；前端 React19.3.0/Vite8.3.4/TS7.0.2/genlayer-js1.1.8/viem2.57.4。服务器各 Validator 二进制版本未单独取证，不能由源码 header 推断。

## 2. 真实证据闭合

用户完成的真实 Studio T01–T10 与本阶段的只读复核分开记录。**23/23 实际只读 SDK 操作成功**：chain1/source1/schema1/tx10/state10。十笔均 FINALIZED / MAJORITY_AGREE，历史最终轮 Accepted。T01–T07/T09 Leader SUCCESS/Return；T08/T10 Leader ERROR/Rollback ACTIVE_MEMBER_ONLY 是预期合约安全拒绝，不是成功写入。

ROOT_ID=1、Room1=1、Room2=2、Note=1 来自真实收据/状态。当前 root1 revoked=true；Room1历史ELIGIBLE仍在，但 Wallet B active=false；Room2 NOT_ELIGIBLE / active=false；早前note1保留、Room2无note；counts2/1/2/1。T04之前 active=true 属于用户人工历史验收，本轮仅重读撤销后的最终态，未虚构历史瞬间读取。

T07包含两轮：首轮 Leader ContractError/exit_code1、JSONDecodeError，Validator结果3 disagree/1 idle；rotation_count1 后最终 Accepted/NOT_ELIGIBLE，最终votes3 agree/2 idle。T04最终也为3 agree/2 idle。T01/T09各5 agree。完整地址、每轮回执、错误/等价输出在 t01-t10.json 与无损原始压缩归档。**未宣称每轮全票赞同或模型格式稳定。** 不改 Prompt、不换网络、不重发交易。

Explorer网页抓取 T04/T07 受限，未重新验证网页UI；原20张用户截图保留名称/hash/原始字节，并单列关键T07/T08/T09/T10图。T01–T05原截图未在该20张集合中，本轮从真实RPC核验其收据，未补造截图。公开十笔链接和当前链上状态详见 ONCHAIN_EVIDENCE_INDEX.md。

真实23项读取的执行命令（B cwd，exit0）：`node scripts/verify-onchain-readonly.mjs > evidence/phase4c/read-only-run.log 2>&1`。脚本无账户/签名，仅允许指定只读RPC，429即停止。`node scripts/index-phase4c-evidence.mjs` 离线解析归档，绝非又执行了T交易。gzip归档保留解压后SHA与长度。

## 3. 前端激活与必要兼容补丁

按4A计划保留类签名，编译时允许已验证部署的人工写入；不是仅把 WRITES_LOCKED=false。Transactions.submit 和 SdkTransport.write **各自**校验同一静态 canonical地址/61999/RPC/SHA，前者在 wallet.assert/save前、后者在签名client/provider前拒绝其他目标。手填inspection地址继续只读，App实际writeIntent固定canonical；无env/query/storage开关、测试模式或自动交易。

canonical默认选中、无钱包访客可手动刷新真实示例；新增已记录真实证据文案、源码/部署/交易链接，历史ELIGIBLE和当前inactive分开。首屏不自动请求RPC、连接钱包或发签名；refresh/reload只恢复journal，要求手工核验。新申请明确提醒root1已撤销，不能复用。

实际 pinned Studio leader_receipt 数组还包含Validator，T03/T06的最后项为quorum后取消的Validator/contract_error；旧decoder取最后项会错误识别业务结果。现在按mode=leader选择真正Leader，并要求MAJORITY_AGREE、SUCCESS、Return，结合FINALIZED/精确hash-sender-contract-method-calldata绑定及每种方法最新最终态readback才能确认。已用捕获的真实T02–T10 payload通过 pinned SDK的Mock HTTP离线重放验证；不是新网络/钱包成功。

Rollback显示业务拒绝，未验明共识为undetermined并阻止重复写，网络错误保持hash/pending；NOT_ELIGIBLE为真实永久业务拒绝。保持钱包二次链/账户校验、单次send gate、原始sign路径禁用、签名前持久化、拒签4001、unknown恢复、旧confirmed降级、429 Retry-After/合并/350ms限流/最多3次读尝试、无write retry。详见 FRONTEND_ACTIVATION_REPORT.md。

## 4. 实际验收结果

| 检查 | 最终实际结果 |
|---|---|
| A D/N/S/地址全套 | **240/240 PASS**，0失败/错误/skips；原163+地址77，仍离线 |
| B 前端 | **145/145 PASS**，7 files，0失败/pending；原124全保留+激活20+manifest1 |
| A/B lint/schema | PASS，5写/6读/0构造参数 |
| A/B Python默认类型 | PASS，零diagnostics |
| A/B Python Strict | **FAIL**，各Exit1/ok=false，原七条reportUnknownMemberType |
| TS Strict | PASS，strict=true/skipLibCheck=false，原两条精确声明bridge保留 |
| 生产build | PASS，472modules，主chunk781.69kB/gzip191.65kB，>500kB warning保留 |
| A/B/部署字节、freeze/dependency locks | PASS，未改锁定版本 |
| 实际只读RPC | **23/23 PASS**；不纳入offline测试数量 |
| 真实前端桌面/手机视觉、console、浏览器路由 | **NOT RUN**：正常Chrome访问本地Vite ERR_CONNECTION_REFUSED |
| 真实前端wallet/sign/send/提交后reload与readback | **NOT RUN**，本阶段没有请求真实签名或交易 |
| GitHub Pages托管/Portal | NOT PUBLISHED / NOT SUBMITTED |

七条Python Strict诊断原样保存：六个public.view未知装饰器类型、一条run_nondet_unsafe未参数化Result；与原诊断message/rule相同。没有压制、改SDK或误用summary.errors=0宣称PASS。S01–S20依旧脚本预期，不是20场真实模型准确性测试；真实语义样本仅T04/T07。前端Mock wallet/HTTP/Transport与真实Studio E2E分开。

初次准备脚本因当前临时SDK缓存缺失Exit1，随后实际执行 `../phase4a-env/bin/genvm-lint download --version v0.2.16`，恢复同一216630904bytes官方artifact，SHA4f0b358ec98ec148be9b95cdfb0f0e1a6cbe64da0194fdfac3fffc6f5d1d93e2由prepare_direct_sdk校验，未升级。中间前端失败分别为改bindingfixture后corrupt-storage测试key大小写不一致和新增UI查询重复匹配，均修复后完整重跑至145/145；未把中间失败算PASS。

## 5. 真实执行命令

主离线harness：`python scripts/verify-phase4c.py`（B cwd），Exit0；工具PATH前置 /workspace/scratch/114f91cc6678/phase4a-env/bin。它明确保留strict Exit1而不假装PASS。每个命令cwd、UTC起止、退出码、全原始输出/JUnit/frontend JSON在A/B evidence/phase4c。下面是该轮真实命令：

| 仓库 / 检查 | 实际命令 | Exit |
|---|---|---|
| repository-a / prepare-sdk | `/workspace/scratch/114f91cc6678/phase4a-env/bin/python scripts/prepare_direct_sdk.py` | 0 |
| repository-a / all-tests | `/workspace/scratch/114f91cc6678/phase4a-env/bin/python -m pytest tests/direct tests/consensus -q --junitxml=evidence/phase4c/all-results.xml` | 0 |
| repository-a / static | `/workspace/scratch/114f91cc6678/phase4a-env/bin/genvm-lint check contracts/context_bound_attestation.py --json` | 0 |
| repository-a / default-types | `/workspace/scratch/114f91cc6678/phase4a-env/bin/genvm-lint typecheck contracts/context_bound_attestation.py --json` | 0 |
| repository-a / strict-types | `/workspace/scratch/114f91cc6678/phase4a-env/bin/genvm-lint typecheck contracts/context_bound_attestation.py --strict --json` | 1 |
| repository-a / pip-check | `/workspace/scratch/114f91cc6678/phase4a-env/bin/python -m pip check` | 0 |
| repository-a / python-lock | `/workspace/scratch/114f91cc6678/phase4a-env/bin/python -m pip freeze` | 0 |
| repository-b / frontend-tests | `npm test -- --reporter=default --reporter=json --outputFile=evidence/phase4c/frontend-results.json` | 0 |
| repository-b / typescript-strict | `npm run typecheck` | 0 |
| repository-b / source-verifier | `npm run verify:source` | 0 |
| repository-b / production-build | `npm run build` | 0 |
| repository-b / frontend-lock | `npm ls --depth=0 --json` | 0 |
| repository-b / static | `/workspace/scratch/114f91cc6678/phase4a-env/bin/genvm-lint check intelligent-contract/contracts/context_bound_attestation.py --json` | 0 |
| repository-b / default-types | `/workspace/scratch/114f91cc6678/phase4a-env/bin/genvm-lint typecheck intelligent-contract/contracts/context_bound_attestation.py --json` | 0 |
| repository-b / strict-types | `/workspace/scratch/114f91cc6678/phase4a-env/bin/genvm-lint typecheck intelligent-contract/contracts/context_bound_attestation.py --strict --json` | 1 |


浏览器：实际 `npm run dev -- --host 127.0.0.1 --port 5173` 正常ready；正常cua_repl Chrome打开 http://127.0.0.1:5173/contextpass-genlayer/ 返回ERR_CONNECTION_REFUSED。停止server Exit130为主动Ctrl-C，不是构建失败。未换隧道、代理、file URL或绕过安全限制。RELEASE_READINESS_CHECKLIST提供人工Desktop1440×900/Mobile390×844/console/四hash routes/reload清单；组件与CSS检查不冒充真实视觉PASS。

## 6. GitHub交付与合并依赖

- A [gqzy1/context-bound-attestation-genlayer](https://github.com/gqzy1/context-bound-attestation-genlayer)，独立phase4c-evidence-closure，目标phase4b-address-compatibility：A_PHASE4C_DRAFT_PR_PENDING。
- B [gqzy1/contextpass-genlayer](https://github.com/gqzy1/contextpass-genlayer)，独立phase4c-frontend-activation，目标phase4b-address-compatibility：B_PHASE4C_DRAFT_PR_PENDING。
- 新PR仅Draft，不合并。源文件不变；A变更仅证据/检查日志/文档，B仅必要前端激活/compatibility/测试/文档。最终HEAD以PR为准，文档链接补充不改变测试代码。
- 未来经另行批准的顺序：A #1→#2→#3→Phase4C；B #1→#2→Phase4C。合并父PR后复核/retarget子PR基线与diff；不要只合并末尾PR丢失parent实现。A/B原main及旧Draft保持不变。

## 7. 剩余风险与STOP

Release gate仍未完成：正常桌面/手机视觉/console、实际浏览器钱包扩展/拒签/账户链事件、真实前端人工提交及reload恢复未测试；已发表Pages路径未测试且本阶段禁止发布。Python Strict七条上游诊断和SDK较大bundle未解决。真实T07格式失败/反对票暴露模型输出稳定性风险，不隐瞒、不更改协议；两个语义交易不能证明所有自然语言/注入场景或未来服务稳定性。RPC免费额度/faucet/ hosted模型可用性没有无限保障。snapshot只是记录，不授予当前权限。

未发现必须改变冻结协议/接口的硬阻断。新增现金支出0，无付费API/服务器/数据库、部署、升级、真实签名/交易、私钥/助记词处理、main写入、merge、Pages或Portal。真实前端发交易与发布均需用户未来明确授权，不能从本阶段推导。

**STOP — Phase4C工作完成后等待人工验收及后续发布授权。**
