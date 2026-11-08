/* County Kids of Steel — small site behaviours (no dependencies) */
(function () {
  // Mobile menu
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      document.body.classList.toggle('nav-open', open);
    });
    // On touch/narrow screens a folder link expands its submenu on first tap
    nav.querySelectorAll('.has-sub > a').forEach(function (a) {
      a.addEventListener('click', function (e) {
        if (window.matchMedia('(max-width: 1023px)').matches) {
          e.preventDefault();
          a.parentElement.classList.toggle('expanded');
        }
      });
    });
  }

  // "Fit" headings: scale a single line of text to the width of its block
  function fitText() {
    document.querySelectorAll('.fit').forEach(function (box) {
      var el = box.firstElementChild;
      if (!el) return;
      var width = box.clientWidth;
      if (!width) return;
      el.style.fontSize = '100px';
      el.style.display = 'inline-block';
      el.style.whiteSpace = 'nowrap';
      var textWidth = el.getBoundingClientRect().width;
      el.style.display = '';
      if (textWidth) {
        el.style.fontSize = (100 * width / textWidth * 0.98).toFixed(2) + 'px';
        el.style.lineHeight = '1.2';
      }
    });
  }
  fitText();
  window.addEventListener('resize', fitText);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitText);

  // Background videos keep the playback speed set on the original site
  document.querySelectorAll('video[data-rate]').forEach(function (v) {
    v.playbackRate = parseFloat(v.dataset.rate) || 1;
    v.addEventListener('loadedmetadata', function () {
      v.playbackRate = parseFloat(v.dataset.rate) || 1;
    });
  });
})();
