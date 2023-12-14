#
# Copyright (c) 2022 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#

from sysinv.common import exception
from sysinv.helm import base

from k8sapp_sts_silicom.common import constants as app_constants
from oslo_log import log as logging

LOG = logging.getLogger(__name__)


class StsSilicomHelm(base.BaseHelm):
    """Class to encapsulate helm operations for the sts-silicom chart"""

    SUPPORTED_NAMESPACES = base.BaseHelm.SUPPORTED_NAMESPACES + \
        [app_constants.HELM_NS_STS_SILICOM]
    SUPPORTED_APP_NAMESPACES = {
        app_constants.HELM_APP_STS_SILICOM:
            base.BaseHelm.SUPPORTED_NAMESPACES +
            [app_constants.HELM_NS_STS_SILICOM]
    }

    CHART = app_constants.HELM_CHART_STS_SILICOM

    SERVICE_NAME = app_constants.HELM_APP_STS_SILICOM

    def get_namespaces(self):
        return self.SUPPORTED_NAMESPACES

    def get_overrides(self, namespace=None):
        overrides = {
            app_constants.HELM_NS_STS_SILICOM: {}
        }

        if namespace in self.SUPPORTED_NAMESPACES:
            return overrides[namespace]
        elif namespace:
            raise exception.InvalidHelmNamespace(chart=self.CHART,
                                                 namespace=namespace)
        else:
            return overrides
