# マヒル建築 ロゴ フルキット ― 納品メモ

2026-11-01。maki が第2ラウンド推奨の D案「継ぎ手の段」を選択 → スキル Phase 7 のフルキットを構築。

## 決定事項
- 採用マーク: D ― 継ぎ手の段（Stepped Joint）。マスター形状は第2ラウンドの v3 をそのまま最終原稿化（監査 100/100、単一パス＋実カットアウトの継ぎ目）。
- ブランドカラー: **真昼の藍 #1E3A5F**（RGB 30/58/95、CMYK近似 68/39/0/63、白地コントラスト約11.5:1）。
- 主署名: 横組み・和文（マヒル建築＋MAHIRU KENCHIKU サブライン）。

## 構成
- `symbol/` ― マスター／小サイズ版（継ぎ目26単位に拡大、16px 実測で継ぎ目が読めることを確認）／black・white・藍mono／square／favicon／app-icon（SVG＋PNG 512・1024）
- `lockups/` ― 横組み EN／JP、縦組み EN、ワードマーク EN／JP。各 black・white・藍mono＋PNG 1024（横組み・縦組み分）
- `web-icons/` ― favicon.ico（16/32/48）、favicon.svg、apple-touch-icon、icon-192/512、maskable、site.webmanifest、head-snippet.html
- `board/` ― 最終プレゼンテーションボード（board.html、board-top.png、board-full.png、spec.json）
- `guidelines.md` ― 使用ガイドライン簡易版
- `build_lockups.py` ― ワードマークのアウトライン化とロックアップ生成スクリプト（再生成用）

## 技術メモ（正直な記録）
- ワードマークは Noto Sans Bold／Regular、Noto Sans CJK JP Bold（いずれも SIL OFL 1.1）から fontTools でアウトライン化。ライブテキストは最終原稿に含まない。
- svg_audit の警告はロックアップ分のみ（82〜98点）で、内容は欧文・漢字の字形そのものに由来するもの（A の斜線角度、築の微細部品・画数）。シンボル本体は全バリアント 100 点。実務上の問題はないが、記録として残す。
- 白版（反転）はマスターの反転そのまま。継ぎ目幅 16/256（6.25%）のため照度膨張の影響は小さく、目視で問題なしと判断。

## 次の候補（未実施）
- Pantone／看板現物での色合わせ
- 名刺・封筒など実印刷物の入稿データ化
- サイト（mahiru-kenchiku リポジトリ）への favicon・ロゴ差し替え
- 商標の正式調査（実務化時）
