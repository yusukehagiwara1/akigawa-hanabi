# チケットページの在庫表示を毎朝更新する手順

毎朝9時の定期実行（Claude デスクトップアプリの「スケジュール」:【毎朝】花火チケット在庫表示の更新）がこの手順で動く。
手で実行するときも同じ。WordPress へのログイン・更新は不要。

## 仕組み

- チケットページ（WordPress 固定ページ 1711）は `wp-snippets/stock.js` を読み込んでいる。
- stock.js は `https://akigawa-hanabi.pages.dev/wp-snippets/stock.json` を読み、購入リンク（〇△✕）・席ごとの表示
  （空席あり／残りわずか／完売）・カードの表示・「○月○日時点」を差し替える。
  ページに書いてある日付の方が新しいとき、読めないときは何もしない。
- stock.json は `build_stock_json.py` が作る。push すると Cloudflare Pages に1〜2分で載る。

## 判定

1. 「在庫」シート（配分−販売数）の記号: 〇／△（残り5以下・25%以下）／✕
2. 販売サイトの画面で見た状態を重ねる（悪い方をとる。在庫を増やす方向には変えない）
   - アソビュー・KKday・JRE MALL・チケットぴあ: ブラウザで画面を開き、`browser/*.js` で読む
   - 楽天トラベル: `site_checks.check_rakuten()`（画面の「予約へ進む」と同じ在庫確認。予約はしない）
3. 手で決めている枠（`update_stock.py` の SET_MARK / FORCE_MARK / NOT_ON_SALE / SOLD_OUT）
   - SET_MARK は主催者から連絡のあった記号（再販など）。シートの代わりに使い、画面で売り切れ・残りわずかを見たらそちらが勝つ

「○月○日時点」は、5サイトすべてを確かめられた日だけその日の日付になる。

自動でスクリプトから読めないサイトがある（アソビューは購入者用の待合室の先、KKday は bot 対策、
JRE はサイト全体が待合室）。すり抜けはせず、ふつうのブラウザで画面を開いて読む。

## 手順

1. `git pull --ff-only`
2. ブラウザで次を順に開き（1ページずつ、数秒あける）、結果を observed.json にまとめる
   - アソビュー（7商品）: 商品ページを開く → `browser/asoview_open.js` → `browser/asoview_read.js`
     - 15a2d40e-de69-49cb-aa22-3450dd5e17b3（SS・S・A席）
     - 4e015166-974c-4717-aa29-7ea7a902a8c8（S席追加販売）
     - 0c5d63ab-40cf-4f97-b50b-c0b905a48cbc（≪S席追加販売≫ 10/23〜）
     - e42dce79-988e-4b5d-bc20-099dbaf02d1d（リクライニングペアシート 10/23 再販）
     - eeb73892-7a4f-4cc6-aeb9-20d7980d5298（駐車場 観覧会場隣接）
     - bcd564e0-361e-4a67-bdec-0a608cc54213（駐車場 プール側）
     - 6dbcf060-4a33-4e3c-9348-551a867822d1（フリーエリア。チャネル d58e8525-…）
   - KKday: https://www.kkday.com/ja/product/527261 → `browser/kkday_read.js`
   - JRE MALL: https://event.jreast.co.jp/activity/detail/a180/a180-09 と a180-10 → `browser/jre_read.js`
   - チケットぴあ: https://t.pia.jp/pia/ticketInformation.do?eventCd=2625008&rlsCd=001 → `browser/pia_read.js`
3. `python gas/hanabi-uriage/build_stock_json.py --observed observed.json`
4. `wp-snippets/stock.json` と `wp-snippets/ticket-page-content.html` を commit・push

observed.json の形:

```json
{
  "asoview": {"<商品ID>": <asoview_read.js の戻り値>, ...},
  "kkday": <kkday_read.js の戻り値>,
  "jre09": <a180-09 での jre_read.js の戻り値>,
  "jre10": <a180-10 での jre_read.js の戻り値>,
  "pia": <pia_read.js の戻り値>
}
```

各 JS の戻り値には read_at（読んだ時刻）が入る。その日（日本時間）に読んだものでないと使わない。

## 止まるとき（表示は前のまま）

- 在庫シートの席種・販売サイトがそろっていない、記号が〇△✕―以外（#VALUE! など）
- ページの購入リンクの行に対応するURLが分からない（`update_stock.py` の URLS に足す）
- 購入リンクの枠の中身が想定と違う

## 手で直すとき

売り切れ・再販などの手直しは WordPress ではなく `update_stock.py` の SET_MARK / SOLD_OUT / FORCE_MARK / NOT_ON_SALE に入れて、
build → commit → push する。WordPress の本文だけ直しても、同じ日付の stock.json で stock.js が上書きする。

## 集計が終わったとき

在庫シートが変わったら、上の手順をそのまま1回実行すればよい（WordPress の更新は不要）。
