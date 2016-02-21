#!/usr/bin/env python

import agate

class ZScores(agate.Computation):
    """
    Computes the z-scores (standard scores) of a given column.
    """
    def __init__(self, column_name):
        self._column_name = column_name

        self._mean = None
        self._sd = None

    def get_computed_data_type(self, table):
        return agate.Number()

    def validate(self, table):
        column = table.columns[self._column_name]

        if not isinstance(column.data_type, agate.Number):
            raise agate.DataTypeError('ZScores column must contain Number data.')

    def run(self, table):
        self._mean = table.aggregate(agate.Mean(self._column_name))
        self._sd = table.aggregate(agate.StDev(self._column_name))

        new_column = [(row[self._column_name] - self._mean) / self._sd for row in table.rows]
        
        return new_column
