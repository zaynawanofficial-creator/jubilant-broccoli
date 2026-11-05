/* SEO Booster: Services mega panel (desktop) and slide-in menu drawer (tablet/phone). No dependencies. */
(function () {
	'use strict';
	var doc = document, root = doc.documentElement;

	/* ---------- Mega panel ---------- */
	var triggers = doc.querySelectorAll('.sb-nav__trigger');
	function closeMega(except) {
		triggers.forEach(function (t) { if (t !== except) { t.setAttribute('aria-expanded', 'false'); t.parentNode.classList.remove('is-open'); } });
	}
	triggers.forEach(function (btn) {
		var item = btn.parentNode, timer;
		btn.addEventListener('click', function () {
			var open = btn.getAttribute('aria-expanded') !== 'true';
			closeMega(btn);
			btn.setAttribute('aria-expanded', String(open));
			item.classList.toggle('is-open', open);
		});
		if (window.matchMedia('(hover: hover)').matches) {
			item.addEventListener('mouseenter', function () { clearTimeout(timer); closeMega(btn); btn.setAttribute('aria-expanded', 'true'); item.classList.add('is-open'); });
			item.addEventListener('mouseleave', function () { timer = setTimeout(function () { btn.setAttribute('aria-expanded', 'false'); item.classList.remove('is-open'); }, 160); });
		}
		item.addEventListener('focusout', function (e) { if (!item.contains(e.relatedTarget)) { btn.setAttribute('aria-expanded', 'false'); item.classList.remove('is-open'); } });
		item.addEventListener('keydown', function (e) { if (e.key === 'Escape' && item.classList.contains('is-open')) { closeMega(); btn.focus(); } });
	});
	doc.addEventListener('click', function (e) { if (!e.target.closest('.has-mega')) { closeMega(); } });

	/* ---------- Drawer ---------- */
	var drawer = doc.getElementById('sb-drawer');
	var burgers = doc.querySelectorAll('.sb-burger');
	if (!drawer || !burgers.length) { return; }
	var lastFocus = null;
	var focusables = 'a[href], button:not([disabled]), input, summary, [tabindex]:not([tabindex="-1"])';

	function openDrawer(btn) {
		lastFocus = btn || doc.activeElement;
		drawer.hidden = false;
		root.classList.add('sb-lock');
		burgers.forEach(function (b) { b.setAttribute('aria-expanded', 'true'); });
		requestAnimationFrame(function () { requestAnimationFrame(function () { drawer.classList.add('is-open'); }); });
		var close = drawer.querySelector('.sb-drawer__close');
		if (close) { setTimeout(function () { close.focus(); }, 60); }
	}
	function closeDrawer() {
		if (drawer.hidden) { return; }
		drawer.classList.remove('is-open');
		root.classList.remove('sb-lock');
		burgers.forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
		var done = function () { drawer.hidden = true; };
		var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
		if (reduce) { done(); } else { setTimeout(done, 260); }
		if (lastFocus && lastFocus.focus) { lastFocus.focus(); }
	}
	burgers.forEach(function (b) { b.addEventListener('click', function () { openDrawer(b); }); });
	drawer.addEventListener('click', function (e) {
		if (e.target.closest('[data-sb-close]')) { closeDrawer(); return; }
		var a = e.target.closest('a[href]');
		if (a && a.getAttribute('href').indexOf('#') !== 0) { closeDrawer(); }
	});
	doc.addEventListener('keydown', function (e) {
		if (drawer.hidden) { return; }
		if (e.key === 'Escape') { closeDrawer(); return; }
		if (e.key !== 'Tab') { return; }
		var list = Array.prototype.filter.call(drawer.querySelectorAll(focusables), function (el) { return el.offsetParent !== null; });
		if (!list.length) { return; }
		var first = list[0], last = list[list.length - 1];
		if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); last.focus(); }
		else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
	});
	/* Close if the window grows to desktop width while open. */
	var mq = window.matchMedia('(min-width: 1024px)');
	var onMq = function () { if (mq.matches) { closeDrawer(); } };
	if (mq.addEventListener) { mq.addEventListener('change', onMq); } else if (mq.addListener) { mq.addListener(onMq); }
})();
