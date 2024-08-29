# (C) Copyright IBM Corp. 2024.
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

import os
from typing import Tuple

from data_processing.test_support import get_tables_in_folder
from data_processing.data_access import DataAccessFactory
from data_processing.utils import RANDOM_SEED
from data_processing.test_support.transform import AbstractTableTransformTest
from fdedup.utils import BucketsHash, MurmurMH, DocsMinHash
from fdedup.transforms.base import (doc_column_name_key, int_column_name_key, shingles_size_key,
                                    delimiters_key, mn_min_hash_key, minhashes_cache_key, buckets_cache_key)
from fdedup.transforms.python import FdedupPreprocessorTransform


class TestFdedupPreprocessorTransform(AbstractTableTransformTest):
    """
    Extends the super-class to define the test data for the tests defined there.
    The name of this class MUST begin with the word Test so that pytest recognizes it as a test class.
    """

    def get_test_transform_fixtures(self) -> list[Tuple]:
        basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../test-data"))
        input_dir = os.path.join(basedir, "input")
        input_tables = get_tables_in_folder(input_dir)
        data_access_factory = DataAccessFactory()
        mn_min_hash = MurmurMH(num_perm=64, seed=RANDOM_SEED)
        minhash_collector = DocsMinHash({"id": 0, "data_access": data_access_factory, "snapshot": None})
        bucket_collector = BucketsHash({"id": 0, "data_access": data_access_factory, "snapshot": None})

        fdedup_params = {doc_column_name_key: "contents", int_column_name_key: "Unnamed: 0", shingles_size_key: 5,
                         delimiters_key: " ", mn_min_hash_key: mn_min_hash, minhashes_cache_key: minhash_collector,
                         buckets_cache_key: bucket_collector}
        expected_metadata_list = [{'generated buckets': 3, 'generated minhashes': 5}, {}]
        expected_tables = []
        return [
            (FdedupPreprocessorTransform(fdedup_params), input_tables, expected_tables, expected_metadata_list),
        ]