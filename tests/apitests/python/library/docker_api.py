# -*- coding: utf-8 -*-

import base

try:
    import docker
except ImportError:
    import pip
    pip.main(['install', 'docker'])
    import docker

class DockerAPI(object):
    def __init__(self):
        self.DCLIENT = docker.APIClient(base_url='unix://var/run/docker.sock',version='auto',timeout=10)

    def docker_login(self, registry, username, password):
        try:
            self.DCLIENT.login(registry = registry, username=username, password=password)
        except docker.errors.APIError, e:
            raise Exception(r" Docker login failed, error is [{}]".format (e.message))

    def docker_image_pull(self, image, tag = None):
        _tag = "latest"
        if tag is not None:
            _tag = tag
        try:
            tag = base._random_name("tag")
            pull_ret = base._get_string_from_unicode(self.DCLIENT.pull('{}:{}'.format(image, _tag)))
            print "pull_ret:", pull_ret
        except docker.errors.APIError, e:
            raise Exception(r" Docker pull image {} failed, error is [{}]".format (image, e.message))

    def docker_image_tag(self, image, harbor_registry, tag = None):
        _tag = base._random_name("tag")
        if tag is not None:
            _tag = tag
        try:
            tag_ret = self.DCLIENT.tag(image, harbor_registry, _tag, force=True)
            print "tag_ret:", tag_ret
            return harbor_registry, _tag
        except docker.errors.APIError, e:
            raise Exception(r" Docker tag image {} failed, error is [{}]".format (image, e.message))

    def docker_image_push(self, harbor_registry, tag):
        try:
            push_ret = base._get_string_from_unicode(self.DCLIENT.push(harbor_registry, tag, stream=True))
            print "push_ret:", push_ret
        except docker.errors.APIError, e:
            raise Exception(r" Docker tag image {} failed, error is [{}]".format (image, e.message))    