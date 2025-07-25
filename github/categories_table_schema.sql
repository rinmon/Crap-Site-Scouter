-- Supabase用カテゴリ（ジャンル）テーブルDDL例
CREATE TABLE categories (
    id serial PRIMARY KEY,
    code text NOT NULL UNIQUE,        -- ジャンルコード（大・小共通、APIのcode）
    name text NOT NULL,               -- ジャンル名
    parent_code text,                 -- 親ジャンルのcode（大ジャンルはNULL、小ジャンルは大ジャンルのcode）
    created_at timestamp with time zone DEFAULT now()
);

-- インデックスや追加カラムは必要に応じて拡張してください。
-- 例: description, url, sort_order など
