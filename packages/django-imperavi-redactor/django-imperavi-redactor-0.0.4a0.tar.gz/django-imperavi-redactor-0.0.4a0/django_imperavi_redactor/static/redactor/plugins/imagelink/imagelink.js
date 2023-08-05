(function ($R) {
    $R.add('plugin', 'imagelink', {
        reImageUrl: /(https?:\/\/)?([da-z.-]+).([a-z.]{2,6})([/w.-=?]*)*\/?/,
        translations: {
            en: {
                "imagelink": "Image Link",
                "imagelink-html-code": "Image Link"
            }
        },
        modals: {
            'imagelink':
                '<form action=""> \
                    <div class="form-item"> \
                        <label for="modal-imagelink-input">## imagelink-html-code ##</label> \
                        <input id="modal-imagelink-input" type="text" name="imagelink" ></input> \
                    </div> \
                </form>'
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
            imagelink: {
                opened: function($modal, $form)
                {
                    $form.getField('imagelink').focus();
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

    		if (data.imagelink.trim() === '')
    		{
        	    return;
    		}

    		// inserting
    		if (data.imagelink.match(this.reImageUrl)){
                this.insertion.insertHtml('<img src="' + data.imagelink + '">');
            }
		},
        // public
        start: function()
        {
            var obj = {
                title: this.lang.get('imagelink'),
                api: 'plugin.imagelink.open',
                observe: 'imagelink'
            };

            this.toolbar.addButton('imagelink', obj);
        },
        open: function()
		{
            var options = {
                title: this.lang.get('imagelink'),
                width: '600px',
                name: 'imagelink',
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
