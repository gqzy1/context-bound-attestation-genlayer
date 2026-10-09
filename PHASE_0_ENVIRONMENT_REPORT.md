# ContextPass — PHASE 0 ENVIRONMENT REPORT

日期：2026-10-10（Asia/Shanghai）。最后核验时间：2026-10-09T19:10:57Z。

**结论：PASS — 满足 Phase 0 环境准入条件。** 无阻断下一阶段的必要环境问题。另有一项可选严格类型检查 FAIL，详见第 6 节；不应把本报告解释成所有检查全绿、产品已通过测试或已完成链上共识。

**执行终点：STOP。Phase 1 未执行，仓库未创建，未提交任何链上交易。**

## 1. 权威依据及范围

唯一设计依据是附件 `ContextPass_Architecture_Freeze_V1_Work_Handoff(1).zip`。通过本地附件读取全部 9 个文件，未更改原包。没有从旧项目复用设计、代码或版本结论。

| 文件 | 阅读 | 包内清单 SHA256 核验 |
|---|---|---|
| 00_READ_FIRST.md | 完整 | PASS |
| 01_DUPLICATION_AND_GATE.md | 完整 | PASS |
| 02_ARCHITECTURE_FREEZE_V1.md | 完整 | PASS |
| 03_CANONICAL_CONSENSUS_PROMPT.md | 完整 | PASS |
| 04_TEST_ACCEPTANCE_PLAN.md | 完整 | PASS |
| 05_WORK_MASTER_AND_PHASE_COMMANDS.md | 完整 | PASS |
| 06_DEPLOYMENT_EVIDENCE_SUBMISSION.md | 完整 | PASS |
| 07_PROJECT_CHECKPOINT_TEMPLATE.md | 完整 | PASS |
| 08_FILE_MANIFEST.md | 完整 | 清单本身无自校验条目 |

清单中 8 个文件的字节数、SHA256 均匹配。冻结语义保留：单合约、唯一语义入口、Leader/Validator 独立执行、exact decision 比较、非传递根绑定、撤销即时禁写、只使用 Stable Studionet、用户手动签名、无后端或付费 AI。

本轮只安装环境依赖、读取官方文档与版本信息、做只读网络检查和通用工具冒烟。官方 Storage 示例仅用于环境检查，不是 ContextPass 实现。其内存写入不产生交易。

## 2. PASS / FAIL 矩阵

| 必要检查 | 结果 | 实际证据与边界 |
|---|---|---|
| GitHub 当前认证账号 | PASS | 指定 gqzy1 连接的 authenticated login 返回 `gqzy1`，用户 ID `155161534` |
| Stable Studionet 配置 | PASS | 官方网络文档及已安装 genlayer-js 的 studionet 均为 61999 / https://studio.genlayer.com/api |
| 实际只读 RPC | PASS | Node + genlayer-js `client.getChainId()` 返回整数 `61999` |
| Stable Studio 浏览器可达 | PASS | 实际打开 https://studio.genlayer.com/contracts，读取官方 Storage 模板 |
| 稳定 GenVM / Python SDK runner 固定 | PASS | 当前 Stable Studio 模板 header、官方 v0.2.16 release artifact 与本地 runner 精确匹配 |
| Python / Direct Mode | PASS | Python 3.12.14；genlayer-test 0.29.2 安装成功；官方 Storage 构造、读取、内存更新及再次读取成功 |
| Direct Mode pytest 插件 | PASS | `pytest --fixtures -q` 显示 direct_vm、direct_deploy、direct_accounts 等；未执行产品测试 |
| 自定义 nondet API | PASS（工具冒烟） | 固定 SDK 源码提供 run_nondet_unsafe；通用固定 mock 响应经 leader 执行后，run_validator 独立再次调用 mock，返回 True；无网络 LLM |
| SDK 状态类型 | PASS | 固定 SDK 可导入 TreeMap、DynArray、Address |
| 静态 lint + SDK schema 校验 | PASS | 官方 Storage `genvm-lint check --json`：ok=true，lint passed=3，validate ok=true |
| 默认类型检查 | PASS | 官方 Storage `genvm-lint typecheck --json`：ok=true，无诊断 |
| Python 依赖一致性 | PASS | `pip check`：No broken requirements found；gltest.direct 实际导入成功 |
| genlayer-js 稳定版及客户端 API | PASS | npm latest=1.1.8；readContract/writeContract/getTransactionReceipt/waitForTransactionReceipt 均为 function；只调用 getChainId |
| 前端工具安装及构建引擎 | PASS | React/Vite/TS/Vitest/RTL/jsdom 安装成功；Vite + React 插件对现成 React 模块完成内存 bundle |
| 零额外现金依赖路径 | PASS（架构与本轮执行） | 本轮无付费服务、无付费 API 调用；公开仓库 + GitHub Pages 免费路径有官方依据；无需 Docker 或私有节点 |

