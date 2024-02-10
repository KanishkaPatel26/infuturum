import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set page config to wide layout
st.set_page_config(layout="wide", page_title="FeedPage", page_icon=":bar_chart:")

# Define the preferred order of categories
preferred_order = ['positive', 'hate speech', 'sexist', 'not hate speech', 'non-sexist']

# Function to rerank posts
def rerank_posts(posts_df):
    # Create a dictionary to map categories to their preferred order
    category_order_map = {category: index for index, category in enumerate(preferred_order)}
    
    # Function to calculate the score for each post based on category
    def get_score(category):
        return category_order_map.get(category, len(preferred_order))
    
    # Sort the DataFrame based on the sorting key
    reranked_posts = posts_df.sort_values(by='Category', key=lambda x: x.map(get_score))
    
    return reranked_posts

# Function to calculate statistics
def calculate_statistics(posts_df):
    # Calculate statistics such as % of hateful content
    total_posts = len(posts_df)
    hateful_posts = len(posts_df[posts_df['Category'].isin(['hate speech', 'sexist'])])
    percentage_hateful = (hateful_posts / total_posts) * 100
    return percentage_hateful

# Main Streamlit code
def main():
    # Add custom CSS to set the background color
    st.markdown("""
        <style>
            body {
                background-color: #0000FF;  
            }
        </style>
    """, unsafe_allow_html=True)

    # Take user input for 5 sentences as posts
    st.subheader('Enter 5 sentences:')
    posts_input = [st.text_input(f'Sentence {i+1}:') for i in range(5)]
    
    # Generate random categories for each sentence
    categories = np.random.choice(preferred_order, size=5)
    
    # Create DataFrame from user input and generated categories
    posts_df = pd.DataFrame({'Post': posts_input, 'Category': categories})

    # Display input sentences with styled DataFrame
    st.subheader('Input Sentences')
    st.dataframe(posts_df.style.set_properties(**{'background-color': 'blue', 
                                                   'color': 'black',
                                                   'border': '1px solid black',
                                                   'border-collapse': 'collapse',
                                                   'font-size': '14px',
                                                   'padding': '8px',
                                                   'text-align': 'center'}), height=200)

    # Rerank button
    if st.button('Rerank', key='rerank_button'):
        with st.spinner('Reranking input sentences...'):
            reranked_posts = rerank_posts(posts_df)
            st.subheader('Reranked Sentences')

            # Display reranked sentences with styled DataFrame
            st.dataframe(reranked_posts.style.set_properties(**{'background-color': 'lightblue', 
                                                                'color': 'black',
                                                                'border': '1px solid black',
                                                                'border-collapse': 'collapse',
                                                                'font-size': '14px',
                                                                'padding': '8px',
                                                                'text-align': 'center'}), height=200)

            # Calculate statistics
            st.subheader('Statistics')
            percentage_hateful = calculate_statistics(reranked_posts)
            st.write(f'Percentage of hateful content in reranked sentences: {percentage_hateful:.2f}%')

            # Plot pie chart with adjusted size
            st.subheader('Pie Chart of Categories')
            category_counts = reranked_posts['Category'].value_counts()
            fig, ax = plt.subplots(figsize=(4, 3))  # Adjust figure size here
            ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)

if __name__ == '__main__':
    main()
