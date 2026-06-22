import os
import pytest
from db import init_db, save_score, get_top_scores, get_all_scores, clear_scores, get_player_best


@pytest.fixture
def tmp_db(tmp_path):
    db_file = str(tmp_path / "test_scores.db")
    init_db(db_file)
    return db_file


# ---------- init_db ----------

def test_init_db_creates_file(tmp_path):
    db_file = str(tmp_path / "new_scores.db")
    init_db(db_file)
    assert os.path.exists(db_file)


def test_init_db_idempotent(tmp_path):
    db_file = str(tmp_path / "scores.db")
    init_db(db_file)
    init_db(db_file)
    assert os.path.exists(db_file)


# ---------- save_score ----------

def test_save_score_success(tmp_db):
    save_score("Alice", 5, 1, 100, tmp_db)
    scores = get_all_scores(tmp_db)
    assert len(scores) == 1
    assert scores[0][0] == "Alice"
    assert scores[0][1] == 5


def test_save_score_strips_whitespace(tmp_db):
    save_score("  Bob  ", 3, 1, 100, tmp_db)
    scores = get_all_scores(tmp_db)
    assert scores[0][0] == "Bob"


def test_save_score_stores_range(tmp_db):
    save_score("Charlie", 7, 1, 200, tmp_db)
    scores = get_all_scores(tmp_db)
    assert scores[0][2] == 1
    assert scores[0][3] == 200


def test_save_score_empty_name_raises(tmp_db):
    with pytest.raises(ValueError):
        save_score("", 5, 1, 100, tmp_db)


def test_save_score_whitespace_name_raises(tmp_db):
    with pytest.raises(ValueError):
        save_score("   ", 5, 1, 100, tmp_db)


def test_save_score_zero_attempts_raises(tmp_db):
    with pytest.raises(ValueError):
        save_score("Alice", 0, 1, 100, tmp_db)


def test_save_score_negative_attempts_raises(tmp_db):
    with pytest.raises(ValueError):
        save_score("Alice", -1, 1, 100, tmp_db)


# ---------- get_top_scores ----------

def test_get_top_scores_sorted_by_attempts(tmp_db):
    save_score("Alice", 10, 1, 100, tmp_db)
    save_score("Bob", 3, 1, 100, tmp_db)
    save_score("Charlie", 7, 1, 100, tmp_db)
    scores = get_top_scores(10, tmp_db)
    attempts = [s[1] for s in scores]
    assert attempts == sorted(attempts)


def test_get_top_scores_respects_limit(tmp_db):
    for i in range(15):
        save_score(f"Player{i}", i + 1, 1, 100, tmp_db)
    scores = get_top_scores(10, tmp_db)
    assert len(scores) == 10


def test_get_top_scores_empty_db(tmp_db):
    assert get_top_scores(10, tmp_db) == []


def test_get_top_scores_first_is_best(tmp_db):
    save_score("Alice", 10, 1, 100, tmp_db)
    save_score("Bob", 3, 1, 100, tmp_db)
    scores = get_top_scores(10, tmp_db)
    assert scores[0][0] == "Bob"


# ---------- get_all_scores ----------

def test_get_all_scores_returns_all(tmp_db):
    save_score("A", 5, 1, 100, tmp_db)
    save_score("B", 3, 1, 100, tmp_db)
    save_score("C", 8, 1, 100, tmp_db)
    assert len(get_all_scores(tmp_db)) == 3


def test_get_all_scores_empty(tmp_db):
    assert get_all_scores(tmp_db) == []


# ---------- clear_scores ----------

def test_clear_scores_empties_table(tmp_db):
    save_score("Alice", 5, 1, 100, tmp_db)
    clear_scores(tmp_db)
    assert get_all_scores(tmp_db) == []


def test_clear_scores_on_empty_db(tmp_db):
    clear_scores(tmp_db)
    assert get_all_scores(tmp_db) == []


# ---------- get_player_best ----------

def test_get_player_best_returns_minimum(tmp_db):
    save_score("Alice", 10, 1, 100, tmp_db)
    save_score("Alice", 5, 1, 100, tmp_db)
    save_score("Alice", 8, 1, 100, tmp_db)
    row = get_player_best("Alice", tmp_db)
    assert row[1] == 5


def test_get_player_best_not_found_returns_none(tmp_db):
    assert get_player_best("Unknown", tmp_db) is None


def test_get_player_best_empty_name_raises(tmp_db):
    with pytest.raises(ValueError):
        get_player_best("", tmp_db)


def test_get_player_best_whitespace_name_raises(tmp_db):
    with pytest.raises(ValueError):
        get_player_best("   ", tmp_db)


def test_get_player_best_ignores_other_players(tmp_db):
    save_score("Alice", 3, 1, 100, tmp_db)
    save_score("Bob", 1, 1, 100, tmp_db)
    row = get_player_best("Alice", tmp_db)
    assert row[0] == "Alice"
    assert row[1] == 3
