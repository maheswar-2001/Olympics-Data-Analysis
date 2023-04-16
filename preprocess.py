import pandas as pd



def process(df,df_region):

    #Filtering for Summer Olympics
    df = df[df['Season'] == 'Summer']

    #Merging the region data frame
    df = df.merge(df_region,on='NOC',how='left')

    # Removing the duplicate row from the dataframe
    df.drop_duplicates(inplace=True)

    #one hot encoding or implementing dummby varaibles
    dummy = pd.get_dummies(df['Medal'])
    df = pd.concat([df,dummy],axis=1)

    #deleting the notes column as it contains only NAN values
    df = df.drop(['notes'],axis=1)
    return df