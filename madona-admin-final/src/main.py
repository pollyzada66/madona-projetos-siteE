import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
CORS(app)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definição dos modelos
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Blog {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content
        }

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer, nullable=True) # in minutes

    def __repr__(self):
        return f'<Video {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'duration': self.duration
        }

class CourseEbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=True)
    file_url = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<CourseEbook {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'file_url': self.file_url
        }

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Testimonial {self.author}>'

    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author,
            'text': self.text
        }

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<TeamMember {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'bio': self.bio,
            'image_url': self.image_url
        }

class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<FAQ {self.question}>'

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer
        }

# Rotas da API
@app.route('/')
def index():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'admin.html')

@app.route('/admin.html')
def admin_html():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'admin.html')

@app.route('/api/status')
def status():
    return jsonify({'status': 'Painel de Administração com DB PostgreSQL Online!'})

# Rotas para Blogs
@app.route('/api/blogs', methods=['GET'])
def get_blogs():
    blogs = Blog.query.all()
    return jsonify([blog.to_dict() for blog in blogs])

@app.route('/api/blogs', methods=['POST'])
def add_blog():
    data = request.json
    new_blog = Blog(title=data['title'], content=data['content'])
    db.session.add(new_blog)
    db.session.commit()
    return jsonify(new_blog.to_dict()), 201

@app.route('/api/blogs/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    data = request.json
    blog.title = data['title']
    blog.content = data['content']
    db.session.commit()
    return jsonify(blog.to_dict())

@app.route('/api/blogs/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    return '', 204

# Rotas para Vídeos
@app.route('/api/videos', methods=['GET'])
def get_videos():
    videos = Video.query.all()
    return jsonify([video.to_dict() for video in videos])

@app.route('/api/videos', methods=['POST'])
def add_video():
    data = request.json
    new_video = Video(title=data['title'], description=data.get('description'), url=data['url'], duration=data.get('duration'))
    db.session.add(new_video)
    db.session.commit()
    return jsonify(new_video.to_dict()), 201

@app.route('/api/videos/<int:video_id>', methods=['PUT'])
def update_video(video_id):
    video = Video.query.get_or_404(video_id)
    data = request.json
    video.title = data['title']
    video.description = data.get('description')
    video.url = data['url']
    video.duration = data.get('duration')
    db.session.commit()
    return jsonify(video.to_dict())

@app.route('/api/videos/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    db.session.delete(video)
    db.session.commit()
    return '', 204

# Rotas para Cursos/E-books
@app.route('/api/courses_ebooks', methods=['GET'])
def get_courses_ebooks():
    courses_ebooks = CourseEbook.query.all()
    return jsonify([ce.to_dict() for ce in courses_ebooks])

@app.route('/api/courses_ebooks', methods=['POST'])
def add_course_ebook():
    data = request.json
    new_ce = CourseEbook(title=data['title'], description=data.get('description'), price=data.get('price'), file_url=data.get('file_url'))
    db.session.add(new_ce)
    db.session.commit()
    return jsonify(new_ce.to_dict()), 201

@app.route('/api/courses_ebooks', methods=['PUT'])
def update_course_ebook(ce_id):
    ce = CourseEbook.query.get_or_404(ce_id)
    data = request.json
    ce.title = data['title']
    ce.description = data.get('description')
    ce.price = data.get('price')
    ce.file_url = data.get('file_url')
    db.session.commit()
    return jsonify(ce.to_dict())

@app.route('/api/courses_ebooks/<int:ce_id>', methods=['DELETE'])
def delete_course_ebook(ce_id):
    ce = CourseEbook.query.get_or_404(ce_id)
    db.session.delete(ce)
    db.session.commit()
    return '', 204

# Rotas para Depoimentos
@app.route('/api/testimonials', methods=['GET'])
def get_testimonials():
    testimonials = Testimonial.query.all()
    return jsonify([t.to_dict() for t in testimonials])

@app.route('/api/testimonials', methods=['POST'])
def add_testimonial():
    data = request.json
    new_t = Testimonial(author=data['author'], text=data['text'])
    db.session.add(new_t)
    db.session.commit()
    return jsonify(new_t.to_dict()), 201

@app.route('/api/testimonials/<int:t_id>', methods=['PUT'])
def update_testimonial(t_id):
    t = Testimonial.query.get_or_404(t_id)
    data = request.json
    t.author = data['author']
    t.text = data['text']
    db.session.commit()
    return jsonify(t.to_dict())

@app.route('/api/testimonials/<int:t_id>', methods=['DELETE'])
def delete_testimonial(t_id):
    t = Testimonial.query.get_or_404(t_id)
    db.session.delete(t)
    db.session.commit()
    return '', 204

# Rotas para Membros da Equipe
@app.route('/api/team_members', methods=['GET'])
def get_team_members():
    team_members = TeamMember.query.all()
    return jsonify([tm.to_dict() for tm in team_members])

@app.route('/api/team_members', methods=['POST'])
def add_team_member():
    data = request.json
    new_tm = TeamMember(name=data['name'], role=data['role'], bio=data.get('bio'), image_url=data.get('image_url'))
    db.session.add(new_tm)
    db.session.commit()
    return jsonify(new_tm.to_dict()), 201

@app.route('/api/team_members/<int:tm_id>', methods=['PUT'])
def update_team_member(tm_id):
    tm = TeamMember.query.get_or_404(tm_id)
    data = request.json
    tm.name = data['name']
    tm.role = data['role']
    tm.bio = data.get('bio')
    tm.image_url = data.get('image_url')
    db.session.commit()
    return jsonify(tm.to_dict())

@app.route('/api/team_members/<int:tm_id>', methods=['DELETE'])
def delete_team_member(tm_id):
    tm = TeamMember.query.get_or_404(tm_id)
    db.session.delete(tm)
    db.session.commit()
    return '', 204

# Rotas para FAQs
@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    faqs = FAQ.query.all()
    return jsonify([f.to_dict() for f in faqs])

@app.route('/api/faqs', methods=['POST'])
def add_faq():
    data = request.json
    new_f = FAQ(question=data['question'], answer=data['answer'])
    db.session.add(new_f)
    db.session.commit()
    return jsonify(new_f.to_dict()), 201

@app.route('/api/faqs/<int:f_id>', methods=['PUT'])
def update_faq(f_id):
    f = FAQ.query.get_or_404(f_id)
    data = request.json
    f.question = data['question']
    f.answer = data['answer']
    db.session.commit()
    return jsonify(f.to_dict())

@app.route('/api/faqs/<int:f_id>', methods=['DELETE'])
def delete_faq(f_id):
    f = FAQ.query.get_or_404(f_id)
    db.session.delete(f)
    db.session.commit()
    return '', 204

# Cria o banco de dados se não existir
with app.app_context():
    # Verifica se as tabelas já existem antes de criar
    # Isso é importante para evitar a recriação de tabelas em um banco de dados existente
    # Em um ambiente de produção, você usaria ferramentas de migração como Flask-Migrate
    # ou Alembic para gerenciar as alterações do esquema do banco de dados.
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

