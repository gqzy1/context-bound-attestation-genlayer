# PHASE_4B_ADDRESS_COMPATIBILITY_REPORT

**2026-10-10 — 地址规范化修复与离线验收 PASS；Python Strict 仍 FAIL（7 条原有上游 SDK 诊断）。补丁尚未部署，T02–T10 保持暂停。**

本轮使用 gqzy1（再次认证 login=gqzy1 / ID155161534）。没有部署、升级、发送真实交易、解锁前端、发布 Pages、合并 PR、提交 Portal 或处理私钥/助记词。完成后 STOP。

## 1. 基线与用户提供的真实证据

A 从 `daf0bf9a70357fb626b0a8e732826c8db6e0c1fc` 的 phase2-independent-consensus 创建独立 phase4b-address-compatibility 分支。B 从 `3c9760cf6e1eb444123b9a85296a174fd98b4123` 的 phase3-frontend-integration 创建同名独立分支。main 和原有 Phase1/2/3 PR 不修改、不合并。完整冻结架构/Canonical Prompt/测试、现有源码及原测试为实现依据；冻结9文件 A/B 对照基线逐字节未改，见 freeze-integrity.json。

用户提供：旧合约 `0x97B9003a17A8EDBD1b5E3379AA659753791497d9` 部署 FINALIZED / Accepted / SUCCESS；两次 issue_attestation 均 FINALIZED / Rollback / INVALID_ADDRESS，第二次输入正确 B 且 Explorer 显示整数。get_decision(1,B) 出现泛化读取错误，get_counts 全零。

本轮未独立取得失败交易 ID、完整 raw calldata 或 Explorer 显示的精确十进制值。这些链上状态是用户报告，不伪装为本轮实测。特别是 **get_decision 的泛化错误不能单独证明根因**；没有真实 Studio 页面或网络 Validator 测试成功的声明。

## 2. 已确认的源码根因与真实 SDK 复现

旧 `_address` 只接受 `isinstance(value, Address)`，拒绝所有合法整数/字节/字符串。锁定 SDK 的 `calldata.decode` 保留 wire 类型：地址标记返回 Address，普通整数返回 int，字节返回 bytes，字符串返回 str。公开方法的 Address 注解用于 schema，不自动转换输入；原 SDK `_genlayer_runner.py` 直接调用 `meth2call(contract_instance, *cd.get('args', []), **cd.get('kwargs', {}))`。

**先复现、后修改**：初始 regression 通过实际 Python SDK encode/decode 传入 `int(Wallet B,16)`，解码确认为 int；真实消息 sender 是 Wallet A 的 Address；调用原 issue_attestation 在 `_address(holder)` 抛 INVALID_ADDRESS。首次命令 exit1、1 failed，原始 traceback/JUnit 保存在 before-fix.log/xml。之后相同用例修复后 PASS。

另外使用真实 genlayer-js **1.1.8** `abi.calldata.encode` 为 A/B 各生成 Address 标记、BigInt、Uint8Array、字符串四种方法调用 envelope，八组原始十六进制 Calldata 经锁定 Python SDK 解码，再进入生产公开方法，全部通过。见 js-calldata.json 与 8 项跨语言测试。生成器只导入 ABI/地址类型，没有 client、钱包签名或网络调用。

这里确认的是**原合约的输入规范化缺陷**及与用户整数输入现象一致的可复现路径。不能从 Explorer 的显示形式推断全部原始 wire 类型；实际失败交易的 bytes、十进制精确值及端序仍需补充验证。补丁的真实 Stable Studionet 重跑尚未执行，不能宣称已解决该部署上的全部异常。

### 端序与 SDK 类型事实

Pinned SDK `Address` 构造器接受 hex/base64 字符串和20字节 buffer，**不提供数字地址转换**；直接 Address(integer) 会走 bytes(integer)，不是合法规范化办法。`Address.as_int` 是 **little-endian**。本边界将整数明确定义为常规 `int('0x…',16)` 的160位数值，以20字节 **big-endian** 转换，不猜测、不按账户角色自动翻转。as_int 与同地址的十六进制整数不同，专门测试了这一点。

Wallet A：`0xEB56F245EFEceD0899b7e23697FeE512a39DBdCc`；Wallet B：`0x5EDb6E65aaEA10A7B3CC34e8d5724e41D1f6da84`。只有公开地址进入离线测试；没有签名/账户密钥。

SDK 原文件哈希、构造器/消息/dispatcher 摘录：pinned-sdk-source.json、sdk-runtime-excerpts.txt。当前官方地址文档 https://docs.genlayer.com/developers/intelligent-contracts/types/address 仅作参考；最终以 v0.2.16 提取的实际源码和测试为准。

## 3. 最小改动与安全范围

生产合约**仅修改 `_address` 函数**，AST 比较移除该函数后与 Phase2 基线完全相同。五个公开写方法、六个只读方法的签名及其实现、构造参数、存储结构、权限控制、状态机、Canonical Prompt、Leader/Validator、Equivalence Principle 均不变。

