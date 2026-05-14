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
  "https://machizukuri-con.or.jp/privacy-policy/"    = "privacy-policy.html"
  "https://machizukuri-con.or.jp/privacy-policy"     = "privacy-policy.html"
  "https://machizukuri-con.or.jp/"                   = "index.html"
}

$template = @'
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <meta name="theme-color" content="#0f1828">
    <meta name="color-scheme" content="light dark">
    <meta name="referrer" content="strict-origin-when-cross-origin">
    <link rel="manifest" href="/manifest.json">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="秋川花火">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="application-name" content="秋川花火">
    <meta name="msapplication-TileColor" content="#0f1828">
    <title>{{TITLE}}｜秋川流域花火大会【公式】</title>
    <meta name="description" content="{{DESC}}">
    <meta name="keywords" content="秋川流域花火大会, あきる野, 花火大会, 秋花火, 東京サマーランド, 紅葉, 音楽花火, 西多摩, 紅葉と花火, 秋 花火 デート, 子連れ 花火 東京, 11月 花火大会, 東京 秋 イベント, 駐車場あり 花火, Tokyo Autumn Fireworks, {{TITLE}}">
    <meta name="author" content="特定非営利活動法人まちづくりコンソーシアム">
    <link rel="canonical" href="https://akigawa-hanabi.pages.dev/{{FILE}}">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="秋川流域花火大会【公式】">
    <meta property="og:locale" content="ja_JP">
    <meta property="og:url" content="https://akigawa-hanabi.pages.dev/{{FILE}}">
    <meta property="og:title" content="{{TITLE}}｜秋川流域花火大会【公式】">
    <meta property="og:description" content="{{DESC}}">
    <meta property="og:image" content="https://akigawa-hanabi.pages.dev/assets/keyvisual.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="900">
    <meta property="og:image:alt" content="夜空に咲く秋川流域花火大会のキービジュアル">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{{TITLE}}｜秋川流域花火大会【公式】">
    <meta name="twitter:description" content="{{DESC}}">
    <meta name="twitter:image" content="https://akigawa-hanabi.pages.dev/assets/keyvisual.jpg">
    <meta name="twitter:image:alt" content="夜空に咲く秋川流域花火大会のキービジュアル">
    <meta name="twitter:label1" content="開催日">
    <meta name="twitter:data1" content="2026年11月14日（土） 18:00〜18:50">
    <meta name="twitter:label2" content="会場">
    <meta name="twitter:data2" content="東京サマーランド 第2駐車場（あきる野市）">
    <link rel="icon" href="assets/favicon.ico" sizes="any">
    <link rel="apple-touch-icon" href="assets/favicon.ico">
    <link rel="dns-prefetch" href="https://0k3w9bd30b.microcms.io">
    <link rel="dns-prefetch" href="https://images.microcms-assets.io">
    <link rel="dns-prefetch" href="https://www.googletagmanager.com">
    <link rel="dns-prefetch" href="https://www.google-analytics.com">
    <link rel="dns-prefetch" href="https://stats.g.doubleclick.net">
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
    <link rel="preload" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900{{AMP}}family=Zen+Old+Mincho:wght@700;900{{AMP}}display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900{{AMP}}family=Zen+Old+Mincho:wght@700;900{{AMP}}display=swap"></noscript>
    <style>
    /* Critical CSS for sub-pages — inlined to render the header and
       page-hero without waiting for styles.css. */
    :root{--ink:#172026;--muted:#62707a;--paper:#fffdf7;--cream:#f7efe2;--gold:#d7a947;--gold-text:#8e6a1f;--red:#b83f37;--teal:#0f6868;--night:#10182a;--line:rgba(23,32,38,.13)}
    *{box-sizing:border-box}
    html{scroll-behavior:smooth;scroll-padding-top:80px}
    body{margin:0;color:var(--ink);background:var(--paper);font-family:"Noto Sans JP",system-ui,sans-serif;line-height:1.7}
    a{color:inherit;text-decoration:none}
    img{max-width:100%}
    h1,h2,p{margin-top:0}
    h1,h2{font-family:"Zen Old Mincho",serif;line-height:1.18}
    .skip-link{position:absolute;left:12px;top:12px;z-index:100;padding:10px 16px;background:var(--ink);color:#fff;font-weight:700;border-radius:6px;transform:translateY(-200%)}
    .skip-link:focus-visible{transform:translateY(0)}
    .site-header{position:fixed;z-index:20;top:0;left:0;right:0;display:flex;align-items:center;justify-content:space-between;gap:24px;min-height:72px;padding:14px clamp(18px,4vw,54px);color:#fff;background:rgba(10,16,28,.94);backdrop-filter:blur(12px)}
    .brand{display:flex;align-items:center;gap:12px;font-weight:900;white-space:nowrap;font-size:1.02rem;letter-spacing:.04em}
    .brand-mark{display:block;height:40px;width:auto;filter:invert(1) grayscale(1);mix-blend-mode:difference;opacity:.95}
    .nav{display:flex;align-items:center;gap:clamp(14px,2vw,30px);font-size:.91rem;font-weight:700}
    .nav a{opacity:.88}
    .header-cta{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 18px;border-radius:999px;font-weight:800;color:var(--night);background:#fff;white-space:nowrap}
    .nav-toggle{display:none}
    @media (max-width:920px){.nav{display:none}.nav-toggle{display:flex;width:44px;height:44px;padding:0;border:0;background:transparent;cursor:pointer;align-items:center;justify-content:center;flex-direction:column;gap:6px}.nav-toggle span{display:block;width:24px;height:2px;background:#fff;border-radius:2px}}
    .page-main{padding-top:72px}
    .page-hero{position:relative;padding:clamp(80px,11vw,140px) clamp(22px,5vw,70px) clamp(40px,6vw,80px);background:radial-gradient(circle at 12% 18%,rgba(215,169,71,.18),transparent 55%),radial-gradient(circle at 88% 22%,rgba(184,63,55,.12),transparent 50%),linear-gradient(180deg,#0f1828,#0f3939 70%,var(--cream));color:#fff;overflow:hidden}
    .page-hero-inner{position:relative;width:min(1120px,calc(100% - 40px));margin-inline:auto}
    .page-hero h1{max-width:920px;margin:0;font-size:clamp(2rem,5vw,3.6rem);color:#fff;word-break:keep-all;line-break:strict}
    .page-hero .tag{display:inline-flex;align-items:center;gap:10px;color:var(--gold);font-size:.78rem;font-weight:900;letter-spacing:.12em;text-transform:uppercase;margin-bottom:12px}
    .page-hero .page-back{display:inline-flex;align-items:center;gap:6px;margin-bottom:18px;padding:8px 14px;border:1px solid rgba(255,255,255,.32);border-radius:999px;font-size:.86rem;font-weight:700;color:rgba(255,255,255,.88)}
    .page-hero-pill{display:inline-flex;align-items:center;gap:8px;margin:0 0 16px;padding:6px 14px 6px 10px;background:linear-gradient(135deg,rgba(215,169,71,.22),rgba(184,63,55,.18));border:1px solid rgba(215,169,71,.5);border-radius:999px;color:#fff;font-size:.78rem;font-weight:800}
    .page-hero-pill strong{color:var(--gold);font-weight:900}
    .page-hero-pill-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:var(--gold)}
    @media (prefers-color-scheme:dark){:root{--ink:#f1eee5;--muted:#a4b1ba;--paper:#0c1320;--cream:#1a2236;--gold-text:#e0c478;--line:rgba(255,255,255,.10)}}
    </style>
    <link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="styles.css"></noscript>
    <script src="analytics.js" defer></script>
    <script src="ui.js" defer></script>
    <script src="sponsor-urls.js" defer></script>
    <script>
      if ("serviceWorker" in navigator) {
        window.addEventListener("load", function () {
          navigator.serviceWorker.register("/sw.js").catch(function () {});
        });
      }
    </script>
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

      <aside class="subpage-signup-cta" aria-label="次回開催情報を受け取る">
        <div class="subpage-signup-cta-inner">
          <div class="subpage-signup-cta-text">
            <span class="tag">Next Edition</span>
            <h2>第8回 秋川流域花火大会の<br>最新情報をいち早く受け取る</h2>
            <p>開催日・チケット販売開始のお知らせを、メール・SNSでお届けします。</p>
          </div>
          <div class="subpage-signup-cta-actions">
            <a class="signup-option signup-instagram" href="https://www.instagram.com/akigawa_hanabitaikai/" target="_blank" rel="noopener" data-ga-cta="signup:instagram">
              <span class="signup-option-icon" aria-hidden="true">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
              </span>
              <span class="signup-option-body"><strong>Instagram</strong><span>@akigawa_hanabitaikai</span></span>
            </a>
            <a class="signup-option signup-email" href="index.html#signup" data-ga-cta="signup:lp">
              <span class="signup-option-icon" aria-hidden="true">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
              </span>
              <span class="signup-option-body"><strong>メールで通知を受け取る</strong><span>登録ページへ</span></span>
            </a>
          </div>
        </div>
      </aside>
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
            <a href="akiruno-kanko.html">周辺観光</a>
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
  # Force external ticket links to open in a new tab (KKday / asoview / urakata)
  $h = [regex]::Replace(
    $h,
    '<a href="(https://(?:www\.kkday\.com/product/[^"]+|machizukuricon\.my\.urakata\.app/channels/[^"]+))"(?![^>]*\btarget=)',
    '<a href="$1" target="_blank" rel="noopener"'
  )
  # Strip anchor wrappers for removed Yahoo!ニュース / 忘れ物一覧 sub-pages (keep the image)
  $h = [regex]::Replace($h, '<a href="https://machizukuri-con\.or\.jp/yahoo-news/?">(\s*<img[^>]*>)\s*</a>', '$1', 'Singleline')
  $h = [regex]::Replace($h, '<a href="https://machizukuri-con\.or\.jp/lost-item/?">(\s*<img[^>]*>)\s*</a>', '$1', 'Singleline')
  $h = [regex]::Replace($h, '<a href="yahoo-news\.html">(\s*<img[^>]*>)\s*</a>', '$1', 'Singleline')
  $h = [regex]::Replace($h, '<a href="lost-item\.html">(\s*<img[^>]*>)\s*</a>', '$1', 'Singleline')
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
  # Inject width/height attributes for known image src so the browser can
  # reserve aspect-ratio boxes during layout (Core Web Vitals: CLS, LCP).
  $h = Add-ImageDimensions $h
  return $h
}

# Cache of image natural dimensions: relative path -> @{ W=int; H=int }
$script:imgDimsCache = $null
function Get-ImageDimsLookup {
  if ($script:imgDimsCache) { return $script:imgDimsCache }
  $script:imgDimsCache = @{}
  $assetsDir = Join-Path (Split-Path -Parent $PSScriptRoot) "assets"
  if (-not (Test-Path $assetsDir)) { return $script:imgDimsCache }
  $shell = New-Object -ComObject Shell.Application
  Get-ChildItem -Path $assetsDir -Recurse -Include *.webp,*.jpg,*.jpeg,*.png -File | ForEach-Object {
    $rel = $_.FullName.Substring((Split-Path -Parent $PSScriptRoot).Length + 1) -replace '\\','/'
    try {
      $dir = $shell.Namespace($_.DirectoryName)
      $item = $dir.ParseName($_.Name)
      $raw = $dir.GetDetailsOf($item, 31)
      if ($raw -match '(\d+)\s*x\s*(\d+)') {
        $script:imgDimsCache[$rel] = @{ W = [int]$matches[1]; H = [int]$matches[2] }
      }
    } catch {}
  }
  return $script:imgDimsCache
}

function Add-ImageDimensions([string]$html) {
  $lookup = Get-ImageDimsLookup
  if ($lookup.Count -eq 0) { return $html }
  return [regex]::Replace($html, '<img\b[^>]*?>', {
    param($m)
    $tag = $m.Value
    # Skip if already has width or height
    if ($tag -match '(?i)\swidth\s*=' -or $tag -match '(?i)\sheight\s*=') { return $tag }
    if ($tag -notmatch '(?i)\ssrc\s*=\s*"([^"]+)"') { return $tag }
    $src = $matches[1]
    $norm = $src -replace '^/', '' -replace '[\?#].*$', ''
    if (-not $lookup.ContainsKey($norm)) { return $tag }
    $w = $lookup[$norm].W
    $h = $lookup[$norm].H
    return [regex]::Replace($tag, '(?i)(\ssrc\s*=\s*"[^"]+")', "`$1 width=`"$w`" height=`"$h`"", 1)
  })
}

function Apply-SponsorAltFix([string]$h) {
  # WP shipped a generic-slug filename as alt text for the unnamed 2-2
  # logo placeholder. Replace with a neutral fallback so screen readers
  # don't read out file slugs.
  $h = $h.Replace('alt="2-2 企業ロゴ"', 'alt="協賛企業ロゴ"')
  return $h
}

function Apply-AccessStaleGuard([string]$h) {
  # access.html ships with a bus-stop timetable imported verbatim from WP
  # at 第7回 (2025). Bus schedules change year to year; append a disclaimer
  # so visitors verify the latest times rather than rely on a stale table.
  $note = @'

<p class="access-timetable-note"><strong>※ 上記時刻表は前回開催（2025年）時点の路線バス情報です。</strong>当日は<a href="https://www.summerland.co.jp/access/" target="_blank" rel="noopener">東京サマーランド アクセスページ</a>または各バス会社の公式時刻表で最新運行情報をご確認ください。</p>
'@
  $h = [regex]::Replace(
    $h,
    '(<figure class="wp-block-table"><table class="has-fixed-layout"><tbody><tr><td>発（秋川駅）</td>.*?</table></figure>)',
    "`$1$note",
    'Singleline'
  )
  return $h
}

function Apply-TicketStaleGuard([string]$h) {
  # The WP source ships with live KKday / アソビュー reservation links from
  # the previous edition. They must not be clickable after 第7回 ended —
  # rewrite to "販売準備中" notices that funnel to the signup flow.

  # 1) Unwrap the top "purchase method" platform logos
  $h = [regex]::Replace(
    $h,
    '<a href="https://www\.kkday\.com/[^"]+" target="_blank" rel="noopener">(<img[^>]*alt="KKdayで予約"[^>]*/?>)</a>',
    '$1'
  )
  $h = [regex]::Replace(
    $h,
    '<a href="https://machizukuricon\.my\.urakata\.app/[^"]+" target="_blank" rel="noopener">(<img[^>]*alt="アソビューで予約"[^>]*/?>)</a>',
    '$1'
  )
  $h = $h.Replace('alt="KKdayで予約"',     'alt="KKday（前回販売プラットフォーム）"')
  $h = $h.Replace('alt="アソビューで予約"', 'alt="アソビュー（前回販売プラットフォーム）"')

  # 2) Rephrase the lead text above the platform logos
  $h = $h.Replace(
    '<p class="u-mb-ctrl u-mb-0">以下2つのサイトからチケットを購入可能です。</p>',
    '<p class="u-mb-ctrl u-mb-0">前回（第7回）は以下 2 つのプラットフォームで販売しました。第8回の販売開始時にも同様の事前購入制を予定しています（販売開始日・販売チャネルは決定次第ご案内）。</p>'
  )

  # 3) Replace the SS / A / フリーエリア button-pair columns with the
  #    `.ticket-sale-pending` notice. The seat name is captured from the
  #    KKday button span (kept verbatim by WP) and reused in aria-label.
  $btnPattern = '(?s)<div class="wp-block-columns">\s*<div class="wp-block-column">\s*<div class="swell-block-button blue_[^"]*"><a href="https://www\.kkday\.com/[^"]+" target="_blank" rel="noopener" class="swell-block-button__link"><span>\s*(SS席|A席|フリーエリア)をKKdayで予約する\s*</span></a></div>\s*</div>\s*<div class="wp-block-column">\s*<div class="swell-block-button red_[^"]*"><a href="https://machizukuricon\.my\.urakata\.app/[^"]+" target="_blank" rel="noopener" class="swell-block-button__link"><span><strong>\1をアソビューで予約する</strong></span></a></div>\s*</div>\s*</div>'

  $noticeTemplate = @'
<div class="ticket-sale-pending" role="status" aria-label="{SEAT}の販売状況">
  <div class="ticket-sale-pending-msg">
    <span class="ticket-sale-pending-tag">準備中</span>
    <strong>第8回（2026.11.14）の販売開始までお待ちください</strong>
    <span class="ticket-sale-pending-sub">前回（第7回・2025年）の販売は終了しています</span>
  </div>
  <a class="ticket-sale-pending-cta" href="index.html#signup" data-ga-cta="ticket-pending:signup">
    販売開始通知を受け取る
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14"></path><path d="M13 5l7 7-7 7"></path></svg>
  </a>
</div>
'@

  $h = [regex]::Replace($h, $btnPattern, {
    param($m)
    $seat = $m.Groups[1].Value
    return $noticeTemplate.Replace('{SEAT}', $seat)
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
  <strong>第8回 秋川流域花火大会 開催決定：2026年11月14日（土）</strong>
  <p>花火打ち上げ 18:00〜18:50／約5,000発。チケット販売開始日は決定次第ご案内します。最新情報は <a href="index.html#signup">次回開催情報ページ</a>、または<a href="https://www.instagram.com/akigawa_hanabitaikai/" target="_blank" rel="noopener">公式Instagram</a>でお知らせします。</p>
  <p class="page-status-actions">
    <a class="page-status-calendar" href="akigawa-hanabi-2026.ics" download="akigawa-hanabi-2026.ics" data-ga-cta="calendar:download-ticket">
      📅 カレンダーに開催日を追加（.ics）
    </a>
  </p>
</aside>

'@
    $content = $banner + $content
    $content = Apply-TicketStaleGuard $content
  }
  if ($page.slug -eq "access") {
    $content = Apply-AccessStaleGuard $content
  }
  if ($page.slug -eq "sponsor") {
    $content = Apply-SponsorAltFix $content
  }
  if ($page.slug -eq "event") {
    $banner = @'
<aside class="page-status-banner" role="status">
  <strong>このページの楽曲・出演団体は前回（第7回・2025年）開催時の内容です。</strong>
  <p>第8回（2026年11月14日 土曜）のプログラム詳細は決定次第本サイトでご案内します。打ち上げ規模・コンセプト・打ち上げ時間（18:00〜18:50）は前回同様の予定です。最新情報は <a href="index.html#signup">次回開催情報ページ</a> または <a href="https://www.instagram.com/akigawa_hanabitaikai/" target="_blank" rel="noopener">公式Instagram</a> でお知らせします。</p>
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
  [System.IO.File]::WriteAllText($outPath, $html, [System.Text.UTF8Encoding]::new($true))
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
