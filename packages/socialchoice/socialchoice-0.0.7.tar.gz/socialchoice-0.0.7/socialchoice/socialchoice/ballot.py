import warnings

import networkx as nx
from more_itertools import flatten

from socialchoice import util
from socialchoice.induction.vote_induction import vote_induction


class BallotBox:
    """An interface for the features of ballot boxes. """

    def get_candidates(self) -> set:
        """
        :return: The set of all candidates in this election.
        """
        pass

    def get_victory_graph(self) -> nx.DiGraph:
        """
        A victory graph is a matchup graph of each candidate, but with only edges for wins.
        Every out-edge represents a win over another candidate. Two candidates will not have
        any edge between them if there is a perfect tie (by win ratio).

        See `get_matchup_graph` for a description of the attributes on nodes and edges.
         """
        pass

    def get_matchup_graph(self) -> nx.DiGraph:
        """
        A matchup graph is a fully-connected graph, with each out-edge corresponding to a matchup
        and each in-edge corresponding to the same matchup, but with wins and losses flipped.
        An edge `(a, b)` from a to b will have `wins` corresponding to the number of wins `a`
        has over `b`, while the edge `(b, a)` will have `wins` corresponding to the number of wins
        `b` has over `a`.

        Every edge has the attributes `wins` (described above), `losses`, `ties`, and `margin`.
        `losses` and `ties` are self explanatory, simply the number of losses or ties between
        the two candidates. `margin` is the ratio of wins to overall votes.
        """
        pass

    def get_matchups(self) -> dict:
        """This matchup shows the number of wins and losses each candidate has against each other.
        The shape of the final dictionary returned is:

         >>> {\
            "candidate1": { \
                 {"candidate2": {"win": 12, "loss": 10, "tie": 5}}, \
                 {"candidate3": {"win": 3,  "loss": 23, "tie": 9}}, \
                 # potentially many more \
             }, \
             "candidate2": { \
                 {"candidate1": {"win": 10, "loss": 12, "tie": 5}}, \
                 {"candidate3": {"win": 23, "loss":  3, "tie": 9}}, \
                 # potentially many more \
             },\
             # and so on\
          }

        :return: a matchup mapping, as described above
        """

    def supports_ordering_based_methods(self):
        """Does this ballot box support ordering-based methods? That is, can it produce a set of
        orderings?

        False by default for `PairwiseBallotBox`es.
        If this doesn't return True, ordering-based methods such as Borda count will fail.
        If you want to use Borda count on a PairwiseBallotBox, use `enable_ordering_based_methods`
        """
        return self.get_orderings() is not None

    def get_orderings(self):
        """
        Returns a list of orderings, or None if this ballot box does not have complete orderings.

        All orderings will be lists of sets (or frozensets), with sets representing ties. For
        example:

        ```
        >>> RankedChoiceBallotBox([1, 2, 3], [{2, 3}, 1]).get_orderings()
        [{1}, {2}, {3}], [{2, 3}, {1}]

        >>> from socialchoice import IntransitivityResolverFactory
        >>> from socialchoice import IncompletenessResolverFactory
        >>> ballots = PairwiseBallotBox([1,2,"win"])
        >>> intransitivity_res = IntransitivityResolverFactory(ballots).make_break_random_link()
        >>> incompleteness_res = IncompletenessResolverFactory(ballots).make_add_random_edges()
        >>> ballots.enable_ordering_based_methods(intransitivity_res, incompleteness_res)
        [{"a"}, {"b"}]
        ```
        :return: all the orderings in this BallotBox.
        """

    def enable_ordering_based_methods(self, intransitivity_resolver, incompleteness_resolver):
        """If this election has a ballot box that supports pairwise comparisons but
        not ordering based methods, use the given intransitivity and incompleteness
        resolver to make each pairwise comparison (or, if there are voters, each voter's
        set of pairwise comparisons) into an ordering.

        :param intransitivity_resolver: see socialchoice.pairwise_collapse.resolving_intransitivity
        :param incompleteness_resolver: see socialchoice.pairwise_collapse.resolving_incompleteness
        :return: None
        """
        if self.supports_ordering_based_methods():
            warnings.warn(
                "Enabling ordering-based methods on ballot box which already supports ordering-based methods"
            )


