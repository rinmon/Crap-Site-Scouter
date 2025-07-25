# Crap Site Scouter

[![GitHub version](https://badge.fury.io/gh/rinmon%2FCrap-Site-Scouter.svg)](https://badge.fury.io/gh/rinmon%2FCrap-Site-Scouter)

## 概要

Crap Site Scouterは「えきてん」等のWebサイトから都道府県・市町村・ジャンル等のデータを自動取得・整形するPythonスクリプト群です。

- API・HTMLパースによるデータ取得
- Supabase等へのデータ投入補助
- 拡張性を考慮した実装

## ディレクトリ構成

```
github/
  ekiten_api_scraper.py      # えきてんAPIから市町村データ取得
  ekiten_genre_scraper.py    # ジャンルデータ取得（予定）
  supabase_insert.py         # Supabase投入用スクリプト
  categories_table_schema.sql # Supabase用DDL例
  README.md                  # このファイル
```

## セットアップ

1. Python 3.8以降を推奨
2. 必要なパッケージをインストール
   ```sh
   pip install -r requirements.txt
   ```
3. 各スクリプトを実行
   ```sh
   python ekiten_api_scraper.py
   # など
   ```

## ライセンス
MIT License
