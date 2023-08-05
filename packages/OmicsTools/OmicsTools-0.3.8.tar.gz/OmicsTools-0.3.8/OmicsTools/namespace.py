#!/usr/bin/env python3

import pandas as pd
import mygene


mg = mygene.MyGeneInfo()


class SymbolMapping: 

	def __init__(self, symbols, symbol_type): 

		if symbol_type not in ['uniprot', 'ensemblgene']: 
			raise ValueError('symbol_type must be `uniprot` or `ensemblgene`')

		self.symbols = symbols
		self.symbol_type = symbol_type # uniprot, ensemblgene

		self.mapping = self._get_namespace_mapping()

	def _get_namespace_mapping(self): 
		"""Returns namespace mapping following a gene symbol prioritization procedure for duplicate mappings."""

		mapping = mg.querymany(self.symbols, scopes=self.symbol_type, as_dataframe=True, returnall=True)["out"]
		# Queries with duplicated gene symbols may be returned in any order, so we prioritize certain gene symbols 
		# such that gene fusions do not appear first and protein subunits are sorted alphabetically. 
		mapping['is_fusion'] = mapping.symbol.str.contains('-')
		mapping = mapping.sort_values(by=['is_fusion', 'symbol']).loc[self.symbols, 'symbol']
		return mapping

	def convert(self, df, how='one_to_one', remove_duplicates=None): 
		"""
		Converts input dataframe index to gene symbols.

		Arguments: 
			df (pd.DataFrame): input dataframe 
			how (str): 
				- 'one_to_one':   unique inputs to unique gene symbol
				- 'many_to_one':  each input maps to a single gene symbol (not necessarily unique)
				- 'one_to_many':  each input may map to multiple unique gene gene symbols
				- 'many_to_many': all mappings
			remove_duplicates (str): 
				- 'mean':     for duplicate gene symbols, take mean of values
				- 'median':   for duplicate gene symbols, take median of values
				- 'row_sum':  eliminate duplicate gene symbols by taking row with largest sum
				- 'na_count': eliminate duplicate gene symbols by taking row with least missing values (default)

		Return:
			mapped_df (pd.DataFrame): same as `df` but indexed with gene symbols
		"""
		mapping = self.mapping.dropna()

		# Input symbols can only map to one gene symbol, so take the first in mapping
		if how.endswith('to_one'): 
			mapping = mapping[ ~mapping.index.duplicated(keep='first') ]

		mapped_df = df.merge(mapping, left_index=True, right_index=True, how='inner')

		# Remove any duplicate gene symbols
		if how.startswith('one_to'): 

			# Set default mode
			if remove_duplicates is None: remove_duplicates = 'na_values'

			if remove_duplicates == 'mean': 
				mapped_df = mapped_df.groupby('symbol').mean().reset_index()

			elif remove_duplicates == 'median': 
				mapped_df = mapped_df.groupby('symbol').median().reset_index()

			elif remove_duplicates == 'row_sum': 
				mapped_df['row_sum'] = mapped_df.sum(axis=1)
				mapped_df = mapped_df.sort_values('row_sum', ascending=False).drop(columns=['row_sum']).drop_duplicates(subset=['symbol'], keep='first')

			elif remove_duplicates == 'na_count': 
				mapped_df['na_count'] = mapped_df.isna().sum(axis=1)
				mapped_df = mapped_df.sort_values('na_count').drop(columns=['na_count']).drop_duplicates(subset=['symbol'], keep='first')

			else: 
				mapped_df = mapped_df.drop_duplicates(subset=['symbol'], keep='first')

			assert mapped_df['symbol'].is_unique

		return mapped_df.set_index('symbol')



