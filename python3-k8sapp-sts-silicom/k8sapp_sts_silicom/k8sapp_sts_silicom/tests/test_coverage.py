#
# Copyright (c) 2026 Wind River Systems, Inc.
#
# SPDX-License-Identifier: Apache-2.0
#
"""Unit tests for sts-silicom lifecycle and helm modules."""

import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from k8sapp_sts_silicom.common import constants as app_constants
from k8sapp_sts_silicom.helm.sts_silicom import StsSilicomHelm
from k8sapp_sts_silicom.lifecycle.lifecycle_sts_silicom import (
    StsSilicomAppLifecycleOperator
)
from sysinv.common import constants
from sysinv.common import exception
from sysinv.helm.lifecycle_constants import LifecycleConstants


class TestStsSilicomConstants(unittest.TestCase):
    """Tests for application constants."""

    def test_helm_app_name(self):
        """Verify HELM_APP_STS_SILICOM value."""
        self.assertEqual(
            app_constants.HELM_APP_STS_SILICOM, 'sts-silicom'
        )

    def test_helm_namespace(self):
        """Verify HELM_NS_STS_SILICOM value."""
        self.assertEqual(
            app_constants.HELM_NS_STS_SILICOM, 'sts-silicom'
        )

    def test_helm_chart_name(self):
        """Verify HELM_CHART_STS_SILICOM value."""
        self.assertEqual(
            app_constants.HELM_CHART_STS_SILICOM, 'sts-silicom'
        )

    def test_helm_component_label(self):
        """Verify HELM_COMPONENT_LABEL_STS_SILICOM value."""
        self.assertEqual(
            app_constants.HELM_COMPONENT_LABEL_STS_SILICOM,
            'app.starlingx.io/component'
        )


class TestStsSilicomHelm(unittest.TestCase):
    """Tests for StsSilicomHelm class."""

    def setUp(self):
        """Set up test fixtures."""
        self.helm = StsSilicomHelm.__new__(StsSilicomHelm)

    def test_chart_attribute(self):
        """Verify CHART class attribute."""
        self.assertEqual(
            StsSilicomHelm.CHART,
            app_constants.HELM_CHART_STS_SILICOM
        )

    def test_service_name_attribute(self):
        """Verify SERVICE_NAME class attribute."""
        self.assertEqual(
            StsSilicomHelm.SERVICE_NAME,
            app_constants.HELM_APP_STS_SILICOM
        )

    def test_supported_namespaces_includes_sts_silicom(self):
        """Verify sts-silicom namespace in SUPPORTED_NAMESPACES."""
        self.assertIn(
            app_constants.HELM_NS_STS_SILICOM,
            StsSilicomHelm.SUPPORTED_NAMESPACES
        )

    def test_supported_app_namespaces(self):
        """Verify SUPPORTED_APP_NAMESPACES structure."""
        self.assertIn(
            app_constants.HELM_APP_STS_SILICOM,
            StsSilicomHelm.SUPPORTED_APP_NAMESPACES
        )

    def test_get_namespaces(self):
        """Verify get_namespaces returns SUPPORTED_NAMESPACES."""
        result = self.helm.get_namespaces()
        self.assertEqual(result, StsSilicomHelm.SUPPORTED_NAMESPACES)

    def test_get_overrides_supported_namespace(self):
        """Test get_overrides with a supported namespace."""
        result = self.helm.get_overrides(
            namespace=app_constants.HELM_NS_STS_SILICOM
        )
        self.assertEqual(result, {})

    def test_get_overrides_no_namespace(self):
        """Test get_overrides with no namespace returns all."""
        result = self.helm.get_overrides(namespace=None)
        self.assertIn(app_constants.HELM_NS_STS_SILICOM, result)

    def test_get_overrides_invalid_namespace(self):
        """Test get_overrides raises on invalid namespace."""
        with self.assertRaises(
            exception.InvalidHelmNamespace
        ):
            self.helm.get_overrides(namespace='invalid-ns')


