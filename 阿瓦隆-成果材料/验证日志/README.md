# 已执行验证的关键日志摘录

本目录只保留与当前成果分支结论直接相关的标记性摘录。完整运行日志由 `scripts/ai-rtos/aicp.sh` 默认写入 `tmp/ai-rtos/logs/`；录制演示视频时应重新执行命令并展示实时滚动输出，而不是回放本文件。

## Linux–ArceOS 双 Guest AICP TCP/IP 闭环

已执行命令：

```sh
scripts/ai-rtos/aicp.sh prepare
scripts/ai-rtos/aicp.sh smoke 3 ai 300
```

一次实际 QEMU 运行的关键输出如下：

```text
AICP_RTOS_NET_READY iface=eth0 ip=10.0.3.2/24
AICP_RTOS_READY
AICP Linux guest client starting server=10.0.3.2:8800 client=10.0.3.3 mode=ai transport=tcp iterations=3 stress_procs=0
CONTROL seq=2 target=0.480 measured=0.168 output=0.828
CONTROL seq=3 target=0.495 measured=0.170 output=0.106
CONTROL seq=4 target=0.511 measured=0.205 output=0.290
AICP_LINUX_DONE ok=3 failed=0 avg_rtt_ns=209135104 max_rtt_ns=240836240
[ai-rtos] PASS: Linux-to-ArceOS AICP TCP/IP control loop completed
```

RTT 数值来自容器内嵌套 QEMU 的该次运行，只用于证明端到端测量字段和闭环链路存在；它不是固定硬件平台下的最坏时延结论。

## Linux–ArceOS YOLOv8n ONNX Runtime CPU 闭环

已执行命令：

```sh
apps/ai-rtos-demo/yolov8-onnx-cpu/build-docker.sh
apps/ai-rtos-demo/yolov8-rust-onnx/build-aarch64-docker.sh
AICP_CLIENT_IMPL=yolo-rust scripts/ai-rtos/aicp.sh run linux arceos 3 ai 600
```

一次实际 QEMU 运行的关键输出如下：

```text
AICP_RTOS_READY
AICP_YOLO_RUST_BEGIN model=/model/yolov8n.onnx images=3 host=10.0.3.2 port=8800 dry_run=0 target_class=32 backend=onnxruntime-cpu language=rust
AICP_YOLO_RUST_CONTROL image=/validation/tennis-ball-close.jpg applied_seq=2 ... rtt_ns=203928208
AICP_YOLO_RUST_CONTROL image=/validation/tennis-ball-black-box.jpg applied_seq=4 ... rtt_ns=351020592
AICP_YOLO_RUST_CONTROL image=/validation/tennis-ball-plant.jpg applied_seq=4 ... rtt_ns=698186992
AICP_YOLO_RUST_DONE ok=3 failed=0 avg_load_ns=380851568 avg_preprocess_ns=230951088 avg_infer_ns=62841325066 max_infer_ns=70100758784 avg_postprocess_ns=23382314 avg_rtt_ns=417711930 max_rtt_ns=698186992 avg_e2e_ns=64977108037 max_e2e_ns=72752147168
[ai-rtos] PASS: Linux (yolo-rust) and arceos completed the AICP TCP/IP closed loop
```

## AxVisor 实时 idle 定时器回归

已执行命令：

```sh
cargo xtask image pull qemu-aarch64 --extract-dir tmp/axbuild/images
cargo xtask axvisor test qemu --arch aarch64 --test-case rt-poll-idle-timer-wake
```

通过标记为：

```text
AXVISOR_RT_POLL_IDLE_TIMER_WAKE_PASSED
axvisor qemu test summary:
  PASS rt-poll-idle-timer-wake (44.79s)
result: 1/1 case(s) passed
total: 253.61s
```

该标记证明 `rt-poll-idle` 配置下的 idle→定时器唤醒→继续执行路径可运行；周期抖动、调度延迟、中断响应延迟和长时间压力数据需在固定环境中另行采集。
