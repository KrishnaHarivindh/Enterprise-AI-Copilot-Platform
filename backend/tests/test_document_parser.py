from app.services.document_parser import extract_text
from app.services.document_service import estimate_chunk_count, get_extension
from app.services.chunk_service import chunk_text
from app.services.agent_service import create_meeting_notes


def test_extract_plain_text(tmp_path):
    file_path = tmp_path / "notes.txt"
    file_path.write_text("Enterprise knowledge platform", encoding="utf-8")

    assert extract_text(file_path, "txt") == "Enterprise knowledge platform"


def test_extract_markdown_as_plain_text(tmp_path):
    file_path = tmp_path / "readme.md"
    file_path.write_text("# Project\nDocument intelligence", encoding="utf-8")

    assert "Document intelligence" in extract_text(file_path, "md")


def test_extract_csv_text(tmp_path):
    file_path = tmp_path / "metrics.csv"
    file_path.write_text("name,value\nDocuments,3\n", encoding="utf-8")

    extracted_text = extract_text(file_path, "csv")

    assert "Documents" in extracted_text
    assert "value" in extracted_text


def test_document_helpers():
    assert get_extension("Policy.PDF") == "pdf"
    assert estimate_chunk_count("") == 0
    assert estimate_chunk_count("x" * 1201) == 2


def test_chunk_text_with_overlap():
    chunks = chunk_text("abcdefghij", chunk_size=4, overlap=1)

    assert chunks == ["abcd", "defg", "ghij"]


def test_meeting_notes_agent_extracts_actions_and_decisions():
    notes = create_meeting_notes("Agreed to ship v1.\nAction: Hari will prepare demo.")

    assert notes["decisions"]
    assert notes["action_items"]
