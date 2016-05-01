from GoogleAPI import GoogleAPI


class GoogleSitemaps(GoogleAPI):
    def submit(self, subdomain, sitemap):
        return self.service.sitemaps().submit(
            siteUrl=subdomain,
            feedpath=sitemap).execute()

    def list(self, subdomain):
        return self.service.sitemaps().list(
            siteUrl=subdomain).execute()

    def get(self, subdomain, sitemap):
        return self.service.sitemaps().get(
            siteUrl=subdomain,
            feedpath=sitemap).execute()

    def delete(self, subdomain, sitemap):
        return self.service.sitemaps().delete(
            siteUrl=subdomain,
            feedpath=sitemap).execute()
