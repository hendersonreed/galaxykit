"""
Holds all of the functions used by GalaxyClient to handle Docker operations
"""

from subprocess import run


class DockerClient:
    """
    DockerClient authenticates with the passed registry, as well as
    provides utility functions for pushing, tagging, and pulling images.
    """

    engine = ""
    registry = ""

    def __init__(
        self,
        auth_tuple=None,
        engine="podman",
        registry="docker.io/library/",
        tls_verify=True,
    ):
        """
        auth_tuple should be `(username, password)` for logging into the docker registry.

        If not provided, then no login attempt is made.
        """
        self.engine = engine
        self.registry = registry

        if auth_tuple:  # we only need to auth if creds are supplied
            run_args = [
                engine,
                "login",
                registry,
                "--username",
                auth_tuple[0],
                "--password",
                auth_tuple[1],
            ]
            if not tls_verify:
                run_args.append("--tls-verify=false")
            run(run_args)

    def pull_image(self, image_name):
        """
        pull an image from the configured default registry
        """
        run([self.engine, "pull", self.registry + image_name])

    def tag_image(self, image_name, newtag, version="latest"):
        """
        Tags an image with the given tag
        """
        run([self.engine, "image", "tag", image_name, f"{newtag}:{version}"])

    def push_image(self, image_tag):
        """
        Pushes an image
        """
        run([self.engine, "push", image_tag])
