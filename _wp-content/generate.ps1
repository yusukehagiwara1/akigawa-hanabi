param()

$ErrorActionPreference = "Stop"
$projectDir = Split-Path -Parent $PSScriptRoot
$wpDir = $PSScriptRoot

$pages = @(
  @{ slug = "donation";          file = "donation.html";         tag = "Donation"     }
  @{ slug = "ticket";            file = "ticket.html";           tag = "Tickets"      }
  @{ slug = "access";            file = "access.html";           tag = "Access"       }
  @{ slug = "qa";                file = "qa.html";               tag = "FAQ"          }
  @{ slug = "sponsor";           file = "sponsor.html";          tag = "Sponsors"     }
  @{ slug = "contact";           file = "contact.html";          tag = "Contact"      }
  @{ slug = "2024-hanabi";       file = "2024-hanabi.html";      tag = "Past Event"   }
  @{ slug = "event";             file = "event.html";            tag = "Event"        }
  @{ slug = "company-overview";  file = "company.html";          tag = "About"        }
  @{ slug = "pr";                file = "pr.html";               tag = "Media"        }
  @{ slug = "food-application";  file = "food-application.html"; tag = "Food"         }
  @{ slug = "akiruno-kanko";     file = "akiruno-kanko.html";    tag = "Tourism"      }
  @{ slug = "yahoo-news";        file = "yahoo-news.html";       tag = "News"         }
  @{ slug = "lost-item";         file = "lost-item.html";        tag = "Lost & Found" }
  @{ slug = "privacy-policy";    file = "privacy-policy.html";   tag = "Policy"       }
)

$urlMap = @{
  "https://machizukuri-con.or.jp/donation/"          = "donation.html"
  "https://machizukuri-con.or.jp/donation"           = "donation.html"
  "https://machizukuri-con.or.jp/ticket/"            = "ticket.html"
  "https://machizukuri-con.or.jp/ticket"             = "ticket.html"
  "https://machizukuri-con.or.jp/access/"            = "access.html"
  "https://machizukuri-con.or.jp/access"             = "access.html"
  "https://machizukuri-con.or.jp/qa/"                = "qa.html"
  "https://machizukuri-con.or.jp/qa"                 = "qa.html"
  "https://machizukuri-con.or.jp/sponsor-2025/"      = "sponsor.html"
  "https://machizukuri-con.or.jp/sponsor-2025"       = "sponsor.html"
  "https://machizukuri-con.or.jp/contact/"           = "contact.html"
  "https://machizukuri-con.or.jp/contact"            = "contact.html"
  "https://machizukuri-con.or.jp/2024-hanabi/"       = "2024-hanabi.html"
  "https://machizukuri-con.or.jp/2024-hanabi"        = "2024-hanabi.html"
  "https://machizukuri-con.or.jp/event/"             = "event.html"
  "https://machizukuri-con.or.jp/event"              = "event.html"
  "https://machizukuri-con.or.jp/company-overview/"  = "company.html"
  "https://machizukuri-con.or.jp/company-overview"   = "company.html"
  "https://machizukuri-con.or.jp/pr/"                = "pr.html"
  "https://machizukuri-con.or.jp/pr"                 = "pr.html"
  "https://machizukuri-con.or.jp/food-application/"  = "food-application.html"
  "https://machizukuri-con.or.jp/food-application"   = "food-application.html"
  "https://machizukuri-con.or.jp/akiruno-kanko/"     = "akiruno-kanko.html"
  "https://machizukuri-con.or.jp/akiruno-kanko"      = "akiruno-kanko.html"
  "https://machizukuri-con.or.jp/yahoo-news/"        = "yahoo-news.html"
  "https://machizukuri-con.or.jp/yahoo-news"         = "yahoo-news.html"
  "https://machizukuri-con.or.jp/lost-item/"         = "lost-item.html"
  "https://machizukuri-con.or.jp/lost-item"          = "lost-item.html"
  "https://machizukuri-con.or.jp/privacy-policy/"    = "privacy-policy.html"
  "https://machizukuri-con.or.jp/privacy-policy"     = "privacy-policy.html"
  "https://machizukuri-con.or.jp/"                   = "index.html"
}