| 补充检查 | 结果 | 说明 |
|---|---|---|
| Python urllib 对 RPC 的直接 POST | FAIL（不阻断） | 本次返回 HTTP 403；Node SDK 的实际同链只读调用随后成功。原因未被确定，不能据此宣布 RPC 宕机或 Python 路径永久不可用 |
| 官方 Storage 严格类型检查 | FAIL（不阻断环境准入） | 退出码 1；SDK view 装饰器 reportUnknownMemberType，详见第 6 节 |
| ContextPass 合约/前端/共识业务验收 | NOT RUN | D01–D24、S01–S20、N01–N10、F01–F10、T01–T10 均未执行；无实现代码 |
| 真实钱包签名及 SDK write 路径 | NOT RUN | 只验证 API 存在，未连接用户钱包、签名或发送交易 |
| GitHub 仓库创建、写权限与 Pages 发布 | NOT RUN | 本轮禁止写入；当前账号认证成功不等于已经实测创建/发布权限 |

## 3. 本轮版本锁定

这些值是本轮重新发现并安装的版本，不是从历史项目照搬。后续避免 `latest` 自动升级；项目正式 lockfile 只能在相应实现阶段建立。

### 合约与 Python 工具

| 项目 | 锁定值 | 依据 |
|---|---|---|
| Python | 3.12.14 | 当前实际解释器 |
| GenVM 合约目标 | v0.2.16 | Stable Studio 官方模板第一行；官方 release 存在并已下载 |
| 合约 Python SDK runner | py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6 | Stable Studio 模板 Depends 与 artifact 内精确 runner |
| SDK 标准库 | py-lib-genlayer-std:11rhn002yfajawsz7fai6mykznbxkxs6l91iskj5cm82c92qhy3v | 固定 runner.json 的传递依赖 |
| cloudpickle runner | py-lib-cloudpickle:1dlk6mnfabi0z7r39635amyfzw8xb6rm8bv4pmgv6ji1bfx9hghd | 固定 runner.json |
| CPython runner | cpython:1bk9g3zgym0rrpd9lk584cxfaa4rg0cz36w6xhzkqdj1m2p4xa9n | 固定 runner.json |
| genlayer-test | 0.29.2 | PyPI 当前发行与实际安装 |
| genvm-linter | 0.11.0 | PyPI 当前发行与实际安装 |
| pytest | 9.1.1 | 实际安装，插件发现成功 |
| genlayer-py | 0.16.3 | 测试工具依赖的网络客户端；实际安装与导入 |
| web3 | 8.0.0 | 本轮解析所得；pip check、gltest 导入成功 |
| pyright | 1.1.414 | 实际安装、默认类型检查执行成功 |

**名称区分：** `genlayer-js 1.1.8` 是 JavaScript 客户端；`genlayer-py 0.16.3` 是 Python 网络客户端；合约运行时的 `py-genlayer` SDK 以 runner hash 锁定。不能把前两个客户端版本当作合约 SDK 版本。

本轮检查的是当前 Stable Studio 模板目标和对应本地 SDK artifact；没有借部署或交易证明服务端每台 validator 的二进制版本，也没有把 GitHub `/releases/latest` 当作 Studionet 版本。该 latest 实际返回名称含 RC 的 `v0.3.0-rc7`，本轮不使用。

官方 `genvm-universal.tar.xz`（v0.2.16）大小 216630904 bytes，下载文件 SHA256：

`4f0b358ec98ec148be9b95cdfb0f0e1a6cbe64da0194fdfac3fffc6f5d1d93e2`

与官方 GitHub release API 的 asset digest 完全相同。

### 前端工具

| 项目 | 实际安装 / 建议锁定 |
|---|---|
| Node.js | 24.19.0 |
| npm | 11.9.0 |
| genlayer-js | 1.1.8（npm latest；未使用 2.0.0-rc.1） |
| viem | 2.57.4 |
| react / react-dom | 19.3.0 / 19.3.0 |
| vite | 8.3.4 |
| @vitejs/plugin-react | 6.1.2 |
| typescript | 7.0.2 |
| vitest | 5.0.3 |
| @testing-library/react | 16.3.3 |
| jsdom | 30.1.2 |
| @types/react / @types/react-dom | 19.3.0 / 19.3.0 |
| @types/node | 24.19.2（对应 Node 24 major） |
| Git | 2.51.1 |

前端检查只证明这些工具能安装、相关 CLI 能启动、Vite + React 插件能完成通用构建。ContextPass 的 TS 编译、交互测试、真实浏览器钱包兼容性、移动端和 GitHub Pages 路径必须在 Phase 3 再验收，不提前标记通过。

