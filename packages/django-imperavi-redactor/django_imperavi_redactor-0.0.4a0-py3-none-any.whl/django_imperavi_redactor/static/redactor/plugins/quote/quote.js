var $ = jQuery || django.jQuery;

$("head").append($('<link href="/static/redactor/plugins/quote/quote.css" rel="stylesheet" type="text/css" />'));


(function ($R) {
    $R.add('plugin', 'quote', {
        translations: {
            en: {
                "quote": "Quote",
                "quote-author": "Author",
                "quote-who" : "About the Author",
                "quote-text": "Quote",
            }
        },
        modals: {
            'quote':
                '<form action=""> \
                    <div class="form-item"> \
                        <label for="modal-quote-input">## quote-author ##</label> \
                        <input id="modal-quote-input" type="text" name="quoteauthor" ></input> \
                        <label for="modal-quote-who">## quote-who ##</label> \
                        <input id="modal-quote-who" type="text" name="quotewho" ></input> \
                        <label for="modal-quote-textarea">## quote-text ##</label> \
                        <textarea id="modal-quote-textarea" name="quotetext" ></textarea> \
                    </div> \
                </form>',
        },
        init: function(app)
        {
            this.app = app;
            this.lang = app.lang;
            this.toolbar = app.toolbar;
            this.component = app.component;
            this.insertion = app.insertion;
        },
        onmodal: {
            quote: {
                opened: function($modal, $form)
                {
                    this._setUpload($form);
                },
                insert: function($modal, $form)
                {
                    var data = $form.getData();
                    this._insert(data);
                }
            }
        },
        _insert: function(data)
		{
    		this.app.api('module.modal.close');
    		    const authorName = data.quoteauthor ? `<div class="blockquote__author-name">${ data.quoteauthor }</div>` : '';
    		    const authorWho = data.quotewho ? `<div class="blockquote__author-who">${ data.quotewho }</div>` : '';
    		    const authorStr = data.quoteauthor || data.quotewho ? `<div class="blockquote__author">${authorName}${authorWho}</div>` : '';

            var insertHtml =
                `<blockquote class="blockquote"> \
                    <svg class="blockquote__icon" viewBox="0 0 32 20"><path d="M24.407 14.144h.007a.91.91 0 0 1 .566.191.817.817 0 0 1 .303.49c.387 2.112-1.093 3.696-2.477 4.688a.271.271 0 0 0-.103.165.26.26 0 0 0 .037.189c.036.056.093.099.16.12.066.02.138.017.203-.008 10.504-3.837 8.794-13.24 8.794-13.24a6.818 6.818 0 0 0-1.434-3.835A7.471 7.471 0 0 0 27.026.448a7.934 7.934 0 0 0-4.304-.266 7.624 7.624 0 0 0-3.748 2.012 6.934 6.934 0 0 0-1.953 3.625 6.699 6.699 0 0 0 .488 4.04 7.19 7.19 0 0 0 2.766 3.118 7.833 7.833 0 0 0 4.132 1.167zm-16.9 0h.007a.91.91 0 0 1 .566.191.817.817 0 0 1 .302.49c.388 2.112-1.092 3.696-2.476 4.688a.272.272 0 0 0-.103.165.261.261 0 0 0 .037.189c.036.056.092.099.16.12.066.02.138.017.202-.008 10.505-3.837 8.795-13.24 8.795-13.24a6.819 6.819 0 0 0-1.434-3.836A7.473 7.473 0 0 0 10.126.446 7.935 7.935 0 0 0 5.82.18a7.625 7.625 0 0 0-3.749 2.012A6.935 6.935 0 0 0 .12 5.818a6.7 6.7 0 0 0 .488 4.04 7.192 7.192 0 0 0 2.767 3.12 7.833 7.833 0 0 0 4.132 1.166z" /></svg> \
                    <div class="blockquote__text">${ data.quotetext }</div> \
                    ${ authorStr }
                </blockquote>`;

    		// inserting
    		this.insertion.insertHtml(insertHtml);
		},
        // public
        start: function()
        {
            var obj = {
                title: this.lang.get('quote'),
                api: 'plugin.quote.open',
                observe: 'quote'
            };

            this.toolbar.addButton('quote', obj);
        },
        open: function()
		{
            var options = {
                title: this.lang.get('quote'),
                width: '600px',
                name: 'quote',
                handle: 'insert',
                commands: {
                    insert: { title: this.lang.get('insert') },
                    cancel: { title: this.lang.get('cancel') }
                }
            };

            this.app.api('module.modal.build', options);
		},
        remove: function(node)
        {
            this.component.remove(node);
        },
    });

})(Redactor);
