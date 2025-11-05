const config = {
  appId: 'club.rankingdepadel.app',
  appName: 'Ranking de Pádel',
  webDir: 'dist',
  bundledWebRuntime: false,
  
  // === PRODUCTION build ===
  // server: {
  //   url: 'https://rankingdepadel.club',
  //   cleartext: false,
  //   allowNavigation: ['rankingdepadel.club', 'www.rankingdepadel.club'],
  // },

  // === STAGING build ===
  server: {
    url: 'https://staging.rankingdepadel.club/mobiletest/',
    cleartext: false,
    allowNavigation: ['staging.rankingdepadel.club'],

  },
};

export default config;
