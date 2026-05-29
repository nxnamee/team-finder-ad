document.addEventListener("click", function(e) {
  var btn = e.target.closest(".pf-share-btn");
  if (!btn) return;
  e.preventDefault();

  var url = btn.dataset.url
    ? window.location.origin + btn.dataset.url
    : window.location.href;

  navigator.clipboard.writeText(url).then(function() {
    if (window.toast) window.toast("Copied: " + url);
    else alert("Copied: " + url);
  }).catch(function(err) {
    console.error("copy failed:", err);
    fallback(url);
  });
});

function fallback(text) {
  try {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.top = "-1000px";
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    var ok = document.execCommand("copy");
    document.body.removeChild(ta);
    if (!ok) throw new Error("execCommand failed");
    if (window.toast) window.toast("Copied: " + text);
    else alert("Copied: " + text);
  } catch(err) {
    console.error("fallback failed:", err);
    window.prompt("Copy link:", text);
  }
}
