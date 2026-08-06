(() => {
  const initializeHomeSearch = () => {
    document.querySelectorAll("[data-home-search]").forEach((form) => {
      if (form.dataset.searchInitialized === "true") {
        return;
      }

      form.dataset.searchInitialized = "true";

      form.addEventListener("submit", (event) => {
        event.preventDefault();

        const homeInput = form.querySelector('input[type="search"]');
        const nativeToggle = document.querySelector('[data-md-toggle="search"]');
        const nativeInput = document.querySelector(".md-search__input");
        const query = homeInput ? homeInput.value.trim() : "";

        if (!nativeToggle || !nativeInput) {
          return;
        }

        nativeToggle.checked = true;
        nativeToggle.dispatchEvent(new Event("change", { bubbles: true }));

        nativeInput.value = query;
        nativeInput.dispatchEvent(new Event("input", { bubbles: true }));
        nativeInput.dispatchEvent(new Event("change", { bubbles: true }));

        window.setTimeout(() => {
          nativeInput.focus();
          const end = nativeInput.value.length;
          if (typeof nativeInput.setSelectionRange === "function") {
            nativeInput.setSelectionRange(end, end);
          }
        }, 60);
      });
    });
  };

  if (typeof document$ !== "undefined") {
    document$.subscribe(initializeHomeSearch);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeHomeSearch);
  } else {
    initializeHomeSearch();
  }
})();
