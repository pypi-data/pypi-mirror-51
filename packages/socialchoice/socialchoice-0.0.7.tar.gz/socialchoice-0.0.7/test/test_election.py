import pytest

from socialchoice import Election, PairwiseBallotBox, RankedChoiceBallotBox

empty_election = Election(PairwiseBallotBox([]))
example_votes = PairwiseBallotBox(
    [[0, 1, "win"], [3, 2, "loss"], [2, 3, "win"], [0, 3, "tie"], [3, 0, "win"]]
)


def test_get_ranked_pairs_ranking():
    """Tests that ranked_pairs on a pairwise ballot box produces the correct outcome."""
    assert empty_election.ranking_by_ranked_pairs() == []

    e_1 = Election(example_votes)
    assert e_1.ranking_by_ranked_pairs() == [2, 3, 0, 1]


def test_get_win_ratio():
    assert empty_election.ranking_by_win_ratio() == []

    e_1 = Election(example_votes)
    assert e_1.ranking_by_win_ratio(include_score=True) == [
        (2, 1.0),
        (0, 0.5),
        (3, 1 / 3),
        (1, 0.0),
    ]


def test_get_win_tie_ratio():
    assert empty_election.ranking_by_win_tie_ratio() == []

    e_1 = Election(example_votes)
    assert e_1.ranking_by_win_tie_ratio(include_score=True) == [
        (2, 1.0),
        (0, 2 / 3),
        (3, 0.5),
        (1, 0.0),
    ]


def test_flatten_ties():
    election = Election(PairwiseBallotBox([(1, 2, "win"), (3, 4, "win")], candidates={1, 2, 3, 4}))
    ranking = election.ranking_by_win_ratio(group_ties=True, include_score=True)
    assert ranking == [[(1, 1.0), (3, 1.0)], [(2, 0.0)]]


def test_borda_count_pairwise_raises_ballot_type_error():
    with pytest.raises(ValueError):
        Election(PairwiseBallotBox([])).ranking_by_borda_count()


def test_borda_count_ranked_choice():
    ballots = RankedChoiceBallotBox([[1, 2, 3]])
    election = Election(ballots)
    # assert election.ranking_by_borda_count() == [1, 2, 3]
    assert election.ranking_by_borda_count(include_score=True) == [(1, 2), (2, 1), (3, 0)]


def test_borda_count_ranked_choice_with_ties():
    ballots = RankedChoiceBallotBox([[1, 2, 3], [{1, 2, 3}], [1, {2, 3}]])
    election = Election(ballots)
    # assert election.ranking_by_borda_count() == [1, 2, 3]
    assert election.ranking_by_borda_count(include_score=True) == [(1, 4), (2, 1), (3, 0)]
