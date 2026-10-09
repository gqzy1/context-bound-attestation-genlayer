# PROJECT_CHECKPOINT — ContextPass A

**阶段：** PHASE 2 — Independent Leader / Validator Consensus，离线完成。
**账号：** gqzy1 / ID 155161534，已再次核验。
**Repository：** gqzy1/context-bound-attestation-genlayer。
**新分支：** phase2-independent-consensus。
**Base：** phase1-deterministic-core，精确基线 6f498abbf1525f304174ed2018509a4445d441c8。
**实现/测试 commit：** a1ec692946c787d3abbd329397638dc51365ed45，后续文档补充 commit 不改变合约/测试。
**Draft PR：** [https://github.com/gqzy1/context-bound-attestation-genlayer/pull/2](https://github.com/gqzy1/context-bound-attestation-genlayer/pull/2)，Draft/open/unmerged；目标 phase1-deterministic-core。
**最终 HEAD：** 查询 PR 当前分支；外部交付报告补充最终提交，避免文件自引用。
**Phase 1 PR #1：** Draft/open/unmerged；保持原状。

## 1. 总目标

单一原始凭证范围覆盖的 GenLayer 准入 primitive；后续产品使用字节一致源码。只用 Stable Studionet 61999，用户手动签名，零付费后端/API。当前只有 Repository A。

## 2. 本阶段目标

在既有私有语义边界实现锁定 SDK custom run_nondet_unsafe：Leader 与各 Validator 原始输入独立完整分类，严格一字段解析与 exact 标签比较。完成离线 N/S 和 D 回归后 STOP。

## 3. 已确认完成及证据

- 163/163 PASS，0 failed/errors/skipped；D54、N61、S40、补充8。JUnit、实际命令与离线 trace 在 evidence/phase2/。
- 101 个 trace 记录 183 次离线脚本模型调用；N09 证明 Leader + 3 个独立 Validator 同 Prompt 调用及后续反对票阻断测试闸门。
- 原生 Direct Mode 捕获和重跑生产 Validator；锁定 cloudpickle 回调序列化通过；不宣称网络共识。
- Static lint/schema PASS（5 writes/6 views/0 ctor args），default typecheck PASS，pip check PASS。
- Raw strict FAIL：6 条原 public.view 上游告警 + 1 条 SDK run_nondet_unsafe 泛型告警，原始记录保留且无全局屏蔽。
- 冻结文件、存储注解/record、其余方法 AST、lockfile 与 Phase 1 相同；权限、根绑定、撤销与留言保持不变。
- README、CONSENSUS、TESTING、SPEC/部署状态文档与阶段报告已更新；Phase 0/1 报告和证据未改动。
- 没有真实模型/网络结果、部署/交易、前端、Repository B 或 merge。

## 4. 冻结决定

一条独立自定义语义共识入口；七规则 Canonical Prompt；两标签 exact 比较；
不转移、不传递、root-only、one-decision-ever；immutable issuer/scope；
issuer-only 撤销与动态禁写；公开历史/20 页上限/30 留言上限不变。

## 5. 未解决问题与边界

Strict SDK 类型元数据未修复。真实 S 模型分类/注入抵抗与多 Validator 收敛、轮换、finality 尚无证据。
S 设计标签只是测试脚本，不是实测准确率。任何未决/异常不能记为 NOT_ELIGIBLE 或批准。
Direct Mode 测试内同步 executor 不等于网络 majority 或 rollback 实现。

## 6. 排除选项

未采用 strict_eq / prompt_comparative / prompt_non_comparative、JSON-only Validator、
Leader 结论入 Prompt、方便等价/容差、客户端结果、管理员 grant、其他测试网、
付费服务或旧项目代码。没有因类型告警改变协议或全局关闭检查。

## 7. 依赖与假设

原 Phase 0 Python 3.12.14 / GenVM v0.2.16 / SDK 精确 runner / test0.29.2 / linter0.11.0；
requirements.lock.txt 不变。序列化测试提取原 cloudpickle runner，无新版本。
无新增现金支出。B 尚未授权，因此跨仓源码一致性与前端 F/T 不适用本轮。

## 8. 下一步

STOP。仅等待用户明确批准 PHASE 3，再按冻结规格建立 B 最小前端；不自行 merge/deploy/交易。
后续真实网络与用户签名应另行授权。

## 9. 恢复说明

先完整读取冻结文件、Phase 0/1/2 报告、checkpoint，再核验实际 main/Phase 1/Phase 2 分支与两份 Draft PR。
Phase 1 尚未 merge，Phase 2 PR 目标是 Phase 1 分支。不得凭离线记录推断链上 Finalized 或已准入。
只执行最新明确授权阶段。
