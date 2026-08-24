# 源代码说明

本比赛分支的仓库根目录即完整源代码交付，避免在成果目录内复制第二份代码树造成版本漂移。

| 能力 | 主要位置 |
| --- | --- |
| AICP Rust 协议契约 | `components/aicp-protocol/` |
| C 协议、参考服务、控制状态机与回归 | `apps/ai-rtos-demo/` |
| ArceOS TCP/UDP 控制服务 | `apps/arceos/aicp-server/` |
| Linux 2 vCPU 与 ArceOS 双 Guest runner | `scripts/ai-rtos/`、`os/axvisor/configs/` |
| AxVM realtime polling、通知与定时器回归 | `virtualization/axvm/`、`test-suit/axvisor/normal/qemu-rt-poll-idle/` |

交付基线为 `competition/avalon-submission` 分支。构建和运行命令以 `../技术文档/技术报告与复现手册.md` 为准。