$template = @'
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#0f1828">
    <meta name="referrer" content="strict-origin-when-cross-origin">
    <link rel="manifest" href="/manifest.json">
    <title>{{TITLE}}｜秋川流域花火大会</title>
    <meta name="description" content="{{DESC}}">
    <link rel="canonical" href="https://akigawa-hanabi.pages.dev/{{FILE}}">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="秋川流域花火大会">
    <meta property="og:locale" content="ja_JP">
    <meta property="og:url" content="https://akigawa-hanabi.pages.dev/{{FILE}}">
    <meta property="og:title" content="{{TITLE}}｜秋川流域花火大会">
    <meta property="og:description" content="{{DESC}}">
    <meta property="og:image" content="https://akigawa-hanabi.pages.dev/assets/keyvisual.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="900">
    <meta property="og:image:alt" content="夜空に咲く秋川流域花火大会のキービジュアル">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{{TITLE}}｜秋川流域花火大会">
    <meta name="twitter:description" content="{{DESC}}">
    <meta name="twitter:image" content="https://akigawa-hanabi.pages.dev/assets/keyvisual.jpg">
    <meta name="twitter:image:alt" content="夜空に咲く秋川流域花火大会のキービジュアル">
    <link rel="icon" href="assets/favicon.ico" sizes="any">
    <link rel="apple-touch-icon" href="assets/favicon.ico">
    <link rel="dns-prefetch" href="https://0k3w9bd30b.microcms.io">
    <link rel="dns-prefetch" href="https://images.microcms-assets.io">
    <link rel="dns-prefetch" href="https://www.googletagmanager.com">
    <link rel="dns-prefetch" href="https://docs.google.com">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "WebPage",
          "@id": "https://akigawa-hanabi.pages.dev/{{FILE}}",
          "url": "https://akigawa-hanabi.pages.dev/{{FILE}}",
          "name": "{{TITLE}}｜秋川流域花火大会",
          "description": "{{DESC}}",
          "inLanguage": "ja",
          "isPartOf": { "@id": "https://akigawa-hanabi.pages.dev/#website" },
          "primaryImageOfPage": "https://akigawa-hanabi.pages.dev/assets/keyvisual.jpg"
        },
        {
          "@type": "BreadcrumbList",
          "itemListElement": [
            { "@type": "ListItem", "position": 1, "name": "トップ", "item": "https://akigawa-hanabi.pages.dev/" },
            { "@type": "ListItem", "position": 2, "name": "{{TITLE}}", "item": "https://akigawa-hanabi.pages.dev/{{FILE}}" }
          ]
        }
      ]
    }
    </script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900{{AMP}}family=Zen+Old+Mincho:wght@700;900{{AMP}}display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
    <script src="analytics.js" defer></script>
    <script src="ui.js" defer></script>
    <script src="sponsor-urls.js" defer></script>
  </head>
  <body>
    <a class="skip-link" href="#main-content">本文へスキップ</a>
    <header class="site-header">
      <a class="brand" href="index.html" aria-label="秋川流域花火大会 トップへ">
        <img class="brand-mark" src="assets/logo-npo.webp" alt="NPO法人まちづくりコンソーシアム" width="120" height="36">
        <span>秋川流域花火大会</span>
      </a>
      <button class="nav-toggle" aria-label="メニューを開く" aria-expanded="false" aria-controls="primary-nav">
        <span></span>
        <span></span>
        <span></span>
      </button>
      <nav class="nav" id="primary-nav" aria-label="主要ナビゲーション">
        <a href="index.html#about">コンセプト</a>
        <a href="ticket.html">チケット</a>
        <a href="donation.html">寄付協賛</a>
        <a href="access.html">アクセス</a>
        <a href="qa.html">よくある質問</a>
        <a href="contact.html">お問い合わせ</a>
      </nav>
      <a class="header-cta" href="ticket.html">チケットを見る</a>
    </header>

    <main class="page-main" id="main-content">
      <section class="page-hero">
        <div class="page-hero-inner">
          <a class="page-back" href="index.html">← トップへ戻る</a>
          <span class="tag">{{TAG}}</span>
          <h1>{{TITLE}}</h1>
        </div>
      </section>

      <section class="page-body">
        <div class="prose">
{{CONTENT}}
        </div>
      </section>
    </main>

    <button class="scroll-top" type="button" aria-label="トップに戻る" hidden>
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M18 15l-6-6-6 6"></path>
      </svg>
    </button>

    <a class="mobile-sticky-cta" href="ticket.html" aria-label="チケットを見る">
      <span>チケットを見る</span>
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M5 12h14"></path>
        <path d="M13 5l7 7-7 7"></path>
      </svg>
    </a>

    <footer class="footer">
      <div class="footer-grid">
        <div class="footer-brand">
          <p class="footer-title">秋川流域花火大会</p>
          <p class="footer-lead">紅葉の山々と秋川を背景に、地域の力で受け継ぐ秋の花火大会。</p>
          <div class="footer-social">
            <a href="https://www.instagram.com/akigawa_hanabitaikai/" target="_blank" rel="noopener">Instagram</a>
            <a href="contact.html">お問い合わせ</a>
          </div>
        </div>
        <div class="footer-org">
          <p class="footer-label">主催</p>
          <img class="footer-org-logo" src="assets/logo-npo.webp" alt="NPO法人まちづくりコンソーシアム" width="120" height="38">
          <p>特定非営利活動法人まちづくりコンソーシアム</p>
          <p class="footer-sub">〒197-0804 東京都あきる野市秋川2-6-10 田村ビル2F</p>
          <p class="footer-sub">理事長：立花 晋也</p>
          <p class="footer-label spacer">共催</p>
          <p>あきる野青年会議所</p>
        </div>
        <nav class="footer-nav" aria-label="フッターナビゲーション">
          <div class="footer-nav-group">
            <p class="footer-label">大会情報</p>
            <a href="index.html">トップ</a>
            <a href="company.html">団体概要</a>
            <a href="event.html">プログラム</a>
            <a href="2024-hanabi.html">2024年の様子</a>
          </div>
          <div class="footer-nav-group">
            <p class="footer-label">来場・参加</p>
            <a href="ticket.html">チケット</a>
            <a href="donation.html">寄付協賛</a>
            <a href="access.html">アクセス</a>
            <a href="qa.html">よくある質問</a>
            <a href="food-application.html">飲食出店募集</a>
          </div>
          <div class="footer-nav-group">
            <p class="footer-label">関連情報</p>
            <a href="sponsor.html">協賛企業様</a>
            <a href="pr.html">メディア掲載</a>
            <a href="yahoo-news.html">Yahoo!ニュース</a>
            <a href="akiruno-kanko.html">周辺観光</a>
            <a href="lost-item.html">忘れ物一覧</a>
            <a href="contact.html">お問い合わせ</a>
          </div>
        </nav>
      </div>
      <div class="footer-base">
        <small>&copy; 秋川流域花火大会 / NPO まちづくりコンソーシアム</small>
        <a class="footer-policy" href="privacy-policy.html">プライバシーポリシー</a>
      </div>
    </footer>
  </body>
