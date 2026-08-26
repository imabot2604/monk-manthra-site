/* monk manthra — site behaviour
 *
 * There is exactly one piece of motion on this site: the mark draws once,
 * outward, in 1.4 seconds, on load. It never loops. It never pulses.
 * Everything else is a colour or border transition measured in tenths.
 */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function drawMarks() {
    var marks = document.querySelectorAll(".mark[data-draw]");
    Array.prototype.forEach.call(marks, function (mark) {
      if (mark.classList.contains("is-drawn")) return;

      // Measure each arc so the stroke reveals at its true length.
      var rings = mark.querySelectorAll(".ring");
      Array.prototype.forEach.call(rings, function (ring) {
        var len = 0;
        try { len = ring.getTotalLength(); } catch (e) { len = 0; }
        if (len) ring.style.setProperty("--len", len.toFixed(2));
      });

      mark.classList.add("is-drawn");

      // Once drawn, it stays drawn. The keyframes fill forwards and run exactly
      // once, so the final frame simply persists — there is nothing to reset and
      // nothing that could start it a second time. Dropping the attribute is
      // what retires it; clearing the inline styles would strip the very
      // dash values holding the finished arcs on screen.
      window.setTimeout(function () {
        mark.removeAttribute("data-draw");
      }, reduced ? 0 : 1600);
    });
  }

  // Apply the reduction rule automatically: three rings at 96px and up,
  // two rings between 48 and 95, one ring plus the seed at 32 and below.
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

  // The header is only a material while content is actually underneath it.
  // At the top of the page there is nothing to blur, so it stays plain.
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

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    applyReduction();
    floatingHeader();
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
