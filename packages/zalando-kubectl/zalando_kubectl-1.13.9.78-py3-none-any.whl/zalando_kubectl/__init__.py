# This is replaced during release process.
# flake8: noqa
__version_suffix__ = '78'

APP_NAME = "zalando-kubectl"

KUBECTL_VERSION = 'v1.13.9'
KUBECTL_SHA512 = {
    'linux': '8c76e782e6aab12f21447d3e5b9241b0d8e4d4058fe16972c62d91dc92b130d646693fd497be9318a284c94a7a1856e42b95c3aac725fe8927ef96d66593e6f5',
    'darwin': 'f08a3b1a490a5ec2611951df1a164d949aaa7b66003a40fb27e5863a86862e9a339e90f13fdaa2e09d863bc5370d9618a18ffefbcee40d253fd293288aca1aa9'
}

STERN_VERSION = '1.10.0'
STERN_SHA256 = {
    'linux': 'a0335b298f6a7922c35804bffb32a68508077b2f35aaef44d9eb116f36bc7eda',
    'darwin': 'b91dbcfd3bbda69cd7a7abd80a225ce5f6bb9d6255b7db192de84e80e4e547b7'
}

APP_VERSION = KUBECTL_VERSION + "." + __version_suffix__
