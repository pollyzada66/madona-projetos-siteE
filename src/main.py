import os
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///madona.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

# Modelos da Base de Dados
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=True)
    date = db.Column(db.String(20), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'date': self.date,
            'image_url': self.image_url
        }

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(200), nullable=False)
    thumbnail = db.Column(db.String(200), nullable=True)
    duration = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'thumbnail': self.thumbnail,
            'duration': self.duration
        }

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.String(50), nullable=True)
    duration = db.Column(db.String(50), nullable=True)
    level = db.Column(db.String(50), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'duration': self.duration,
            'level': self.level,
            'image_url': self.image_url
        }

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    position = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'rating': self.rating,
            'image_url': self.image_url,
            'position': self.position
        }

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    linkedin = db.Column(db.String(200), nullable=True)
    instagram = db.Column(db.String(200), nullable=True)
    github = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'bio': self.bio,
            'image_url': self.image_url,
            'social_links': {
                'linkedin': self.linkedin,
                'instagram': self.instagram,
                'github': self.github
            }
        }

class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category
        }

# Rotas da API para blogs
@app.route('/api/blogs', methods=['GET'])
def get_blogs():
    blogs = Blog.query.all()
    return jsonify([blog.to_dict() for blog in blogs])

@app.route('/api/blogs', methods=['POST'])
def create_blog():
    data = request.json
    blog = Blog(
        title=data.get('title', ''),
        content=data.get('content', ''),
        author=data.get('author', ''),
        date=data.get('date', ''),
        image_url=data.get('image_url', '')
    )
    db.session.add(blog)
    db.session.commit()
    return jsonify(blog.to_dict()), 201

