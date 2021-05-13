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

    def __init__(self, user="", password="", engine="podman", registry=""):
        self.engine = engine
        self.registry = registry

        if registry != "":
            self.engine = engine
            self.registry = registry
            run([engine, "login", registry, "--username", user, "--password", password])
        else:  # if registry == "", then assume standard docker hub
            if user != "" and password != "":
                # we only login to dockerhub if user/pass are provided
                run([engine, "login", "--username", user, "--password", password])

    def pull_image(self, image_name):
        """
        pull an image from the configured default registry
        """
        run([self.engine, "pull", self.registry + image_name])

    def pull_image_dockerhub(self, image_name):
        """
        pull an image from dockerhub
        """
        run([self.engine, "pull", image_name])

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
