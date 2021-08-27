from models import User, Post, Tag, PostTag, db
from app import app

db.drop_all()
db.create_all()

vvd = User(first_name = "Virjil", last_name = "Van Djik", position="CD", c_of_origin="Neitherland", image_url = "https://technosports.co.in/wp-content/uploads/2020/04/vvd.jpg")
dj = User(first_name = "Diego", last_name = "Jota", position="LWF", c_of_origin="Portugal", image_url = "https://www.coachesvoice.com/wp-content/uploads/2020/09/JotaMobile.png")
fab = User(first_name = "Fabinho", position="DMF", c_of_origin="Brasil", image_url = "https://images.daznservices.com/di/library/GOAL/e2/9d/fabinho-liverpool_5vqvpvvtfh1714lzlo39jcdrl.jpg?t=-1464135580&quality=100")


db.session.add_all([vvd, dj, fab])
db.session.commit()

fir = Post(title = "first post", content="Yesssssssss! i enjoyrd the game", user_id="1")
thi = Post(title = "happy", content="cool to have scored in today's game game", user_id="1")
fou = Post(title = "praise", content="nice defence from us", user_id="1")
sec = Post(title = "first post", content="Yesssssssss! i enjoyrd the game", user_id="2")

db.session.add_all([fir, thi, fou, sec])
db.session.commit()


t1 = Tag(name = "wellness")
t2 = Tag(name = "sad")
t3 = Tag(name ="happy")

db.session.add_all([t1, t2, t3])
db.session.commit()

pt1 = PostTag(post_id = 1, tag_id = "happy")
pt2 = PostTag(post_id = 1, tag_id = "wellness")
pt3 = PostTag(post_id = 3, tag_id = "wellness")

db.session.add_all([pt1, pt2, pt3])
db.session.commit()