# -*- coding: utf-8 -*-
from pathlib import Path

from django.test import TestCase
from eth_tester import EthereumTester
from web3 import HTTPProvider, IPCProvider
from web3.providers.eth_tester import EthereumTesterProvider

from ..exceptions import UnknownBlock
from ..web3_service import Web3Service, Web3ServiceProvider


class TestSingleton(TestCase):

    def setUp(self):
        self.web3_service = Web3Service(provider=EthereumTesterProvider(EthereumTester()))
        self.web3 = self.web3_service.web3
        self.web3.eth.defaultAccount = self.web3.eth.coinbase
        self.provider = self.web3.provider
        self.tx_data = {'from': self.web3.eth.coinbase,
                        'gas': 1000000}
        self.event_receivers = []

    def tearDown(self):
        # Delete centralized oracles
        self.provider.ethereum_tester.reset_to_genesis()
        self.assertEqual(0, self.web3.eth.blockNumber)

        # Delete provider
        try:
            del Web3ServiceProvider.instance
        except AttributeError:
            pass

    def test_unknown_block(self):
        current_block_number = self.web3_service.get_current_block_number()
        self.assertRaises(UnknownBlock, self.web3_service.get_block, current_block_number + 10)

    def test_unknown_blocks(self):
        current_block_number = self.web3_service.get_current_block_number()
        self.assertRaises(UnknownBlock, self.web3_service.get_block, range(current_block_number + 10))

    def test_provider_http(self):
        with self.settings(ETHEREUM_NODE_URL='http://localhost:8545'):
            web3_service = Web3ServiceProvider()
            provider = web3_service.web3.provider
            self.assertTrue(isinstance(provider, HTTPProvider))

        with self.settings(ETHEREUM_NODE_URL='https://localhost:8545'):
            web3_service = Web3ServiceProvider()
            provider = web3_service.web3.provider
            self.assertTrue(isinstance(provider, HTTPProvider))

    def test_provider_ipc(self):
        socket_path = str(Path('/tmp/socket.ipc').expanduser().resolve())
        with self.settings(ETHEREUM_NODE_URL='ipc://' + socket_path):
            web3_service = Web3ServiceProvider()
            provider = web3_service.web3.provider
            self.assertTrue(isinstance(provider, IPCProvider))
            self.assertEqual(provider.ipc_path, socket_path)