- 接受合法 Address、非零且小于2^160的整数、20字节 bytes/bytearray/memoryview、完整 0x+40 hex 字符串和严格 canonical base64。
- 各表示统一构造规范 Address；拒绝零地址、bool、负数、越界整数、错误长度、非法 hex、非 canonical/含垃圾 base64、其他类型。数字不截断、不浮点转换；不剥离空白或猜测端序。
- issue_attestation / create_space / get_decision / is_active_member 既有边界均直接得到修复；gl.message.sender_address 保持原 SDK Address，不改变 sender 信任来源。
- A/B 别名身份比较、自签发拒绝、holder-only、issuer-only、trusted issuer、非会员/已撤销留言拒绝均回归通过。任何地址输入都不能改变来源身份或绕过共识。
- B 完整合约副本逐字节同步，生产 TS 只更新源码哈希；adapter/service 两层写入锁未改，仍 WRITES_LOCKED=true。新增前端测试和来源/部署清单区分旧部署与未部署候选。

**为何旧测试漏掉：** 原 Direct Mode 并非绕过 Calldata。原正常流程先构造 Address 对象，编码带地址标记，解码仍 Address；D04 只测坏字符串/长度和零地址，缺少合法整数/字节/字符串通过相同公开方法的路径。新测试补足这一表示兼容性缺口，不替换原163项。

## 4. 版本、源码与最终验证

| 检查 | 实际结果 |
|---|---|
| GenVM / Depends | v0.2.16 / py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6，未变 |
| Stdlib | py-lib-genlayer-std:11rhn002yfajawsz7fai6mykznbxkxs6l91iskj5cm82c92qhy3v，未变 |
| Python / Direct Mode / linter | 3.12.14 / genlayer-test0.29.2 / genvm-linter0.11.0 |
| pytest / pyright / JS SDK | 9.1.1 / 1.1.414 / genlayer-js1.1.8 |
| 修复前原源码复现 | EXPECTED FAIL，1 failed，INVALID_ADDRESS traceback |
| 新地址兼容性套件 | 77/77 PASS |
| A 全部回归 | **240/240 PASS**，原163+新77；0 failures/errors/skips |
| B 全部前端测试 | **124/124 PASS**，原116+新8；0 failed/pending |
| 基础静态 / schema | PASS，11 methods / 5 writes / 6 reads / 0 constructor params |
| Python 默认类型检查 | PASS，无诊断 |
| Python Strict | **FAIL，exit1 / ok=false，7条 reportUnknownMemberType** |
| TypeScript Strict / skipLibCheck=false | PASS |
| 前端生产构建 | PASS；保留已有 >500kB chunk 提示 |
| pip check | PASS |
| 冻结文档 / AST / A-B副本 | PASS，未改协议，byte-identical |
| 真实 Studio/网络/多Validator/升级测试 | NOT RUN |

Python Strict 最终七条是六个 SDK public.view 缺类型注解、一个 run_nondet_unsafe Result 泛型未知。工具 summary.errors=0 与 diagnostics 不一致，依据 exit/ok/实际列表标为 FAIL。没有全局屏蔽、ignore、SDK修改或虚报。首次修复 Strict 有新增 memoryview 参数未知诊断（共8条），已通过 `.tobytes()` 安全转换修正并全部重跑；strict-initial-eight-diagnostics.log 保留。前端新增测试首次类型检查出现3条字符串/hex类型诊断，已明确 literal 类型并重跑 PASS；typecheck-initial-failure.log 保留。

旧源码 SHA256：`4412035632f586b72c376fb42e618f68ff665063cf356dd727849d76dd7f08ec`。

**补丁候选 A/B 新 SHA256：`e50cb6703ba63da5095dafc5d9867246888c5151d0773489aed3166033484b3d`。**

A `contracts/context_bound_attestation.py` → B `intelligent-contract/contracts/context_bound_attestation.py` 二进制复制，无重写、压缩或换行转换。source-integrity.json 记录新 blob 和 AST 核验。旧已部署地址不能被绑定到新源码哈希。

## 5. 实际执行命令与证据

以下为实际路径（cwd A/B 如标注）；command-results.json 保存完整绝对命令/退出码，全部证据在各仓库 evidence/phase4b/。

