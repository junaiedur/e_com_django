from django.conf import settings

# settings থেকে নিরাপদে পড়া
USE_WEASY = getattr(settings, "USE_WEASY", False)

# WeasyPrint থাকলে ইমপোর্ট, না থাকলে fallback
if USE_WEASY:
    try:
        from weasyprint import HTML, CSS
    except ImportError:
        USE_WEASY = False

if not USE_WEASY:
    from xhtml2pdf import pisa
