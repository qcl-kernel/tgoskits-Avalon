# 演示视频

本目录只接收真实的动态录屏，不使用静态画面拼接、伪造终端输出或含个人路径/敏感信息的视频。

录制时应在隔离虚拟桌面中实际输入并执行：

```sh
scripts/ai-rtos/aicp.sh doctor
scripts/ai-rtos/aicp.sh prepare
scripts/ai-rtos/aicp.sh smoke 3 ai 300
cargo xtask axvisor test qemu --arch aarch64 --test-case rt-poll-idle-timer-wake
```

画面应清晰呈现动态滚动日志中的 `AICP_RTOS_READY`、`CONTROL seq=`、`AICP_LINUX_DONE ok=3 failed=0` 与 `AXVISOR_RT_POLL_IDLE_TIMER_WAKE_PASSED`；字幕仅解释当前步骤，不遮挡关键日志。

视频文件在完成上述真实录制并人工核验后再添加到本目录。
