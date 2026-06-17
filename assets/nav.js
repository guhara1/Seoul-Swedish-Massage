/* ========================================
   간다GO — Nav & TOC Script
   ======================================== */

(function () {
  'use strict';

  /* ----------------------------------------
     Hamburger Menu Toggle
     ---------------------------------------- */
  const hamburger = document.querySelector('.hamburger');
  const navMenu = document.querySelector('.nav-menu');

  if (hamburger && navMenu) {
    hamburger.addEventListener('click', function () {
      const isOpen = navMenu.classList.toggle('open');
      hamburger.classList.toggle('open', isOpen);
      hamburger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });

    // Close on outside click
    document.addEventListener('click', function (e) {
      if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
        navMenu.classList.remove('open');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      }
    });

    // Close on nav link click (mobile)
    navMenu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        navMenu.classList.remove('open');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        document.body.style.overflow = '';
      });
    });
  }

  /* ----------------------------------------
     TOC Active Highlight on Scroll
     ---------------------------------------- */
  const toc = document.querySelector('.page-toc');
  if (!toc) return;

  const tocLinks = Array.from(toc.querySelectorAll('a[href^="#"]'));
  if (tocLinks.length === 0) return;

  const sectionIds = tocLinks.map(function (a) {
    return a.getAttribute('href').replace('#', '');
  });

  const sections = sectionIds
    .map(function (id) { return document.getElementById(id); })
    .filter(Boolean);

  if (sections.length === 0) return;

  function setActive(id) {
    tocLinks.forEach(function (a) {
      a.classList.remove('active');
      if (a.getAttribute('href') === '#' + id) {
        a.classList.add('active');
      }
    });
  }

  // IntersectionObserver: mark as active when section enters viewport
  const observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          setActive(entry.target.id);
        }
      });
    },
    {
      rootMargin: '-80px 0px -60% 0px',
      threshold: 0,
    }
  );

  sections.forEach(function (section) {
    observer.observe(section);
  });

  // Fallback: scroll-based for older browsers
  if (!('IntersectionObserver' in window)) {
    var navHeight = parseInt(
      getComputedStyle(document.documentElement).getPropertyValue('--nav-height') || '64'
    );
    document.addEventListener('scroll', function () {
      var scrollY = window.scrollY + navHeight + 40;
      var current = sections[0].id;
      sections.forEach(function (section) {
        if (section.offsetTop <= scrollY) {
          current = section.id;
        }
      });
      setActive(current);
    }, { passive: true });
  }
})();
