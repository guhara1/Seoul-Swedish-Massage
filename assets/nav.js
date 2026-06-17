(function () {
  'use strict';

  // Hamburger toggle
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      const open = nav.classList.toggle('open');
      toggle.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', open);
    });
    // Sub-menu touch toggle on mobile
    document.querySelectorAll('.nav-item.has-sub > a').forEach(function (link) {
      link.addEventListener('click', function (e) {
        if (window.innerWidth <= 768) {
          e.preventDefault();
          const item = link.closest('.nav-item');
          item.classList.toggle('sub-open');
          const sub = item.querySelector('.sub-menu');
          if (sub) sub.style.display = item.classList.contains('sub-open') ? 'block' : '';
        }
      });
    });
  }

  // TOC active on scroll
  const tocLinks = document.querySelectorAll('.page-toc a');
  if (tocLinks.length) {
    const sections = Array.from(tocLinks).map(function (a) {
      return document.querySelector(a.getAttribute('href'));
    }).filter(Boolean);
    const onScroll = function () {
      let current = sections[0];
      sections.forEach(function (sec) {
        if (window.scrollY >= sec.offsetTop - 120) current = sec;
      });
      tocLinks.forEach(function (a) {
        a.classList.toggle('active', a.getAttribute('href') === '#' + current.id);
      });
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }
})();
