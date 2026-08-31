/* monk manthra — Shopify Storefront API cart
 *
 * NOT part of the brand guide. The guide governs the mark, colour, type and
 * copy; it says nothing about commerce UI. This drawer is a new surface, so
 * it borrows the site's existing tokens (Half White ground, Deep Purple ink,
 * Fraunces for product names, Plex Mono for money, one gold action) rather
 * than inventing a second visual language.
 *
 * Talks to Shopify's Storefront API directly from the browser — no backend,
 * so this runs fine on GitHub Pages. The Storefront access token is public
 * by design (Shopify scopes it read/cart-only); it is not a secret and is
 * safe to ship in this file. Never put an Admin API token here — that one
 * IS a secret and belongs on a server you control, not in client JS.
 *
 * Stays completely inert — every "Add to order" link behaves exactly as it
 * does today, a plain link to start.html — until window.SHOP.domain and
 * window.SHOP.token are both set to real values. See README.md, "Selling
 * on Shopify" for the three steps that produce those values.
 */
(function () {
  "use strict";

  var SHOP = window.SHOP || {};
  var configured = !!(SHOP.domain && SHOP.token &&
    SHOP.domain.indexOf("YOUR-STORE") === -1 &&
    SHOP.token.indexOf("YOUR-") === -1);

  if (!configured) return; // every [data-buy] link is left as a plain <a href>

  var ENDPOINT = "https://" + SHOP.domain + "/api/" + (SHOP.apiVersion || "2025-10") + "/graphql.json";
  var CART_KEY = "mm_cart_id";

  function gql(query, variables) {
    return fetch(ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Shopify-Storefront-Access-Token": SHOP.token
      },
      body: JSON.stringify({ query: query, variables: variables || {} })
    }).then(function (r) { return r.json(); }).then(function (json) {
      if (json.errors) throw new Error(json.errors.map(function (e) { return e.message; }).join("; "));
      return json.data;
    });
  }

  var CART_FIELDS =
    "id checkoutUrl totalQuantity " +
    "cost { subtotalAmount { amount currencyCode } } " +
    "lines(first: 50) { edges { node { " +
    "  id quantity " +
    "  merchandise { ... on ProductVariant { " +
    "    id title image { url altText } " +
    "    price { amount currencyCode } " +
    "    product { title handle } " +
    "  } } " +
    "} } }";

  function cartCreate(variantId, qty) {
    return gql(
      "mutation($lines: [CartLineInput!]) { cartCreate(input: { lines: $lines }) { " +
      "cart { " + CART_FIELDS + " } userErrors { message } } }",
      { lines: [{ merchandiseId: variantId, quantity: qty }] }
    ).then(function (d) { return d.cartCreate.cart; });
  }

  function cartLinesAdd(cartId, variantId, qty) {
    return gql(
      "mutation($cartId: ID!, $lines: [CartLineInput!]!) { cartLinesAdd(cartId: $cartId, lines: $lines) { " +
      "cart { " + CART_FIELDS + " } userErrors { message } } }",
      { cartId: cartId, lines: [{ merchandiseId: variantId, quantity: qty }] }
    ).then(function (d) { return d.cartLinesAdd.cart; });
  }

  function cartLinesUpdate(cartId, lineId, qty) {
    return gql(
      "mutation($cartId: ID!, $lines: [CartLineUpdateInput!]!) { cartLinesUpdate(cartId: $cartId, lines: $lines) { " +
      "cart { " + CART_FIELDS + " } userErrors { message } } }",
      { cartId: cartId, lines: [{ id: lineId, quantity: qty }] }
    ).then(function (d) { return d.cartLinesUpdate.cart; });
  }

  function cartLinesRemove(cartId, lineId) {
    return gql(
      "mutation($cartId: ID!, $lineIds: [ID!]!) { cartLinesRemove(cartId: $cartId, lineIds: $lineIds) { " +
      "cart { " + CART_FIELDS + " } userErrors { message } } }",
      { cartId: cartId, lineIds: [lineId] }
    ).then(function (d) { return d.cartLinesRemove.cart; });
  }

  function cartFetch(cartId) {
    return gql("query($id: ID!) { cart(id: $id) { " + CART_FIELDS + " } }", { id: cartId })
      .then(function (d) { return d.cart; }); // null if the cart expired
  }

  // ---------------------------------------------------------------- state --
  var cart = null;

  function money(amount, currency) {
    var n = Number(amount);
    var symbol = currency === "INR" ? "₹" : currency + " ";
    return symbol + (Number.isInteger(n) ? n : n.toFixed(2)).toLocaleString("en-IN");
  }

  function persist() {
    try {
      if (cart && cart.id) localStorage.setItem(CART_KEY, cart.id);
      else localStorage.removeItem(CART_KEY);
    } catch (e) { /* private browsing — cart just won't survive a reload */ }
  }

  function render() {
    var badge = document.querySelector("[data-cart-count]");
    var body = document.querySelector("[data-cart-body]");
    var subtotal = document.querySelector("[data-cart-subtotal]");
    var checkoutLink = document.querySelector("[data-cart-checkout]");
    if (!badge) return;

    var qty = (cart && cart.totalQuantity) || 0;
    badge.textContent = qty;
    badge.hidden = qty === 0;

    if (!cart || qty === 0) {
      body.innerHTML = '<p class="cart-empty">Nothing in the order yet.</p>';
      subtotal.textContent = "";
      checkoutLink.setAttribute("aria-disabled", "true");
      checkoutLink.removeAttribute("href");
      return;
    }

    checkoutLink.removeAttribute("aria-disabled");
    checkoutLink.href = cart.checkoutUrl;
    subtotal.textContent = money(cart.cost.subtotalAmount.amount, cart.cost.subtotalAmount.currencyCode);

    body.innerHTML = cart.lines.edges.map(function (edge) {
      var l = edge.node, v = l.merchandise;
      return (
        '<li class="cart-line" data-line-id="' + l.id + '">' +
        '<span class="cart-line__name">' + v.product.title +
        (v.title !== "Default Title" ? ' <span class="cart-line__variant">' + v.title + "</span>" : "") +
        "</span>" +
        '<span class="cart-line__qty">' +
        '<button type="button" class="cart-step" data-step="-1" aria-label="One fewer">−</button>' +
        '<span class="data">' + l.quantity + "</span>" +
        '<button type="button" class="cart-step" data-step="1" aria-label="One more">+</button>' +
        "</span>" +
        '<span class="cart-line__price data">' + money(v.price.amount, v.price.currencyCode) + "</span>" +
        '<button type="button" class="cart-remove" data-remove aria-label="Remove ' + v.product.title + '">×</button>' +
        "</li>"
      );
    }).join("");
  }

  function setCart(next) { cart = next; persist(); render(); }

  // ------------------------------------------------------------- add flow --
  function ensureCart(variantId, qty) {
    if (cart && cart.id) return cartLinesAdd(cart.id, variantId, qty);
    var existing = null;
    try { existing = localStorage.getItem(CART_KEY); } catch (e) {}
    if (existing) {
      return cartFetch(existing).then(function (found) {
        return found ? cartLinesAdd(found.id, variantId, qty) : cartCreate(variantId, qty);
      });
    }
    return cartCreate(variantId, qty);
  }

  function addToCart(variantId, qty, trigger) {
    trigger.classList.add("is-adding");
    ensureCart(variantId, qty)
      .then(function (c) { setCart(c); openDrawer(); })
      .catch(function (err) {
        console.error("[shop] add to cart failed:", err.message);
        trigger.classList.add("is-error");
        window.setTimeout(function () { trigger.classList.remove("is-error"); }, 1600);
      })
      .finally(function () { trigger.classList.remove("is-adding"); });
  }

  // -------------------------------------------------------------- drawer --
  var lastFocus = null;

  function openDrawer() {
    var drawer = document.querySelector(".cart-drawer");
    var scrim = document.querySelector(".cart-scrim");
    if (!drawer) return;
    lastFocus = document.activeElement;
    document.body.classList.add("cart-open");
    drawer.setAttribute("aria-hidden", "false");
    scrim.hidden = false;
    var close = drawer.querySelector(".cart-drawer__close");
    if (close) close.focus();
  }

  function closeDrawer() {
    var drawer = document.querySelector(".cart-drawer");
    var scrim = document.querySelector(".cart-scrim");
    if (!drawer) return;
    document.body.classList.remove("cart-open");
    drawer.setAttribute("aria-hidden", "true");
    scrim.hidden = true;
    if (lastFocus) lastFocus.focus();
  }

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    // Every buy button becomes live — intercept instead of navigating to start.html
    document.addEventListener("click", function (e) {
      var buy = e.target.closest("[data-buy]");
      if (buy && buy.dataset.variantId) {
        e.preventDefault();
        addToCart(buy.dataset.variantId, Number(buy.dataset.qty || 1), buy);
        return;
      }
      if (e.target.closest("[data-cart-toggle]")) { e.preventDefault(); openDrawer(); return; }
      if (e.target.closest("[data-cart-close], .cart-scrim")) { closeDrawer(); return; }

      var step = e.target.closest(".cart-step");
      if (step && cart) {
        var line = step.closest("[data-line-id]").dataset.lineId;
        var current = cart.lines.edges.find(function (l) { return l.node.id === line; }).node.quantity;
        var next = current + Number(step.dataset.step);
        (next < 1 ? cartLinesRemove(cart.id, line) : cartLinesUpdate(cart.id, line, next)).then(setCart);
        return;
      }
      var remove = e.target.closest("[data-remove]");
      if (remove && cart) {
        cartLinesRemove(cart.id, remove.closest("[data-line-id]").dataset.lineId).then(setCart);
      }
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("cart-open")) closeDrawer();
    });

    // Resume a cart left over from a previous visit
    var existing = null;
    try { existing = localStorage.getItem(CART_KEY); } catch (e) {}
    if (existing) cartFetch(existing).then(function (c) { if (c) setCart(c); });
    else render(); // shows the empty state so the badge/drawer exist correctly
  });
})();
