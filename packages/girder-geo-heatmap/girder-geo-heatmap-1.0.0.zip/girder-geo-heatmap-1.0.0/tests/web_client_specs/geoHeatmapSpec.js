/* globals girderTest, describe, it, waitsFor */

girderTest.addScripts([
  '/static/built/plugins/geo_heatmap/plugin.min.js'
]);

girderTest.startApp();

$(function () {
  describe('Test the geo_heatmap plugin', function () {
    it('create the admin user', function () {
      girderTest.createUser(
        'admin', 'admin@email.com', 'Admin', 'Admin', 'testpassword')();
      waitsFor(function () {
        return $('a.g-nav-link[g-target="admin"]').length > 0;
      }, 'admin console link to load');
    });
  });
});
