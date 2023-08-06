/* DjangoMultiUploadJS */

(function ($) {
    $(document).ready(function () {
        if (typeof ajaxImageUploadData === 'undefined') {
            return;
        }

        ajaxImageUploadData.forEach(function (item) {
            var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
            var template =
                '<form action="' + item.upload_to + '/"\n' +
                '     class="multi-upload active js-multi-upload"\n' +
                '     data-id="' + item.prefix + '-group">\n' +
                '    <input type="hidden" name="csrfmiddlewaretoken" value="' + csrfToken + '">\n' +
                '    <input type="file" name="file" style="display: none;">\n' +
                '    <div class="multi-upload__progress js-multi-upload-progress">\n' +
                '        <div></div>\n' +
                '        <div></div>\n' +
                '    </div>\n' +
                '    <div class="multi-upload__text js-multi-upload-text">Перетащи изображения!</div>\n' +
                '</form>';
            $('#' + item.prefix + '-group').append(template);
        });

        var $blocks = jQuery('.js-multi-upload');
        $blocks.each(function () {
            var $block = $(this);

            var $text = $('.js-multi-upload-text', $block),
                $progress = $('.js-multi-upload-progress', $block),
                activeText = $text.text(),
                activeClass = 'active',
                disableClass = 'disabled',
                hoverClass = 'hover';

            var images;

            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            var csrftoken = getCookie('csrftoken');

            function csrfSafeMethod(method) {
                // these HTTP methods do not require CSRF protection
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }

            function sameOrigin(url) {
                // test that a given url is a same-origin URL
                // url could be relative or scheme relative or absolute
                var host = document.location.host; // host + port
                var protocol = document.location.protocol;
                var sr_origin = '//' + host;
                var origin = protocol + sr_origin;
                // Allow absolute or scheme relative URLs to same origin
                return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                    (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                    // or any other URL that isn't scheme relative or absolute i.e relative.
                    !(/^(\/\/|http:|https:).*/.test(url));
            }

            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                        // Only send the token to relative URLs i.e. locally.
                        xhr.setRequestHeader("X-CSRFToken",
                            $('input[name="csrfmiddlewaretoken"]').val());
                    }
                }
            });

            initForm();

            $block.on('drag dragstart dragend dragover dragenter dragleave drop', function (e) {
                e.preventDefault();
                e.stopPropagation();
            })
                .on('dragover dragenter', function () {
                    $(this).addClass(hoverClass);
                })
                .on('dragleave dragend drop', function () {
                    $block.removeClass(hoverClass);
                })
                .on('drop', function (e) {
                    if (!$block.hasClass(disableClass)) {
                        var $input = $block.find('input[type="file"]');
                        images = e.originalEvent.dataTransfer.files;
                        jQuery.each(images, function (i, item) {
                            $block.find('input[type="file"]').prop('file', item);
                            var data = new FormData($block.get(0));
                            data.append($input.attr('name'), item);
                            $.ajax({
                                method: 'POST',
                                url: $block.attr('action'),
                                data: data,
                                dataType: 'json',
                                cache: false,
                                contentType: false,
                                processData: false,
                                xhr: function () {
                                    var xhr = new window.XMLHttpRequest();
                                    xhr.upload.addEventListener("progress", function (evt) {
                                        if (evt.lengthComputable) {
                                            var percentComplete = Math.round(evt.loaded / evt.total * 100);

                                            uploadProgress(percentComplete);
                                        }
                                    }, false);
                                    xhr.addEventListener("progress", function (evt) {
                                        if (evt.lengthComputable) {
                                            var percentComplete = Math.round(evt.loaded / evt.total * 100);

                                            uploadProgress(percentComplete);
                                        }
                                    }, false);
                                    return xhr;
                                },
                                beforeSend: function (xhr) {
                                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                                },
                                complete: function () {
                                    makeFormActive(activeText);
                                },
                                success: function (data) {
                                    addImagesToList(data);
                                }
                            });
                        });
                    }
                });

            function uploadProgress(precents) {
                $block.removeClass(activeClass);
                $block.addClass(disableClass);

                $progress.children().eq(0).text(precents + '%');
                $progress.children().eq(1).text(precents + '%');
                $progress.children().eq(1).css({
                    height: precents + '%'
                });
                $text.text('Терпение, мой друг');
            }

            function makeFormActive(text) {
                $block.removeClass(disableClass);
                $block.addClass(activeClass);
                $text.text(text);
            }

            function addImagesToList(data) {
                var $inline = $block.closest('.inline-group');

                $('.add-row a', $inline).trigger('click');

                var link = $('.file-link[href=""]', $inline).eq(0);

                if (link.attr('href') === '') {
                    link.attr('href', data.url);
                    link.children('img').attr('src', data.url);
                }

                var input = link.siblings('input.file-path');

                input.val(data.filename);

                var parent = link.parent('.form-active');

                parent.removeClass('form-active');
                parent.addClass('img-active');
            }

            function initForm() {
                $block.addClass(activeClass);
            }
        });
    });
})(django.jQuery);
