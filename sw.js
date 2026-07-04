// Service Worker — 自己破棄版 (Round 113)
// 静的サイトの運用終了に伴い、既存訪問者のブラウザに残っている旧 Service Worker と
// キャッシュをすべて削除し、自身の登録も解除する。
// これにより次のナビゲーションはネットワークへ抜け、_redirects の 301 で
// 本番サイト (machizukuri-con.or.jp) へ転送される。
// 旧 sw.js のバックアップ: _build/_sw.js.bak-round113

self.addEventListener("install", () => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    (async () => {
      // 全キャッシュを削除
      const keys = await caches.keys();
      await Promise.all(keys.map((key) => caches.delete(key)));
      // 自身の登録を解除
      await self.registration.unregister();
      // 開いているタブを再読み込みさせ、301 リダイレクトで本番へ送る
      const clients = await self.clients.matchAll({ type: "window" });
      clients.forEach((client) => client.navigate(client.url));
    })()
  );
});