class PairwiseBallotBox(BallotBox):
    """Stores ballots in pairwise form, as in: ["Alice",  "Bob", "win"]"""

    def __init__(self, votes, candidates=None):
        """
        Creates a new PairwiseBallotBox.

        :param votes: An array of votes, where a vote is any indexable object of length 3.
        The first two elements are the ids of the two candidates being voted on, and the third is
        one of "win", "loss", or "tie", indicating the result.

        :param candidates: None, meaning to infer the candidate set from the votes, or a
        collection of the candidates that were being voted on in this election.

        :raises InvalidVoteShapeException: if given any vote with length != 3
        """
        votes = list(votes)
        self.ballots = self.__ensure_valid_votes(votes)
        self.ordering_ballot_box = None
        self.candidates = candidates or self.__get_all_candidates_from_votes(self.ballots)

    @staticmethod
    def __get_all_candidates_from_votes(votes) -> set:
        """:return: All the candidates mentioned in the votes"""
        return {vote[0] for vote in votes} | {vote[1] for vote in votes}

    @staticmethod
    def __ensure_valid_votes(votes: iter) -> list:
        for vote in votes:
            if not len(vote) == 3:
                raise InvalidBallotDataException(
                    "Expected a vote of length three, got " + str(vote)
                )

            if not vote[2] in {"win", "loss", "tie"}:
                raise InvalidBallotDataException(
                    """Expected type to be one of {"win", "loss", "tie"}, got""" + str(vote)
                )

        return list(votes)

    def get_candidates(self) -> set:
        return self.candidates

    def get_victory_graph(self) -> nx.DiGraph:
        matchups = self.get_matchup_graph()
        edges_to_remove = []
        for u, v in matchups.edges:
            margin_u_to_v = matchups.get_edge_data(u, v)["margin"]
            margin_v_to_u = matchups.get_edge_data(v, u)["margin"]

            # u->v has lower win margin than v->u, keep the "winning edge" with higher win ratio
            # this will remove both if there is a perfect tie - but that's okay
            if margin_u_to_v <= margin_v_to_u:
                edges_to_remove.append((u, v))

        matchups.remove_edges_from(edges_to_remove)
        return matchups

    def get_matchup_graph(self) -> nx.DiGraph:
        matchups = self.get_matchups()
        ids = matchups.keys()

        g = nx.DiGraph()
        g.add_nodes_from(ids)
        for candidate1 in matchups:
            for candidate2 in matchups[candidate1]:
                candidate1to2 = matchups[candidate1][candidate2]
                total_votes_candidate1to2 = sum(candidate1to2.values())
                if total_votes_candidate1to2 != 0:
                    g.add_edge(
                        candidate1,
                        candidate2,
                        wins=candidate1to2["wins"],
                        losses=candidate1to2["losses"],
                        ties=candidate1to2["ties"],
                        margin=candidate1to2["wins"] / total_votes_candidate1to2,
                    )

                candidate2to1 = matchups[candidate2][candidate1]
                total_votes_candidate2to1 = sum(candidate2to1.values())
                if total_votes_candidate2to1 != 0:
                    g.add_edge(
                        candidate2,
                        candidate1,
                        wins=candidate2to1["wins"],
                        losses=candidate2to1["losses"],
                        ties=candidate2to1["ties"],
                        margin=candidate2to1["wins"] / total_votes_candidate2to1,
                    )

        return g

    def get_matchups(self) -> dict:
        matchups = {}
        for candidate in self.candidates:
            matchups[candidate] = {}

        for candidate1 in self.candidates:
            for candidate2 in self.candidates:
                if candidate1 == candidate2:
                    continue
                matchups[candidate1][candidate2] = {"wins": 0, "losses": 0, "ties": 0}
                matchups[candidate2][candidate1] = {"wins": 0, "losses": 0, "ties": 0}

        for vote in self.ballots:
            candidate1, candidate2, result = vote
            if result == "win":
                matchups[candidate1][candidate2]["wins"] += 1
                matchups[candidate2][candidate1]["losses"] += 1
            if result == "loss":
                matchups[candidate1][candidate2]["losses"] += 1
                matchups[candidate2][candidate1]["wins"] += 1
            if result == "tie":
                matchups[candidate1][candidate2]["ties"] += 1
                matchups[candidate2][candidate1]["ties"] += 1

        return matchups

    def get_orderings(self):
        if self.ordering_ballot_box is None:
            return None
        else:
            return self.ordering_ballot_box.get_orderings()

    def enable_ordering_based_methods(self, intransitivity_resolver, incompleteness_resolver):
        super().enable_ordering_based_methods(intransitivity_resolver, incompleteness_resolver)
        self.ordering_ballot_box = RankedChoiceBallotBox(
            [
                vote_induction([ballot], intransitivity_resolver, incompleteness_resolver)
                for ballot in self.ballots
            ]
        )


