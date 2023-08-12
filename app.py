import instaloader
import mysql.connector

L = instaloader.Instaloader()

target_profile = 'instagram'  # Replace with the desired profile
profile = instaloader.Profile.from_username(L.context, target_profile)
posts_data = []

#  profile's posts and collect data
for post in profile.get_posts():
    post_data = {
        'shortcode': post.shortcode,
        'likes': post.likes,
        'comments': post.comments,
        'timestamp': post.date_utc.timestamp(),
        'link': f"https://www.instagram.com/p/{post.shortcode}/"
    }
    posts_data.append(post_data)

    if len(posts_data) >= 10:
        break

# Store data in a MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="postdb"
)
cursor = conn.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS posts (
    shortcode VARCHAR(255) PRIMARY KEY,
    likes INT,
    comments INT,
    timestamp INT,
    link VARCHAR(255)
)
'''
cursor.execute(create_table_query)

for post_data in posts_data:
    insert_query = '''
    INSERT INTO posts (shortcode, likes, comments, timestamp, link)
    VALUES (%s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (post_data['shortcode'], post_data['likes'], post_data['comments'], post_data['timestamp'], post_data['link']))

conn.commit()
conn.close()

print("Data scraped and stored successfully.")