</html>
'@

function Decode-Html([string]$s) {
  return [System.Net.WebUtility]::HtmlDecode($s)
}

function Clean-Content([string]$html) {
  $h = $html
  $h = [regex]::Replace($h, ' style="[^"]*"', '')
  $h = [regex]::Replace($h, ' decoding="[^"]*"', '')
  $h = [regex]::Replace($h, ' loading="[^"]*"', '')
  # Re-apply async decoding + lazy loading uniformly to all images
  $h = [regex]::Replace($h, '<img ', '<img loading="lazy" decoding="async" ')
  # Inject loading="lazy" on all iframes that don't already have it
  $h = [regex]::Replace($h, '<iframe(?![^>]*\bloading=)', '<iframe loading="lazy"')
  # Add a descriptive title to Google Maps iframes (YouTube embeds have their own title)
  $h = [regex]::Replace($h, '<iframe(?![^>]*\btitle=)(?=[^>]*google\.com/maps)', '<iframe title="東京サマーランド 第2駐車場 周辺地図"')
  $h = [regex]::Replace($h, ' srcset="[^"]*"', '')
  $h = [regex]::Replace($h, ' sizes="[^"]*"', '')
  $h = [regex]::Replace($h, ' width="\d+"', '')
  $h = [regex]::Replace($h, ' height="\d+"', '')
  # Replace stale 'Coming Soon' placeholders with neutral wording (event has ended)
  $h = [regex]::Replace($h, '<p>Coming Soon</p>', '<p class="placeholder-tba">— 詳細掲載なし —</p>')
  $h = [regex]::Replace($h, '<strong>Coming Soon</strong>', '<strong>（詳細未掲載）</strong>')
  # Drop fully-placeholder vendor columns (image=Coming Soon stock, heading=（詳細未掲載）, body=— 詳細掲載なし —)
  $h = [regex]::Replace($h, '<div class="wp-block-column">\s*<figure class="wp-block-image[^"]*"[^>]*><img[^>]*src="assets/wp/1-10\.webp"[^>]*/></figure>\s*<h4[^>]*><strong>（詳細未掲載）</strong></h4>\s*<p class="placeholder-tba">— 詳細掲載なし —</p>\s*</div>\s*', '', 'Singleline')
  # Replace the music-program image scroll (1-1..5-1 819x1024 set) with a text-based music program block
  $musicBlock = @'
<div class="music-program">
  <h3 class="music-program-title">楽曲紹介</h3>
  <div class="music-program-section">
    <p class="music-program-label"><span>OPENING</span></p>
    <p class="music-program-headline">米津玄師「IRIS OUT」</p>
    <p class="music-program-sub">大ヒット映画「チェンソーマン 劇場版」主題歌</p>
  </div>
  <div class="music-program-section">
    <p class="music-program-label"><span>MAIN — 映画音楽パート</span></p>
    <p class="music-program-sub">2025年は映画生誕130周年。老若男女誰もが聞いたことのある名曲を中心に。</p>
  </div>
  <ol class="music-program-list">
    <li><span class="track-no">01</span><span class="track-title">IRIS OUT</span><span class="track-artist">米津玄師</span></li>
    <li><span class="track-no">02</span><span class="track-title">APT.</span><span class="track-artist">ブルーノ・マーズ</span></li>
    <li><span class="track-no">03</span><span class="track-title">ライラック</span><span class="track-artist">Mrs. GREEN APPLE</span></li>
    <li><span class="track-no">04</span><span class="track-title">SAY YES</span><span class="track-artist">CHAGE and ASKA</span></li>
    <li><span class="track-no">05</span><span class="track-title">銀の龍の背に乗って</span><span class="track-artist">中島みゆき</span></li>
    <li><span class="track-no">06</span><span class="track-title">時の流れに身をまかせ</span><span class="track-artist">テレサ・テン / 夏川りみ</span></li>
    <li><span class="track-no">07</span><span class="track-title">20th Century Fox Fanfare</span><span class="track-artist">—</span></li>
    <li><span class="track-no">08</span><span class="track-title">「スター・ウォーズ」メインテーマ</span><span class="track-artist">—</span></li>
    <li><span class="track-no">09</span><span class="track-title">Take My Breath Away（愛は吐息のように）</span><span class="track-artist">ベルリン</span></li>
    <li><span class="track-no">10</span><span class="track-title">ムーン・リバー</span><span class="track-artist">オードリー・ヘップバーン</span></li>
    <li><span class="track-no">11</span><span class="track-title">Wasted Nights</span><span class="track-artist">ONE OK ROCK</span></li>
    <li><span class="track-no">12</span><span class="track-title">満月の夜なら</span><span class="track-artist">あいみょん</span></li>
    <li><span class="track-no">13</span><span class="track-title">今宵の月のように</span><span class="track-artist">エレファントカシマシ</span></li>
  </ol>
</div>
'@
  $h = [regex]::Replace($h, '<div class="swell-block-columns"[^>]*>\s*<div class="c-scrollHint">[^<]*<span>[^<]*</span>[^<]*</div>\s*<div class="swell-block-columns__inner">\s*(?:<div class="swell-block-column[^"]*">\s*(?:<figure[^>]*>\s*)*<figure class="wp-block-image[^"]*"[^>]*><img[^>]*src="assets/wp/[1-5]-1-819x1024\.webp"[^>]*/></figure>\s*(?:</figure>)?\s*</div>\s*){5}</div>\s*</div>', $musicBlock, 'Singleline')
  # Prefer 「観覧」over「鑑賞」for fireworks context (user style guide)
  $h = $h.Replace('鑑賞', '観覧')
  # Inject ids on ticket page headings so the homepage cards can anchor-link
  $h = $h.Replace('<h3 class="wp-block-heading">SS席</h3>', '<h3 id="ss" class="wp-block-heading">SS席</h3>')
  $h = $h.Replace('<h3 class="wp-block-heading">A席</h3>', '<h3 id="a" class="wp-block-heading">A席</h3>')
  $h = $h.Replace('<h3 class="wp-block-heading">フリーエリア</h3>', '<h3 id="free" class="wp-block-heading">フリーエリア</h3>')
  # Redirect KKday/asoview product URLs to their official home pages (event has ended)
  $h = [regex]::Replace($h, 'https://www\.kkday\.com/product/[^"''\s]+', 'https://www.kkday.com/ja')
  $h = [regex]::Replace($h, 'https://machizukuricon\.my\.urakata\.app/channels/[^"''\s]+', 'https://www.asoview.com/')
  foreach ($k in $urlMap.Keys) {
    $local = $urlMap[$k]
    $escaped = [regex]::Escape($k)
    $h = [regex]::Replace($h, "href=`"$escaped`"", "href=`"$local`"")
  }
  # Rewrite all wp-content/uploads URLs to local assets/wp/{filename}
  $assetPattern = 'https://machizukuri-con\.or\.jp/wp-content/uploads/([^\s"<>'']+)'
  $h = [regex]::Replace($h, $assetPattern, {
    param($m)
    $rest = $m.Groups[1].Value
    # Strip subdirectories (year/month) and percent-decode
    $fileName = [System.IO.Path]::GetFileName($rest)
    $fileName = [System.Web.HttpUtility]::UrlDecode($fileName)
    return "assets/wp/" + $fileName
  })
  # Swap .jpg/.jpeg/.png references under assets/wp/ to .webp when available
  $script:webpCache = $script:webpCache
  if (-not $script:webpCache) {
    $script:webpCache = @{}
    $wpAssets = Join-Path (Split-Path -Parent $PSScriptRoot) "assets\wp"
    if (Test-Path $wpAssets) {
      Get-ChildItem -Path $wpAssets -File -Filter "*.webp" | ForEach-Object {
        $script:webpCache[$_.BaseName] = $true
      }
    }
  }
  $h = [regex]::Replace($h, 'assets/wp/([^"<>\s'']+?)\.(jpg|jpeg|png)', {
    param($m)
    $base = $m.Groups[1].Value
    if ($script:webpCache.ContainsKey($base)) {
      return "assets/wp/" + $base + ".webp"
    }
    return $m.Value
  })
  return $h
}

function Get-ContactBody {
  return @'
<p>協賛・取材・運営に関するご質問、その他お問い合わせは以下のフォームよりお寄せください。内容を確認のうえ、運営委員会よりご連絡いたします。</p>

<div class="contact-cta">
  <a class="button primary contact-cta-button" href="https://docs.google.com/forms/d/e/1FAIpQLSfavCvVmfAFlPusgrOQNudAsnSfT2GeBAMKMw4GUflGGydFuQ/viewform" target="_blank" rel="noopener">
    お問い合わせフォームを開く
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path d="M5 12h14"></path>
      <path d="M13 5l7 7-7 7"></path>
    </svg>
  </a>
  <p class="contact-cta-note">外部の Google フォームが新しいタブで開きます。</p>
</div>

<aside class="contact-alt">
  <h2>その他の連絡手段</h2>
  <ul>
    <li><strong>Instagram:</strong> <a href="https://www.instagram.com/akigawa_hanabitaikai/" target="_blank" rel="noopener">@akigawa_hanabitaikai</a></li>
    <li><strong>所在地:</strong> 〒197-0804 東京都あきる野市秋川2-6-10 田村ビル2F</li>
  </ul>
</aside>
'@
}

function Build-Page([hashtable]$page) {
  $jsonPath = Join-Path $wpDir ($page.slug + ".json")
  $raw = Get-Content -Raw -Encoding UTF8 -Path $jsonPath
  $obj = $raw | ConvertFrom-Json
  $title = Decode-Html $obj.title.rendered
  if ($page.slug -eq "contact") {
    $content = Get-ContactBody
  } else {
    $content = Clean-Content $obj.content.rendered
  }
  # Prepend a status banner for pages whose underlying event has ended.
  if ($page.slug -eq "ticket") {
    $banner = @'
<aside class="page-status-banner" role="status">
  <strong>第7回（2025年11月15日）の販売は終了しました。</strong>
  <p>たくさんのご来場、誠にありがとうございました。次回開催のチケット情報は、本サイトおよび<a href="https://www.instagram.com/akigawa_hanabitaikai/" target="_blank" rel="noopener">公式Instagram</a>でご案内します。</p>
</aside>

'@
    $content = $banner + $content
  }
  if ($page.slug -eq "food-application") {
    $banner = @'
<aside class="page-status-banner" role="status">
  <strong>第7回（2025年）の出展者募集は締め切りました。</strong>
  <p>たくさんのお申込みをいただきまして、誠にありがとうございました。次回開催の出展募集は、決まり次第本サイトおよび<a href="https://www.instagram.com/akigawa_hanabitaikai/" target="_blank" rel="noopener">公式Instagram</a>でご案内します。</p>
</aside>

'@
    $content = $banner + $content
  }
  $tag = $page.tag

  # Extract a snippet of plain text from raw WP content for meta description
  $plain = $obj.content.rendered -replace '<[^>]+>', '' -replace '\s+', ' '
  $plain = (Decode-Html $plain).Trim()
  if ($plain.Length -gt 110) { $plain = $plain.Substring(0, 110) + "…" }
  if ([string]::IsNullOrWhiteSpace($plain)) { $plain = "$title｜秋川流域花火大会" }
  # Escape double quotes and ampersands for HTML attribute safety
  $desc = $plain.Replace('&', '&amp;').Replace('"', '&quot;')

  $html = $template
  $html = $html.Replace('{{TITLE}}', $title)
  $html = $html.Replace('{{DESC}}', $desc)
  $html = $html.Replace('{{TAG}}', $tag)
  $html = $html.Replace('{{CONTENT}}', $content)
  $html = $html.Replace('{{FILE}}', $page.file)
  $html = $html.Replace('{{AMP}}', '&')

  $outPath = Join-Path $projectDir $page.file
  [System.IO.File]::WriteAllText($outPath, $html, [System.Text.UTF8Encoding]::new($false))
  $size = (Get-Item $outPath).Length
  Write-Output ("OK  {0,8} bytes  {1}" -f $size, $page.file)
}

foreach ($p in $pages) {
  try {
    Build-Page $p
  } catch {
    Write-Output ("ERR {0}: {1}" -f $p.slug, $_.Exception.Message)
  }
}
