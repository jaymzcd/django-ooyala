# django-ooyala

## Introduction

This library allows you to interact and make requests to Ooyala for video data.
Once installed and linked into a django site you can cache your video data and make
use of videos within ooayla in other models. 

### Installation (on django)

Add "ooyala" to your settings.py and your ooyala API keys thus:

    OOYALA = {
        'API_KEYS' : {
            'PARTNER_CODE' : 'partner_code_here',
            'SECRET_CODE' : 'secret_code_here',
        }
    }

The templates within *ooyala/templates/ooyala* will use the *ooyala_base.html* file
but you can override this by adding a 'BASE_TEMPLATE' key to the OOYALA settings
variable, eg:

    OOYALA.update('BASE_TEMPLATE', 'videos/custom_ooyala.html')

The admin_views aren't needed, I use those just to do some debugging as the code
is developed. For the client side urls (detail/index/search) add in the client_urls.
To hook them in use the following in your urlconf.

        (r'^videos/', include('ooyala.client_urls', namespace='video')),
        (r'^admin/ooyala/', include('ooyala.urls', namespace='ooyala')),

Note that (for now) the client urls are namespaced to *video* whilst the admin
ones use *ooyala*.

### Usage outside of models

You're welcome to use the library file without having to use django models - the requests
return the full xml from ooyala so if you're happy to work with this you can
avoid having to use django.

    from ooyala.library import OoyalaQuery
    req = OoyalaQuery(page_id=500)
    ooyala_response = req.process()

    print ooyala_response
    print req.url

    if type(ooyala_response)!=str:
        items = ooyala_response.getElementsByTagName('item')
        print ooyala_response.toprettyxml()

When using the code within django you'll be able to run the management commands
as cron jobs and cache all your content within linkable django models.