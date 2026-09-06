---
name: machines-and-network
description: 計算に使えるマシンと到達経路（2026-09-05 実測）— white-san / lab(i9-13900KF) / node(Windows) の素性、tailnet の分断、bit 一致の可否
metadata:
  type: reference
---

proj_004 の走は **bit 一致検査（S-null/S-mirror）を持つので、参照ログを作ったマシンから動かせない**（[[proj-004-edge-law-0905]]）。したがって「使えるマシン」は**到達経路**と**CPU の ISA プロファイル**の両方で決まる。

| | white-san（本番機） | lab | node |
|---|---|---|---|
| CPU | i7-14700K（20 実コア・8P+12E） | **i9-13900KF（24 実コア）** | i7-13700F（16 実コア・8P+8E） |
| ISA | AVX2 止まり・`avx_vnni`・L3 33 MiB | 同左・L3 36 MiB | 同左（Raptor Lake） |
| RAM | 30 GiB | **62 GiB** | **15.7 GiB（空き 7.3）** |
| OS | Ubuntu 24.04 相当・python 3.12.3 | Ubuntu 22.04（python は uv の 3.12.3） | **Windows 11 Home・WSL なし** |
| 到達 | — | **経路なし**（別 tailnet） | **`ssh issan@100.74.60.33`（鍵認証・8ms・direct）** |
| bit 一致 | 基準 | **MATCH 実証済み**（630 列全一致・17.9s） | 未検証（Windows wheel は別バイナリなので同一 CPU でも保証なし） |

- **3 台とも Raptor Lake/AVX2 止まり**。これが効く: GCP は Intel 系が全部 AVX-512、AMD 系は MKL のベンダ判定が別経路で、**「Intel・AVX2 最大・VNNI あり」は consumer 部品にしか無い**。
- **lab は白さんの tailnet にいない**（白さんの tailnet = `Issan0511@`: white-san 100.81.103.50 / issa / node / pixel-10 / tab-s9）。lab の 100.65.177.104 は**別 tailnet**で ping も 22 番も通らない。繋ぐには Tailscale のノード共有か同一 tailnet への参加が要る（管理コンソール操作なので Claude からは不可）。lab 側には秘密鍵が 1 本も無いので、繋ぐなら **white-san → lab 方向**（白さんで鍵を作り lab の authorized_keys に登録）。
- **node は繋がるが RAM 15.7 GiB・WSL なし**なので、この種の走には使えない（30 腕同時には 42 GiB 要る）。小物の退避先には使える。
- 転送手段が無いときは**ギガファイル便**（ファイルごとに cookie jar を分ける・`repo/specs/HANDOFF_edge_law_0905.md` §2 に手順）。
