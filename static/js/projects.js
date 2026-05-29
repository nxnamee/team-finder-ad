(function(){
  document.addEventListener("DOMContentLoaded", function() {
    var doneBtn = document.getElementById("close-listing-btn");
    if (doneBtn) {
      doneBtn.addEventListener("click", async function(e) {
        e.preventDefault();
        var pid = doneBtn.dataset.id;
        if (!pid) return;
        try {
          var resp = await fetch('/api/close/' + pid + '/', {
            method: "POST",
            headers: {
              "X-CSRFToken": window.getCookie ? window.getCookie("csrftoken") : "",
              "Content-Type": "application/json"
            },
            body: "{}"
          });
          var data = await resp.json();
          if (data.status === "closed") {
            var badge = document.querySelector(".pf-badge-dark");
            if (badge) badge.textContent = "Closed";
            doneBtn.remove();
            if (window.toast) window.toast("Project closed", { type: 'info' });
          } else {
            if (window.toast) window.toast("Failed to close", { type: 'error' });
          }
        } catch(err) {
          console.error("close error:", err);
          if (window.toast) window.toast("Network error", { type: 'error' });
        }
      });
    }

    var joinBtn = document.getElementById("join-btn");
    var roster = document.getElementById("roster-list");
    var counter = document.getElementById("roster-count");
    if (joinBtn && roster && counter) {
      var uid = joinBtn.dataset.userId || null;
      var pid = joinBtn.dataset.project;
      var uname = joinBtn.dataset.userName || "";
      var upic = joinBtn.dataset.userAvatar || "";

      joinBtn.addEventListener("click", async function(e) {
        e.preventDefault();
        if (!pid) return;
        try {
          var resp = await fetch('/api/toggle-join/' + pid + '/', {
            method: "POST",
            headers: {
              "X-CSRFToken": window.getCookie ? window.getCookie("csrftoken") : "",
              "Content-Type": "application/json"
            },
            body: "{}"
          });
          var data = await resp.json();
          if (data.joined === true) {
            joinBtn.textContent = "Leave";
            var empty = document.getElementById("roster-empty");
            if (empty) empty.remove();

            var link = document.createElement("a");
            link.href = "/profile/" + uid + "/";
            link.id = "member-" + uid;
            link.innerHTML = '<div class="pf-roster-item"><img src="' + upic + '" alt="" class="pf-avatar"><div class="pf-team-info"><span class="pf-team-name">' + uname + '</span><span class="pf-team-role">Member</span></div></div>';
            roster.appendChild(link);
            counter.textContent = parseInt(counter.textContent) + 1;
          } else if (data.joined === false) {
            joinBtn.textContent = "Join";
            var el = document.getElementById("member-" + uid);
            if (el) el.remove();
            var n = parseInt(counter.textContent) - 1;
            counter.textContent = n;
            if (n === 0) {
              var p = document.createElement("p");
              p.id = "roster-empty";
              p.textContent = "No members yet";
              roster.appendChild(p);
            }
          } else {
            if (data.error) {
              if (window.toast) window.toast(data.error, { type: 'error' });
            } else {
              if (window.toast) window.toast("Request failed", { type: 'error' });
            }
          }
        } catch(err) {
          console.error("join error:", err);
          if (window.toast) window.toast("Network error", { type: 'error' });
        }
      });
    }
  });
})();
