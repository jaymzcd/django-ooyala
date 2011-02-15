
class OoyalaAPI(object):
    # The various api's - these append to the QUERY_URI to make the API request

    BASE_URL = 'http://api.ooyala.com/'

    class BACKLOT(object):
        QUERY = 'query'
        THUMB = 'thumbnails'
        ATTR = 'edit'
        LABEL = 'labels'
        CHANNEL = 'channels'
        URL = 'partner/'

    class INGESTION(object):
        URL = 'partner/ingestion/'
        INGESTION = 'ingestion'

    class ANALYTICS(object):
        URL = ''
        ANALYTICS = 'analytics'

class OoyalaConstants(object):

    # Status choices for the various API calls
    OOYALA_ATTR_STATUS_PAUSED = 'paused'
    OOYALA_ATTR_STATUS_LIVE = 'live'
    OOYALA_ATTR_STATUS_DELETED = 'deleted'
    OOYALA_ATTR_STATS_LIFETIME = 'lifetime'
    OOYALA_QUERY_STATUS_DELETED = 'deleted'
    OOYALA_QUERY_STATUS_LIVE = 'live'
    OOYALA_QUERY_STATUS_ERROR = 'error'
    OOYALA_QUERY_STATUS_FILEMISSING = 'filemissing'
    OOYALA_QUERY_STATUS_UPLOADING = 'uploading'
    OOYALA_QUERY_STATUS_PAUSED = 'paused'
    OOYALA_QUERY_STATUS_UPLOADED = 'uploaded'
    OOYALA_QUERY_STATUS_NA = 'na',
    OOYALA_QUERY_STATUS_CREMOVED = 'cremoved'
    OOYALA_QUERY_STATUS_API_UPLOADING = 'auploading'
    OOYALA_QUERY_STATUS_API_UPLOADED = 'auploaded'
    OOYALA_QUERY_STATUS_DUPLICATE = 'duplicate'
    OOYALA_QUERY_STATUS_PENDING = 'pending'
    OOYALA_QUERY_STATUS_PROCESSING = 'processing'

    # Field options for the Query API
    OOYALA_FIELDS_LABELS = 'labels'
    OOYALA_FIELDS_METADATA = 'metadata'
    OOYALA_FIELDS_RATINGS = 'ratings'

    # Query API limit
    OOYALA_QUERY_LIMIT = 1000 # default is 500 [Actually, this is a hard maximum]

    # Mode options for the Label Management API
    class LABEL_MODE(object):
        LIST = 'listLabels'
        CREATE = 'createLabels'
        DELETE = 'deleteLabels'
        ASSIGN = 'assignLabels'
        UNASSIGN = 'unassignLabels'
        RENAME = 'renameLabels'
        CLEAR = 'clearLabels'

    # Mode options for the Channel API
    class CHANNEL_MODE(object):
        LIST = 'list'
        ASSIGN = 'assign'
        CREATE = 'create'

    # Variables for statistics requsts for Query API
    class STATS(object):
        DAY = '1d'
        TWO_DAYS = '2d'
        THREE_DAYS = '3d'
        FOUR_DAYS = '4d'
        WORKWEEK = '5d'
        WEEK = '7d'
        FORTNIGHT = '14d'
        FOUR_WEEKS = '28d'
        TWENTYNINE_DAYS = '29d'
        THIRTY_DAYS = '30d'
        THIRTYONE_DAYS = '31d'

    class GRANULATIRY(object):
        DAY = 'day'
        WEEK = 'week'
        MONTH = 'month'
        TOTAL = 'total'

    class ANALYTIC_METHODS(object):
        TOTALS = 'account.totals' # for the entire account
        GEO_TOTALS = 'account.geoTotals'
        ACCOUNT_VIDEOS  = 'account.videoTotals'
        ACCOUNT_DOMAIN = 'account.domainTotals'
        VIDEO = 'video.totals' # for specific embed code (required)
        VIDEO_DOMAIN = 'video.domainTotals'
        VIDEO_BEHAVIORAL = 'video.behavioral'

    # Ordering variables for Query API
    OOYALA_ORDER_ASC = 'asc'
    OOYALA_ORDER_DESC = 'desc'

    # Joining for query API calls
    OOYALA_QUERY_MODE_OR = 'or'
    OOYALA_QUERY_MODE_AND = 'and'

    # Number of seconds to add to current time for expiry
    DEFAULT_EXPIRE_TIME = 300
