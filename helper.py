from urlextract import URLExtract
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import emoji

def fetch_stats(selected_user,df):

    

    if selected_user != 'Overall':

        df = df[df['user'] == selected_user]
    
    number_of_mesages = df.shape[0]

    words = []
    links = []

    extractor = URLExtract()

    for message in df['message']:
        words.extend(message.split())
        links.extend(extractor.find_urls(message))


    num_images = df[df['message'].str.contains('image omitted')].shape[0]
    num_stickers = df[df['message'].str.contains('sticker omitted')].shape[0]
    num_GIF = df[df['message'].str.contains('GIF omitted')].shape[0]
    num_video = df[df['message'].str.contains('video omitted')].shape[0]
    total_media = num_images + num_stickers + num_GIF + num_video
 

    return number_of_mesages,len(words),total_media,num_images,num_stickers,num_GIF,num_video,len(links)

def most_active_users(df):

    x = df['user'].value_counts().head()
    df1 = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x,df1
    # plt.bar(x.index,x.values)
    # plt.xticks(rotation = 'vertical')

def create_wordcoud(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f = open('stopwords_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    #temp = temp[temp['message'] != 'image omitted\n' or temp['message'] != 'sticker omitted' or temp['message'] != 'video omitted' or temp['message'] != 'GIF omitted']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words and word !=" ":
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df


def emoji_analysis(selected_user,df):

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
    
def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()


def activity_heat_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    activity_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return activity_heatmap