```bash
# 环境恢复：原 venv python symlink 失效，首次 genvm-lint exit127；修复后沿用同版本
python -m venv --upgrade phase4a-env
phase4a-env/bin/genvm-lint download --version v0.2.16
# 官方 216630904-byte 制品 SHA256 4f0b358ec98ec148be9b95cdfb0f0e1a6cbe64da0194fdfac3fffc6f5d1d93e2 复核
# cwd A
../phase4a-env/bin/python scripts/prepare_direct_sdk.py
../phase4a-env/bin/python -m pytest tests/direct/test_address_compatibility.py -q --junitxml=evidence/phase4b/before-fix.xml
../phase4a-env/bin/python -m pytest tests/direct/test_address_compatibility.py -q --junitxml=evidence/phase4b/address-results.xml
../phase4a-env/bin/python -m pytest tests/direct tests/consensus -q --junitxml=evidence/phase4b/all-results.xml
../phase4a-env/bin/genvm-lint check /workspace/scratch/114f91cc6678/repository-a/contracts/context_bound_attestation.py --json
PATH="/workspace/scratch/114f91cc6678/phase4a-env/bin:$PATH" ../phase4a-env/bin/genvm-lint typecheck /workspace/scratch/114f91cc6678/repository-a/contracts/context_bound_attestation.py --json
PATH="/workspace/scratch/114f91cc6678/phase4a-env/bin:$PATH" ../phase4a-env/bin/genvm-lint typecheck /workspace/scratch/114f91cc6678/repository-a/contracts/context_bound_attestation.py --strict --json
../phase4a-env/bin/python -m pip check
# cwd B（最初同等 inline Node 生成器，随后保存此可重复脚本；输出逐字节一致）
node scripts/generate-address-calldata.mjs > evidence/phase4b/js-calldata.json
npm test -- --reporter=json --outputFile=evidence/phase4b/frontend-results.json
npm run typecheck
npm run build
npm run verify:source
```

全量共识测试使用 CONTEXTPASS_TRACE_FILE 指向 evidence/phase4b/consensus-traces.json。原 N/S 的离线模型脚本和独立 callback 测试保留；不宣称真实模型、网络多 Validator 或 FINALIZED。新公开入口权限测试中的 boundary 是 TEST ONLY 的确定性隔离，不进入生产源码。所有 Direct 测试禁用网络 socket 与集成插件。

## 6. Draft PR 交付

A：gqzy1/context-bound-attestation-genlayer；head phase4b-address-compatibility → base phase2-independent-consensus。
B：gqzy1/contextpass-genlayer；head phase4b-address-compatibility → base phase3-frontend-integration。

A 实现/source commit：`7a7078cfb07c1d65faf5db432049a5287ce4f5a6`；[Draft PR #3](https://github.com/gqzy1/context-bound-attestation-genlayer/pull/3)。

B 实现/打包 commit：`61aac58e0b465a71a0fe3cf4162b1b10f43d1128`；[Draft PR #2](https://github.com/gqzy1/contextpass-genlayer/pull/2)。

两者创建与只读复查均确认 Draft/open/merged=false，作者 gqzy1。后续仅报告/证据/checkpoint 的文档提交不改变源码；最终 HEAD 以 PR head 为准，避免文件自引用。通过公开 git fetch 取回两个精确提交，远端 A/B 合约与本地字节及新 SHA 完全一致。github-verification.json 记录初始补丁提交后的只读快照。

原 A PR1：head 6f498abbf1525f304174ed2018509a4445d441c8；PR2：head daf0bf9a70357fb626b0a8e732826c8db6e0c1fc；B PR1：head 3c9760cf6e1eb444123b9a85296a174fd98b4123；均仍 Draft/open/unmerged。main 仍 A770aa5d4cf6d4ef2b6ef28fb8c81c78230a6fa0b、B5095cdc5503dda4642c917cfa4576d1286c36319。未使用 halihalibt 连接或修改其任何仓库。

## 7. 尚未解决的风险与下一步建议（本轮不执行）

1. 补充第二次失败交易 ID/原始 calldata/精确十进制整数；必须与 `int(Wallet B,16)` 对照。若表示为 SDK little-endian as_int，不得悄悄翻转推断身份；先明确调用侧转换来源。当前八组 SDK 测试证明规范映射，**不等于取得了实际失败交易字节**。
2. 普通 get_decision 错误仍需 RPC 错误明细验证；该入口的整数回归通过不证明网络/Studio错误全部消失。
3. 现有部署继续运行旧代码。优先在另行授权、人工签名后以精确新源码**重新部署**到 Stable Studionet61999，构造参数空；保存真实部署 tx/finality/source/hash。项目没有应用级 upgrade 或状态迁移入口，未验证平台升级能力，不承诺原地址可原地升级。本轮不执行任何部署或升级。
4. 新地址和源码验证后才能重新开始 T02–T10。使用真实返回 root/space IDs；A issuer/owner，B holder；先核对存储 issuer/holder/trusted_issuer，再申请准入。真实共识可能拒绝/分歧/未决，必须安全停止，不放宽 Prompt 或 Equivalence Principle。
5. 旧 counts 全零仅为用户报告，应在人工操作前读回确认；不得假造状态迁移成功。新候选没有链上证据。前端写入锁和空 candidate address 保留，不能提前声称 Verified Demo。
6. Python Strict 七条上游诊断、真实 SDK/GenVM全网络运行和多 Validator收敛风险保留。不增加付费依赖或切换网络。

**STOP：本轮只完成地址兼容性修复、离线验证和 Draft PR；等待用户进一步明确授权及真实链上证据。**
