
misc notes
----------

influx table query: `SELECT last(value), max(value), min(value) FROM "magrathea"."autogen"."temperature" where time > now()-1d GROUP BY "name"`

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
    * clock
        * render bug on raspbian - chromium
    * server status
        * 0 ms ping != None ping !!!!
* move more than on widget simultaneously
    * select them somehow
* autohide controlbar trigger icon
* export / import widget settings
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
* themes
    * proper night mode
    * dark mode
        * the white widget bg not good
    * dashboard wide widget bg css?
* move dashboard id from localstorage to url
* light theme
* localization
    * labels
    * moment
    * dashboard settings?
