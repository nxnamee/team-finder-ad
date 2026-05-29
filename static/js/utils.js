(function(){
  if (!window.getCookie) {
    window.getCookie = function(name) {
      var val = null;
      if (document.cookie && document.cookie !== "") {
        var parts = document.cookie.split(";");
        for (var i = 0; i < parts.length; i++) {
          var c = parts[i].trim();
          if (c.indexOf(name + "=") === 0) {
            val = decodeURIComponent(c.substring(name.length + 1));
            break;
          }
        }
      }
      return val;
    }
  }

  if (!window.toast) {
    function ensureBox() {
      var el = document.getElementById('pf-toast-area');
      if (el) return el;
      el = document.createElement('div');
      el.id = 'pf-toast-area';
      el.style.cssText = 'position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center;gap:8px;z-index:2147483647';
      document.body.appendChild(el);
      return el;
    }

    window.toast = function(msg, opts) {
      opts = opts || {};
      var type = opts.type || 'info';
      var dur = opts.duration || 2200;
      var box = ensureBox();

      var el = document.createElement('div');
      el.textContent = msg;
      el.style.cssText = 'max-width:90vw;background:' + (type === 'error' ? 'rgba(220,38,38,0.95)' : 'rgba(17,17,17,0.92)') + ';color:#fff;padding:12px 16px;border-radius:8px;box-shadow:0 6px 20px rgba(0,0,0,0.25);font-size:14px;line-height:1.35;word-break:break-all;text-align:center;opacity:0;transition:opacity 180ms ease';

      box.appendChild(el);
      requestAnimationFrame(function() { el.style.opacity = '1'; });

      setTimeout(function() {
        el.style.opacity = '0';
        setTimeout(function() { el.remove(); }, 200);
      }, Math.max(1200, dur));
    }
  }
})();
