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
    <title>{{TITLE}}｜秋川流域花火大会</title>
    <meta name="description" content="{{DESC}}">
    <meta property="og:title" content="{{TITLE}}｜秋川流域花火大会">
    <meta property="og:description" content="{{DESC}}">
    <meta property="og:image" content="assets/keyvisual.jpg">
    <link rel="icon" href="assets/favicon.ico" sizes="any">
    <link rel="apple-touch-icon" href="assets/favicon.ico">
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "WebPage",
          "@id": "https://akigawa-hanabi.netlify.app/{{FILE}}",
          "url": "https://akigawa-hanabi.netlify.app/{{FILE}}",
          "name": "{{TITLE}}｜秋川流域花火大会",
          "description": "{{DESC}}",
          "inLanguage": "ja",
          "isPartOf": { "@id": "https://akigawa-hanabi.netlify.app/#website" },
          "primaryImageOfPage": "https://akigawa-hanabi.netlify.app/assets/keyvisual.jpg"
        },
        {
          "@type": "BreadcrumbList",
          "itemListElement": [
            { "@type": "ListItem", "position": 1, "name": "トップ", "item": "https://akigawa-hanabi.netlify.app/" },
            { "@type": "ListItem", "position": 2, "name": "{{TITLE}}", "item": "https://akigawa-hanabi.netlify.app/{{FILE}}" }
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
  </head>
  <body>
    <header class="site-header">
      <a class="brand" href="index.html" aria-label="秋川流域花火大会 トップへ">
        <span class="brand-mark"></span>
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

    <main class="page-main">
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
          <p>特定非営利活動法人まちづくりコンソーシアム</p>
          <p class="footer-sub">〒197-0804 東京都あきる野市秋川2-6-10 田村ビル2F</p>
          <p class="footer-sub">理事長：立花 晋也</p>
          <p class="footer-label spacer">共催</p>
          <p>あきる野青年会議所</p>
        </div>
        <nav class="footer-nav" aria-label="フッターナビゲーション">
          <p class="footer-label">サイトマップ</p>
          <a href="index.html">トップ</a>
          <a href="company.html">団体概要</a>
          <a href="event.html">イベント一覧</a>
          <a href="ticket.html">チケット</a>
          <a href="donation.html">寄付協賛</a>
          <a href="sponsor.html">協賛企業様</a>
          <a href="access.html">アクセス</a>
          <a href="qa.html">よくある質問</a>
          <a href="pr.html">メディア掲載</a>
          <a href="2024-hanabi.html">2024年の様子</a>
          <a href="food-application.html">飲食出店募集</a>
          <a href="akiruno-kanko.html">周辺観光</a>
          <a href="contact.html">お問い合わせ</a>
        </nav>
      </div>
      <div class="footer-base">
        <small>(C) 秋川流域花火大会 / NPO まちづくりコンソーシアム</small>
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
  $h = [regex]::Replace($h, ' srcset="[^"]*"', '')
  $h = [regex]::Replace($h, ' sizes="[^"]*"', '')
  $h = [regex]::Replace($h, ' width="\d+"', '')
  $h = [regex]::Replace($h, ' height="\d+"', '')
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

<div class="contact-embed">
  <iframe
    src="https://docs.google.com/forms/d/e/1FAIpQLSfavCvVmfAFlPusgrOQNudAsnSfT2GeBAMKMw4GUflGGydFuQ/viewform?embedded=true"
    title="秋川流域花火大会 お問い合わせフォーム"
    loading="lazy"
    frameborder="0"
    marginheight="0"
    marginwidth="0">読み込んでいます…</iframe>
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
  $tag = $page.tag

  $html = $template
  $html = $html.Replace('{{TITLE}}', $title)
  $html = $html.Replace('{{DESC}}', "$title｜秋川流域花火大会")
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
