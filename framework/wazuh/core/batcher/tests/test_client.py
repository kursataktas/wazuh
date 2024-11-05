from unittest.mock import patch, AsyncMock, call

import pytest

from framework.wazuh.core.batcher.client import BatcherClient
from wazuh.core.indexer.bulk import Operation
from wazuh.core.indexer.models.events import AgentMetadata, SCAEvent, StatefulEvent, Module, ModuleName


@patch("wazuh.core.batcher.mux_demux.MuxDemuxQueue")
def test_send_event(queue_mock):
    """Check that the `send_event` method works as expected."""
    batcher = BatcherClient(queue=queue_mock)
    agent_metadata = AgentMetadata(
        uuid='ac5f7bed-363a-4095-bc19-5c1ebffd1be0',
        groups=[],
        type='endpoint',
        os='Debian 12',
        platform='Linux',
        arch='x86_64',
        version='v5.0.0',
        ip='127.0.0.1'
    )
    document_id = '1234'
    event = StatefulEvent(
        document_id=document_id,
        operation=Operation.CREATE,
        module=Module(name=ModuleName.SCA),
        data=SCAEvent()
    )

    item_id = batcher.send_event(agent_metadata, event)
    assert item_id == document_id
    queue_mock.send_to_mux.assert_called_once()


@pytest.mark.asyncio
@patch("wazuh.core.batcher.mux_demux.MuxDemuxQueue")
async def test_get_response(queue_mock):
    """Check that the `get_response` method works as expected."""
    batcher = BatcherClient(queue=queue_mock)

    event = {"data": "test event"}
    expected_uid = 1234

    queue_mock.is_response_pending.return_value = False
    queue_mock.receive_from_demux.return_value = event

    result = await batcher.get_response(expected_uid)

    queue_mock.is_response_pending.assert_called_once_with(expected_uid)
    assert result == event


@pytest.mark.asyncio
@patch("wazuh.core.batcher.mux_demux.MuxDemuxQueue")
@patch("asyncio.sleep", new_callable=AsyncMock)
async def test_get_response_wait(sleep_mock, queue_mock):
    """Check that the `get_response` method works as expected with no response."""
    batcher = BatcherClient(queue=queue_mock)

    event = {"data": "test event"}
    expected_uid = "ac5f7bed-363a-4095-bc19-5c1ebffd1be0"

    queue_mock.is_response_pending.side_effect = [True, False]
    queue_mock.receive_from_demux.return_value = event

    result = await batcher.get_response(expected_uid)

    queue_mock.is_response_pending.assert_has_calls([call(expected_uid), call(expected_uid)])
    sleep_mock.assert_awaited()
    assert result == event
