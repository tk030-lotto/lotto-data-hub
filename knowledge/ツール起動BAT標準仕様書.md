# 【1枚要約】Windows用「ツール起動.bat」標準仕様書

## 1. 目的と特徴
* **目的**: 初心者が「Download ZIP → 解凍 → ダブルクリック」だけでツールを使えるようにする。
* **動作**: Node.js確認 → 初回のみ自動セットアップ（`npm install`） → ブラウザ自動オープン → サーバー起動。
* **最重要仕様**: 文字コードは必ず **Shift-JIS (CP932)** で保存（cmd.exeの文字化け・エラー防止）。

---

## 2. 標準テンプレートコード（Next.js / Node.js用）
※保存形式: **Shift-JIS (CP932)** / ファイル名: `ツール起動.bat`

```cmd
@echo off
chcp 932 > nul
title ツール起動ランチャー

echo ========================================================
echo   ツールの起動準備を行っています...
echo ========================================================
echo.

:: 1. Node.js の確認
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [エラー] Node.js が見つかりません。
    echo 公式サイト（https://nodejs.org/）からインストールしてください。
    echo.
    pause
    exit /b 1
)

:: 2. 初回のみ依存関係インストール
if not exist "node_modules" (
    echo [初回準備] 必要なライブラリをインストールしています...
    call npm install
    if %errorlevel% neq 0 (
        echo [エラー] インストールに失敗しました。
        pause
        exit /b 1
    )
)

:: 3. データベース初期化（Prisma使用時）
if exist "prisma\schema.prisma" (
    if not exist "dev.db" (
        echo [初回準備] データベースを初期化しています...
        call npx prisma db push
    )
)

:: 4. ブラウザ起動＆サーバー開始
echo サーバーを起動しています...
echo ブラウザで http://localhost:3000 を開きます。
start "" "http://localhost:3000"
call npm run dev
pause
```

---

## 3. 動作フロー＆重要ポイント

| 項目 | 内容・仕様 |
| :--- | :--- |
| **起動分岐** | `node_modules` の有無で判定。初回は自動インストール、2回目以降は即座に起動。 |
| **外部呼出** | npm等の外部コマンド実行時は、処理中断を防ぐため必ず `call npm ...` と記述。 |
| **ブラウザ** | `start "" "http://localhost:3000"` により、既定のブラウザで自動表示。 |
| **HTML単体版** | Node不要の静的ツールの場合は `start "" "index.html"` ＆ `exit` のみで構成。 |
