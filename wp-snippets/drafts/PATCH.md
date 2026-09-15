# PATCH.md — 部品ファイルの差し込み手順（作業者向け）

作成: 2026-09-15 ／ 対象: `S/out/` の部品ファイル（`S` = scratchpad フォルダ）

## 0. 前提とルール
- 差し込み先は WordPress の `content.raw`（ブロックコメント `<!-- wp:x -->` 付き）。`S/wp/page_7.html` は **rendered**（コメント無し・`width/height` 付き）なので位置確認の参考にだけ使い、実作業は REST の `?context=edit` で取った raw に対して行う。
- 文字コード UTF-8、改行 LF。差し込み後は必ず `python S/check_blocks.py <file> --net` で `errors=0` を確認する（部品もブロック単位で閉じているので同じチェックが使える）。
- ConoHa WAF: 本文に `<script` と `/*` を書かない。先頭 4KB が検査されるので、ページ冒頭の `wp:html` の `<style>` にコメントを入れない。
- `wp:embed` の wrapper 内は YouTube URL の生テキストのみ（iframe を書かない）。
- **自動適用**: `python S/patch_parts.py [--net] [--news-url URL] [--hanabishi-url URL] [--top-raw FILE]` が、§1〜§5 の差し込みを原本のコピー（`S/out/_patched/`）に対して行い、check_blocks まで実行する。アンカーが 1 件でないと中断するので、差し込み先が変わっていれば気づける。手作業でやる場合は下のアンカーを使う。

## 依存関係（作業順）
1. ⑫ `b12/post.html` を投稿（カテゴリ「お知らせ」）として公開 → 記事 URL `https://machizukuri-con.or.jp/news/<ID>/` が確定（9/19）。
2. ⑬ `b13/embed-top.html` → 本番トップ(page 7)（§5）。`embed-more` → b5、`embed-enjoy` → b3（§2・§3）は下書きの段階で差し込んでよい（9/19）。
3. ⑪ `b11/content.html` を固定ページとして公開（9/26）。公開時に「お知らせ」リンクを⑫記事へ（§7-2）。⑪公開後に `b12/post.html` 末尾に⑪への案内を追加（§7-3）。
4. ③ 公開時（10/3）: `b12/section.html` を差し込み済みの状態にし（§1）、部品内のリンクを⑫記事 URL へ（§7-1）。
5. ⑤ 公開時（10/10）: 楽曲の一文を⑫記事へのリンクに差し替え（§4）。
6. ②③ 公開後、トップページ①の整理時に `b2/section.html`・`b3/section.html` を置く（§6）。

---

## 1. `b12/section.html` → `b3/content.html`（「感動する｜音楽と花火」節、`id="akg-hanabi"` の fullWide 内）

**1-a. 差し替え対象 A（この wp:paragraph ブロック全体を `b12/section.html` の内容に置き換える）**
検索アンカー: `第8回の楽曲は、決まり次第お知らせします。</p>`（b3 内で 1 件）
```
<!-- wp:paragraph -->
<p>花火は18時から19時頃まで、約1時間で5,000発を打ち上げる予定です。音楽に合わせて打ち上がる演出が特徴で、第7回（2025年）は米津玄師「IRIS OUT」に合わせたオープニングと、映画音楽に合わせたパートが予告されました。第8回の楽曲は、決まり次第お知らせします。</p>
<!-- /wp:paragraph -->
```
- `b12/section.html` の先頭 `<!-- wp:html --><style>.akg-todo{…}</style><!-- /wp:html -->`（5行+空行）は **省く**。b3 の冒頭 `wp:html` に同じ `.akg-todo{…}` 定義がある（`.akg-todo{` が b3 に 1 件）。残しても表示は変わらないが、定義の重複になる。
- 部品の中身: 紹介文の段落 → 「2026年9月13日時点の予定です…」の段落 → `wp:table {"swlScrollable":"sp","swlTableWidth":"600px"}`（14曲） → `.akg-todo`（My花火の説明文の枠） → お知らせ記事へのリンク段落。

**1-b. 削除対象 B（直後の空行ごと削除。§2 で同じ位置に動画を入れる）**
検索アンカー: `ここに第8回の花火演出の見どころ（楽曲・構成など）が入ります`（b3 内で 1 件）
```
<!-- wp:paragraph {"className":"akg-todo"} -->
<p class="akg-todo">【委員会確認】ここに第8回の花火演出の見どころ（楽曲・構成など）が入ります。確定後に差し替えます。</p>
<!-- /wp:paragraph -->
```
- A と B の間には写真3枚の `wp:loos/columns`（横スクロール）と注記 `写真は過去の大会の様子です。` がある。この注記は b3 に 3 件あるのでアンカーに使わない。
- 差し込み後の `.akg-todo` は 5 か所（出店店舗／出演団体／子ども向け／My花火／タイムテーブル）。SPEC ③ の「5か所」と同数だが内訳が変わる（花火演出の見どころ → My花火）。