class VoterTrackingPairwiseBallotBox(BallotBox):
    """
    Like a PairwiseBallotBox, but keeps track of which voter submitted which vote. There is no
    different in the two for pairwise methods, but if you are converting voters vote sets to
    orderings with `enable_ordering_based_methods`, this will be faster and more accurate.
    Because it can process each voter's set of votes together, the resulting orderings will capture
    more of the underlying data, and the conversion only has to happen once.
    """

    def __init__(self, votes, candidates=None):
        """

        :param votes: An iterable of votes, where a vote is any indexable object of length 4. The
        first three elements must be the same as PairwiseBallotBox, and the fourth indicates the
        id of the voter who placed the vote.

        :param candidates: None, meaning to infer the candidate set from the votes, or a
                           collection of the candidates that were being voted on in this election.

        :raises InvalidVoteShapeException: if given any invalid votes
        """
        self.votes = list(votes)
        # Lean on PairwiseBallotBox for pairwise methods. We don't care about who placed a vote
        # if all that matters is the number of wins/losses/ties in each matchup.
        votes_without_voter_ids = [v[0:3] for v in votes]
        self.pairwise_ballot_box = PairwiseBallotBox(votes_without_voter_ids, candidates)

        # Lazily initialize the ordering ballot box.
        self.ordering_ballot_box = None

    def get_candidates(self) -> set:
        return self.pairwise_ballot_box.candidates

    def get_victory_graph(self) -> nx.DiGraph:
        return self.pairwise_ballot_box.get_victory_graph()

    def get_matchup_graph(self) -> nx.DiGraph:
        return self.pairwise_ballot_box.get_matchup_graph()

    def get_matchups(self) -> dict:
        return self.pairwise_ballot_box.get_matchups()

    def supports_ordering_based_methods(self):
        return self.ordering_ballot_box is None

    def get_orderings(self):
        if self.ordering_ballot_box:
            return self.ordering_ballot_box.get_orderings()
        else:
            return None

    def enable_ordering_based_methods(self, intransitivity_resolver, incompleteness_resolver):
        voter_to_vote_set = {}

        for vote in self.votes:
            vote_content = vote[0:3]
            voter = vote[3]
            if voter in voter_to_vote_set:
                voter_to_vote_set[voter].append(vote_content)
            else:
                voter_to_vote_set[voter] = [vote_content]

        # Now, voter_to_vote_set is a mapping from a voter to a set of orderings. We want to
        # create an ordering for each.

        orderings = []
        for voter, vote_set in voter_to_vote_set.items():
            orderable_set = incompleteness_resolver(intransitivity_resolver(vote_set))
            ordering = list(nx.topological_sort(orderable_set))
            orderings.append(ordering)

        # And then use those orderings as the basis for our ordering methods. One per voter.
        self.ordering_ballot_box = RankedChoiceBallotBox(orderings, self.get_candidates())


class RankedChoiceBallotBox(BallotBox):
    def __init__(self, ballots, candidates=None):
        """Creates a RankedChoiceBallotBox from the given ballots. Each ballot must be a list, where
        each element is either a candidate or a set of candidates. A single candidate in a ballot
        represents that candidate being at that position, and a set represents a tie for that
        position.

        Each ballot must contain every candidate found in candidates, or if candidates is not
        provided, the candidates mentioned in every other ballot.

        :param ballots: a list of ballots, as described above.
        :param candidates: the set of candidates being voted on. Inferred from ballots if not
        provided.
        """
        self.ballots = self.__ensure_valid_ballots(ballots, candidates)
        self.ballots_all_sets = self.__convert_to_sets(self.ballots)

        # We want to convert to pairwise ballots because there's no use reimplementing the code in
        # PairwiseBallotBox for rankings, we can just convert a ranking to its constituent
        # pairwise preferences and create our own PairwiseBallotBox that we can forward
        # requests for pairwise-result based rankings to.
        pairwise_ballots = flatten(
            util.ranking_to_pairwise_ballots(ballot) for ballot in self.ballots_all_sets
        )

        self.pairwise_ballot_box = PairwiseBallotBox(pairwise_ballots)

    def get_candidates(self) -> set:
        return self.pairwise_ballot_box.candidates

    def get_victory_graph(self) -> nx.DiGraph:
        return self.pairwise_ballot_box.get_victory_graph()

    def get_matchup_graph(self) -> nx.DiGraph:
        return self.pairwise_ballot_box.get_matchup_graph()

    def get_matchups(self) -> dict:
        return self.pairwise_ballot_box.get_matchups()

    def __ensure_valid_ballots(self, ballots, candidates):
        if not len(ballots):
            raise InvalidBallotDataException(
                "Cannot create RankedChoiceBallotBox with empty ballot list"
            )
        for ballot in ballots:
            if not isinstance(ballot, list):
                raise InvalidBallotDataException(
                    f"Ballots must be a collection of lists, one ballot was {ballot}"
                )

        # Need to either get or infer the candidate set to validate that ballots are full, and to
        # ensure that each ballot doesn't contain elements not in the candidate set.
        if candidates:
            candidate_set = set(candidates)
            if not len(candidates) == len(candidate_set):
                raise InvalidElectionDataException(f"Duplicate candidates in {candidates}")
        else:
            candidate_set = set()
            for ballot in ballots:
                try:
                    candidate_set |= util.candidates_in_ranked_choice_ballot(ballot)
                except ValueError as e:
                    raise InvalidBallotDataException(e)

        for ballot in ballots:
            try:
                ballot_contents = util.candidates_in_ranked_choice_ballot(ballot)
            except ValueError as e:
                raise InvalidBallotDataException(e)

            if ballot_contents != candidate_set:
                raise InvalidBallotDataException(
                    f"Ballot {ballot} did not contain exactly {candidate_set}."
                )

        return ballots

    def __convert_to_sets(self, ballots):
        """Takes ballots, which may include single items at rankings which do not have ties, into a list of sets."""
        return [util.ranking_with_all_sets(b) for b in ballots]

    def get_orderings(self):
        return self.ballots_all_sets


class InvalidElectionDataException(Exception):
    """Raised if there is invalid data somewhere other than the ballots."""


class InvalidBallotDataException(Exception):
    """Raised if a ballot has invalid data, for example, contains a candidate not in the list of candidates."""
