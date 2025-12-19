# CSS Template Guide

gospelo-md2pdfのデフォルトCSSテンプレートの説明と、カスタマイズ方法のガイドです。

## 目次

- [デフォルトスタイルの概要](#デフォルトスタイルの概要)
- [ページ設定](#ページ設定)
- [タイポグラフィ](#タイポグラフィ)
- [見出し](#見出し)
- [テーブル](#テーブル)
- [コードブロック](#コードブロック)
- [特殊クラス](#特殊クラス)
- [Mermaidダイアグラム](#mermaidダイアグラム)
- [カスタマイズ例](#カスタマイズ例)

---

## デフォルトスタイルの概要

デフォルトCSSは、日本語ビジネスドキュメント向けに最適化されています。

| 特徴 | 設定値 |
|------|--------|
| 用紙サイズ | A4 |
| 余白 | 20mm |
| 基本フォントサイズ | 10pt |
| 行間 | 1.7 |
| カラースキーム | ブルー系（#1a365d〜#3182ce） |

---

## ページ設定

### @page ルール

```css
@page {
    size: A4;              /* 用紙サイズ */
    margin: 20mm;          /* 余白 */

    @top-right {
        content: counter(page);  /* ページ番号 */
        font-size: 9pt;
        color: #666;
    }
}

@page :first {
    @top-right {
        content: none;     /* 1ページ目はページ番号なし */
    }
}
```

### カスタマイズ例

```css
/* Letter サイズに変更 */
@page {
    size: Letter;
    margin: 1in;
}

/* 横向きに変更 */
@page {
    size: A4 landscape;
}

/* ヘッダー・フッターを追加 */
@page {
    @top-center {
        content: "会社名 - 機密文書";
        font-size: 8pt;
        color: #999;
    }
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
    }
}
```

---

## タイポグラフィ

### 基本設定

```css
body {
    font-family: 'Noto Sans CJK JP', 'Noto Sans JP', 'Hiragino Sans', 'Yu Gothic', sans-serif;
    font-size: 10pt;
    line-height: 1.7;
    color: #333;
    text-align: justify;  /* 両端揃え */
}
```

### フォント優先順位

1. **Noto Sans CJK JP** - Google提供、Linux/macOS
2. **Noto Sans JP** - Google提供（Web版）
3. **Hiragino Sans** - macOS標準
4. **Yu Gothic** - Windows標準
5. **sans-serif** - フォールバック

### カスタマイズ例

```css
/* 明朝体に変更 */
body {
    font-family: 'Noto Serif CJK JP', 'Hiragino Mincho ProN', 'Yu Mincho', serif;
}

/* フォントサイズを大きく */
body {
    font-size: 11pt;
    line-height: 1.8;
}
```

---

## 見出し

### デフォルト設定

| レベル | フォントサイズ | 色 | 装飾 |
|--------|--------------|------|------|
| h1 | 18pt | #1a365d | 下線3px、中央揃え |
| h2 | 14pt | #2c5282 | 下線2px |
| h3 | 12pt | #2b6cb0 | なし |
| h4 | 11pt | #3182ce | なし |

### CSS定義

```css
h1 {
    color: #1a365d;
    font-size: 18pt;
    text-align: center;
    margin-bottom: 8px;
    padding-bottom: 10px;
    border-bottom: 3px solid #2c5282;
}

h2 {
    color: #2c5282;
    font-size: 14pt;
    border-bottom: 2px solid #2c5282;
    padding-bottom: 5px;
    margin-top: 25px;
    margin-bottom: 12px;
}

h3 {
    color: #2b6cb0;
    font-size: 12pt;
    margin-top: 18px;
    margin-bottom: 8px;
}

h4 {
    color: #3182ce;
    font-size: 11pt;
    margin-top: 12px;
    margin-bottom: 6px;
}
```

### サブタイトル

```css
h1.subtitle {
    font-size: 14pt;
    border-bottom: none;
    margin-top: 0;
    padding-bottom: 0;
}
```

**使用例:**
```html
<h1>メインタイトル</h1>
<h1 class="subtitle">サブタイトル</h1>
```

---

## テーブル

### デフォルト設定

```css
table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    font-size: 9pt;
    page-break-inside: avoid;  /* ページをまたがない */
}

thead {
    display: table-header-group;  /* ページをまたぐ場合にヘッダー繰り返し */
}

th {
    background-color: #2c5282;
    color: white;
    padding: 10px 8px;
    text-align: left;
    font-weight: bold;
    border: 1px solid #2c5282;
}

td {
    padding: 8px;
    border: 1px solid #cbd5e0;
    vertical-align: top;
}

tr:nth-child(even) {
    background-color: #f7fafc;  /* 偶数行の背景色 */
}

/* 比較表用：1列目を強調 */
td:first-child {
    background-color: #edf2f7;
    font-weight: bold;
    white-space: nowrap;
}
```

### カスタマイズ例

```css
/* シンプルなテーブル */
table {
    border: 1px solid #ddd;
}
th {
    background-color: #f5f5f5;
    color: #333;
}
td:first-child {
    background-color: transparent;
    font-weight: normal;
}

/* 緑系のテーブル */
th {
    background-color: #38a169;
}
```

---

## コードブロック

### インラインコード

```css
code {
    font-family: 'Noto Sans Mono CJK JP', 'Source Code Pro', monospace;
    background-color: #f1f5f9;
    padding: 2px 5px;
    border-radius: 3px;
    font-size: 9pt;
}
```

### コードブロック

```css
pre {
    background-color: #1e293b;  /* ダークテーマ */
    color: #e2e8f0;
    padding: 12px;
    border-radius: 5px;
    overflow-x: auto;
    font-size: 9pt;
    line-height: 1.5;
    margin: 12px 0;
}

pre code {
    background-color: transparent;
    padding: 0;
    color: inherit;
}
```

### カスタマイズ例

```css
/* ライトテーマのコードブロック */
pre {
    background-color: #f8f8f8;
    color: #333;
    border: 1px solid #ddd;
}
```

---

## 特殊クラス

### サマリーボックス（緑）

```css
.summary {
    background-color: #f0fff4;
    border: 1px solid #9ae6b4;
    border-radius: 5px;
    padding: 15px;
    margin: 15px 0;
}
```

**使用例:**
```html
<div class="summary">
重要なポイントをここに記載します。
</div>
```

### 警告ボックス（オレンジ）

```css
.warning {
    background-color: #fffaf0;
    border: 1px solid #fbd38d;
    border-radius: 5px;
    padding: 15px;
    margin: 15px 0;
}
```

**使用例:**
```html
<div class="warning">
注意事項をここに記載します。
</div>
```

### 情報ボックス（青）

```css
.info {
    background-color: #ebf8ff;
    border: 1px solid #90cdf4;
    border-radius: 5px;
    padding: 15px;
    margin: 15px 0;
}
```

**使用例:**
```html
<div class="info">
補足情報をここに記載します。
</div>
```

### メリット（緑、左ボーダー）

```css
.pros {
    background-color: #f0fff4;
    border-left: 4px solid #48bb78;
    padding: 10px 15px;
    margin: 10px 0;
}
```

**使用例:**
```html
<div class="pros">
メリット：コストが低い、導入が容易
</div>
```

### デメリット（赤、左ボーダー）

```css
.cons {
    background-color: #fff5f5;
    border-left: 4px solid #fc8181;
    padding: 10px 15px;
    margin: 10px 0;
}
```

**使用例:**
```html
<div class="cons">
デメリット：機能が限定的
</div>
```

### 免責事項

```css
.disclaimer {
    font-size: 8pt;
    color: #666;
    background-color: #f7fafc;
    padding: 12px;
    margin-top: 25px;
    border-radius: 5px;
    border: 1px solid #e2e8f0;
}
```

**使用例:**
```html
<div class="disclaimer">
本レポートは情報提供を目的としており、法的助言ではありません。
</div>
```

### 日付表示

```css
.date {
    text-align: center;
    color: #666;
    font-size: 9pt;
    margin-bottom: 25px;
}
```

**使用例:**
```html
<p class="date">作成日：2025年1月19日</p>
```

---

## ページ制御

### 改ページ

```css
.page-break {
    page-break-before: always;
}
```

**使用例:**
```html
<div class="page-break"></div>
```

### ページをまたがない

```css
.no-break {
    page-break-inside: avoid;
}
```

**使用例:**
```html
<div class="no-break">
このブロックはページをまたぎません。
</div>
```

---

## Mermaidダイアグラム

```css
.mermaid-diagram {
    text-align: center;
    margin: 20px 0;
    padding: 15px;
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}

.mermaid-diagram img {
    max-width: 100%;
    height: auto;
}
```

Mermaidダイアグラムは自動的にPNG画像に変換され、このスタイルが適用されます。

---

## 引用

```css
blockquote {
    border-left: 4px solid #3182ce;
    margin: 15px 0;
    padding: 10px 15px;
    background-color: #ebf8ff;
    color: #2c5282;
}

blockquote p {
    margin: 0;
}
```

---

## カスタマイズ例

### 完全なカスタムCSSファイル

```css
/* custom-style.css */

/* ページ設定 */
@page {
    size: A4;
    margin: 25mm 20mm;
}

/* 基本フォント */
body {
    font-family: 'Noto Serif CJK JP', serif;
    font-size: 11pt;
    line-height: 1.8;
    color: #222;
}

/* 見出しをグリーン系に */
h1 { color: #276749; border-color: #38a169; }
h2 { color: #2f855a; border-color: #48bb78; }
h3 { color: #38a169; }

/* テーブルヘッダーをグリーン系に */
th {
    background-color: #38a169;
}

/* コードブロックをライトテーマに */
pre {
    background-color: #f7fafc;
    color: #1a202c;
    border: 1px solid #e2e8f0;
}
```

**使用方法:**
```bash
gospelo-md2pdf report.md --css custom-style.css
```

### 部分的なオーバーライド

デフォルトCSSを使いつつ、一部だけ変更する場合：

```css
/* override.css */

/* ヘッダーの色だけ変更 */
th {
    background-color: #805ad5;  /* 紫系 */
}

/* 見出しの色だけ変更 */
h1, h2, h3 {
    color: #553c9a;
}
```

---

## カラーパレット

デフォルトCSSで使用しているカラーパレット（Tailwind CSS準拠）：

### ブルー系（メインカラー）

| 用途 | 色コード | 説明 |
|------|---------|------|
| h1 | #1a365d | ダークブルー |
| h2 | #2c5282 | ミディアムブルー |
| h3 | #2b6cb0 | ブルー |
| リンク | #3182ce | ライトブルー |
| 情報ボックス背景 | #ebf8ff | 薄いブルー |

### グリーン系（サマリー・メリット）

| 用途 | 色コード |
|------|---------|
| 背景 | #f0fff4 |
| ボーダー | #9ae6b4, #48bb78 |

### オレンジ系（警告）

| 用途 | 色コード |
|------|---------|
| 背景 | #fffaf0 |
| ボーダー | #fbd38d |

### レッド系（デメリット）

| 用途 | 色コード |
|------|---------|
| 背景 | #fff5f5 |
| ボーダー | #fc8181 |

### グレー系（テキスト・背景）

| 用途 | 色コード |
|------|---------|
| 本文 | #333 |
| 補足テキスト | #666 |
| テーブル偶数行 | #f7fafc |
| ボーダー | #cbd5e0, #e2e8f0 |

---

## 関連ドキュメント

- [README.md](../README.md) - 基本的な使用方法
- [README_jp.md](README_jp.md) - 日本語ドキュメント
- [CHANGELOG.md](CHANGELOG.md) - 変更履歴
