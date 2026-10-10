# ONCHAIN_EVIDENCE_INDEX — Phase 4C

Stable Studionet / **61999** / `https://studio.genlayer.com/api`。Canonical contract: `0xDe9abfBe2E4A61d23e27b552e241f5Bb1d1821b8`。SHA256: `e50cb6703ba63da5095dafc5d9867246888c5151d0773489aed3166033484b3d`。Wallet A: `0xEB56F245EFEceD0899b7e23697FeE512a39DBdCc`；Wallet B: `0x5EDb6E65aaEA10A7B3CC34e8d5724e41D1f6da84`。

真实 Studio T01–T10 由用户人工执行；本阶段仅使用锁定 genlayer-js 1.1.8 **只读重新核验**。23/23 SDK 操作成功：chain、源码、ABI、十笔交易、十项最终态读取。操作和 HTTP 的实际 UTC 时间在原始记录中。Explorer 网页抓取 T04/T07 受限，**未重新验证网页 UI**；用户原截图与本阶段实际 RPC 返回是不同证据来源。未制作新 Explorer 截图。

A/B/部署源码逐字节相同。零构造参数、五写六读。公开交易链接保留在下表；`MAJORITY_AGREE` 是 RPC 原始字段，历史轮次同时给出 `Accepted`。Accepted 共识不等于业务成功：T08/T10 是接受的 Rollback。

## T01–T10 最终收据

