(function(){
  document.addEventListener("DOMContentLoaded", function() {
    var btn = document.querySelector('.pf-user-menu');
    var panel = document.getElementById('userSidebar');
    var shade = document.getElementById('sidebarOverlay');
    if (!btn || !panel || !shade) return;

    function open() { panel.classList.add('show'); shade.classList.add('show'); }
    function close() { panel.classList.remove('show'); shade.classList.remove('show'); }

    btn.addEventListener('click', function(e) {
      e.stopPropagation(); open();
    });

    document.addEventListener('click', function(e) {
      if (!panel.contains(e.target) && !btn.contains(e.target) && panel.classList.contains('show')) {
        close();
      }
    });
  });
})();
