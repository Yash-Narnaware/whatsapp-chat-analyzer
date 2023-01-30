import streamlit as st
import preprocess
import helper
import seaborn as sns
import matplotlib.pyplot as plt


st.sidebar.title("Whatsapp")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode("utf-8")
    df = preprocess.preprocess(data)

    # st.dataframe(df)

    users = df['user'].unique().tolist()
    users.remove("group_notification")
    users.sort()
    users.insert(0,"Overall")

    selected_user = st.sidebar.selectbox('select user',users)

    if st.sidebar.button("Analyze"):
        

        number_of_messages,words,total_media,num_images,num_stickers,num_GIF,num_video,num_links = helper.fetch_stats(selected_user,df)

        st.title("Some statistics")
        col1, col2, col3, col4 = st.columns(4)
        # sub_col1,sub_col2,sub_col3,sub_col4 = col3.columns(4)


        with col1:
            st.header("Total messages")
            st.title(number_of_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(total_media)
            st.text("Images:")
            st.text(num_images)
            st.text("Stickers:")
            st.text(num_stickers)
            st.text("GIFs:")
            st.text(num_GIF)
            st.text("Videos:")
            st.text(num_video)
        with col4:
            st.header("Links")
            st.title(num_links)

        if selected_user == 'Overall':
            st.title('Most active users')

            x,new_df1 = helper.most_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df1)

        #creating a wordcloud
        st.title('Wordcloud')
        df_wc = helper.create_wordcoud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        Most_common_words = helper.most_common_words(selected_user,df)
        
        fig,ax = plt.subplots()

        ax.bar(Most_common_words[0],Most_common_words[1])
        plt.xticks(rotation='vertical')

        st.title("Most common words")
        st.pyplot(fig)
        
        st.dataframe(Most_common_words)

        #emoji
        # emoji_df = helper.emoji_analysis(selected_user,df)
        # st.dataframe(emoji_df)

        #monthly timeline
        timeline = helper.monthly_timeline(selected_user,df)

        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation='vertical')
        plt.xlabel('monthly timeline')
        plt.ylabel('number of messages')
        st.title('Monthly Timeline')
        st.pyplot(fig)

        #daily timeline
        daily_timeline = helper.daily_timeline(selected_user,df)

        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'])
        plt.xticks(rotation='vertical')
        plt.xlabel('daily timeline')
        plt.ylabel('number of messages')
        st.title('Daily Timeline')
        st.pyplot(fig)

        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            plt.xticks(rotation='vertical')
            ax.bar(busy_month.index,busy_month.values)
            st.pyplot(fig)
        
        st.title("Weekly activity map")
        activity_heatmap = helper.activity_heat_map(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(activity_heatmap)
        st.pyplot(fig)



