#
# Copyright (c) 2022-2023 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from k8sapp_sts_silicom.common import constants as app_constants

from sysinv.tests.db import base as dbbase


class K8SAppStsSilicomAppMixin(object):
    app_name = app_constants.HELM_APP_STS_SILICOM
    path_name = app_name + '.tgz'

    def setUp(self):
        super(K8SAppStsSilicomAppMixin, self).setUp()


# Test Configuration:
# - Controller
# - IPv6
# - Ceph Storage
# - sts-silicom app
class K8SAppStsSilicomControllerTestCase(K8SAppStsSilicomAppMixin,
                                         dbbase.BaseIPv6Mixin,
                                         dbbase.BaseCephStorageBackendMixin,
                                         dbbase.ControllerHostTestCase):
    pass


# Test Configuration:
# - AIO
# - IPv4
# - Ceph Storage
# - sts-silicom app
class K8SAppStsSilicomAIOTestCase(K8SAppStsSilicomAppMixin,
                                  dbbase.BaseCephStorageBackendMixin,
                                  dbbase.AIOSimplexHostTestCase):
    pass