class TestLifecycleActions(unittest.TestCase):
    """Tests for StsSilicomAppLifecycleOperator."""

    def setUp(self):
        """Set up test fixtures."""
        self.operator = StsSilicomAppLifecycleOperator()
        self.context = MagicMock()
        self.conductor_obj = MagicMock()
        self.app_op = MagicMock()
        self.app = MagicMock()
        self.app.name = 'sts-silicom'

    def _make_hook_info(self, lifecycle_type, operation,
                        timing):
        """Create a mock hook_info object."""
        hook_info = MagicMock()
        hook_info.lifecycle_type = lifecycle_type
        hook_info.operation = operation
        hook_info.relative_timing = timing
        return hook_info

    def test_post_apply_triggered(self):
        """Test post_apply is called on fluxcd post-apply."""
        hook_info = self._make_hook_info(
            LifecycleConstants.APP_LIFECYCLE_TYPE_FLUXCD_REQUEST,
            constants.APP_APPLY_OP,
            LifecycleConstants.APP_LIFECYCLE_TIMING_POST
        )
        with patch.object(
            self.operator, 'post_apply'
        ) as mock_post:
            self.operator.app_lifecycle_actions(
                self.context, self.conductor_obj,
                self.app_op, self.app, hook_info
            )
            mock_post.assert_called_once_with(
                self.app_op, self.app, hook_info
            )

    def test_pre_remove_triggered(self):
        """Test pre_remove is called on operation pre-remove."""
        hook_info = self._make_hook_info(
            LifecycleConstants.APP_LIFECYCLE_TYPE_OPERATION,
            constants.APP_REMOVE_OP,
            LifecycleConstants.APP_LIFECYCLE_TIMING_PRE
        )
        with patch.object(
            self.operator, 'pre_remove'
        ) as mock_pre:
            self.operator.app_lifecycle_actions(
                self.context, self.conductor_obj,
                self.app_op, self.app, hook_info
            )
            mock_pre.assert_called_once_with(self.app)

    def test_post_remove_triggered(self):
        """Test post_remove is called on operation post-remove."""
        hook_info = self._make_hook_info(
            LifecycleConstants.APP_LIFECYCLE_TYPE_OPERATION,
            constants.APP_REMOVE_OP,
            LifecycleConstants.APP_LIFECYCLE_TIMING_POST
        )
        with patch.object(
            self.operator, 'post_remove'
        ) as mock_post:
            self.operator.app_lifecycle_actions(
                self.context, self.conductor_obj,
                self.app_op, self.app, hook_info
            )
            mock_post.assert_called_once_with(self.app)

    def test_unhandled_lifecycle_calls_super(self):
        """Test unhandled lifecycle type calls parent."""
        hook_info = self._make_hook_info(
            'unknown_type', 'unknown_op', 'unknown_timing'
        )
        self.operator.app_lifecycle_actions(
            self.context, self.conductor_obj,
            self.app_op, self.app, hook_info
        )


