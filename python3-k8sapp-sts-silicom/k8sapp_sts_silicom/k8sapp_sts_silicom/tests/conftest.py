#
# Copyright (c) 2026 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
"""Pytest configuration and shared fixtures for sts-silicom tests."""

import sys
from types import ModuleType
from unittest import mock


class _AppLifecycleOperator(object):
    """Stub for AppLifecycleOperator."""

    def app_lifecycle_actions(self, context, conductor_obj,
                             app_op, app, hook_info):
        """No-op base."""


class _BaseHelm(object):
    """Stub for BaseHelm."""

    SUPPORTED_NAMESPACES = ['kube-system']


class _LifecycleConstants(object):
    """Stub for LifecycleConstants."""

    APP_LIFECYCLE_TYPE_FLUXCD_REQUEST = 'fluxcd-request'
    APP_LIFECYCLE_TYPE_OPERATION = 'operation'
    APP_LIFECYCLE_TIMING_PRE = 'pre'
    APP_LIFECYCLE_TIMING_POST = 'post'
    EXTRA = 'extra'
    RETURN_CODE = 'return_code'


class LifecycleMissingInfo(Exception):
    """Stub exception."""


class ApplicationApplyFailure(Exception):
    """Stub exception."""

    def __init__(self, name=None):
        super(ApplicationApplyFailure, self).__init__(name)


class HelmOverrideNotFound(Exception):
    """Stub exception."""


class InvalidHelmNamespace(Exception):
    """Stub exception."""

    def __init__(self, chart=None, namespace=None):
        super(InvalidHelmNamespace, self).__init__()


# Build module hierarchy using ModuleType
_sysinv = ModuleType('sysinv')
_sysinv_common = ModuleType('sysinv.common')
_sysinv_helm = ModuleType('sysinv.helm')

_lifecycle_base = ModuleType('sysinv.helm.lifecycle_base')
_lifecycle_base.AppLifecycleOperator = _AppLifecycleOperator

_base_helm = ModuleType('sysinv.helm.base')
_base_helm.BaseHelm = _BaseHelm

_lc_mod = ModuleType('sysinv.helm.lifecycle_constants')
_lc_mod.LifecycleConstants = _LifecycleConstants

_exc_mod = ModuleType('sysinv.common.exception')
_exc_mod.LifecycleMissingInfo = LifecycleMissingInfo
_exc_mod.ApplicationApplyFailure = ApplicationApplyFailure
_exc_mod.HelmOverrideNotFound = HelmOverrideNotFound
_exc_mod.InvalidHelmNamespace = InvalidHelmNamespace

_constants_mod = ModuleType('sysinv.common.constants')
_constants_mod.APP_APPLY_OP = 'apply'
_constants_mod.APP_REMOVE_OP = 'remove'

_kube_mod = ModuleType('sysinv.common.kubernetes')
_kube_mod.KUBERNETES_ADMIN_CONF = '/etc/kubernetes/admin.conf'

_utils_mod = ModuleType('sysinv.common.utils')
_utils_mod.trycmd = mock.MagicMock(return_value=('', ''))

_oslo_log = ModuleType('oslo_log')
_oslo_log_log = ModuleType('oslo_log.log')
_oslo_log_log.getLogger = mock.MagicMock(
    return_value=mock.MagicMock()
)

# Wire hierarchy
_sysinv_helm.lifecycle_base = _lifecycle_base
_sysinv_helm.base = _base_helm
_sysinv_helm.lifecycle_constants = _lc_mod
_sysinv_common.constants = _constants_mod
_sysinv_common.exception = _exc_mod
_sysinv_common.kubernetes = _kube_mod
_sysinv_common.utils = _utils_mod
_sysinv.common = _sysinv_common
_sysinv.helm = _sysinv_helm
_oslo_log.log = _oslo_log_log

# Register in sys.modules
sys.modules['oslo_log'] = _oslo_log
sys.modules['oslo_log.log'] = _oslo_log_log
sys.modules['sysinv'] = _sysinv
sys.modules['sysinv.common'] = _sysinv_common
sys.modules['sysinv.common.constants'] = _constants_mod
sys.modules['sysinv.common.exception'] = _exc_mod
sys.modules['sysinv.common.kubernetes'] = _kube_mod
sys.modules['sysinv.common.utils'] = _utils_mod
sys.modules['sysinv.helm'] = _sysinv_helm
sys.modules['sysinv.helm.base'] = _base_helm
sys.modules['sysinv.helm.lifecycle_base'] = _lifecycle_base
sys.modules['sysinv.helm.lifecycle_constants'] = _lc_mod
