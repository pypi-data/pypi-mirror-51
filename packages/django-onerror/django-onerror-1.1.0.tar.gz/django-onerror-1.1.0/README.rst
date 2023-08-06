==============
django-onerror
==============

Django ``window.onerror`` Report

Installation
============

::

    pip install django-onerror


Urls.py
=======

::

    urlpatterns = [
        url(r'^e/', include('django_onerror.urls', namespace='django_onerror')),
    ]


or::

    urlpatterns = [
        url(r'^report', err_views.err_report, name='err_report'),
    ]


Settings.py
===========

::

    INSTALLED_APPS = (
        ...
        'django_onerror',
        ...
    )


FrontEnd
========

::

    <script>
        window.onerror = function(errorMessage, scriptURI, lineNo, columnNo, error) {
            if (['Uncaught ReferenceError: WeixinJSBridge is not defined', 'ResizeObserver loop limit exceeded'].indexOf(errorMessage) >= 0) {
                return
            }
            // 构建错误对象
            var errorObj = {
                href: window.location.href,
                ua: window.navigator.userAgent,
                lineNo: lineNo || 0,
                columnNo: columnNo || 0,
                scriptURI: scriptURI || null,
                errorMessage: errorMessage || null,
                stack: error && error.stack ? error.stack : null
            };
            // 构建Http请求
            if (XMLHttpRequest) {
                var xhr = new XMLHttpRequest();
                xhr.open('post', '/e/report', true);
                xhr.setRequestHeader('Content-Type', 'application/json'); // 设置请求头
                xhr.send(JSON.stringify(errorObj)); // 发送参数
            }
        }
    </script>

