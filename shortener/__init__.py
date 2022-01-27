import falcon
from falcon.errors import HTTPBadRequest, HTTPNotFound
from urllib.parse import urlparse, urlunparse

from shortener.models import db, Link

app = falcon.App(cors_enable=True)

ALLOWED_HOSTS = (
    "peterboroughtenants.org",
    "peterboroughtenants.app",
    "www.peterboroughtenants.org",
    "www.peterboroughtenants.app",
    "api.peterboroughtenants.app",
)


class LinkResource:
    def on_get(self, req, resp, code):
        """
        Return a redirect to the correct URL
        """

        l: Link = db.query(Link).get(code)
        if l is None:
            raise HTTPNotFound

        resp.status = 303
        resp.append_header("Location", l.destination)

    def on_put_link(self, req, resp):
        """
        Create a new short-link
        """

        body = req.get_media()
        if "destination" not in body:
            raise HTTPBadRequest

        schema = urlparse(body["destination"])
        schema._replace(scheme="https")

        if schema.hostname not in ALLOWED_HOSTS:
            raise HTTPBadRequest(
                description="Hostname must be in list of allowed hosts."
            )

        url = urlunparse(schema)

        l = db.query(Link).filter(Link.destination == url).one_or_none()
        if l is None:
            l = Link(url)
            db.add(l)
            db.commit()

        resp.media = {
            "link": f"https://ptu2.link/{l.id}"
        }


app.add_route("/", LinkResource(), suffix="link")
app.add_route("/{code}", LinkResource())
