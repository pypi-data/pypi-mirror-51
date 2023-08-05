var $ = jQuery || django.jQuery;

$("head").append($('<script src="https://api.glvrd.ru/v1/glvrd.js"></script>'));
$("head").append($('<link href="https://api.glvrd.ru/v1/glvrd.css" rel="stylesheet" type="text/css" />'));
$("head").append($('<link href="/static/redactor/plugins/glvrdplugin/glvrdplugin.css" rel="stylesheet" type="text/css" />'));


(function ($R) {
    $R.add('plugin', 'glvrdplugin', {
        translations: {
            en: {
                "glvrdplugin": "Glvrd",
            }
        },
        modals: {
            'glvrdplugin':
                '<section id="glvrd-section"> \
                    <div id="glvrd-left"> \
                        Проверяем текст, не переключайтесь... \
                        <br/><br/> \
                        <img src="https://media.giphy.com/media/zZMTVkTeEfeEg/giphy.gif" /> \
                    </div> \
                    <div id="glvrd-right"> \
                        <div id="glvrd-right-inner"></div> \
                    </div> \
                </section>'
        },
        init: function (app) {
            this.app = app;
            this.lang = app.lang;
            this.toolbar = app.toolbar;
            this.component = app.component;
            this.insertion = app.insertion;
            this.text = '';
        },
        onmodal: {
            glvrdplugin: {
                opened: function ($modal, $form) {
                    var self = this;

                    if (self.app.editor.$editor != undefined) {
                        self.text = self.app.editor.$editor.nodes[0].innerHTML.replace(
                            /<img[^>]*>/g, ''
                        ).replace(
                            /<blockquote.*<\/blockquote>/g, ''
                        ).replace(
                            /<iframe.*<\/iframe>/g, ''
                        );
                    }

                    $('.redactor-modal').removeAttr('style');
                    $('.redactor-modal').css({
                        maxWidth: '1200px',
                        marginTop: '117.5px !important',
                    });

                    glvrd.getStatus( function(result) {
                        if( result.status != "ok" ) {
                            self.error(result);
                        } else {
                            glvrd.proofread(self.text, function (result) {
                                self.proofread(result, self);
                            });
                        }
                    });

                }
            }
        },
        error: function (result) {
            $("#glvrd-left").text("Не могу проверить текст. Ошибка: " + result.message)
        },
        proofread: function (result, self) {
            var data = self.text;

            if( result.status != "ok" ) {
                this.error(result)
            } else {
                var right = $("<div><p>Оценка Главреда:</p></div>").append(
                    $("<h2></h2>").text(result.score + ' из 10')
                );

                right.append('<div id="glvrd-info"></div>');

                $("#glvrd-right-inner").append(right);

                // Отступ относительно оригинала
                var offset = 0

                for ( var index in result.fragments ) {

                    var fragment = result.fragments[index];

                    // Вытаскиваем нужный нам кусок
                    var inner = data.substr(fragment.start + offset, fragment.end - fragment.start);
                    // Оборачиваем спаном
                    var repl = $("<span class='glvrd-underline' data-glvrd-item='true' data-glvrd-fragment='"+ index +"'>" + inner + "</span>");

                    // Вставляем на законное место
                    data = data.substr(0, fragment.start + offset) + repl[0].outerHTML + data.substr(fragment.end + offset, data.length);

                    // Пересчитываем отступ:
                    // Длина обертки минус длина оригинала
                    offset += repl[0].outerHTML.length - inner.length
                }

                // Вставляем на законное место
                $("#glvrd-left").html(data);

                // Накидываем события
                $("#glvrd-left span[data-glvrd-item='true']").click(function() {
                    // Выбираем нужный фрагмент и отображаем справа
                    self.setFragment(result.fragments[+$(this).attr('data-glvrd-fragment')]);

                    // Убираем active у всех
                    $("#glvrd-left span.glvrd-underline-active").removeClass('glvrd-underline-active');

                    // Вешаем active на выбранный
                    $(this).addClass('glvrd-underline-active')
                });
            }
        },
        setFragment: function (fragment) {
            var info = $("#glvrd-info");

            info.html('');
            info.append($("<h1></h1>").html(fragment.hint.name));
            info.append($("<p></p>").html(fragment.hint.description))
        },
        // public
        start: function()
        {
            var obj = {
                title: this.lang.get('glvrdplugin'),
                api: 'plugin.glvrdplugin.open',
                observe: 'glvrdplugin'
            };

            this.toolbar.addButton('glvrdplugin', obj);
        },
        open: function()
		{
            var options = {
                title: this.lang.get('glvrdplugin'),
                name: 'glvrdplugin',
                handle: 'insert',
                commands: {
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
