from typing import Tuple
from uuid import uuid4

from opwen_email_server import config
from opwen_email_server.services.auth import EnvironmentAuth
from opwen_email_server.services.queue import AzureQueue
from opwen_email_server.services.storage import AzureTextStorage

STORAGE = AzureTextStorage(account=config.STORAGE_ACCOUNT,
                           key=config.STORAGE_KEY,
                           container=config.CONTAINER_SENDGRID_MIME)

QUEUE = AzureQueue(account=config.STORAGE_ACCOUNT, key=config.STORAGE_KEY,
                   name=config.QUEUE_SENDGRID_MIME)

CLIENTS = EnvironmentAuth()


def receive(client_id: str, email: str) -> Tuple[str, int]:
    if client_id not in CLIENTS:
        return 'client is not registered', 403

    email_id = str(uuid4())

    STORAGE.store_text(email_id, email)

    QUEUE.enqueue({
        '_version': '0.1',
        '_type': 'mime_email_received',
        'resource_id': email_id,
        'container_name': STORAGE.container,
    })

    return 'received', 200