| 步骤 / 真实交易 | 钱包 / 方法 | FINALIZED / Consensus | Leader GenVM / 返回 | 最终 Validator 票 / Rotation |
|---|---|---|---|---|
| [T01](https://explorer-studio.genlayer.com/transactions/0x26282c539033879705d9a8dea18c8676dae46c0cd09df9f91cb20d740f9be994)<br>`0x26282c539033879705d9a8dea18c8676dae46c0cd09df9f91cb20d740f9be994` | A / `deploy / constructor()` | FINALIZED / MAJORITY_AGREE (Accepted) | SUCCESS / Return / `null` | 5 agree / 0 |
| [T02](https://explorer-studio.genlayer.com/transactions/0x7ee1a2f00471548e57d7f88df97ac2eed586c5a2e219f7e0ef1626fe78a58208)<br>`0x7ee1a2f00471548e57d7f88df97ac2eed586c5a2e219f7e0ef1626fe78a58208` | A / `issue_attestation` | FINALIZED / MAJORITY_AGREE (Accepted) | SUCCESS / Return / `1` | 3 agree, 2 idle / 0 |
| [T03](https://explorer-studio.genlayer.com/transactions/0x5392bec255be79edc94e01992bfae19c13a66b71e416a0a0e37fa4e9249a0108)<br>`0x5392bec255be79edc94e01992bfae19c13a66b71e416a0a0e37fa4e9249a0108` | A / `create_space` | FINALIZED / MAJORITY_AGREE (Accepted) | SUCCESS / Return / `1` | 3 agree, 2 idle / 0 |
| [T04](https://explorer-studio.genlayer.com/transactions/0xd977e00d326e41b972c1560f3912b0c7f4cc1e8766544a0c7052956243bc0e50)<br>`0xd977e00d326e41b972c1560f3912b0c7f4cc1e8766544a0c7052956243bc0e50` | B / `apply_and_join` | FINALIZED / MAJORITY_AGREE (Accepted) | SUCCESS / Return / `ELIGIBLE` | 3 agree, 2 idle / 0 |
| [T05](https://explorer-studio.genlayer.com/transactions/0xc36ffd19c14b7a522ea1287b8b7440dc3494d1fbba232528e9e3e4811e2532d2)<br>`0xc36ffd19c14b7a522ea1287b8b7440dc3494d1fbba232528e9e3e4811e2532d2` | B / `post_room_note` | FINALIZED / MAJORITY_AGREE (Accepted) | SUCCESS / Return / `1` | 2 idle, 3 agree / 0 |
| [T06](https://explorer-studio.genlayer.com/transactions/0x7592f079b93662134a88d14a34242817314cfe02a413cd36584afd70d0ffb61d)<br>`0x7592f079b93662134a88d14a34242817314cfe02a413cd36584afd70d0ffb61d` | A / `create_space` | FINALIZED / MAJORITY_AGREE (Accepted) | SUCCESS / Return / `2` | 2 idle, 3 agree / 0 |
| [T07](https://explorer-studio.genlayer.com/transactions/0xbd5200b6dfbca29c91bd4c4f0d473b4447af4042e35b7db5423766a6ced838c6)<br>`0xbd5200b6dfbca29c91bd4c4f0d473b4447af4042e35b7db5423766a6ced838c6` | B / `apply_and_join` | FINALIZED / MAJORITY_AGREE (Accepted) | SUCCESS / Return / `NOT_ELIGIBLE` | 3 agree, 2 idle / 1 |
| [T08](https://explorer-studio.genlayer.com/transactions/0x42765027562169a896139dc2d676a4c0140179bdbd610c8d873e09ce6557a2dc)<br>`0x42765027562169a896139dc2d676a4c0140179bdbd610c8d873e09ce6557a2dc` | B / `post_room_note` | FINALIZED / MAJORITY_AGREE (Accepted) | ERROR / Rollback / `ACTIVE_MEMBER_ONLY` | 3 agree, 2 idle / 0 |
| [T09](https://explorer-studio.genlayer.com/transactions/0xcf88f40a1beab8a8c979b7c0f3442e0ba484ac79bda78da8668c4d214669f2d6)<br>`0xcf88f40a1beab8a8c979b7c0f3442e0ba484ac79bda78da8668c4d214669f2d6` | A / `revoke_attestation` | FINALIZED / MAJORITY_AGREE (Accepted) | SUCCESS / Return / `null` | 5 agree / 0 |
| [T10](https://explorer-studio.genlayer.com/transactions/0x9b3365e65452c635a0663218edec0913dddf59f777b1be9209b03763959da01b)<br>`0x9b3365e65452c635a0663218edec0913dddf59f777b1be9209b03763959da01b` | B / `post_room_note` | FINALIZED / MAJORITY_AGREE (Accepted) | ERROR / Rollback / `ACTIVE_MEMBER_ONLY` | 3 agree, 2 idle / 0 |

## 精确 calldata、真实对象及读回

整数用十进制字符串归档以避免 JS 精度损失；这是原始 Studio 数字 calldata，不是前端新发交易的编码。前端保留 CalldataAddress，合约兼容边界已验证二者。T02 holder 整数对应 Wallet B，T03/T06 trusted issuer 整数对应 Wallet A。

- T01: `{}`
- T02: `{"args":["541538612603074768941462119095399617015271840388","React UI components","Can develop and maintain React UI components."],"method":"issue_attestation"}`
- T03: `{"args":["React Components","Contribute React UI components to this room.","1343551800202270405973087331704405998159169174988"],"method":"create_space"}`
- T04: `{"args":["1","1"],"method":"apply_and_join"}`
- T05: `{"args":["1","Hello from an approved member"],"method":"post_room_note"}`
- T06: `{"args":["Security Audit","Perform security audits of production authentication systems.","1343551800202270405973087331704405998159169174988"],"method":"create_space"}`
- T07: `{"args":["2","1"],"method":"apply_and_join"}`
- T08: `{"args":["2","should not pass"],"method":"post_room_note"}`
- T09: `{"args":["1"],"method":"revoke_attestation"}`
- T10: `{"args":["1","should fail after revocation"],"method":"post_room_note"}`

ROOT_ID=1，ROOM1_ID=1，ROOM2_ID=2，NOTE_ID=1，来自真实返回及状态，非预设。当前 latest-final 状态：

```json
{
  "counts": {
    "attestations": "1",
    "decisions": "2",
    "notes": "1",
    "spaces": "2"
  },
  "root1": {
    "holder": "0x5EDb6E65aaEA10A7B3CC34e8d5724e41D1f6da84",
    "id": "1",
    "issuer": "0xEB56F245EFEceD0899b7e23697FeE512a39DBdCc",
    "label": "React UI components",
    "revoked": true,
    "source_scope": "Can develop and maintain React UI components.",
    "status": "FOUND"
  },
  "room1": {
    "id": "1",
    "owner": "0xEB56F245EFEceD0899b7e23697FeE512a39DBdCc",
    "required_scope": "Contribute React UI components to this room.",
    "status": "FOUND",
    "title": "React Components",
    "trusted_issuer": "0xEB56F245EFEceD0899b7e23697FeE512a39DBdCc"
  },
  "room2": {
    "id": "2",
    "owner": "0xEB56F245EFEceD0899b7e23697FeE512a39DBdCc",
    "required_scope": "Perform security audits of production authentication systems.",
    "status": "FOUND",
    "title": "Security Audit",
    "trusted_issuer": "0xEB56F245EFEceD0899b7e23697FeE512a39DBdCc"
  },
  "decision1": {
    "decision": "ELIGIBLE",
    "holder": "0x5EDb6E65aaEA10A7B3CC34e8d5724e41D1f6da84",
    "root_attestation_id": "1",
    "space_id": "1",
    "status": "FOUND"
  },
  "decision2": {
    "decision": "NOT_ELIGIBLE",
    "holder": "0x5EDb6E65aaEA10A7B3CC34e8d5724e41D1f6da84",
    "root_attestation_id": "1",
    "space_id": "2",
    "status": "FOUND"
  },
  "active1": false,
  "active2": false,
  "notes1": {
    "next_offset": "1",
    "notes": [
      {
        "author": "0x5EDb6E65aaEA10A7B3CC34e8d5724e41D1f6da84",
        "id": "1",
        "space_id": "1",
        "text": "Hello from an approved member"
      }
    ],
    "status": "FOUND",
    "total": "1"
  },
  "notes2": {
    "next_offset": "0",
    "notes": [],
    "status": "FOUND",
    "total": "0"
  }
}
```

T04 的 ELIGIBLE 是历史永久决定，**不表示现在 active=true**。T09 已撤销 root 1；当前两房间 active=false。T05 的历史 note 1 仍在 Room 1，Room 2 无留言，counts 为 spaces=2 / attestations=1 / decisions=2 / notes=1。T08/T10 Leader 明确 Rollback `ACTIVE_MEMBER_ONLY`，不是 RPC 失败、NOT_ELIGIBLE 或未决。T04 当时 active=true 是用户已验收的历史事实；本轮无法通过“当前读取”重建撤销前瞬时状态，未冒充重读。当前 SDK 状态快照不能证明失败前后所有瞬时计数；原始拒绝收据与当前历史共同归档。

## T04 / T07 与轮换完整性

T04 最终 Leader Return ELIGIBLE，equivalence output 0 为严格单字段 `{"decision":"ELIGIBLE"}`。T07 最终为 NOT_ELIGIBLE，对应单字段输出。真实调用不同于离线 S01–S20 的脚本预期，不将这两个实际语义样本外推为所有模型场景准确率。

T07 `rotation_count=1`，两轮：首轮 Leader Rotation，Leader ContractError / `exit_code 1`，stderr 为 `JSONDecodeError: Expecting value: line 1 column 1 (char 0)`；该轮 validator_results 包含 3 disagree、1 idle。后续轮 Accepted，Leader SUCCESS / NOT_ELIGIBLE，最终 votes 为 3 agree、2 idle。保留首轮错误及反对票，**不声称首次即成功或五票一致**。未修改 Prompt、Equivalence Principle、committee 或 leaderOnly。未来出现持续未决/分歧，应停止后续共识写入并交回证据，不调整协议来取得想要的结果。

## 每笔 Validator 信息

### T01

Final Leader: `0xE6BD8050758CB15fC88387223E31Ae2708B119dC`。初始 Validators: 5。

| Validator address | 最终 vote |
|---|---|
| `0x03D58A4DeF6fDFc032A56374785a5F571D07Bc11` | agree |
| `0x3D83ab507785b95ca5C208bEc80CCe3D5ca98100` | agree |
| `0xE6BD8050758CB15fC88387223E31Ae2708B119dC` | agree |
| `0xacc2459F341D7a887bcA8FAA62F1EC9378d4Bc67` | agree |
| `0xcE1d6bBB36B744536153966B4DD42276f5ADd0F8` | agree |
### T02

Final Leader: `0x3D83ab507785b95ca5C208bEc80CCe3D5ca98100`。初始 Validators: 5。

| Validator address | 最终 vote |
|---|---|
| `0x3D83ab507785b95ca5C208bEc80CCe3D5ca98100` | agree |
| `0x5310dcF075E0BD47d29B8ec6581F736C767f54D2` | agree |
| `0x90402341F0B0e97b23023c0a87de957FB7148E0F` | idle |
| `0xacc2459F341D7a887bcA8FAA62F1EC9378d4Bc67` | agree |
| `0xec2Fb79cd12255Eb34886CEd7332f27B98DEe658` | idle |
### T03

Final Leader: `0xcE1d6bBB36B744536153966B4DD42276f5ADd0F8`。初始 Validators: 5。

| Validator address | 最终 vote |
|---|---|
| `0x4404Fb70d490c935758146f42A73DC850FF95C71` | agree |
| `0x9ea87b28DcA2F79fe108CF06a4c13B4c876AC23d` | agree |
| `0xBBb165E4c9d73a1493D363280f7067Cd07891dBE` | agree |
| `0xacc2459F341D7a887bcA8FAA62F1EC9378d4Bc67` | idle |
| `0xcE1d6bBB36B744536153966B4DD42276f5ADd0F8` | idle |
### T04

Final Leader: `0x3D83ab507785b95ca5C208bEc80CCe3D5ca98100`。初始 Validators: 5。

| Validator address | 最终 vote |
|---|---|
| `0x03D58A4DeF6fDFc032A56374785a5F571D07Bc11` | agree |
| `0x3D83ab507785b95ca5C208bEc80CCe3D5ca98100` | agree |
| `0x5310dcF075E0BD47d29B8ec6581F736C767f54D2` | agree |
| `0x772ffCd1dF6Cc566eC4b8d3f4F4f8eBbb6B36C84` | idle |
| `0x90402341F0B0e97b23023c0a87de957FB7148E0F` | idle |
### T05

Final Leader: `0xacc2459F341D7a887bcA8FAA62F1EC9378d4Bc67`。初始 Validators: 5。

| Validator address | 最终 vote |
|---|---|
| `0x14402D49f317CE1a2F35BAE01b1804A2A9703dCb` | idle |
| `0x4EDbE1FC9EAeC7b0EBA849b0C76AE73Eb0ad5C47` | agree |
| `0xDB1c35c1f05d885999b8f13e5735307BcC16Be88` | idle |
| `0xacc2459F341D7a887bcA8FAA62F1EC9378d4Bc67` | agree |
| `0xec2Fb79cd12255Eb34886CEd7332f27B98DEe658` | agree |
### T06

Final Leader: `0x03D58A4DeF6fDFc032A56374785a5F571D07Bc11`。初始 Validators: 5。

| Validator address | 最终 vote |
|---|---|
| `0x03D58A4DeF6fDFc032A56374785a5F571D07Bc11` | idle |
| `0x36728d2a123aB444E603EE5b2ad17d18Bb193557` | agree |
| `0x3D83ab507785b95ca5C208bEc80CCe3D5ca98100` | idle |
| `0x4404Fb70d490c935758146f42A73DC850FF95C71` | agree |
| `0x4EDbE1FC9EAeC7b0EBA849b0C76AE73Eb0ad5C47` | agree |
### T07

Final Leader: `0x36728d2a123aB444E603EE5b2ad17d18Bb193557`。初始 Validators: 5。

| Validator address | 最终 vote |
|---|---|
| `0x03D58A4DeF6fDFc032A56374785a5F571D07Bc11` | agree |
| `0x14402D49f317CE1a2F35BAE01b1804A2A9703dCb` | agree |
| `0x36728d2a123aB444E603EE5b2ad17d18Bb193557` | agree |
| `0x772ffCd1dF6Cc566eC4b8d3f4F4f8eBbb6B36C84` | idle |
| `0xE6BD8050758CB15fC88387223E31Ae2708B119dC` | idle |
### T08

Final Leader: `0x03D58A4DeF6fDFc032A56374785a5F571D07Bc11`。初始 Validators: 5。

| Validator address | 最终 vote |
|---|---|
| `0x03D58A4DeF6fDFc032A56374785a5F571D07Bc11` | agree |
| `0x36728d2a123aB444E603EE5b2ad17d18Bb193557` | idle |
| `0xBBb165E4c9d73a1493D363280f7067Cd07891dBE` | idle |
| `0xDB1c35c1f05d885999b8f13e5735307BcC16Be88` | agree |
| `0xE6BD8050758CB15fC88387223E31Ae2708B119dC` | agree |
### T09

Final Leader: `0x5310dcF075E0BD47d29B8ec6581F736C767f54D2`。初始 Validators: 5。

| Validator address | 最终 vote |
|---|---|
| `0x4aba638Cf0Cf5249437AaD968fC69dde46ae6BAC` | agree |
| `0x5310dcF075E0BD47d29B8ec6581F736C767f54D2` | agree |
| `0xBBb165E4c9d73a1493D363280f7067Cd07891dBE` | agree |
| `0xDB1c35c1f05d885999b8f13e5735307BcC16Be88` | agree |
| `0xcE1d6bBB36B744536153966B4DD42276f5ADd0F8` | agree |
### T10

Final Leader: `0x03D58A4DeF6fDFc032A56374785a5F571D07Bc11`。初始 Validators: 5。

| Validator address | 最终 vote |
|---|---|
| `0x03D58A4DeF6fDFc032A56374785a5F571D07Bc11` | agree |
| `0x3D83ab507785b95ca5C208bEc80CCe3D5ca98100` | agree |
| `0x772ffCd1dF6Cc566eC4b8d3f4F4f8eBbb6B36C84` | idle |
| `0xE6BD8050758CB15fC88387223E31Ae2708B119dC` | agree |
| `0xacc2459F341D7a887bcA8FAA62F1EC9378d4Bc67` | idle |

## 原始材料与来源

- [t01-t10.json](evidence/phase4c/t01-t10.json)：逐交易、逐轮 Leader/Validator 角色、地址、vote、GenVM stderr/error、return/equivalence output、精确输入、时间和对象。
- [state-readback.json](evidence/phase4c/state-readback.json)：链 ID、真实 ABI、十项状态，均实际成功。
- [source-integrity.json](evidence/phase4c/source-integrity.json) 和 integrity.json：部署源码 hash 与 A/B 原始字节核验。
- Repository B [rpc-http.json.gz](https://github.com/gqzy1/contextpass-genlayer/blob/phase4c-frontend-activation/evidence/phase4c/rpc-http.json.gz)、[onchain-readonly.json.gz](https://github.com/gqzy1/contextpass-genlayer/blob/phase4c-frontend-activation/evidence/phase4c/onchain-readonly.json.gz)：无损压缩的真实 HTTP 响应与 SDK 解码；archive-integrity.json 保存解压后 SHA/大小。`gzip -dk` 或 Python gzip 可读取，未过滤错误票。
- B evidence/phase4c/user-explorer-screenshots.tar.gz：用户提供的 20 张原图，screenshots-index.json 保留原文件名与 hash；不是助手新拍图。T01–T05 原截图未纳入这批 20 张，本轮以原始真实 RPC 收据核验它们。
- B [T07-rotation.png](https://github.com/gqzy1/contextpass-genlayer/blob/phase4c-frontend-activation/evidence/phase4c/T07-rotation.png)、T07-execution.png、T08-rollback.png、T09-revoke.png、T10-rollback.png 单独保留关键截图。截图可见 Accepted/Return/Rollback；实际 Validator 地址/票来自 RPC，而非推测截图。
- B scripts/verify-onchain-readonly.mjs：只允许 eth_chainId / eth_getTransactionByHash / gen_getContractCode / gen_getContractSchema / gen_call(type=read)，没有 account/签名/write 接口；429 即停。

前端真实签名/提交/恢复：**NOT RUN**。不得把用户的 Studio 交易写成已通过前端执行的测试。Pages 未发布，Portal 未提交。STOP。
