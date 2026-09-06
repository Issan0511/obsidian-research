---
name: nvidia-driver-mismatch-check
description: torch.cuda.is_available() が False のときは真っ先にドライバ版不一致(apt更新後の再起動待ち)を疑う
metadata:
  type: reference
---

このマシン (Ubuntu 24.04 / RTX 5060 Ti sm_120 / nvidia-driver-580-open) で GPU が使えないときは、**まずカーネルモジュールとユーザ空間ライブラリのバージョン一致を確認する**。`unattended-upgrades` がドライバパッケージを更新しても、再起動するまで動いているカーネルモジュールは古いままで、CUDA は初期化に失敗する。

```bash
cat /proc/driver/nvidia/version                       # 実際にロード中のモジュール版
dpkg -l | grep -E 'nvidia-driver|libnvidia-compute'   # インストール済みの版
```

この 2 つが食い違っていたら **再起動が唯一の実用的な解**(表示サーバが GPU を掴んでいるので `rmmod`/`modprobe` は通らない)。

典型的な症状 (2026-08-20 に実際に遭遇。稼働 30 日、モジュール 580.159.03 / パッケージ 580.173.02):
- `nvidia-smi` → `Failed to initialize NVML: Driver/library version mismatch`
- `torch.cuda.is_available()` → `False`
- CUDA 呼び出し → `Error 804: forward compatibility was attempted on non supported HW`

「torch が CUDA ビルドでない」「デバイスが無い」と誤診しないこと。torch は `2.13.0+cu130` で正しく、[[proj-004-drift-experiment]] のとおり sm_120 で動作実績がある。再起動はユーザーの判断事項なので、勝手に実行せず報告する。
