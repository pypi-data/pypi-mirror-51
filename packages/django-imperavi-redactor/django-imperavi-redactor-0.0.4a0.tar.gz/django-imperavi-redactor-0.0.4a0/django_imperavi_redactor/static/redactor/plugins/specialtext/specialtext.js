var $ = jQuery || django.jQuery;

$("head").append($('<link href="/static/redactor/plugins/specialtext/specialtext.css" rel="stylesheet" type="text/css" />'));

(function ($R) {
  $R.add('plugin', 'specialtext', {
    translations: {
      en: {
        "special-text": "Special Text",
      }
    },
    init: function (app) {
      this.app = app;
      this.toolbar = app.toolbar;
      this.lang = app.lang;
      this.selection = app.selection;
      this.component = app.component;
      this.insertion = app.insertion;
      this.caret = app.caret;
    },

    start: function () {
      const buttonData = {
        title: this.lang.get('special-text'),
        api: 'plugin.specialtext.mark',
      };

      this.toolbar.addButton('special-text-button', buttonData);
    },

    remove: function (node) {
      this.component.remove(node);
    },

    mark: function () {
      const blocks = this.selection.getBlocks({first: true});

      if (blocks && blocks.length) {
        let resultHtml = blocks.map(item => item.outerHTML).join('');

        this.insertion.insertHtml(`<blockquote class="special-text">${ resultHtml }</blockquote>`)
      } else {
        const insertedBlock = this.insertion.insertNode(`<blockquote class="special-text"></blockquote>`);
        this.caret.setStart(insertedBlock);
      }
    },
  });
})(Redactor);
