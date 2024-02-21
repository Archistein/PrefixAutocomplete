import pandas as pd


class Autocomplete:

    def __init__(self, data_path: str, brands_path: str) -> None:
        self.data = pd.read_csv(data_path,
                                usecols=[0, 1, 2],
                                index_col=[0, 1])
        self.brands = pd.read_csv(brands_path,
                                  usecols=[0, 1, 2],
                                  index_col=[1, 0],
                                  dtype={'product_uid': 'Int32'}).loc['MFG Brand Name']
        self.index_for_bin_search = self.data.index.get_level_values(
            'search_term')

    def get_suggestions(self, query: str) -> dict:
        n = self.index_for_bin_search.searchsorted(query)
        idx = self.data.iloc[n:].groupby('search_term', sort=False).max()[:5]
        suggestions = idx.sort_values(
            'relevance', ascending=False).index.to_list()
        most_relevance_products = self.data.loc[idx.index].nlargest(
            5, 'relevance').index.get_level_values('product_uid')
        brands_list = self.brands.loc[
            filter(lambda x: x in self.brands.index, most_relevance_products)
        ]['value'].to_list()

        return {
            'Suggestions': suggestions,
            'Brands': brands_list,
        }
