# ─── Global ColdGuard Constants ──────────────────────
# Shared across all apps


class AppInfo:
    """Application information"""
    NAME    = 'ColdGuard'
    VERSION = '1.0.0'


class SupportedLanguages:
    """Supported dashboard languages"""
    GERMAN = 'de'
    ARABIC = 'ar'
    ALL    = [GERMAN, ARABIC]


class NotificationType:
    """Supported notification channels"""
    EMAIL    = 'email'
    WHATSAPP = 'whatsapp'  # Phase 4
    SMS      = 'sms'       # Phase 4