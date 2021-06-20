#!/usr/bin/env python3
#
# Copyright (C) 2018 Linus Jahn <lnj@kaidan.im>
# Copyright (C) 2019-2021 Hiroshi Miura <miurahr@linux.com>
# Copyright (C) 2020, Aurélien Gâteau
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import multiprocessing
import os
from logging import getLogger
from logging.config import fileConfig
from logging.handlers import QueueHandler, QueueListener

from aqt.helper import Settings


def setup_logging(env_key="LOG_CFG"):
    config = os.getenv(env_key, None)
    if config is not None and os.path.exists(config):
        fileConfig(config)
    else:
        fileConfig(Settings.loggingconf)


class LoggingQueueListener:

    def __init__(self):
        self.queue = multiprocessing.Queue(-1)
        handlers = getLogger("aqt").handlers
        self.listener = QueueListener(self.queue, *handlers, respect_handler_level=False)
        self.listener.start()

    def get_queue_handler(self):
        return QueueHandler(self.queue)

    def stop(self):
        self.listener.stop()
        self.queue.close()
        self.listener = None
        self.queue = None


LoggingQueueListener = LoggingQueueListener()
