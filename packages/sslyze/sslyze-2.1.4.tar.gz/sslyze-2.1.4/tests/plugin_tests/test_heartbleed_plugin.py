import pickle

from sslyze.plugins.heartbleed_plugin import HeartbleedPlugin, HeartbleedScanCommand
from sslyze.server_connectivity_tester import ServerConnectivityTester
from tests.markers import can_only_run_on_linux_64

from tests.openssl_server import LegacyOpenSslServer, ClientAuthConfigEnum


class TestHeartbleedPlugin:

    def test_heartbleed_good(self):
        server_test = ServerConnectivityTester(hostname='www.google.com')
        server_info = server_test.perform()

        plugin = HeartbleedPlugin()
        plugin_result = plugin.process_task(server_info, HeartbleedScanCommand())

        assert not plugin_result.is_vulnerable_to_heartbleed

        assert plugin_result.as_text()
        assert plugin_result.as_xml()

        # Ensure the results are pickable so the ConcurrentScanner can receive them via a Queue
        assert pickle.dumps(plugin_result)

    @can_only_run_on_linux_64
    def test_heartbleed_bad(self):
        with LegacyOpenSslServer() as server:
            server_test = ServerConnectivityTester(
                hostname=server.hostname, ip_address=server.ip_address, port=server.port
            )
            server_info = server_test.perform()

            plugin = HeartbleedPlugin()
            plugin_result = plugin.process_task(server_info, HeartbleedScanCommand())

        assert plugin_result.is_vulnerable_to_heartbleed
        assert plugin_result.as_text()
        assert plugin_result.as_xml()

        # Ensure the results are pickable so the ConcurrentScanner can receive them via a Queue
        assert pickle.dumps(plugin_result)

    @can_only_run_on_linux_64
    def test_succeeds_when_client_auth_failed(self):
        # Given a server that requires client authentication
        with LegacyOpenSslServer(
                client_auth_config=ClientAuthConfigEnum.REQUIRED
        ) as server:
            # And the client does NOT provide a client certificate
            server_test = ServerConnectivityTester(
                hostname=server.hostname,
                ip_address=server.ip_address,
                port=server.port
            )
            server_info = server_test.perform()

            # The plugin works even when a client cert was not supplied
            plugin = HeartbleedPlugin()
            plugin_result = plugin.process_task(server_info, HeartbleedScanCommand())

        assert plugin_result.is_vulnerable_to_heartbleed
        assert plugin_result.as_text()
        assert plugin_result.as_xml()
