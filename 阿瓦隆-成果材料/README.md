# 阿瓦隆-成果材料

本目录是阿瓦隆团队提交“2026 首届‘揭榜挂帅’擂台赛”的成果入口。仓库根目录保留完整可构建源代码；本目录保存与本比赛分支对应的技术文档、测试报告、源代码索引和演示视频。

本成果对应上游项目的总跟踪议题 [#2154](https://github.com/rcore-os/tgoskits/issues/2154)。

## 目录

| 路径 | 内容 |
| --- | --- |
| `技术文档/完整全流程实现与复现手册.md` | 系统架构、实时性改造、AICP 协议、复现命令和演示流程 |
| `技术文档/开发记录与问题排查.md` | 代码边界、关键调用链、设计取舍和故障定位记录 |
| `技术文档/技术报告与复现手册.md` | 当前已执行验证的精简技术报告 |
| `技术文档/测试报告.md` | 当前已执行命令、结果与测量说明 |
| `源代码/README.md` | 本成果分支中源码的责任边界与入口 |
| `验证日志/README.md` | 已执行 QEMU 验证的关键标记摘录 |
| `演示视频/AxVisor_AICP_真实运行演示.mp4` | Linux–FreeRTOS 双 Guest AICP TCP/IP 控制闭环的隔离桌面实录 |

## 与赛题及 #2154 的对应关系

| 赛题任务 | 本分支交付 | 当前可验证证据 |
| --- | --- | --- |
| 任务一：实时性改造与验证 | `rt-poll-idle` vCPU idle/poll 路径、定时器/设备 poll 推进、共享等待对照配置 | AxVM 7 组 feature 静态检查、312 项 host-test、AArch64 `rt-poll-idle-timer-wake` QEMU 回归 |
| 任务二：客户机间通信 | AICP v1、VirtIO 虚拟网卡、TCP 主通道及 UDP 可靠性对比、C/Rust 协议和服务测试 | 13 项 C 协议、10 项 Rust 协议、8 项 ArceOS 服务测试；Linux–ArceOS、Linux–FreeRTOS、Linux–RT-Thread TCP/IP 双 Guest smoke |
| 任务三：AI 模型与控制联动 | Linux 轻量神经网络及 YOLOv8n ONNX Runtime CPU 推理、AICP 控制命令、RTOS 控制状态更新与 STATUS 回传 | Linux–ArceOS、Linux–FreeRTOS、Linux–RT-Thread 轻量神经网络闭环；YOLOv8n–ArceOS 3 图推理、控制与状态回传 |

## 当前可复现主线

当前已实跑的主线包括：**AxVisor/QEMU AArch64 上 Linux（2 vCPU）经 VirtIO 虚拟网卡，以 AICP v1 over TCP/IP 向 ArceOS、FreeRTOS 或 RT-Thread（各 1 vCPU）控制 Guest 下发轻量神经网络输出并接收状态回传；Linux–ArceOS 还完成了 Rust YOLOv8n + ONNX Runtime CPU 的三图推理、控制下发与状态回传。**

快速复现前，请确保宿主具有 `cargo`、`cpio`、`gzip`、`perl`、`qemu-system-aarch64`、`debugfs` 与 `e2fsck`：

```sh
scripts/ai-rtos/aicp.sh doctor
scripts/ai-rtos/aicp.sh prepare
scripts/ai-rtos/aicp.sh run linux freertos 3 ai 300
```

成功时，Linux 与 FreeRTOS Guest 的日志会输出：

```text
AICP_FREERTOS_READY transport=tcp port=8800 ip=10.0.3.2
AICP_FREERTOS_CONTROL seq=2
AICP_LINUX_DONE ok=3 failed=0
```

并由 runner 输出闭环完成结果。

YOLOv8n 闭环复现：

```sh
apps/ai-rtos-demo/yolov8-onnx-cpu/build-docker.sh
apps/ai-rtos-demo/yolov8-rust-onnx/build-aarch64-docker.sh
AICP_CLIENT_IMPL=yolo-rust scripts/ai-rtos/aicp.sh run linux arceos 3 ai 600
```

成功时 Linux Guest 输出 `AICP_YOLO_RUST_BEGIN`、三次
`AICP_YOLO_RUST_CONTROL` 和 `AICP_YOLO_RUST_DONE ok=3 failed=0`。
