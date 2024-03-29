# coding=utf-8
import re
from urllib.parse import urlparse

import plexnet.http

from lib import util
from lib.advancedsettings import adv

from plexnet.util import parsePlexDirectHost

HOSTS_RE = re.compile(r'\s*<hosts>.*</hosts>', re.S | re.I)
HOST_RE = re.compile(r'<entry name="(?P<hostname>.+)">(?P<ip>.+)</entry>')


class PlexHostsManager(object):
    _hosts = None
    _orig_hosts = None

    HOSTS_TPL = """\
  <hosts><!-- managed by PM4K -->
{}
  </hosts>"""
    ENTRY_TPL = '    <entry name="{}">{}</entry>'

    def __init__(self):
        self.load()

    def __bool__(self):
        return bool(self._hosts)

    def __len__(self):
        return self and len(self._hosts) or 0

    def getHosts(self):
        return self._hosts or {}

    def newHosts(self, hosts, source="stored"):
        """
        hosts should be a list of plex.direct connection uri's
        """
        for address in hosts:
            parsed = urlparse(address)
            if parsed.hostname not in self._hosts:
                self._hosts[parsed.hostname] = plexnet.http.RESOLVED_PD_HOSTS.get(parsed.hostname,
                                                                                  parsePlexDirectHost(parsed.hostname))
                util.LOG("Found new unmapped {} plex.direct host: {}".format(source, parsed.hostname))

    @property
    def differs(self):
        return self._hosts != self._orig_hosts

    @property
    def diff(self):
        return set(self._hosts) - set(self._orig_hosts)

    def load(self):
        data = adv.getData()
        self._hosts = {}
        self._orig_hosts = {}
        if not data:
            return

        hosts_match = HOSTS_RE.search(data)
        if hosts_match:
            hosts_xml = hosts_match.group(0)

            hosts = HOST_RE.findall(hosts_xml)
            if hosts:
                self._hosts = dict(hosts)
                self._orig_hosts = dict(hosts)
                util.DEBUG_LOG("Found {} hosts in advancedsettings.xml".format(len(self._hosts)))

    def write(self, hosts=None):
        self._hosts = hosts or self._hosts
        if not self._hosts:
            return
        data = adv.getData()
        cd = "<advancedsettings>\n</advancedsettings>"
        if data:
            hosts_match = HOSTS_RE.search(data)
            if hosts_match:
                hosts_xml = hosts_match.group(0)
                cd = data.replace(hosts_xml, "")
            else:
                cd = data

        finalxml = "{}\n</advancedsettings>".format(
            cd.replace("</advancedsettings>", self.HOSTS_TPL.format("\n".join(self.ENTRY_TPL.format(hostname, ip)
                                                                              for hostname, ip in self._hosts.items())))
        )

        adv.write(finalxml)
        self._orig_hosts = dict(self._hosts)


pdm = PlexHostsManager()
