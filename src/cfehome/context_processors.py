from django.conf import settings


def vendor_files(request):
    static_dir = settings.BASE_DIR / "static"
    vendor_dir = static_dir / "vendor"
    js_files = [x.relative_to(static_dir) for x in vendor_dir.glob("**/*.js")]
    css_files = [x.relative_to(static_dir) for x in vendor_dir.glob("**/*.css")]
    return {
        "vendor_js_files": js_files,
        "vendor_css_files": css_files,
    }