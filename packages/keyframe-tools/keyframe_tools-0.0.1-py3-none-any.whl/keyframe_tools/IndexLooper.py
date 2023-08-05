from keyframe_tools import utils


class IndexLooper:

    def __init__(
            self,
            num_elements,
            num_repetitions=1,
            is_move_forward_then_backwards=False,
            is_only_jump_forward=False,
    ):
        if num_elements < 2:
            raise ValueError(f"num_elements should be greater than 1: {num_elements}")
        if num_repetitions < 1:
            raise ValueError(f"_repetitions should be greater than 0: {num_repetitions}")

        self._is_move_forward_then_backwards = is_move_forward_then_backwards
        self._index_list = [i for i in range(num_elements)]
        if is_move_forward_then_backwards:
            self._index_list += self._index_list[-2::-1]

        self._is_only_jump_forward = is_only_jump_forward

        self._current_index = None

        self._repetitions = num_repetitions
        self._repetitions_done = 0

    @property
    def idx(self):
        if self._current_index is None:
            idx = 0
        else:
            idx = self._current_index
        return self._index_list[idx]

    @property
    def reps_left(self):
        return self._repetitions - self._repetitions_done

    @property
    def is_finished(self):
        return self.reps_left <= 0

    def increment_index(self):
        """
        Advance the index while there are still _repetitions to do.

        Note that the first step steps into the 0th index.

        When the _repetitions are done for the forward loop, it stops at the last index;
        when the _repetitions are done for the forward and last loop, it stops at the first index
        :return:
        """
        if self._current_index is None:
            self._current_index = 0
        elif self.reps_left > 0:

            self._current_index = self._current_index + 1

            if self._current_index >= len(self._index_list):
                self._repetitions_done += 1
                if self.is_finished:
                    self._current_index = 0 if self._is_move_forward_then_backwards else self._current_index-1
                else:
                    self._current_index = 1 if self._is_move_forward_then_backwards else 0
        return self.idx

    def jump_normalized_index(self, normalized_value):
        idx = utils.get_proportional_index(normalized_value, len(self._index_list))
        if self._is_only_jump_forward and self._current_index is not None:
            if idx > self._current_index:
                self._current_index = idx
        else:
            self._current_index = idx
        return self.idx

    def reset(self):
        self._current_index = None
        self._repetitions_done = 0


if __name__ == '__main__':

    _num_elements = 2
    _num_repetitions = 3
    _looper = IndexLooper(_num_elements, _num_repetitions, is_move_forward_then_backwards=True)

    print(f"here is an example of the _looper working for {_num_elements} elements with {_num_repetitions} _repetitions")
    print([_looper.increment_index() for _ in range(1 + _num_repetitions * 2 * (_num_elements - 1))])
    print("after the _looper has gone through all elements for the number of repetitons, it outputs the last value")
    print([_looper.increment_index() for _ in range(5)])
