import instaloader
import mysql.connector

# Create an instance of Instaloader
L = instaloader.Instaloader()

# Define the target Instagram profile (public profile)
target_profile = 'instagram'  # Replace with the desired profile

# Download the profile's metadata
profile = instaloader.Profile.from_username(L.context, target_profile)

# Create an empty list to store post data
posts_data = []

# Iterate through the profile's posts and collect data
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

# Store the data in a MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="postdb"
)
cursor = conn.cursor()

# Create a table (if not exists)
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

# Insert data into the table
for post_data in posts_data:
    insert_query = '''
    INSERT INTO posts (shortcode, likes, comments, timestamp, link)
    VALUES (%s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (post_data['shortcode'], post_data['likes'], post_data['comments'], post_data['timestamp'], post_data['link']))

# Commit and close the connection
conn.commit()
conn.close()

print("Data scraped and stored successfully.")
