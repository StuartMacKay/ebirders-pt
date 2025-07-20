from django.conf import settings


def site_tracking_code(request):
    return {
        "UMAMI_WEBSITE_ID": settings.UMAMI_WEBSITE_ID,
    }

def cache_ttls(request):
    return {
        "CACHE_TTL_SHORT": settings.CACHE_TTL_SHORT,
        "CACHE_TTL_MEDIUM": settings.CACHE_TTL_MEDIUM,
        "CACHE_TTL_LONG": settings.CACHE_TTL_LONG,
    }
