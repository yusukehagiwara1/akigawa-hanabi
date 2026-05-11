window.MICROCMS_CONFIG = {
  serviceDomain: "0k3w9bd30b",
  apiKey: "y7kIMdrY0j0W3YCwORBpovPoaaZCYHX2lYod",
  endpoint: "news",
  limit: 3,
};
window.MICROCMS_EXTRA = {
  sponsors:     { endpoint: "sponsors",     limit: 50, orders: "order" },
  gallery:      { endpoint: "gallery",      limit: 12, orders: "order" },
  testimonial:  { endpoint: "testimonial",  limit: 6,  orders: "-publishedAt" },
  pressRelease: { endpoint: "press_release", limit: 20, orders: "-published_at" },
  faqDynamic:   { endpoint: "faq_dynamic",  limit: 30, orders: "order" },
};