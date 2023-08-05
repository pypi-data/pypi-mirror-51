jQuery(function () {
  window.initializedEditors = [];
  var $ = $ || jQuery || django.jQuery;

  function initEditor() {
    $('textarea[data-type=imperavi-editor]').each(function () {
      var _id = "#" + $(this).attr('id');
      var options = JSON.parse($(this).attr('data-options'));

      if (!_id.match(/__prefix__/) && !this.closest('.empty-form') && window.initializedEditors.indexOf(_id) === -1) {
        $R(_id, options);
        window.initializedEditors.push(_id);
      }
    });
  }

  initEditor();

  $(".add-row a").click(function () {
    setTimeout(initEditor, 200);
    return true;
  });
});
