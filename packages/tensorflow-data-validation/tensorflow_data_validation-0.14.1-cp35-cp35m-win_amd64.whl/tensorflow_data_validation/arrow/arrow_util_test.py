# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License
"""Tests for tensorflow_data_validation.arrow.arrow_util."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools

from absl.testing import absltest
from absl.testing import parameterized
import numpy as np
import six
from tensorflow_data_validation import types
from tensorflow_data_validation.arrow import arrow_util
from tensorflow_data_validation.pyarrow_tf import pyarrow as pa


class ArrowUtilTest(absltest.TestCase):

  def test_invalid_input_type(self):

    functions_expecting_list_array = [
        arrow_util.ListLengthsFromListArray,
        arrow_util.GetFlattenedArrayParentIndices,
    ]
    functions_expecting_array = [arrow_util.GetArrayNullBitmapAsByteArray]
    functions_expecting_binary_array = [arrow_util.GetBinaryArrayTotalByteSize]
    for f in itertools.chain(functions_expecting_list_array,
                             functions_expecting_array,
                             functions_expecting_binary_array):
      with self.assertRaisesRegex(RuntimeError, "Could not unwrap Array"):
        f(1)

    for f in functions_expecting_list_array:
      with self.assertRaisesRegex(RuntimeError, "Expected ListArray but got"):
        f(pa.array([1, 2, 3]))

    for f in functions_expecting_binary_array:
      with self.assertRaisesRegex(RuntimeError, "Expected BinaryArray"):
        f(pa.array([[1, 2, 3]]))

  def test_list_lengths(self):
    list_lengths = arrow_util.ListLengthsFromListArray(
        pa.array([], type=pa.list_(pa.int64())))
    self.assertTrue(list_lengths.equals(pa.array([], type=pa.int32())))
    list_lengths = arrow_util.ListLengthsFromListArray(
        pa.array([[1., 2.], [], [3.]]))
    self.assertTrue(list_lengths.equals(pa.array([2, 0, 1], type=pa.int32())))
    list_lengths = arrow_util.ListLengthsFromListArray(
        pa.array([[1., 2.], None, [3.]]))
    self.assertTrue(list_lengths.equals(pa.array([2, 0, 1], type=pa.int32())))

  def test_get_array_null_bitmap_as_byte_array(self):
    array = pa.array([], type=pa.int32())
    null_masks = arrow_util.GetArrayNullBitmapAsByteArray(array)
    self.assertTrue(null_masks.equals(pa.array([], type=pa.uint8())))

    array = pa.array([1, 2, None, 3, None], type=pa.int32())
    null_masks = arrow_util.GetArrayNullBitmapAsByteArray(array)
    self.assertTrue(
        null_masks.equals(pa.array([0, 0, 1, 0, 1], type=pa.uint8())))

    array = pa.array([1, 2, 3])
    null_masks = arrow_util.GetArrayNullBitmapAsByteArray(array)
    self.assertTrue(null_masks.equals(pa.array([0, 0, 0], type=pa.uint8())))

    array = pa.array([None, None, None], type=pa.int32())
    null_masks = arrow_util.GetArrayNullBitmapAsByteArray(array)
    self.assertTrue(null_masks.equals(pa.array([1, 1, 1], type=pa.uint8())))
    # Demonstrate that the returned array can be converted to a numpy boolean
    # array w/o copying
    np.testing.assert_equal(
        np.array([True, True, True]), null_masks.to_numpy().view(np.bool))

  def test_get_flattened_array_parent_indices(self):
    indices = arrow_util.GetFlattenedArrayParentIndices(
        pa.array([], type=pa.list_(pa.int32())))
    self.assertTrue(indices.equals(pa.array([], type=pa.int32())))

    indices = arrow_util.GetFlattenedArrayParentIndices(
        pa.array([[1.], [2.], [], [3.]]))
    self.assertTrue(indices.equals(pa.array([0, 1, 3], type=pa.int32())))

  def test_get_binary_array_total_byte_size(self):
    binary_array = pa.array([b"abc", None, b"def", b"", b"ghi"])
    self.assertEqual(9, arrow_util.GetBinaryArrayTotalByteSize(binary_array))
    sliced_1_2 = binary_array.slice(1, 2)
    self.assertEqual(3, arrow_util.GetBinaryArrayTotalByteSize(sliced_1_2))
    sliced_2 = binary_array.slice(2)
    self.assertEqual(6, arrow_util.GetBinaryArrayTotalByteSize(sliced_2))

    unicode_array = pa.array([u"abc"])
    self.assertEqual(3, arrow_util.GetBinaryArrayTotalByteSize(unicode_array))

    empty_array = pa.array([], type=pa.binary())
    self.assertEqual(0, arrow_util.GetBinaryArrayTotalByteSize(empty_array))

  def _value_counts_struct_array_to_dict(self, value_counts):
    result = {}
    for value_count in value_counts:
      value_count = value_count.as_py()
      result[value_count["values"]] = value_count["counts"]
    return result

  def test_value_counts_binary(self):
    binary_array = pa.array([b"abc", b"ghi", b"def", b"ghi", b"ghi", b"def"])
    expected_result = {b"abc": 1, b"ghi": 3, b"def": 2}
    self.assertDictEqual(self._value_counts_struct_array_to_dict(
        arrow_util.ValueCounts(binary_array)), expected_result)

  def test_value_counts_integer(self):
    int_array = pa.array([1, 4, 1, 3, 1, 4])
    expected_result = {1: 3, 4: 2, 3: 1}
    self.assertDictEqual(self._value_counts_struct_array_to_dict(
        arrow_util.ValueCounts(int_array)), expected_result)

  def test_value_counts_empty(self):
    empty_array = pa.array([])
    expected_result = {}
    self.assertDictEqual(self._value_counts_struct_array_to_dict(
        arrow_util.ValueCounts(empty_array)), expected_result)

_MAKE_LIST_ARRAY_INVALID_INPUT_TEST_CASES = [
    dict(
        testcase_name="invalid_parent_index",
        num_parents=None,
        parent_indices=np.array([0], dtype=np.int64),
        values=pa.array([1]),
        expected_error=RuntimeError,
        expected_error_regexp="Expected integer"),
    dict(
        testcase_name="parent_indices_not_np",
        num_parents=1,
        parent_indices=[0],
        values=pa.array([1]),
        expected_error=TypeError,
        expected_error_regexp="to be a numpy array"
        ),
    dict(
        testcase_name="parent_indices_not_1d",
        num_parents=1,
        parent_indices=np.array([[0]], dtype=np.int64),
        values=pa.array([1]),
        expected_error=TypeError,
        expected_error_regexp="to be a 1-D int64 numpy array"
    ),
    dict(
        testcase_name="parent_indices_not_int64",
        num_parents=1,
        parent_indices=np.array([0], dtype=np.int32),
        values=pa.array([1]),
        expected_error=TypeError,
        expected_error_regexp="to be a 1-D int64 numpy array"
    ),
    dict(
        testcase_name="parent_indices_length_not_equal_to_values_length",
        num_parents=1,
        parent_indices=np.array([0], dtype=np.int64),
        values=pa.array([1, 2]),
        expected_error=RuntimeError,
        expected_error_regexp="values array and parent indices array must be of the same length"
    ),
    dict(
        testcase_name="num_parents_too_small",
        num_parents=1,
        parent_indices=np.array([1], dtype=np.int64),
        values=pa.array([1]),
        expected_error=RuntimeError,
        expected_error_regexp="Found a parent index 1 while num_parents was 1"
        )
]


_MAKE_LIST_ARRAY_TEST_CASES = [
    dict(
        testcase_name="parents_are_all_empty",
        num_parents=5,
        parent_indices=np.array([], dtype=np.int64),
        values=pa.array([], type=pa.int64()),
        expected=pa.array([None, None, None, None, None],
                          type=pa.list_(pa.int64()))),
    dict(
        testcase_name="long_num_parent",
        num_parents=(long(1) if six.PY2 else 1),
        parent_indices=np.array([0], dtype=np.int64),
        values=pa.array([1]),
        expected=pa.array([[1]])
    ),
    dict(
        testcase_name="leading nones",
        num_parents=3,
        parent_indices=np.array([2], dtype=np.int64),
        values=pa.array([1]),
        expected=pa.array([None, None, [1]]),
    ),
    dict(
        testcase_name="same_parent_and_holes",
        num_parents=4,
        parent_indices=np.array([0, 0, 0, 3, 3], dtype=np.int64),
        values=pa.array(["a", "b", "c", "d", "e"]),
        expected=pa.array([["a", "b", "c"], None, None, ["d", "e"]])
    )
]


class MakeListArrayFromParentIndicesAndValuesTest(parameterized.TestCase):

  @parameterized.named_parameters(*_MAKE_LIST_ARRAY_INVALID_INPUT_TEST_CASES)
  def testInvalidInput(self, num_parents, parent_indices, values,
                       expected_error, expected_error_regexp):
    with self.assertRaisesRegex(expected_error, expected_error_regexp):
      arrow_util.MakeListArrayFromParentIndicesAndValues(
          num_parents, parent_indices, values)

  @parameterized.named_parameters(*_MAKE_LIST_ARRAY_TEST_CASES)
  def testMakeListArray(self, num_parents, parent_indices, values, expected):
    actual = arrow_util.MakeListArrayFromParentIndicesAndValues(
        num_parents, parent_indices, values)
    self.assertTrue(
        actual.equals(expected),
        "actual: {}, expected: {}".format(actual, expected))


class EnumerateArraysTest(absltest.TestCase):

  def testInvalidWeightColumn(self):
    with self.assertRaisesRegex(
        ValueError,
        "weight feature must have exactly one value in each example"):
      for _ in arrow_util.enumerate_arrays(
          pa.Table.from_arrays([pa.array([[1], [2, 3]]),
                                pa.array([[1], []])], ["v", "w"]),
          weight_column="w",
          enumerate_leaves_only=False):
        pass

  def testEnumerate(self):
    input_table = pa.Table.from_arrays([
        pa.array([[1], [2, 3]]),
        pa.array([[{
            "sf1": [["a", "b"]]
        }], [{
            "sf2": [{
                "ssf1": [[3], [4]]
            }]
        }]]),
        pa.array([[1.0], [2.0]])
    ], ["f1", "f2", "w"])
    possible_results = {
        types.FeaturePath(["f1"]): (pa.array([[1], [2, 3]]), [1.0, 2.0]),
        types.FeaturePath(["w"]): (pa.array([[1.0], [2.0]]), None),
        types.FeaturePath(["f2"]): (pa.array([[{
            "sf1": [["a", "b"]]
        }], [{
            "sf2": [{
                "ssf1": [[3], [4]]
            }]
        }]]), [1.0, 2.0]),
        types.FeaturePath(["f2", "sf1"]): (
            pa.array([[["a", "b"]], None]), [1.0, 2.0]),
        types.FeaturePath(["f2", "sf2"]): (
            pa.array([None, [{"ssf1": [[3], [4]]}]]), [1.0, 2.0]),
        types.FeaturePath(["f2", "sf2", "ssf1"]): (
            pa.array([[[3], [4]]]), [2.0]),
    }
    for leaves_only, has_weights in itertools.combinations_with_replacement(
        [True, False], 2):
      actual_results = {}
      for feature_path, feature_array, weights in arrow_util.enumerate_arrays(
          input_table, "w" if has_weights else None, leaves_only):
        actual_results[feature_path] = (feature_array, weights)

      expected_results = {}
      for p in [["f1"], ["f2", "sf1"], ["f2", "sf2", "ssf1"]]:
        feature_path = types.FeaturePath(p)
        expected_results[feature_path] = (possible_results[feature_path][0],
                                          possible_results[feature_path][1]
                                          if has_weights else None)
      if not has_weights:
        expected_results[types.FeaturePath(
            ["w"])] = possible_results[types.FeaturePath(["w"])]
      if not leaves_only:
        for p in [["f2"], ["f2", "sf2"]]:
          feature_path = types.FeaturePath(p)
          expected_results[feature_path] = (possible_results[feature_path][0],
                                            possible_results[feature_path][1]
                                            if has_weights else None)

      self.assertLen(actual_results, len(expected_results))
      for k, v in six.iteritems(expected_results):
        self.assertIn(k, actual_results)
        actual = actual_results[k]
        self.assertTrue(
            actual[0].equals(v[0]), "leaves_only={}; has_weights={}; "
            "feature={}; expected: {}; actual: {}".format(
                leaves_only, has_weights, k, v, actual))
        np.testing.assert_array_equal(actual[1], v[1])


class PrimitiveArrayToNumpyTest(absltest.TestCase):

  def testNumberArrayShouldShareBuffer(self):
    float_array = pa.array([1, 2, np.NaN], pa.float32())
    np_array = arrow_util.primitive_array_to_numpy(float_array)
    self.assertEqual(np_array.dtype, np.float32)
    self.assertEqual(np_array.shape, (3,))
    # Check that they share the same buffer.
    self.assertEqual(np_array.ctypes.data, float_array.buffers()[1].address)

  def testStringArray(self):
    string_array = pa.array(["a", "b"], pa.utf8())
    np_array = arrow_util.primitive_array_to_numpy(string_array)
    self.assertEqual(np_array.dtype, np.object)
    self.assertEqual(np_array.shape, (2,))
    np.testing.assert_array_equal(np_array, [u"a", u"b"])

  def testNumberArrayWithNone(self):
    float_array = pa.array([1.0, 2.0, None], pa.float64())
    np_array = arrow_util.primitive_array_to_numpy(float_array)
    self.assertEqual(np_array.dtype, np.float64)
    np.testing.assert_array_equal(np_array, [1.0, 2.0, np.NaN])


if __name__ == "__main__":
  absltest.main()
