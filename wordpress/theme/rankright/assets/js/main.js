/* RankRight Media — progressive enhancement only. The site works fully without JS. */
(function () {
  'use strict';
  var doc = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Reveal-on-scroll: mark what is already on screen first so nothing flashes.
  var reveals = Array.prototype.slice.call(document.querySelectorAll('.reveal'));
  reveals.forEach(function (el) {
    var r = el.getBoundingClientRect();
    if (r.top < window.innerHeight * 0.95) el.classList.add('in');
  });
  doc.classList.remove('no-js');
  doc.classList.add('js');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { if (!el.classList.contains('in')) io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  // Header background on scroll
  var header = document.querySelector('.site-header');
  var onScroll = function () { if (header) header.classList.toggle('scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile navigation
  var toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Services dropdown (click/keyboard; hover handled by CSS on desktop)
  Array.prototype.forEach.call(document.querySelectorAll('.has-menu > button'), function (btn) {
    btn.addEventListener('click', function () {
      var li = btn.parentElement;
      var open = li.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    Array.prototype.forEach.call(document.querySelectorAll('.has-menu.open'), function (li) {
      li.classList.remove('open');
      var b = li.querySelector('button'); if (b) { b.setAttribute('aria-expanded', 'false'); b.focus(); }
    });
    if (document.body.classList.contains('nav-open') && toggle) {
      document.body.classList.remove('nav-open'); toggle.setAttribute('aria-expanded', 'false');
    }
  });
  document.addEventListener('click', function (e) {
    Array.prototype.forEach.call(document.querySelectorAll('.has-menu.open'), function (li) {
      if (!li.contains(e.target) && !document.body.classList.contains('nav-open')) {
        li.classList.remove('open');
        var b = li.querySelector('button'); if (b) b.setAttribute('aria-expanded', 'false');
      }
    });
  });

  // Count-up stats (text content is already correct for crawlers and no-JS users)
  if (!reduce && 'IntersectionObserver' in window) {
    var counters = document.querySelectorAll('[data-count]');
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target, end = parseFloat(el.getAttribute('data-count')), dec = (el.getAttribute('data-count').split('.')[1] || '').length;
        var suffix = el.getAttribute('data-suffix') || '', t0 = null;
        var step = function (ts) {
          if (!t0) t0 = ts;
          var p = Math.min((ts - t0) / 1400, 1), v = end * (1 - Math.pow(1 - p, 3));
          el.textContent = v.toFixed(dec) + suffix;
          if (p < 1) window.requestAnimationFrame(step);
        };
        window.requestAnimationFrame(step);
        co.unobserve(el);
      });
    }, { threshold: 0.6 });
    Array.prototype.forEach.call(counters, function (c) { co.observe(c); });
  }

  // Contact form: preselect a package passed as ?package=slug
  var sel = document.getElementById('f-package');
  if (sel && window.URLSearchParams) {
    var pkg = new URLSearchParams(window.location.search).get('package');
    if (pkg) {
      for (var i = 0; i < sel.options.length; i++) {
        if (sel.options[i].value === pkg) { sel.selectedIndex = i; break; }
      }
    }
  }
  var err = document.getElementById('form-error');
  if (err && window.URLSearchParams && new URLSearchParams(window.location.search).get('sent') === '0') err.hidden = false;
  // Time-trap value for the spam filter (bots submit instantly)
  var ts = document.getElementById('f-ts');
  if (ts) ts.value = String(Math.floor(Date.now() / 1000));
})();
