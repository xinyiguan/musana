from __future__ import annotations

import typing
from dataclasses import dataclass

import pandas as pd

T = typing.TypeVar('T')


@dataclass
class Sequential:
    _seq: typing.Sequence[T]

    @classmethod
    def from_sequence(cls, sequence: typing.Sequence[T]) -> typing.Self:
        first_object_type = type(sequence[0])
        type_check_pass = all((type(x) == first_object_type for x in sequence))
        if not type_check_pass:
            raise TypeError()
        return cls(_seq=sequence)

    def get_n_grams(self, n: int) -> Sequential:
        length = len(self._seq)
        n_grams = [tuple(self._seq[i:i + n]) for i in range(length - n + 1)]
        n_grams = Sequential.from_sequence(sequence=n_grams)
        return n_grams

    def get_transition_matrix(self, probability: bool) -> pd.DataFrame:
        unique_objects = list(set(self._seq))
        unique_objects = list(map(str, unique_objects))
        transition_matrix = pd.DataFrame(0, columns=unique_objects, index=unique_objects)

        bigrams = self.get_n_grams(n=2)
        for bigram in bigrams._seq:
            source, target = bigram
            transition_matrix.loc[str(source), str(target)] += 1

        if probability:
            transition_prob = transition_matrix.divide(transition_matrix.sum(axis=1), axis=0)
            return transition_prob
        return transition_matrix

    def filter_by_condition(self, condition: typing.Callable[[T, ], bool]) -> Sequential:
        sequence = [x for x in self._seq if condition(x)]
        sequential = self.from_sequence(sequence=sequence)
        return sequential


if __name__ == '__main__':
    pass
