#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
""" Bot to increase YouTube views """

import sys
import time
from random import randrange
from modules.youtube import YouTube
from modules import utils


class Bot:
    """ A bot to increase YouTube views """
    # pylint: disable=R0903

    def __init__(self, options):
        """ init variables """

        self.opts = options

    def run(self):
        """ run """

        count = 1
        ipaddr = None
        while count <= self.opts.visits:
            if self.opts.enable_tor:
                ip_address = utils.get_new_tor_ipaddr(proxy=self.opts.proxy)
            if not ip_address:
                ip_address = utils.get_ipaddr(proxy=self.opts.proxy)
            youtube = YouTube(
                url=self.opts.url,
                proxy=self.opts.proxy,
                verbose=self.opts.verbose
            )
            youtube.get_url()
            title = youtube.get_title()
            if not title:
                if self.opts.verbose:
                    print('there was a problem loading this page. Retrying...')
                    youtube.disconnect()
                    continue
            if self.opts.visits:
                length = (len(title) + 4 - len(str(count)))
                print('[{0}] {1}'.format(count, '-' * length))
            if ip_address:
                print('external IP address:', ip_address)
            print('title:', title)
            views = youtube.get_views()
            if views:
                print('views:', views)
            # youtube.play_video()
            video_duration = youtube.time_duration()
            seconds = 30
            if video_duration:
                print('video duration time:', video_duration)
                seconds = utils.to_seconds(duration=video_duration.split(':'))
                if seconds:
                    sleep_time = randrange(seconds)
                    if self.opts.verbose:
                        print('video duration time in seconds:', seconds)
                print('stopping video in %s seconds' % sleep_time)
                time.sleep(sleep_time)
            youtube.disconnect()
            count += 1


def _main():
    """ main """

    try:
        cli_args = utils.get_cli_args()
        bot = Bot(cli_args)
        bot.run()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    sys.exit(_main())

# vim: set et ts=4 sw=4 sts=4 tw=80
