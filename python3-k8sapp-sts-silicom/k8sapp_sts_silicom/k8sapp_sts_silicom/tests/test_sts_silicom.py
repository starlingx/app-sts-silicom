# Copyright (c) 2022-2023 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from k8sapp_sts_silicom.tests import test_plugins

from sysinv.tests.db import base as dbbase
from sysinv.db import api as dbapi
from sysinv.tests.db import utils as dbutils
from sysinv.tests.helm import base


class StsSilicomTestCase(test_plugins.K8SAppStsSilicomAppMixin,
                         base.HelmTestCaseMixin):

    def setUp(self):
        super(StsSilicomTestCase, self).setUp()
        self.app = dbutils.create_test_app(name='sts-silicom')
        self.dbapi = dbapi.get_instance()


class StsSilicomTestCaseDummy(StsSilicomTestCase, dbbase.ProvisionedControllerHostTestCase):
    # without a test zuul will fail
    def test_dummy(self):
        pass
