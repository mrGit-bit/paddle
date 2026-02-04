(function () {
  const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
  const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
  const isStandalone = window.navigator.standalone === true;

  if (!isIOS || !isSafari || isStandalone) return;
  if (localStorage.getItem("ios-install-dismissed")) return;

  document.addEventListener("DOMContentLoaded", function () {
    const banner = document.getElementById("ios-install-banner");
    if (banner) banner.classList.remove("d-none");
  });
})();