class TestPostApply(unittest.TestCase):
    """Tests for post_apply method."""

    def setUp(self):
        """Set up test fixtures."""
        self.operator = StsSilicomAppLifecycleOperator()
        self.app_op = MagicMock()
        self.app = MagicMock()
        self.app.name = 'sts-silicom'

    def _setup_successful_hook_info(self, return_code=True):
        """Create hook_info that passes initial checks."""
        hook_info = {
            LifecycleConstants.EXTRA: {
                LifecycleConstants.RETURN_CODE: return_code
            }
        }
        return hook_info

    def _setup_app_op(self, user_overrides=""):
        """Configure app_op mocks for post_apply."""
        namespace_mock = MagicMock()
        namespace_mock.metadata.labels = {}
        client_core = MagicMock()
        client_core.read_namespace.return_value = namespace_mock
        self.app_op._kube._get_kubernetesclient_core\
            .return_value = client_core

        dbapi = MagicMock()
        dbapi.kube_app_get.return_value.id = 1
        override_mock = MagicMock()
        override_mock.user_overrides = user_overrides
        dbapi.helm_override_get.return_value = override_mock
        self.app_op._dbapi = dbapi
        return namespace_mock, client_core

    def test_missing_extra_raises(self):
        """Test raises when EXTRA missing from hook_info."""
        hook_info = {}
        with self.assertRaises(
            exception.LifecycleMissingInfo
        ):
            self.operator.post_apply(
                self.app_op, self.app, hook_info
            )

    def test_missing_return_code_raises(self):
        """Test raises when RETURN_CODE missing."""
        hook_info = {LifecycleConstants.EXTRA: {}}
        with self.assertRaises(
            exception.LifecycleMissingInfo
        ):
            self.operator.post_apply(
                self.app_op, self.app, hook_info
            )

    def test_failed_apply_not_aborted_raises(self):
        """Test raises ApplicationApplyFailure on failure."""
        hook_info = self._setup_successful_hook_info(
            return_code=False
        )
        self.app_op.is_app_aborted.return_value = False
        with self.assertRaises(
            exception.ApplicationApplyFailure
        ):
            self.operator.post_apply(
                self.app_op, self.app, hook_info
            )

    def test_failed_apply_aborted_no_raise(self):
        """Test no raise when app is aborted."""
        hook_info = self._setup_successful_hook_info(
            return_code=False
        )
        self.app_op.is_app_aborted.return_value = True
        self._setup_app_op()

        self.operator.post_apply(
            self.app_op, self.app, hook_info
        )

    def test_override_label_application(self):
        """Test namespace label set to application."""
        hook_info = self._setup_successful_hook_info()
        component = (
            app_constants.HELM_COMPONENT_LABEL_STS_SILICOM
        )
        self._setup_app_op(
            user_overrides="%s: application" % component
        )

        with patch('yaml.safe_load', return_value={
            component: 'application'
        }):
            self.operator.post_apply(
                self.app_op, self.app, hook_info
            )

        self.app_op._kube.kube_patch_namespace\
            .assert_called()

    def test_override_label_platform(self):
        """Test namespace label set to platform."""
        hook_info = self._setup_successful_hook_info()
        component = (
            app_constants.HELM_COMPONENT_LABEL_STS_SILICOM
        )
        self._setup_app_op(
            user_overrides="%s: platform" % component
        )

        with patch('yaml.safe_load', return_value={
            component: 'platform'
        }):
            self.operator.post_apply(
                self.app_op, self.app, hook_info
            )

        self.app_op._kube.kube_patch_namespace\
            .assert_called()

    def test_override_label_unsupported(self):
        """Test unsupported label logs warning."""
        hook_info = self._setup_successful_hook_info()
        component = (
            app_constants.HELM_COMPONENT_LABEL_STS_SILICOM
        )
        self._setup_app_op(
            user_overrides="%s: bad_value" % component
        )

        with patch('yaml.safe_load', return_value={
            component: 'bad_value'
        }):
            self.operator.post_apply(
                self.app_op, self.app, hook_info
            )

    def test_namespace_label_change_deletes_pods(self):
        """Test pods deleted on namespace label change."""
        hook_info = self._setup_successful_hook_info()
        component = (
            app_constants.HELM_COMPONENT_LABEL_STS_SILICOM
        )

        namespace_mock, client_core = self._setup_app_op()
        namespace_mock.metadata.labels = {
            component: 'application'
        }

        pod_mock = MagicMock()
        pod_mock.metadata.name = 'test-pod'
        client_core.list_namespaced_pod.return_value\
            .items = [pod_mock]

        self.operator.post_apply(
            self.app_op, self.app, hook_info
        )

        self.app_op._kube.kube_delete_pod.assert_called()


