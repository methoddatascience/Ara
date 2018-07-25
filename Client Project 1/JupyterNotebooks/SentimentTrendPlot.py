
# coding: utf-8

# In[ ]:


def plot_sentiment_trends(dataframe='',term='',style='fivethirtyeight'):
    
    import pandas as pd
    import matplotlib.pyplot as plt
    
    if term == '':
        raise ValueError("Must include a term using the 'term' parameter.")
    else:
        disease = term
        
    if dataframe.empty:
        raise ValueError("Must specify a dataset using the df paramter.")
    else:

        diseases = list(df['disease'].unique())

        if str(disease).lower() in diseases:

            plt.style.use(style)

            plot_df_pos = df[(df['disease']== disease) &                              (df['abs_scores'] >= 0)][['abs_scores','Clean_Date']]
            plot_df_neg = df[(df['disease']== disease) &                              (df['abs_scores'] < 0)][['abs_scores','Clean_Date']]
            plot_df_all = df[(df['disease']== disease)][['abs_scores','Clean_Date']]


            plot_df_pos['group_date'] = plot_df_pos['Clean_Date'].apply(str)                                         .apply(lambda x: x.split('-')[0])
            plot_df_neg['group_date'] = plot_df_neg['Clean_Date']                                         .apply(str)                                         .apply(lambda x: x.split('-')[0])
            plot_df_all['group_date'] = plot_df_all['Clean_Date']                                         .apply(str)                                         .apply(lambda x: x.split('-')[0])



            yearly_pos = pd.DataFrame(plot_df_pos.groupby(['group_date'],
                                                          group_keys=False)['abs_scores'] \
                                                          .agg(['min','max','mean','count']))
            yearly_neg = pd.DataFrame(plot_df_neg.groupby(['group_date'],
                                                          group_keys=False)['abs_scores'] \
                                                          .agg(['min','max','mean','count']))

            yearly_all = pd.DataFrame(plot_df_all.groupby(['group_date'],
                                                          group_keys=False)['abs_scores'] \
                                                          .agg(['min','max','mean','count']))



            yearly = pd.merge(left=yearly_pos.reset_index(),
                              right=yearly_neg.reset_index(),
                              on='group_date',how='outer',
                             suffixes=['_pos','_neg'])
            yearly['perc_pos'] = yearly['count_pos'] / (yearly['count_pos'] + yearly['count_neg'])
            yearly['perc_pos'].fillna(1.0,inplace=True)

            yearly = pd.merge(left=yearly.reset_index(),
                              right=yearly_all.reset_index(),
                              on='group_date',how='outer',
                             suffixes=['','_all'])

            #print(yearly.head())
            yearly = yearly[yearly['count'] > 10].reset_index(drop=True)

            n_years = yearly['group_date'].nunique()
            zeros = [0]*n_years
                                
            plt.figure(figsize=(12,6))
            plt.ylim(0,1.0)
            plt.title("Percent Positive {} Articles".format(disease))
            plt.ylabel("% Articles Positive")
            plt.plot(zeros,'--',linewidth=1,color='red')
            #yearly_pos['max'].plot(label='Max')
            #yearly_pos['min'].plot(label='Min')
            #yearly_pos['mean'].plot(label='Avg')
            plt.plot(yearly['perc_pos'],label='Percent Positive Articles',color='DodgerBlue')
            #yearly_neg['count'].plot(label='Negative')
            plt.xlabel("Year")
            #plt.xticks(yearly.index)
            #ax.set_xticklabels(yearly['group_date'])
            plt.xticks(np.arange(len(zeros)),yearly['group_date'])
            plt.legend()

            #n_years = yearly['group_date'].nunique()
            #zeros = [0]*n_years

            plt.figure(figsize=(12,6))
            plt.title("Average {} Article Sentiment".format(disease))
            plt.ylabel("Average Total Sentiment")
            plt.plot(zeros,'--',linewidth=1,color='red')
            yearly['mean'].plot(label='Mean',color='SeaGreen')
            #yearly_neg['min'].plot(label='Min')
            #yearly_neg['mean'].plot(label='Avg')
            #yearly_neg['count'].plot(label='Count')

            plt.xlabel("Year")
            plt.xticks(yearly.index)
            plt.xticks(np.arange(len(zeros)),yearly['group_date'])
            plt.legend()
            #plt.ylim(-1,3)
            
            return yearly
        else:
            raise ValueError("Please include a valid disease. Options include: {}".format(diseases))
        

