# RELEASE_READINESS_CHECKLIST — Phase 4C

**NOT READY FOR PUBLIC RELEASE。** 集成/证据完成，实际前端浏览器与钱包验收未完成；发布、merge、Portal和新交易尚未获授权。本文件是人工QA/审批清单，不是自动执行计划。

| 项目 | 状态 / 证据 |
|---|---|
| gqzy1身份、A/B独立分支、旧Draft/main完整 | PASS；github-baseline与最终PR核验 |
| Stable61999，真实canonical源码A/B/部署相同 | PASS；e50cb670…源码和integrity.json |
| Studio T01–T10真实证据 | 已完成人工验收；本轮收据/当前状态只读重核PASS；Explorer网页UI未重新验证 |
| T07 rotation/error/disagree保留 | PASS；不得改称全票一致 |
| 撤销后当前资格false，公共历史保留 | PASS；state-readback.json |
| 合约240、前端145测试，TS Strict，build，static/default | PASS；实际原始日志 |
| Python Strict | FAIL；原7条SDK诊断未解决，需明确保留风险接受记录 |
| Frontend正常Desktop/Mobile/console | NOT RUN；正常浏览器本地ERR_CONNECTION_REFUSED |
| 浏览器真实wallet connect/disconnect/wrong chain/events/refusal | NOT RUN；仅offline Test wallet PASS |
| 真实前端用户签名/submission/FINALIZED/readback/reload | NOT RUN；仅offline兼容/恢复PASS |
| GitHub Pages实际静态托管 | NOT PUBLISHED / NOT RUN；离线base/hash检查PASS |
| Portal submission | NOT SUBMITTED |
| 两个新Draft审查/未来依赖合并 | PENDING用户审查和另行批准；本阶段无merge |

## 无链上交易的人工浏览器QA

在正常本地环境npm ci / npm run dev（或npm run build后本地preview），使用`/contextpass-genlayer/`，保存版本、时间、截图和console/network日志。不得使用代理/隧道/安全限制绕过。

- Desktop1440×900、mobile390×844：Overview、Spaces、Credentials、My admissions四hash路由；文字/长地址不溢出、按钮触控、标签/键盘focus、无运行时console error。
- `#/overview`、`#/spaces`、`#/credentials`、`#/admissions`直接打开和reload，未知route fallback；项目base静态资源200，无backend请求。Pages真实host留待另行发布授权，不能由本地页面推断已通过host验收。
- Visitor无自动RPC/wallet/sign/send；canonical默认，显式fresh example读取root1revoked、Room1历史ELIGIBLE/当前inactive、Room2denied/inactive与note1历史。
- 其他inspection地址仅read-only，所有写入口禁用；返回canonical后仍须钱包61999及人工动作。不要点击实际提交。
- 无wallet、错误chain、connection refusal、account/chain切换和disconnect（如用户允许connect）：旧membership清空、不自动切链、不自动签名、不放大RPC。
- 已有journal只读恢复时缓存确认降级，手工refresh严格绑定；不清空unknown再试，不把读取成功当作交易成功。
- 标记每项PASS/FAIL/NOT RUN并保存真实证据。Mock/CSS/component通过不能替代这个列表。

## 后续真实前端操作（需要新授权，本阶段不执行）

用户需先明确授权有限测试及逐笔人工签名。不可复用revoked root1，Wallet B现有两room决定不能重复申请。新数据须真实返回IDs、issuer/holder/space规则相符；不改旧历史、不制造成功演示。验证拒签4001、一次send、真实tx ID、FINALIZED/接受/Return、精确readback、reload恢复和未知hash人工核对。遇真实分歧/持续未决停止后续共识写入；不得改Prompt/equivalence/leaderOnly或反复交易制造结果。费用/测试GEN和免费RPC配额按当时真实情况记录。

## 未来发布与合并门槛

先补上述QA、确认风险/源码/版本/PR diff，再获得用户独立授权。A顺序#1→#2→#3→Phase4C；B #1→#2→Phase4C。每次父合并后复核/retarget子diff及HEAD，保持A/Bbyte一致。不得自动合并。Pages publish、public hosting QA和Portal各自等待明确授权。未满足门槛不要宣称Projects已发布或Portal提交成功。

**STOP。**
