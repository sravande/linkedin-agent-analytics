from src.quality.data_quality import QUALITY_CHECKS


def test_quality_checks_are_configured():
    assert len(QUALITY_CHECKS) >= 5


def test_required_quality_dimensions_exist():
    checks = " ".join(QUALITY_CHECKS.keys())

    assert "fact_required_keys" in checks
    assert "duplicate_interaction_ids" in checks
    assert "future_events" in checks
    assert "orphan_agents" in checks