# Agent Skills: 統合ロト分析システム

このファイルは、各プロジェクトおよび参照資料を活用して、自律的に高度な分析を実行するための専門スキルを定義します。

---

## 1. Skill: Domain-Knowledge-Consultant
- **Trigger**: ロジックの設計、パラメータ調整、または新しい分析エンジンの作成時。
- **Goal**: 以下の2種類の参照先を組み合わせ、数学的・統計的根拠に基づいた提案を行う。
- **参照先①（理論・手法）**: `C:\Users\tk030\Desktop\各種情報\参考資料\` フォルダ内のテキストファイル
    - `宝田式_宝くじ手法110選_完全版.txt`: 手法の引き出し
    - `宝田式7指標_排除力と組み合わせ方.md`: 7指標の排除力・複合排除力、くじ別推奨手順の実測データ
    - `ろき流_ロトの川分析理論.txt`: 出目の推移を「川」として捉える幾何学的分析。前々回±3スライド。
    - `lottery_mathematics_full_report.txt`: 数学的構造 (Lotterycodex)
    - `lottery_math_theory.txt`: ジアネラ理論 (帯域分布)
    - `lottery_detailed_report.txt`: 舩津式4つの黄金法則
    - `loto6_prime_filter_report.txt`: 素数フィルター統計
    - `LOTO_TF_Method_Complete_Data.txt`: TF式・ホイール理論
- **参照先②（各エンジンの現状）**: `C:\Users\tk030\Desktop\各種情報\Projects\` フォルダ内の各プロジェクトの `RECORD.md`
    - 理論を適用する前に、対象エンジンがすでに試みたアプローチと結果を確認すること。
    - **【注意】** 他プロジェクトの記録を参照して全体像を学ぶことは義務だが、そこからコードやロジックを勝手に現在のプロジェクトへコピー・流用することは原則禁止（要事前承認）。

## 2. Skill: exclusion-logic-validator
- **Goal**: 提案されたロジックが「除外理論」に則っているかを検証し、ランダム性を排除する。
- **Logic Source**: `C:\Users\tk030\Desktop\各種情報\参考資料\lottery_mathematics_full_report.txt` の「構造分析」を最優先すること。
- **現状確認**: `C:\Users\tk030\Desktop\各種情報\Projects\排除予想システム\RECORD.md` を参照し、既存の12専門家エンジンとの重複・競合がないか確認すること。

## 3. Skill: Candidate-Survival-Validator
- **Goal**: 除外を強めすぎて「当選数字」を失っていないか、バックテストで検証する。
- **Benchmark**: 統計的有意性の目標は `p値 < 0.05`（ランダムを上回ることを最低基準とする）。
- **参照**: 対象プロジェクトの `RECORD.md` に記載されたバックテスト結果と比較し、改善しているかを判断すること。

## 4. Skill: note-article-generator
- **Trigger**: バックテスト完了時、または新ロジックの発見時。
- **Goal**: `参考資料/lottery_detailed_report.txt` などの形式を参考に、説得力のある「note」投稿用下書きを作成する。
- **Action**: 統計データを表形式でまとめ、数学的根拠を添えて日本語で出力せよ。
- **参照**: `C:\Users\tk030\Desktop\各種情報\Projects\RIVER_FLOW_PUBLISHER\RECORD.md` に記載された出力フォーマットの仕様を参考にすること。

## 5. Skill: Universal-Backtest-Validator
- **Trigger**: バックテストの実装・実行、または新しい予測ロジックの評価時。
- **Goal**: 汎用バックテスト・プロトコルに従い、柔軟かつ客観的なロジック評価と全方位アーカイブを自律的に行う。
- **Action**: `Universal_Backtest_Protocol.md` を読み込み、それに定義された全ルール（捕捉率による評価、未捕捉分析、基準未達時の確認プロセスの実行、および評価済みロジックのテキストベースでの自動アーカイブ保存）を遵守・実行せよ。
- **結果の記録**: バックテスト完了後は、対象プロジェクトの `RECORD.md` の「バックテストの最新結果」セクションを更新すること。

## 6. Skill: Base-Unit-Platform-Adapter
- **Trigger**: 予測エンジンの新規追加、既存ロジックのベースユニット統合（プラグイン化）、またはGUI連動開発時。
- **Goal**: 各ロト予測エンジンを接続ユニットを介さずにベースユニットへ直接プラグイン接続させ、ドラッグ＆ドロップによる完全な疎結合オートロードを確立する。
- **Action**:
  - `C:\Users\tk030\Desktop\各種情報\Base_Unit_Specification.md`（ベースユニット＆自律プラグイン仕様書）を必ず最優先で読み込み、そこで定義された規格（config.jsonおよびpredict_next()のインターフェース、GUI表示メタデータの戻り値仕様）を厳格に遵守すること。
  - プラグイン移植時は、DBロードやチケット生成、Verifier呼び出しなどの「ベース側の共通機能」をロジック側から完全に排除し、移行前の古いコードは `C:\Users\tk030\Desktop\過去の遺産` フォルダへ退避するレガシー退避プロトコルを順守すること。


