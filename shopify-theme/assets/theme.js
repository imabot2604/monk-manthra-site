/* monk manthra — Shopify theme behaviour
 *
 * The mark/reduction/floating-header block below is ported unchanged from
 * assets/js/site.js on the GitHub Pages site — it is pure DOM logic with no
 * dependency on Python, Liquid, or Shopify, so it needed no changes at all.
 *
 * The cart block is new and Shopify-native: Shopify's own Ajax Cart API
 * (/cart/add.js, /cart/change.js, /cart.js), not the Storefront GraphQL
 * client the headless GitHub Pages version used. No access token here —
 * this theme and the cart share an origin, so none is needed. Every cart
 * mutation asks Shopify to re-render the cart-drawer SECTION server-side
 * (via the `sections` param) and swaps that HTML in, rather than
 * reimplementing money formatting and line-item markup in JS a second
 * time — the drawer's real content always comes from the same Liquid that
 * renders it on first page load.
 */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // ---------------------------------------------------------- the mark --
  function drawMarks() {
    var marks = document.querySelectorAll(".mark[data-draw]");
    Array.prototype.forEach.call(marks, function (mark) {
      if (mark.classList.contains("is-drawn")) return;

      var rings = mark.querySelectorAll(".ring");
      Array.prototype.forEach.call(rings, function (ring) {
        var len = 0;
        try { len = ring.getTotalLength(); } catch (e) { len = 0; }
        if (len) ring.style.setProperty("--len", len.toFixed(2));
      });

      mark.classList.add("is-drawn");

      window.setTimeout(function () {
        mark.removeAttribute("data-draw");
      }, reduced ? 0 : 1600);
    });
  }

  function applyReduction() {
    var marks = document.querySelectorAll(".mark");
    Array.prototype.forEach.call(marks, function (mark) {
      if (mark.hasAttribute("data-rings-lock")) return;
      var w = mark.getBoundingClientRect().width;
      if (!w) return;
      var n = w >= 96 ? "3" : w >= 48 ? "2" : "1";
      mark.setAttribute("data-rings", n);
    });
  }

  function floatingHeader() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    var ticking = false;

    function apply() {
      header.classList.toggle("is-floating", window.scrollY > 4);
      ticking = false;
    }
    apply();
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(apply);
    }, { passive: true });
  }

  // ------------------------------------------------------------- cart --
  function postCart(url, body) {
    return fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Accept": "application/json" },
      // Always ask for the cart-drawer section's fresh HTML alongside
      // whatever the mutation itself returns.
      body: JSON.stringify(Object.assign({ sections: "cart-drawer" }, body))
    }).then(function (r) {
      if (!r.ok) return r.json().then(function (e) { throw new Error(e.description || r.statusText); });
      return r.json();
    });
  }

  function refreshBadge() {
    return fetch("/cart.js", { headers: { Accept: "application/json" } })
      .then(function (r) { return r.json(); })
      .then(function (cart) {
        var badge = document.querySelector("[data-cart-count]");
        if (!badge) return;
        badge.textContent = cart.item_count;
        badge.hidden = cart.item_count === 0;
      });
  }

  function swapDrawer(sections) {
    var html = sections && sections["cart-drawer"];
    if (!html) return;
    var wasOpen = document.body.classList.contains("cart-open");

    var tmp = document.createElement("div");
    tmp.innerHTML = html;
    var fresh = tmp.querySelector(".cart-drawer");
    var current = document.querySelector(".cart-drawer");
    if (!fresh || !current) return;

    // The freshly server-rendered section always starts closed
    // (aria-hidden="true") — carry the drawer's actual open state forward
    // across the swap so an in-progress interaction doesn't visibly close.
    if (wasOpen) fresh.setAttribute("aria-hidden", "false");
    current.replaceWith(fresh);
  }

  function updateCart(data) {
    swapDrawer(data.sections);
    return refreshBadge();
  }

  function addToCart(variantId, qty, trigger) {
    trigger.classList.add("is-adding");
    postCart("/cart/add.js", { items: [{ id: variantId, quantity: qty }] })
      .then(updateCart)
      .then(openDrawer)
      .catch(function (err) {
        console.error("[cart] add failed:", err.message);
        trigger.classList.add("is-error");
        window.setTimeout(function () { trigger.classList.remove("is-error"); }, 1600);
      })
      .finally(function () { trigger.classList.remove("is-adding"); });
  }

  function changeLine(key, qty) {
    return postCart("/cart/change.js", { id: key, quantity: qty }).then(updateCart);
  }

  // ----------------------------------------------------------- drawer --
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

  function bindCartEvents() {
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
      if (step) {
        var line = step.closest("[data-line-key]");
        var qtyEl = line.querySelector("[data-line-qty]");
        var next = Number(qtyEl.textContent) + Number(step.dataset.step);
        changeLine(line.dataset.lineKey, Math.max(0, next));
        return;
      }
      var remove = e.target.closest("[data-remove]");
      if (remove) {
        changeLine(remove.closest("[data-line-key]").dataset.lineKey, 0);
      }
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && document.body.classList.contains("cart-open")) closeDrawer();
    });
  }

  // -------------------------------------------------------------------- --
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    applyReduction();
    floatingHeader();
    bindCartEvents();
    if (reduced) {
      var marks = document.querySelectorAll(".mark[data-draw]");
      Array.prototype.forEach.call(marks, function (m) { m.removeAttribute("data-draw"); });
    } else {
      window.requestAnimationFrame(drawMarks);
    }
  });

  var t;
  window.addEventListener("resize", function () {
    window.clearTimeout(t);
    t = window.setTimeout(applyReduction, 200);
  });
})();
