from storages.backends.s3boto3 import S3Boto3Storage

class DefaultACLMixin():
    CANNED_ACL_OPTIONS = [
        'private',
        'public-read',
        'public-read-write',
        'aws-exec-read',
        'authenticated-read',
        'bucket-owner-read',
        'bucket-owner-full-control'
    ]
    def get_default_settings(self):
        _settings = super().get_default_settings()
        _settings['default_acl'] = self.get_default_acl()
        return _settings

    def get_default_acl(self):
        _acl = self.default_acl or None
        if _acl is not None:
            if _acl not in self.CANNED_ACL_OPTIONS:
                acl_options = "\n\t".join(self.CANNED_ACL_OPTIONS)
                raise Exception(f"The default_acl of \"{_acl}\" is invalid. Please use one of the following:\n{acl_options}")
        return _acl

class MediaStorage(S3Boto3Storage):
    location = "media"

class StaticFileStorage(S3Boto3Storage):
    location = "static"

class ProtectedFileStorage(DefaultACLMixin, S3Boto3Storage):
    location = "protected"
    default_acl = "private"