## 2. `b13/embed-enjoy.html` → `b3/content.html`
挿入位置: B を削除した場所（写真の注記の直後）= 次の h3 の **直前**。
検索アンカー（b3 内で 1 件）:
```
<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">メディアでも紹介されました</h3>
```
このアンカーの直前に `embed-enjoy.html`（段落1つ + `wp:embed`）を空行を挟んで入れる。結果の並び: 音楽の紹介と曲目表（§1）→ 写真3枚 → 注記 → 定点映像 → 「メディアでも紹介されました」。

## 3. `b13/embed-more.html` → `b5/content.html`（「動画で見る」節、`id="akg-video"` の fullWide 内）
挿入位置: ドキュメント動画の注記段落（`※音が出ます。動画のファイルが大きいため、スマートフォンではWi-Fi環境での再生をおすすめします。</p>` `<!-- /wp:paragraph -->`）の後、次の h3 の **直前**。
検索アンカー（b5 内で 1 件）:
```
<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">音楽とシンクロする花火</h3>
```
このアンカーの直前に `embed-more.html`（h3「花火の定点映像（第7回・約1時間）」+ 段落 + `wp:embed` + 注記段落）を空行を挟んで入れる。見出しは h2「動画で見る」の下の h3 なので階層は崩れない。

## 4. b5 の楽曲の一文の差し替え（⑫記事の公開後・URL 確定後）
b5 の実際の文は `第8回（2026年）の楽曲は未定です。`（依頼文の「決まり次第お知らせします」ではない。b5 内で 1 件。「音楽とシンクロする花火」h3 直下の段落末尾）。
```
置換前: 第8回（2026年）の楽曲は未定です。</p>
置換後: 第8回（2026年）の楽曲は、お知らせ「<a href="https://machizukuri-con.or.jp/news/<ID>/">第8回大会の音楽紹介</a>」でご紹介しています（2026年9月13日時点の予定です）。</p>
```
- `<ID>` は⑫の投稿 ID。公開前は差し替えない（404 になる）。
- ⑪公開後（任意）: 同じ段落の末尾に `花火を打ち上げる<a href="https://machizukuri-con.or.jp/hanabishi/">花火師のご紹介</a>もご覧ください。` を足す（`patch_parts.py --hanabishi-url`）。
- あわせて SPEC ⑤ ②-3 の「第8回の楽曲は未定と明記」の記述を更新する。

## 5. `b13/embed-top.html` → 本番トップページ（page 7）「ギャラリー」節
位置: h2「ギャラリー」の fullWide の最後。`<h4 class="wp-block-heading">第7回秋川流域花火大会ドキュメント</h4>` → 段落「準備、当日の様子に加え、花火大会に向けた私たちの想いを動画にしました。ぜひご覧ください。」→ `wp:video`（src `…/wp-content/uploads/第7回秋川流域花火大会-ショートムービー.mp4`）の順で、video が節の最後のブロック（rendered では figure の直後に `</div></div>` が来ている）。raw では次の形になっている想定:
```
<!-- wp:video {"id":NNNN} -->
<figure class="wp-block-video"><video controls src="https://machizukuri-con.or.jp/wp-content/uploads/第7回秋川流域花火大会-ショートムービー.mp4"></video></figure>
<!-- /wp:video --></div></div>
<!-- /wp:loos/full-wide -->
```
検索アンカー: `ショートムービー.mp4`（page 7 に 1 件）から後方に最初の `<!-- /wp:video -->` を探し、その **直後**（`</div></div>` の前）に `embed-top.html`（h4「第7回秋川流域花火大会 定点映像」+ 段落 + `wp:embed`）を空行を挟んで入れる。結果: `<!-- /wp:video -->␤␤<!-- wp:heading {"level":4} -->…<!-- /wp:embed --></div></div>`。
- 既存が h4 なので部品も h4（同じ階層）。
- 手順: `GET /wp-json/wp/v2/pages/7?context=edit` → `content.raw` をファイルに保存 → `python S/patch_parts.py --top-raw <file>` → `S/out/_patched/top_content.patched.html` を check_blocks（他の既存ブロックが許可外として出る場合は wp:embed 周辺だけ目視）→ `POST /wp-json/wp/v2/pages/7` で `content` を更新。ページ冒頭 4KB は変わらないので WAF の影響はない。
- `page_7.html`（rendered）を差し込み元にしてはいけない（ブロックコメントが無く、`width="1920" height="1080"` などが付いている）。
- 施策⑤公開時は、この動画の下に「もっと知る」ボタン（`/know-more/`）を置く（⑤SPEC ④-4。①が間に合わない場合の最小対応）。

