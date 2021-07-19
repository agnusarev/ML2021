import sys
import pandas as pd


def optimize_dataframe(df):
    """Optimize pandas dataframe size:
    - downcast numeric (int and float) types columns.
    - convert to Categorical type categorical columns with 2x or more "values/unique" values rate.
    :param df:
    :return:
    """

    #return df  # TODO: remove - check for failure!!!

    int_cols = []
    float_cols = []
    category_cols = []
    other_cols = []

    old_size = sys.getsizeof(df)

    for col_name in df.columns:
        col_type = df.dtypes[col_name]

        if col_type in ['int', 'int32', 'int64']:
            int_cols.append(col_name)
        elif col_type in ['float', 'float32', 'float64']:
            float_cols.append(col_name)
        elif col_type == 'object':
            total = len(df[col_name])
            n_uniq = df[col_name].nunique()
            if n_uniq / total < 0.5:
                category_cols.append(col_name)
            else:
                other_cols.append(col_name)
        else:
            other_cols.append(col_name)

    df_opt = pd.DataFrame()

    if len(int_cols) > 0:
        df_opt[int_cols] = df[int_cols].apply(pd.to_numeric, downcast='integer')

    if len(float_cols) > 0:
        df_opt[float_cols] = df[float_cols].apply(pd.to_numeric, downcast='float')

    if len(category_cols) > 0:
        df_opt[category_cols] = df[category_cols].astype('category')

    if len(other_cols) > 0:
        df_opt[other_cols] = df[other_cols]

    new_size = sys.getsizeof(df_opt)
    print('optimize dataframe ({} to {}, ratio: {})'.format(old_size, new_size, round(old_size/new_size, 2)))

    return df_opt