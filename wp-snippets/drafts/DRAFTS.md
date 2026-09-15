# WordPress 下書き一覧（2026-09-15 作成・確認用）

| 施策 | WP ID | 種別 | 確認用URL（要ログイン） | 元ファイル |
|---|---|---|---|---|
| ② 秋川で過ごす一日 | 4555 | 固定ページ(下書き) | https://machizukuri-con.or.jp/?page_id=4555&preview=true | b2/content.html |
| ③ 楽しみ方（⑫音楽表・⑬動画を差し込み済み） | 4556 | 固定ページ(下書き) | https://machizukuri-con.or.jp/?page_id=4556&preview=true | b3/content.patched.html |
| ⑤ もっと知る（⑬動画を差し込み済み） | 4557 | 固定ページ(下書き) | https://machizukuri-con.or.jp/?page_id=4557&preview=true | b5/content.patched.html |
| ⑧ 初めて来る方へ | 4558 | 固定ページ(下書き) | https://machizukuri-con.or.jp/?page_id=4558&preview=true | b8/content.html |
| ⑩ 天候・開催情報 | 4559 | 固定ページ(下書き) | https://machizukuri-con.or.jp/?page_id=4559&preview=true | b10/content.html |
| ⑪ 花火師（ホソヤエンタープライズ） | 4560 | 固定ページ(下書き) | https://machizukuri-con.or.jp/?page_id=4560&preview=true | b11/content.html |
| ⑫ 第8回の音楽紹介 | 4572 | お知らせ(下書き・カテゴリ news) | https://machizukuri-con.or.jp/?p=4572&preview=true | b12/post.html |
| ⑬ トップページ用の動画部品 | ―（本番トップ page 7 に差し込む） | 部品 | ― | b13/embed-top.html |

## メモ
- ConoHa WING の WAF: お知らせ(投稿)で `<td>` が多数ある表と本文の組み合わせが 403 になった。`<td class="has-text-align-left">`（コア表ブロックの正規の属性）にすると通る。固定ページでは同じ表でも通った。
- REST の DELETE は WAF で 403 → `POST` + `X-HTTP-Method-Override: DELETE` なら通る。
- WP は JSON 属性内の `--` を `--` に自動エスケープする（正常）。
