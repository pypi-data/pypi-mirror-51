#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import pytest
from pandas.testing import assert_frame_equal
from apybiomart import find_marts


def test_find_marts(df_marts):
    """Test the available marts returned by list_marts()."""
    expect = (df_marts
              .sort_values(by="name", axis=0)
              .reset_index(drop=True))
    result = (find_marts()
              .sort_values(by="name", axis=0)
              .reset_index(drop=True))

    assert_frame_equal(result, expect)

