/* PABCD Initiative docs-site — sidebar nav + client-side search */
(function () {
  "use strict";

  /* ---- sidebar toggle (mobile) ---- */
  var toggle = document.querySelector(".sidebar-toggle");
  var sidebar = document.querySelector(".sidebar");
  var overlay = document.querySelector(".sidebar-overlay");
  if (toggle && sidebar) {
    toggle.addEventListener("click", function () {
      sidebar.classList.toggle("open");
      if (overlay) overlay.classList.toggle("open");
    });
    if (overlay) {
      overlay.addEventListener("click", function () {
        sidebar.classList.remove("open");
        overlay.classList.remove("open");
      });
    }
  }

  /* ---- collapsible nav groups ---- */
  document.querySelectorAll(".nav-group-label").forEach(function (btn) {
    btn.addEventListener("click", function () {
      btn.parentElement.classList.toggle("collapsed");
    });
  });

  /* ---- active page highlight ---- */
  var currentPath = location.pathname.replace(/\/$/, "/index.html");
  document.querySelectorAll(".nav-items a").forEach(function (a) {
    var href = a.getAttribute("href");
    if (!href) return;
    /* normalize: resolve relative href to absolute */
    var link = new URL(href, location.href).pathname;
    if (link === currentPath || currentPath.endsWith("/" + href.replace(/^\.\.\//, "").replace(/^\.\//, ""))) {
      a.classList.add("active");
      /* ensure parent group is expanded */
      var group = a.closest(".nav-group");
      if (group) group.classList.remove("collapsed");
    }
  });

  /* ---- client-side search ---- */
  var searchInput = document.getElementById("docs-search");
  var searchResults = document.getElementById("search-results");
  if (!searchInput || !searchResults) return;

  /* build index from embedded data or fetch */
  var searchIndex = [];
  if (window.DOCS_SEARCH_INDEX) {
    searchIndex = window.DOCS_SEARCH_INDEX;
  }

  searchInput.addEventListener("input", function () {
    var q = this.value.trim().toLowerCase();
    searchResults.innerHTML = "";
    if (q.length < 2) return;

    var matches = searchIndex.filter(function (entry) {
      return entry.title.toLowerCase().indexOf(q) !== -1 ||
             entry.text.toLowerCase().indexOf(q) !== -1;
    }).slice(0, 12);

    if (matches.length === 0) {
      searchResults.innerHTML = '<li class="search-empty">No results</li>';
      return;
    }

    matches.forEach(function (m) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = m.url;
      a.textContent = m.title;
      li.appendChild(a);
      searchResults.appendChild(li);
    });
  });
})();