## 4. 关键命令与实际结果

所有路径是本轮临时环境，不是 GitHub 项目。正式仓库没有创建。

```text
python -m venv phase0-env
phase0-env/bin/python -m pip install genlayer-test genvm-linter
=> installed genlayer-test 0.29.2 / genvm-linter 0.11.0

phase0-env/bin/python -m pip check
=> No broken requirements found.

phase0-env/bin/python -m pytest --version
=> pytest 9.1.1

phase0-env/bin/python -m pytest --fixtures -q
=> direct-mode fixtures found; no tests ran

phase0-env/bin/genvm-lint download --version v0.2.16
=> official universal artifact downloaded; official digest matched

phase0-env/bin/genvm-lint check phase0-reference/storage.py --json
=> {"ok":true,"lint":{"ok":true,"passed":3},
    "validate":{"ok":true,"contract":"Storage","methods":2,
    "view_methods":1,"write_methods":1,"ctor_params":1}}

genvm-lint typecheck phase0-reference/storage.py --json
=> ok=true, diagnostics=[], errors=0

genvm-lint typecheck phase0-reference/storage.py --strict --json
=> exit 1, ok=false, SDK decorator reportUnknownMemberType

npm view genlayer-js version dist-tags
=> latest 1.1.8 / rc 2.0.0-rc.1

Node createClient({chain: studionet}).getChainId()
=> 61999

Vite build({plugins:[react()], build:{write:false, lib:{entry:existing React module}}})
=> PASS, one in-memory output chunk; no ContextPass app written
```

Python Direct Mode 对官方 Storage 示例使用显式 `sdk_version='v0.2.16'`，VMContext.activate 内成功验证构造初值、读取、更新和更新后的读取；无 Docker、无 GenLayer 私有节点、无网络 LLM、无链上部署。固定 SDK 源码及实际导入确认 TreeMap / DynArray / Address 和 run_nondet_unsafe 可用。

另行执行通用 Direct Mode mock_llm / run_nondet_unsafe / run_validator 冒烟：固定测试字符串的 leader 与 validator 各调用一次本地 mock，结果比较成功，没有执行 ContextPass 分类 prompt，没有访问外部 AI。Direct Mode 的 run_validator 是测试辅助入口，不会自动等价于真实多 validator 共识。Phase 2 必须显式测试 Validator 独立重新分类及 disagreement/rollback；不能因为本轮工具能导入就宣称 N01–N10 通过。

## 5. GitHub、全部实现依赖及成本

认证核验使用的连接是 `gqzy1` 对应连接，返回 login=gqzy1 / id=155161534。未调用 halihalibt 连接，未读取或写入其仓库。

未来目标路径只来自冻结文档，当前未创建或探测其存在：

- A：gqzy1/context-bound-attestation-genlayer
- B：gqzy1/contextpass-genlayer

| 依赖或服务 | 必要性与成本 |
|---|---|
| Hosted Stable Studio / Studionet | 唯一网络；免费开发路径，官方提供内置测试 GEN faucet。本轮未领 faucet、未消费交易测试 GEN |
| Python SDK / genlayer-test / pytest / genvm-linter / pyright | 本地工具及公开官方 artifact；本轮无需付费授权 |
| React / Vite / TS / genlayer-js / viem / plain CSS | 静态前端依赖；不需要付费托管、数据库或商业组件库 |
| Vitest / React Testing Library / jsdom | 本地前端验收工具；不需要付费测试服务 |
| GitHub / GitHub Pages | 公开仓库 + 默认 github.io 域名的免费路径；GitHub 官方明确 Free 的公开仓库可使用 Pages |
| 用户浏览器钱包 | 后续用户手动签名；前端采用用户已有注入钱包路径，无必须购买的 WalletConnect/托管签名服务 |
| 后端 / 索引器 / 数据库 / 独立 LLM API | 冻结 MVP 不需要，不引入 |
| Docker / 本地 GenLayer 节点 / GenLayer CLI | 本轮未安装；Direct Mode 与 Hosted Studio 路径不需要；不因缺失这些工具判失败 |

本轮新增现金支出：0；付费 API 调用：0；链上交易：0。未来交易可能消费 faucet 测试 GEN，不承诺测试 GEN 零消耗或 faucet 永久无限可用。GitHub Pages 部署能力、账户限制和用户测试余额在对应阶段再查。本报告不承诺 Work 额度消耗、未来免费服务永不变或审核结果。

## 6. 问题、处理及阻断判定

### E01 — Python RPC 403（非阻断）

