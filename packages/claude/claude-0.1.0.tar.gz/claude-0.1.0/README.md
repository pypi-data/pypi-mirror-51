
misc notes
----------

guides in github wiki?

`memcached` package from memcache

influx table query: `SELECT last(value), max(value), min(value) FROM "magrathea"."autogen"."temperature" where time > now()-1d GROUP BY "name"`

generate sri: `openssl dgst -sha384 -binary material-ui.development.js | openssl base64 -A`


TODO
----

* tasks on existsing widgets
    * idokep days
        * show city
    * idokep hours
        * show city
        * show wind info
    * calendar
        * google cal integration
        * holidays (https://calendarific.com/)
    * server status
        * ordering
* new widgets
    * chromecast
    * transmission
    * influx graph
    * network speed
        * need some lib to do with on the router
* proper install guide
* proper dev guide
* widget plugin system
    * guide for it
    * plugins:
        * tvs ep tracker
        * room temperature
* zeroconf
    * host:port info
        * environment set by uwsgi conf
        * app config
* desktop client with electron
* android client with WebView
* night mode
* move dashboard id from localstorage to url
* light theme
* localization
    * labels
    * moment
    * dashboard settings?
