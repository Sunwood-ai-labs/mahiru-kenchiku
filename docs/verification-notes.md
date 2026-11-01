# 検証メモ — Pascal Editor → FreeCAD（2026-11-01 実測）

## Pascal Editor 試用結果

- 導入は CLI `@pascal-app/cli` v1.0.6（ローカルSQLite、サインアップ不要）。
- 内蔵MCP（86ツール）経由で平屋11×8.5m・5室・家具19点の「MAHIRU Model 01 — 真昼の平屋」を構築。検証 valid・衝突ゼロ。
- 書き出し：JSON と GLB（460KB）は実用可。IFC4ライターはコード内に存在するが、ローカル版1.0.6のUIに .ifc 単体ダウンロード導線はなし（「Send to Blender」転送形式専用）。

## FreeCAD 1.1.4 への取り込み

- GLB取り込み結果：Partシェル（面）266個＋グループ42（`wall_` / `door_` / `window_` 等のPascalノード名が保持）。ネイティブなソリッドはゼロ。
- 閉じたシェル174個は `makeSolid` でソリッド化可。
- 寸法は一致：壁 厚100mm・高さ2,450mm を実測、棟高 約5.7m。
- パラメトリック編集は引き継げないため、運用は「Pascalで間取り → FreeCADでは参照モデルとして置いてBIMで作り直し」が現実解。

## シーン名変更の保全確認

- `Moru Small House` → `MAHIRU Model 01 — 真昼の平屋` への改名で、変更前後の graphHash・sizeBytes（38,195）・ノード数（66）が完全一致。形状は無変更、書き出し物は無傷。