urllib 发出只读 eth_chainId POST 返回 HTTP 403；RPC GET 返回 405（该端点使用 JSON-RPC POST）。Node genlayer-js 的同网络实际调用返回 61999，浏览器 Studio 可达。尚无足够证据确定 Python 403 根因，不能推断网站机器人封禁或永久不支持。

处理：冻结前端使用已验证的 genlayer-js / studionet；Python 本地业务测试使用 Direct Mode。若未来某阶段确需 Python 网络客户端，先重新做一次只读检查，不进入反复重试、切换网络或发送交易。本轮未为绕过限制更换网络。

### E02 — Strict Pyright 对 SDK 装饰器告警（非阻断）

严格检查对官方示例 `@gl.public.view` 报 `reportUnknownMemberType`，指出 view 的 `(f: Unknown) -> Unknown` 类型。JSON 的 diagnostics 包含 error，虽然 summary.errors 显示 0；按 `ok=false` 与 exit 1 判 FAIL，没有依赖不一致的 summary 数字来标 PASS。

最初未把虚拟环境 bin 加入工具进程 PATH 时出现 pyright not found；补上 PATH 后工具实际执行，得到上述严格诊断。默认 typecheck 则通过。

冻结验收要求静态 lint / typed methods / SDK serialization，未要求 Pyright --strict 全绿。Phase 1 应使用必需的 `genvm-lint check` 和默认 typecheck，明确记录可选 strict 诊断；如建立 strict 门槛，应仅针对已确认的 SDK 类型边界处理，不能全局屏蔽业务错误，也不能改协议语义。

### E03 — 自动 latest / 默认配置风险（已识别）

GitHub GenVM latest 与 Stable Studio 目标不同；工具自动选择最新或缓存可能误用 RC。后续 Direct Mode 显式指定 v0.2.16，合约保留精确 Depends。genlayer-test 的 pytest 插件发现会打印默认 localnet 配置，但本轮没有调用集成 fixtures 或任何 localnet RPC；Phase 1/2 仅运行 Direct Mode。后续网络配置必须显式锁定 studionet，禁止默认配置意外触发其他环境。

**当前必要环境硬阻断：无。** 独立语义共识的真实收敛、产品链上 gate、源代码一致性与实时签名均属于后续验收，不是本轮已证明的能力。

## 7. 下一阶段建议与停止记录

建议：用户另行批准后进入 **PHASE 1 — Repository A skeleton + deterministic core ONLY**。创建仓库之前再次确认认证账号 gqzy1，并确认该阶段明确授权仓库创建。只实现冻结确定性核心与 D01–D24；不加入语义 LLM、前端、部署或交易。

下一执行者先读冻结包和本报告，按版本表重建环境，不假设临时环境仍存在；对 genlayer-test 显式指定 SDK v0.2.16。项目 lockfile 和 PROJECT_CHECKPOINT.md 在真正的实现阶段生成。本轮没有制作虚构的 Phase 1 checkpoint。

本轮完成状态：环境报告已完成；未创建/修改 GitHub 仓库、分支、commit、PR；未编写 ContextPass 合约或前端实现；未部署、升级、提交交易或进入 Portal；未请求、读取、保存或输出私钥/助记词；未访问其他 GenLayer 测试网。

**STOP — 不自动进入 Phase 1。**

## 8. 官方来源

以下来源结合本轮实际命令与 UI 观察使用，不将文档说明当作真实交易证据。

- [GenLayer Networks](https://docs.genlayer.com/developers/networks)：Stable Studionet 与 preview 区分。
- [GenLayer Studio](https://studio.genlayer.com/contracts)：本轮实际观察的官方模板 header。
- [GenVM v0.2.16 release API](https://api.github.com/repos/genlayerlabs/genvm/releases/tags/v0.2.16)：artifact 元数据和 digest。
- [GenVM v0.2.16 release](https://github.com/genlayerlabs/genvm/releases/tag/v0.2.16)：官方发布。
- [genlayer-test PyPI 元数据](https://pypi.org/pypi/genlayer-test/json)：版本、Python 要求及依赖。
- [genvm-linter PyPI 元数据](https://pypi.org/pypi/genvm-linter/json)：版本和依赖。
- [genlayer-js npm 元数据](https://registry.npmjs.org/genlayer-js/latest)：稳定版本；dist-tags 同时用 npm view 核验。
- [Direct Mode reference](https://docs.genlayer.com/api-references/genlayer-test/direct)：fixture 和测试能力。
- [GenVM Linter](https://docs.genlayer.com/api-references/genlayer-linter)：lint / validate / schema / typecheck。
- [Non-determinism](https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism)：custom validator 与状态写入边界。
- [GenLayerJS](https://docs.genlayer.com/api-references/genlayer-js)：网络 client、合约和交易 API。
- [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)：Free 公开仓库静态托管。
