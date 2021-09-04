"""
Author: Hung Tran
Date Created: 15 April 2021
Date Last Changed: 23 April 2021
This file is for interface class Scene, this is to make sure all inherited classes
must implement these methods
"""


class SceneInterface(object):
    def run(self):
        raise NotImplementedError("The child class must implement this method")

    def destroy(self):
        raise NotImplementedError("The child class must implement this method")

    def write(self):
        raise NotImplementedError("The child class must implement this method")