## 6. `b3/section.html`・`b2/section.html` → トップページ（施策①の整理後に使う）
- どちらも **今は差し込まない**。トップページ①の整理（区画の順番の見直し）のときに置く。
- `b3/section.html`: `wp:loos/full-wide` 1 個（見出し「第8回の楽しみ方」+ 4カード + 注記 + ボタン）。リンクは相対 `/enjoy/#akg-eat` `/enjoy/#akg-see` `/enjoy/#akg-play` `/enjoy/#akg-hanabi` `/enjoy/` → **/enjoy/ を公開してから** 置く。slug が enjoy 以外になったら 5 か所を直す。置き場所の案は「チケット情報」の下（または「コンセプト」の上）。
- `b2/section.html`: 見出し + 3文 + 5枚のカード + ボタン。リンクは絶対 `https://machizukuri-con.or.jp/akigawa-day/` → **/akigawa-day/ を公開してから** 置く（check_blocks --net は公開まで 404 を返す。今回の実行でもこの 1 件だけ error になった）。置き場所は「秋川流域とは」の直後。
- 各ページ公開時にトップへ置くボタン（⑧「初めて来る方へ」＝チケット案内の近く、⑪「花火を打ち上げる花火師を見る」＝今年の見どころ or ギャラリーの近く、⑤「もっと知る」）も①と合わせる。

## 7. 公開後のリンク差し替え一覧
| # | ファイル | アンカー | 置換後 | いつ |
|---|---|---|---|---|
| 7-1 | b3 に差し込んだ `b12/section.html` 末尾 | `<a href="https://machizukuri-con.or.jp/categry/news/">第8回大会の音楽紹介</a>` | `href` を `https://machizukuri-con.or.jp/news/<ID>/` に | ⑫公開後（③公開時） |
| 7-2 | `b11/content.html`（「第8回（2026年）の花火」節） | `<a href="https://machizukuri-con.or.jp/categry/news/">お知らせ</a>でご紹介します。</p>` | `お知らせ「<a href="https://machizukuri-con.or.jp/news/<ID>/">第8回大会の音楽紹介</a>」でご紹介しています。</p>` | ⑪公開時（⑫は公開済み） |
| 7-3 | `b12/post.html` 末尾 | `第7回大会の音楽紹介</a>」をご覧ください。</p>` `<!-- /wp:paragraph -->` の後 | 段落を追加: `花火を打ち上げる花火師については、「<a href="https://machizukuri-con.or.jp/hanabishi/">花火を打ち上げる花火師（株式会社ホソヤエンタープライズ）</a>」のページをご覧ください。` | ⑪公開後 |
| 7-4 | `b5/content.html` | §4 | §4 | ⑤公開時 |
| 7-5 | `b8/content.html`「行く前」冒頭 | `<h2 class="wp-block-heading" id="akg-first-before">1. 行く前に（準備と行き方）</h2>` の `<!-- /wp:heading -->` の後（b8 内で 1 件） | 「開催の可否・雨天時の対応は<a href="/kaisai-joho/">天候・開催情報</a>をご覧ください」の1行 | ⑩公開後 |
| 7-6 | `b10/banner.html`・⑩本文 | `/kaisai-joho/#akg-wx-status` | slug が変わる場合のみ | ⑩公開時 |

## 8. 差し込み後のチェック
- `python S/check_blocks.py out/_patched/b3_content.patched.html --net` / 同 b5 / 同 top → `errors=[]`。今回の実行結果: b3 = 102 ブロック・todo 5、b5 = 56 ブロック・todo 3、模擬トップ = errors 0（`--news-url`/`--hanabishi-url` 指定時は b11 = 59・b12/post = 29 も errors 0）。
- `wp:embed` が 3 ファイルとも `wrapper` 内 URL のみで、`<iframe` が無いこと。
- 見出し階層: b3 は h2 → h3、b5 は h2 → h3、トップは h4 の並び。
- 差し込み後の `.akg-todo` の数（b3 = 5、b5 = 3）を SPEC の記述と合わせる。