@app.route('/api/blogs/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    data = request.json
    blog.title = data.get('title', blog.title)
    blog.content = data.get('content', blog.content)
    blog.author = data.get('author', blog.author)
    blog.date = data.get('date', blog.date)
    blog.image_url = data.get('image_url', blog.image_url)
    db.session.commit()
    return jsonify(blog.to_dict())

@app.route('/api/blogs/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    return jsonify({'message': 'Blog deleted'})

# Rotas da API para vídeos
@app.route('/api/videos', methods=['GET'])
def get_videos():
    videos = Video.query.all()
    return jsonify([video.to_dict() for video in videos])

@app.route('/api/videos', methods=['POST'])
def create_video():
    data = request.json
    video = Video(
        title=data.get('title', ''),
        description=data.get('description', ''),
        url=data.get('url', ''),
        thumbnail=data.get('thumbnail', ''),
        duration=data.get('duration', '')
    )
    db.session.add(video)
    db.session.commit()
    return jsonify(video.to_dict()), 201

@app.route('/api/videos/<int:video_id>', methods=['PUT'])
def update_video(video_id):
    video = Video.query.get_or_404(video_id)
    data = request.json
    video.title = data.get('title', video.title)
    video.description = data.get('description', video.description)
    video.url = data.get('url', video.url)
    video.thumbnail = data.get('thumbnail', video.thumbnail)
    video.duration = data.get('duration', video.duration)
    db.session.commit()
    return jsonify(video.to_dict())

@app.route('/api/videos/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    db.session.delete(video)
    db.session.commit()
    return jsonify({'message': 'Video deleted'})

# Rotas para Cursos
@app.route('/api/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses])

@app.route('/api/courses', methods=['POST'])
def create_course():
    data = request.json
    course = Course(
        title=data.get('title', ''),
        description=data.get('description', ''),
        price=data.get('price', ''),
        duration=data.get('duration', ''),
        level=data.get('level', ''),
        image_url=data.get('image_url', '')
    )
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201

@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.json
    course.title = data.get('title', course.title)
    course.description = data.get('description', course.description)
    course.price = data.get('price', course.price)
    course.duration = data.get('duration', course.duration)
    course.level = data.get('level', course.level)
    course.image_url = data.get('image_url', course.image_url)
    db.session.commit()
    return jsonify(course.to_dict())

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted'})

# Rotas para Depoimentos
@app.route('/api/testimonials', methods=['GET'])
def get_testimonials():
    testimonials = Testimonial.query.all()
    return jsonify([testimonial.to_dict() for testimonial in testimonials])

@app.route('/api/testimonials', methods=['POST'])
def create_testimonial():
    data = request.json
    testimonial = Testimonial(
        name=data.get('name', ''),
        content=data.get('content', ''),
        rating=data.get('rating', 5),
        image_url=data.get('image_url', ''),
        position=data.get('position', '')
    )
    db.session.add(testimonial)
    db.session.commit()
    return jsonify(testimonial.to_dict()), 201

@app.route('/api/testimonials/<int:testimonial_id>', methods=['PUT'])
def update_testimonial(testimonial_id):
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    data = request.json
    testimonial.name = data.get('name', testimonial.name)
    testimonial.content = data.get('content', testimonial.content)
    testimonial.rating = data.get('rating', testimonial.rating)
    testimonial.image_url = data.get('image_url', testimonial.image_url)
    testimonial.position = data.get('position', testimonial.position)
    db.session.commit()
    return jsonify(testimonial.to_dict())

@app.route('/api/testimonials/<int:testimonial_id>', methods=['DELETE'])
def delete_testimonial(testimonial_id):
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    db.session.delete(testimonial)
    db.session.commit()
    return jsonify({'message': 'Testimonial deleted'})

# Rotas para Equipe
@app.route('/api/team', methods=['GET'])
def get_team():
    team_members = TeamMember.query.all()
    return jsonify([member.to_dict() for member in team_members])

@app.route('/api/team', methods=['POST'])
def create_team_member():
    data = request.json
    member = TeamMember(
        name=data.get('name', ''),
        position=data.get('position', ''),
        bio=data.get('bio', ''),
        image_url=data.get('image_url', ''),
        linkedin=data.get('social_links', {}).get('linkedin', ''),
        instagram=data.get('social_links', {}).get('instagram', ''),
        github=data.get('social_links', {}).get('github', '')
    )
    db.session.add(member)
    db.session.commit()
    return jsonify(member.to_dict()), 201

@app.route('/api/team/<int:member_id>', methods=['PUT'])
def update_team_member(member_id):
    member = TeamMember.query.get_or_404(member_id)
    data = request.json
    member.name = data.get('name', member.name)
    member.position = data.get('position', member.position)
    member.bio = data.get('bio', member.bio)
    member.image_url = data.get('image_url', member.image_url)
    member.linkedin = data.get('social_links', {}).get('linkedin', member.linkedin)
    member.instagram = data.get('social_links', {}).get('instagram', member.instagram)
    member.github = data.get('social_links', {}).get('github', member.github)
    db.session.commit()
    return jsonify(member.to_dict())

@app.route('/api/team/<int:member_id>', methods=['DELETE'])
def delete_team_member(member_id):
    member = TeamMember.query.get_or_404(member_id)
    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Membro deleted'})

# Rotas para FAQs
@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    faqs = FAQ.query.all()
    return jsonify([faq.to_dict() for faq in faqs])

@app.route('/api/faqs', methods=['POST'])
def create_faq():
    data = request.json
    faq = FAQ(
        question=data.get('question', ''),
        answer=data.get('answer', ''),
        category=data.get('category', '')
    )
    db.session.add(faq)
    db.session.commit()
    return jsonify(faq.to_dict()), 201

@app.route('/api/faqs/<int:faq_id>', methods=['PUT'])
def update_faq(faq_id):
    faq = FAQ.query.get_or_404(faq_id)
    data = request.json
    faq.question = data.get('question', faq.question)
    faq.answer = data.get('answer', faq.answer)
    faq.category = data.get('category', faq.category)
    db.session.commit()
    return jsonify(faq.to_dict())

@app.route('/api/faqs/<int:faq_id>', methods=['DELETE'])
def delete_faq(faq_id):
    faq = FAQ.query.get_or_404(faq_id)
    db.session.delete(faq)
    db.session.commit()
    return jsonify({'message': 'FAQ deleted'})

@app.route("/admin.html")
def serve_admin():
    return send_from_directory(app.static_folder, "admin.html")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path == "":
        return send_from_directory(static_folder_path, "admin.html")
    elif path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)




