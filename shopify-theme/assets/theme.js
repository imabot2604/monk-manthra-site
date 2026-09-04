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
        // A digit alone is announced as a bare number. Give the live region
        // a sentence, so a screen reader confirms the commit in words.
        var say = document.querySelector("[data-cart-announce]");
        if (say) {
          say.textContent = cart.item_count === 1
            ? "1 item in your order"
            : cart.item_count + " items in your order";
        }
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
    // The node the drag listeners were bound to has just been thrown away.
    // Without this the gesture works exactly once, then dies silently after
    // the first add or quantity change.
    enableDrag();
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

  function drawerEl() { return document.querySelector(".cart-drawer"); }
  function scrimEl() { return document.querySelector(".cart-scrim"); }

  // The markup declares role="dialog" aria-modal="true". That attribute is a
  // promise to a screen reader that focus is contained; without this, Tab
  // walked straight out into the page behind, which is worse than never
  // having claimed it.
  var FOCUSABLE = 'a[href],button:not([disabled]),input:not([disabled]),' +
                  'select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])';

  function trapFocus(e) {
    if (e.key !== "Tab") return;
    var drawer = drawerEl();
    if (!drawer || !document.body.classList.contains("cart-open")) return;
    var items = Array.prototype.filter.call(
      drawer.querySelectorAll(FOCUSABLE),
      function (el) { return el.offsetParent !== null; }
    );
    if (!items.length) return;
    var first = items[0], last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }

  function openDrawer() {
    var drawer = drawerEl(), scrim = scrimEl();
    if (!drawer) return;
    lastFocus = document.activeElement;
    cancelSpring();
    drawer.style.transform = "";          // hand back to CSS
    drawer.classList.remove("is-dragging", "is-springing");
    document.body.classList.add("cart-open");
    drawer.setAttribute("aria-hidden", "false");
    scrim.hidden = false;
    var close = drawer.querySelector(".cart-drawer__close");
    if (close) close.focus();
  }

  function closeDrawer() {
    var drawer = drawerEl(), scrim = scrimEl();
    if (!drawer) return;
    cancelSpring();
    drawer.style.transform = "";
    drawer.classList.remove("is-dragging", "is-springing");
    document.body.classList.remove("cart-open");
    drawer.setAttribute("aria-hidden", "true");
    // Kept out of the a11y tree once it has finished fading, not the instant
    // the class flips — otherwise the scrim vanishes before the sheet leaves.
    window.setTimeout(function () {
      if (!document.body.classList.contains("cart-open")) scrim.hidden = true;
    }, reduced ? 0 : 400);
    if (lastFocus) lastFocus.focus();
  }

  // ------------------------------------------------- drag to dismiss --
  //
  // The only gesture on this site, and the only motion here that is not the
  // mark's one-shot draw. It is a response to input, not decoration — the
  // brand guide bans things that move on their own, not things that answer
  // the user.
  //
  // A CSS transition cannot be grabbed mid-flight, so once a finger lands the
  // sheet is driven frame by frame and the transition is suspended by class.

  var spring = null;

  function cancelSpring() {
    if (spring) { cancelAnimationFrame(spring); spring = null; }
    var d = drawerEl();
    if (d) d.classList.remove("is-springing");
  }

  // Apple's projection from Designing Fluid Interfaces — exponential decay,
  // NOT the textbook v^2/(2a). Answers "where would this come to rest if
  // released now", so a short fast flick still throws the sheet away.
  function project(velocity, decelerationRate) {
    var d = decelerationRate || 0.998;
    return (velocity / 1000) * d / (1 - d);
  }

  // Critically-damped-ish spring, integrated per frame. bounce 0.8 / response
  // 0.3 are the drawer values from the fluid-interfaces table.
  function springTo(from, to, velocity, onFrame, onDone) {
    cancelSpring();
    var drawer = drawerEl();
    if (!drawer) return;
    if (reduced) { onFrame(to); onDone && onDone(); return; }

    drawer.classList.add("is-springing");
    var stiffness = 420, damping = 34, mass = 1;
    var x = from, v = velocity, last = null;

    function step(now) {
      if (last === null) last = now;
      var dt = Math.min((now - last) / 1000, 1 / 30);   // clamp: a backgrounded
      last = now;                                       // tab must not explode
      var force = -stiffness * (x - to);
      var damper = -damping * v;
      v += (force + damper) / mass * dt;
      x += v * dt;
      if (Math.abs(x - to) < 0.4 && Math.abs(v) < 12) {
        onFrame(to);
        drawer.classList.remove("is-springing");
        spring = null;
        onDone && onDone();
        return;
      }
      onFrame(x);
      spring = requestAnimationFrame(step);
    }
    spring = requestAnimationFrame(step);
  }

  function enableDrag() {
    var drawer = drawerEl();
    if (!drawer || !window.PointerEvent) return;

    var dragging = false, decided = false;
    var startX = 0, startY = 0, x = 0, width = 0;
    var samples = [];                       // recent {t, x} for release velocity

    function paint(px) {
      drawer.style.transform = "translateX(" + px + "px)";
      // The scrim tracks the sheet, so the room behind brightens as it leaves.
      var s = scrimEl();
      if (s) s.style.opacity = String(Math.max(0, 1 - px / width));
    }

    function release() {
      var s = scrimEl();
      if (s) s.style.opacity = "";
      drawer.style.transform = "";
    }

    drawer.addEventListener("pointerdown", function (e) {
      if (!document.body.classList.contains("cart-open")) return;
      // Never steal the press from a control inside the drawer.
      if (e.target.closest("button, a, input, select, textarea")) return;
      if (e.pointerType === "mouse" && e.button !== 0) return;
      cancelSpring();
      dragging = true; decided = false;
      startX = e.clientX; startY = e.clientY;
      width = drawer.getBoundingClientRect().width;
      x = 0;
      samples = [{ t: performance.now(), x: 0 }];
    });

    drawer.addEventListener("pointermove", function (e) {
      if (!dragging) return;
      var dx = e.clientX - startX;
      var dy = e.clientY - startY;

      // ~10px hysteresis, and the axis has to be genuinely horizontal — a
      // vertical scroll inside the drawer must not be read as a dismiss.
      if (!decided) {
        if (Math.abs(dx) < 10 && Math.abs(dy) < 10) return;
        if (Math.abs(dy) > Math.abs(dx)) { dragging = false; return; }
        decided = true;
        // Capture keeps tracking alive when the pointer leaves the sheet.
        // It can throw if the pointer is already gone; a throw here would
        // strand the drag mid-commit, so it must not be fatal.
        try { drawer.setPointerCapture(e.pointerId); } catch (err) {}
        drawer.classList.add("is-dragging");
      }

      // Rightward tracks 1:1. Leftward is past the boundary, so it resists
      // progressively instead of stopping dead.
      x = dx >= 0 ? dx : -(Math.abs(dx) * width * 0.55) / (width + 0.55 * Math.abs(dx));
      samples.push({ t: performance.now(), x: x });
      if (samples.length > 6) samples.shift();
      paint(x);
    });

    function finish(e) {
      if (!dragging) return;
      dragging = false;
      if (!decided) return;
      decided = false;
      drawer.classList.remove("is-dragging");
      try { drawer.releasePointerCapture(e.pointerId); } catch (err) {}

      // Velocity from the recent samples, not the single last event.
      var a = samples[0], b = samples[samples.length - 1];
      var dt = (b.t - a.t) / 1000;
      var velocity = dt > 0.004 ? (b.x - a.x) / dt : 0;
      // A near-zero dt divides into an absurd velocity, which the spring then
      // integrates into a several-thousand-pixel overshoot before recovering.
      // Real pointer events carry real timestamps so this is defensive, but a
      // numeric simulation of the release path produced 9334px of overshoot
      // from a degenerate sample, and the clamp costs nothing.
      velocity = Math.max(-3000, Math.min(3000, velocity));

      // Decide on where it is HEADED, and on the sign of the velocity —
      // not on where the finger happened to stop.
      var projected = x + project(velocity);
      var dismiss = projected > width / 2 || velocity > 400;

      if (dismiss) {
        springTo(x, width, velocity, paint, function () {
          release();
          closeDrawer();
        });
      } else {
        springTo(x, 0, velocity, paint, release);
      }
    }

    drawer.addEventListener("pointerup", finish);
    drawer.addEventListener("pointercancel", finish);
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
      trapFocus(e);
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
    enableDrag();
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
