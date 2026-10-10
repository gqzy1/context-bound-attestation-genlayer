# FRONTEND_ACTIVATION_REPORT — Phase 4C

**代码激活补丁完成；未发布，未进行真实签名/交易。** 生产只使用真实SDK，默认写入只许可已证实canonical部署。所有真实前端钱包操作验收NOT RUN，与已完成的Studio T01–T10分开。

| 4A计划条件 | 实际实施 / 证据 |
|---|---|
| 验明部署/版本/ABI | 23项只读操作；source SHA、字节和5写6读核对 |
| 静态canonical配置 | protocol.ts 固定address/61999/RPC/SHA；部署tx和证据manifest同源测试 |
| 双层guard | Transactions.submit + SdkTransport.write各执行assertCanonicalTarget；拒绝其他目标的独立测试证明wallet/storage/factory/write不触发 |
| 任意inspection只读 | 表单控件禁用，并且writeTarget返回canonical；底层直接调用仍拒绝foreign目标 |
| 手动钱包 / 无自动交易 | connect由按钮触发；写由form触发；mount/reload无签名、无发送、无自动poll；测试已证明 |
| 钱包安全 | 原Wallet.assert+guardedProvider检查chain61999/account，并保持single-send/禁raw-sign；拒签事件与晚切换原测试保留 |
| 真实receipt结构 | 捕获T02–T10真实RPC，离线pinned SDK重放；按mode=leader选择，避免把quorum后取消的validator当Leader |
| FINALIZED+接受+正常执行 | status FINALIZED、MAJORITY_AGREE、Leader SUCCESS/Return，错误/缺角色安全拒绝；transaction binding不放松 |
| 方法专属readback | 原五写方法matching readback不变；历史ELIGIBLE恢复后不推导active；Rollback未冒充NOT_ELIGIBLE |
| journal恢复 | 签名前保存intent；hash保存；reload cached confirmed降级；未知提交保留并阻止重复；共识无法验明保持undetermined |
| RPC可靠性 | 原single-flight/350ms/Retry-After/shared cooldown/3次read attempts；不自动重发write |
| 真实示例 | root1撤销，Room1历史ELIGIBLE与active=false分开；Room2拒绝；公开note保留；Fresh按钮手工读取 |
| 保留协议/锁版本 | A/B Python原字节、freeze/Prompt/权限/状态机/Equivalence/依赖全部不变 |

改动范围：protocol.ts、transactions.ts、transport.ts、main.tsx、App.tsx、public manifest及文档/测试。未增加合约方法、修改SDK或引入付费依赖/数据库/后端。WRITES_LOCKED=false只取消阶段全禁，两个实际canonical-target检查继续独立执行，不是以任意手填地址为写目标。

现有124前端用例保留，新增20激活用例与1manifest用例，145/145 PASS；其中真实收据重放仅为离线兼容性证据。历史阶段文字/fixture binding随合法激活更新，明确锁定测试仍显式注入locked=true验证不得调用钱包。生产没有Test wallet/MockTransport。

真实SDK receipt的结果字段和mode/execution_result/consensusRaw来自实际捕获数据；未知或矛盾payload不得猜成功。字段变化时应安全暂停、保存原始响应，不能放宽确认或悄悄改协议。NOT_ELIGIBLE来自正常返回且链上matching永久决定；Rollback是确定业务拒绝；未决/未验共识阻止新写；RPC错误保留已保存ID。

SDK严格编码绑定保持精确：Studio历史T02/T03/T06使用数值地址calldata；前端新写保持CalldataAddress。不得把integer/address展示字符串相同当作字节一致、也不得用另一笔手工Studio交易代替当前journal里的签名结果。手工输入恢复hash必须对应相同sender/contract/method/原始编码arguments。

无授权链上操作在测试中发生。实际签名、front-end submit→FINALIZED→readback→reload仍NOT RUN。正常浏览器本地URL不可达，visual/console NOT RUN。解锁只存在独立Draft代码中，既有Phase3/4B branch和main保持锁定原状；未发布网站。

复原方案（仅下一次需要时另行提交）：设阶段locked=true，同时保留两个canonical guard与所有journal/evidence，不清空未知交易，不发送逆交易。当前不进行回滚或链上状态变更。

**STOP，等待人工验收和后续明确发布/真实钱包测试授权。**
