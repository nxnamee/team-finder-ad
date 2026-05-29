(function(){
  document.addEventListener("DOMContentLoaded", function() {
    var box = document.getElementById("skills-box");
    if (!box) return;

    var pid = box.dataset.projectId;
    var addBtn = document.getElementById("skill-add-btn");
    var wrap = document.getElementById("skill-input-wrap");
    var field = document.getElementById("pf-skill-typed");
    var menu = document.getElementById("skill-suggestions");
    if (!addBtn || !wrap || !field || !menu) return;

    var SKILLS = ['Python','JavaScript','TypeScript','React','Vue','Angular','Node.js','Django','Flask','FastAPI','PostgreSQL','MongoDB','Docker','Kubernetes','AWS','GCP','Azure','Git','UI/UX Design','Figma','Product Management','Data Science','Machine Learning','DevOps','Testing'];

    addBtn.addEventListener("click", function() {
      addBtn.classList.add("hidden");
      wrap.classList.remove("hidden");
      field.value = "";
      menu.innerHTML = "";
      menu.classList.add("hidden");
      field.focus();
    });

    var debounce = null;
    field.addEventListener("input", function() {
      var q = field.value.trim().toLowerCase();
      clearTimeout(debounce);
      if (!q) {
        menu.classList.add("hidden");
        menu.innerHTML = "";
        return;
      }
      debounce = setTimeout(function() {
        var matches = SKILLS.filter(function(s) { return s.toLowerCase().indexOf(q) !== -1; });
        menu.innerHTML = "";
        matches.forEach(function(s) {
          var li = document.createElement("li");
          li.textContent = s;
          li.dataset.name = s;
          menu.appendChild(li);
        });
        var exact = matches.some(function(s) { return s.toLowerCase() === q; });
        if (!exact) {
          var fresh = document.createElement("li");
          fresh.textContent = '+' + field.value.trim();
          fresh.dataset.name = field.value.trim();
          fresh.className = "pf-new-skill";
          menu.appendChild(fresh);
        }
        menu.classList.remove("hidden");
      }, 200);
    });

    menu.addEventListener("mousedown", function(e) {
      var li = e.target.closest("li");
      if (!li) return;
      addChip(li.dataset.name);
      hideWrap();
    });

    field.addEventListener("keydown", function(e) {
      if (e.key === "Enter") {
        e.preventDefault();
        var q = field.value.trim();
        if (!q) return;
        var first = menu.querySelector("li");
        if (first) addChip(first.dataset.name);
        else addChip(q);
        hideWrap();
      }
      if (e.key === "Escape") { hideWrap(); }
    });

    field.addEventListener("blur", function() { setTimeout(hideWrap, 120); });

    function hideWrap() {
      wrap.classList.add("hidden");
      menu.classList.add("hidden");
      addBtn.classList.remove("hidden");
    }

    box.addEventListener("click", function(e) {
      if (e.target.classList.contains("pf-skill-del")) {
        var chip = e.target.closest(".pf-skill");
        if (chip) chip.remove();
      }
    });

    function addChip(name) {
      if (!name) return;
      if (box.querySelector('.pf-skill[data-name="' + name.replace(/"/g,'&quot;') + '"]')) return;
      var chip = document.createElement("span");
      chip.className = "pf-skill";
      chip.dataset.name = name;
      chip.innerHTML = name + ' <button type="button" class="pf-skill-del" aria-label="Remove">x</button>';
      box.insertBefore(chip, addBtn);
      var empty = box.querySelector(".skill-empty");
      if (empty) empty.remove();
    }
  });
})();
