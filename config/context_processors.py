from django.conf import settings


def site_tracking_code(request):
    return {
        "UMAMI_WEBSITE_ID": settings.UMAMI_WEBSITE_ID,
    }
