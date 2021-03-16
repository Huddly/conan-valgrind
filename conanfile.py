#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Conan recipe package for valgrind
"""
import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools


class ValgrindConan(ConanFile):
    name = "valgrind"
    version = "3.14.0"
    license = "gpl-2.0"
    author = "Ivan Ryabov <abbyssoul@gmail.com>"
    url = "https://github.com/abbyssoul/conan-%s.git" % name
    homepage = "http://www.valgrind.org/"
    description = "Valgrind is an instrumentation framework for building dynamic analysis tools."
    topics = ("valgrind", "memory", "debug")
    # settings = "os", "arch"
    settings = "os", "arch", "compiler"
    generators='virtualenv','cmake','cmake_find_package'

    @property
    def _package_name(self):
        #valgrind-3.14.0
        return "{package}-{version}".format(
            package=self.name,
            version=self.version
        )

    def source(self):
        archive = "{}.tar.bz2".format(self._package_name)
        try:
            tools.download("http://www.valgrind.org/downloads/{}".format(archive), archive, overwrite=False)
        except Exception as e:
            pass
        tools.untargz(archive)
        os.unlink(archive)

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure(configure_dir=self._package_name,
                            args=["--enable-lto=yes",
                                  "--host=aarch64-buildroot-linux-musl"  if self.settings.arch == "armv8" else ""
            ])
        autotools.make()
        autotools.install()

    def package(self):
        pass
