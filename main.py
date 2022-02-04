# Importing Pandas and Plotly
import pandas as pd
import plotly.express as px

# Loading the data
df = pd.read_csv('/downloaded_data.csv')

# Labeling queries position
for i in range(1, 10):
    df.loc[(df['Average Position'] >= i) & (
        df['Average Position'] < i + 1), 'Pos label'] = i

# Grouping queries based on their position
df_group = df.groupby(by=['Pos label'])

# The DataFrame for saving the 'df' modified data
modified_df = pd.DataFrame()

# Each position mean CTR list
mean_ctr_list = []

# Looping over 'df_group' groups and append top 20% queries based on impressions to the 'modified_df'
for i in range(1, 10):
    tmp_df = df_group.get_group(i)[df_group.get_group(i)['Impressions'] >= df_group.get_group(i)['Impressions']
                                   .quantile(q=0.8, interpolation='lower')]
    mean_ctr_list.append(tmp_df['Site CTR'].mean())
    modified_df = modified_df.append(tmp_df, ignore_index=True)
del [tmp_df]

# Drawing the box plot
fig = px.box(modified_df, x='Pos label', y='Site CTR', title='Queries CTR distribution based on position',
             points='all', color='Pos label',  height=600, labels={'Pos label': 'Position', 'Site CTR': 'CTR'})
fig.update_yaxes(tickformat=".0%")
fig.show()

# Drawing the bar plot
fig2 = px.bar(x=[pos for pos in range(1, 10)], y=mean_ctr_list, title='Queries CTR distribution based on position',
              labels={'x': 'Position', 'y': 'CTR'}, text_auto=True)
fig2.update_yaxes(tickformat='.0%')
fig2.show()