class TestPreRemove(unittest.TestCase):
    """Tests for pre_remove method."""

    def setUp(self):
        """Set up test fixtures."""
        self.operator = StsSilicomAppLifecycleOperator()
        self.app = MagicMock()
        self.app.name = 'sts-silicom'
        self.app.sync_fluxcd_manifest = '/tmp/test_manifest'

    @patch('k8sapp_sts_silicom.lifecycle'
           '.lifecycle_sts_silicom.cutils.trycmd')
    @patch('os.path.exists', return_value=True)
    def test_pre_remove_file_exists(
        self, mock_exists, mock_trycmd
    ):
        """Test pre_remove when yaml file exists."""
        mock_trycmd.return_value = ('', '')
        self.operator.pre_remove(self.app)
        self.assertEqual(mock_trycmd.call_count, 2)

    @patch('k8sapp_sts_silicom.lifecycle'
           '.lifecycle_sts_silicom.cutils.trycmd')
    @patch('os.path.exists', return_value=False)
    def test_pre_remove_file_not_exists(
        self, mock_exists, mock_trycmd
    ):
        """Test pre_remove when yaml file does not exist."""
        mock_trycmd.return_value = ('', '')
        self.operator.pre_remove(self.app)
        self.assertEqual(mock_trycmd.call_count, 1)


class TestPostRemove(unittest.TestCase):
    """Tests for post_remove method."""

    def setUp(self):
        """Set up test fixtures."""
        self.operator = StsSilicomAppLifecycleOperator()
        self.app = MagicMock()
        self.app.name = 'sts-silicom'
        self.app.sync_fluxcd_manifest = '/tmp/test_manifest'

    @patch('k8sapp_sts_silicom.lifecycle'
           '.lifecycle_sts_silicom.cutils.trycmd')
    def test_post_remove(self, mock_trycmd):
        """Test post_remove uncomments kustomization."""
        mock_trycmd.return_value = ('', '')
        self.operator.post_remove(self.app)
        mock_trycmd.assert_called_once()


class TestGetHelmUserOverrides(unittest.TestCase):
    """Tests for _get_helm_user_overrides method."""

    def setUp(self):
        """Set up test fixtures."""
        self.operator = StsSilicomAppLifecycleOperator()

    def test_override_found(self):
        """Test returns user_overrides when found."""
        dbapi = MagicMock()
        override_mock = MagicMock()
        override_mock.user_overrides = "test: value"
        dbapi.helm_override_get.return_value = override_mock

        result = self.operator._get_helm_user_overrides(
            dbapi, 1
        )
        self.assertEqual(result, "test: value")

    def test_override_not_found_creates(self):
        """Test creates override when not found."""
        dbapi = MagicMock()
        dbapi.helm_override_get.side_effect = (
            exception.HelmOverrideNotFound()
        )
        created_mock = MagicMock()
        created_mock.user_overrides = ""
        dbapi.helm_override_create.return_value = (
            created_mock
        )

        result = self.operator._get_helm_user_overrides(
            dbapi, 1
        )
        self.assertEqual(result, "")
        dbapi.helm_override_create.assert_called_once()

    def test_override_none_returns_empty(self):
        """Test returns empty string when overrides None."""
        dbapi = MagicMock()
        override_mock = MagicMock()
        override_mock.user_overrides = None
        dbapi.helm_override_get.return_value = override_mock

        result = self.operator._get_helm_user_overrides(
            dbapi, 1
        )
        self.assertEqual(result, "")


class TestDeleteStsSilicomPods(unittest.TestCase):
    """Tests for _delete_sts_silicom_pods method."""

    def setUp(self):
        """Set up test fixtures."""
        self.operator = StsSilicomAppLifecycleOperator()

    def test_deletes_all_pods(self):
        """Test all pods in namespace are deleted."""
        app_op = MagicMock()
        client_core = MagicMock()

        pod1 = MagicMock()
        pod1.metadata.name = 'pod-1'
        pod2 = MagicMock()
        pod2.metadata.name = 'pod-2'
        client_core.list_namespaced_pod.return_value\
            .items = [pod1, pod2]

        self.operator._delete_sts_silicom_pods(
            app_op, client_core
        )
        self.assertEqual(
            app_op._kube.kube_delete_pod.call_count, 2
        )

    def test_no_pods_no_delete(self):
        """Test no delete calls when no pods exist."""
        app_op = MagicMock()
        client_core = MagicMock()
        client_core.list_namespaced_pod.return_value\
            .items = []

        self.operator._delete_sts_silicom_pods(
            app_op, client_core
        )
        app_op._kube.kube_delete_pod.assert_not_called()
