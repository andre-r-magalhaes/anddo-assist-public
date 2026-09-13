# tests/test_waba_dto.py
import json
from pathlib import Path

from adapters.waba_dto import WabaDTO


def test_waba_payload_is_converted_to_client_model():
    payload_path = Path(__file__).parent / "waba_payload.json"
    payload = json.loads(payload_path.read_text(encoding="utf-8"))

    client = WabaDTO(**payload).to_model()

    assert client is not None
    assert client.client_id == "00000000000"
    assert len(client.msg_history) == 1