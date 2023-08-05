# Copyright 2010-2017, The University of Melbourne
# Copyright 2010-2017, Brian May
#
# This file is part of Karaage.
#
# Karaage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Karaage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Karaage  If not, see <http://www.gnu.org/licenses/>.

import os.path

from django.conf import settings


try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

GRAPH_TMP = os.path.join(settings.TMP_DIR, settings.GRAPH_TMP)
GRAPH_ROOT = os.path.join(settings.FILES_DIR, settings.GRAPH_DIR)
GRAPH_URL = urlparse.urljoin(settings.FILES_URL, settings.GRAPH_DIR)
