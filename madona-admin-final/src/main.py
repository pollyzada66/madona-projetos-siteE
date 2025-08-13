from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Dados em memória para demonstração (com dados de exemplo)
blogs = [
    {
        'id': 1,
        'title': 'Bem-vindo ao Madona Projetos',
        'content': 'Este é o primeiro blog post do nosso site. Aqui você encontrará conteúdo de qualidade sobre marketing digital e estratégias de negócio.',
        'author': 'Equipe Madona',
        'date': '2025-01-13',
        'image_url': 'https://via.placeholder.com/400x200'
    },
    {
        'id': 2,
        'title': 'Como usar o painel de administração',
        'content': 'Guia completo para usar todas as funcionalidades do painel administrativo. Aprenda a gerenciar conteúdo de forma eficiente.',
        'author': 'Admin',
        'date': '2025-01-13',
        'image_url': 'https://via.placeholder.com/400x200'
    }
]

videos = [
    {
        'id': 1,
        'title': 'Vídeo de Apresentação',
        'description': 'Apresentação completa do Madona Projetos e nossos serviços',
        'url': 'https://youtube.com/watch?v=example1',
        'thumbnail': 'https://via.placeholder.com/320x180',
        'duration': '5:30'
    },
    {
        'id': 2,
        'title': 'Tutorial Completo',
        'description': 'Como usar nossos serviços e maximizar seus resultados',
        'url': 'https://youtube.com/watch?v=example2',
        'thumbnail': 'https://via.placeholder.com/320x180',
        'duration': '12:45'
    }
]

courses = [
    {
        'id': 1,
        'title': 'Curso de Marketing Digital',
        'description': 'Aprenda marketing digital do zero ao avançado com estratégias comprovadas',
        'price': 'R$ 199,00',
        'duration': '40 horas',
        'level': 'Iniciante',
        'image_url': 'https://via.placeholder.com/300x200'
    },
    {
        'id': 2,
        'title': 'E-book: Estratégias de Vendas',
        'description': 'Guia completo com as melhores estratégias de vendas online',
        'price': 'R$ 49,00',
        'duration': '2 horas de leitura',
        'level': 'Intermediário',
        'image_url': 'https://via.placeholder.com/300x200'
    }
]

testimonials = [
    {
        'id': 1,
        'name': 'Maria Silva',
        'content': 'Excelente serviço! A equipe do Madona Projetos transformou completamente minha estratégia de marketing. Recomendo a todos!',
        'rating': 5,
        'image_url': 'https://via.placeholder.com/100x100',
        'position': 'Empresária'
    },
    {
        'id': 2,
        'name': 'João Santos',
        'content': 'Profissionais muito competentes e atenciosos. Consegui triplicar minhas vendas em apenas 3 meses.',
        'rating': 5,
        'image_url': 'https://via.placeholder.com/100x100',
        'position': 'E-commerce'
    }
]

team_members = [
    {
        'id': 1,
        'name': 'Ana Costa',
        'position': 'CEO & Fundadora',
        'bio': 'Especialista em marketing digital com mais de 10 anos de experiência. Formada em Administração e pós-graduada em Marketing Digital.',
        'image_url': 'https://via.placeholder.com/200x200',
        'social_links': {
            'linkedin': 'https://linkedin.com/in/anacosta',
            'instagram': 'https://instagram.com/anacosta'
        }
    },
    {
        'id': 2,
        'name': 'Carlos Lima',
        'position': 'Desenvolvedor Full-Stack',
        'bio': 'Desenvolvedor apaixonado por tecnologia com expertise em React, Node.js e Python. Responsável por toda a parte técnica dos projetos.',
        'image_url': 'https://via.placeholder.com/200x200',
        'social_links': {
            'linkedin': 'https://linkedin.com/in/carloslima',
            'github': 'https://github.com/carloslima'
        }
    }
]

faqs = [
    {
        'id': 1,
        'question': 'Como posso contratar os serviços?',
        'answer': 'Entre em contato conosco através do formulário no site, WhatsApp ou e-mail. Nossa equipe entrará em contato em até 24 horas para agendar uma consulta gratuita.',
        'category': 'Contratação'
    },
    {
        'id': 2,
        'question': 'Vocês oferecem suporte?',
        'answer': 'Sim! Oferecemos suporte completo para todos os nossos clientes. Temos canais de atendimento via WhatsApp, e-mail e telefone durante horário comercial.',
        'category': 'Suporte'
    },
    {
        'id': 3,
        'question': 'Qual o prazo de entrega dos projetos?',
        'answer': 'O prazo varia conforme a complexidade do projeto. Projetos simples: 7-15 dias. Projetos médios: 15-30 dias. Projetos complexos: 30-60 dias.',
        'category': 'Prazos'
    }
]

@app.route('/')
def index():
    return send_from_directory('static', 'admin.html')

@app.route('/admin.html')
def admin():
    return send_from_directory('static', 'admin.html')

# Rotas para Blogs
@app.route('/api/blogs', methods=['GET'])
def get_blogs():
    return jsonify(blogs)

@app.route('/api/blogs', methods=['POST'])
def create_blog():
    data = request.json
    blog = {
        'id': len(blogs) + 1,
        'title': data.get('title', ''),
        'content': data.get('content', ''),
        'author': data.get('author', ''),
        'date': data.get('date', ''),
        'image_url': data.get('image_url', '')
    }
    blogs.append(blog)
    return jsonify(blog), 201

@app.route('/api/blogs/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    data = request.json
    for blog in blogs:
        if blog['id'] == blog_id:
            blog.update(data)
            return jsonify(blog)
    return jsonify({'error': 'Blog not found'}), 404

@app.route('/api/blogs/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    global blogs
    blogs = [blog for blog in blogs if blog['id'] != blog_id]
    return jsonify({'message': 'Blog deleted'})

# Rotas para Vídeos
@app.route('/api/videos', methods=['GET'])
def get_videos():
    return jsonify(videos)

@app.route('/api/videos', methods=['POST'])
def create_video():
    data = request.json
    video = {
        'id': len(videos) + 1,
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'url': data.get('url', ''),
        'thumbnail': data.get('thumbnail', ''),
        'duration': data.get('duration', '')
    }
    videos.append(video)
    return jsonify(video), 201

@app.route('/api/videos/<int:video_id>', methods=['PUT'])
def update_video(video_id):
    data = request.json
    for video in videos:
        if video['id'] == video_id:
            video.update(data)
            return jsonify(video)
    return jsonify({'error': 'Video not found'}), 404

@app.route('/api/videos/<int:video_id>', methods=['DELETE'])
def delete_video(video_id):
    global videos
    videos = [video for video in videos if video['id'] != video_id]
    return jsonify({'message': 'Video deleted'})

# Rotas para Cursos
@app.route('/api/courses', methods=['GET'])
def get_courses():
    return jsonify(courses)

@app.route('/api/courses', methods=['POST'])
def create_course():
    data = request.json
    course = {
        'id': len(courses) + 1,
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'price': data.get('price', ''),
        'duration': data.get('duration', ''),
        'level': data.get('level', ''),
        'image_url': data.get('image_url', '')
    }
    courses.append(course)
    return jsonify(course), 201

@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    data = request.json
    for course in courses:
        if course['id'] == course_id:
            course.update(data)
            return jsonify(course)
    return jsonify({'error': 'Course not found'}), 404

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    global courses
    courses = [course for course in courses if course['id'] != course_id]
    return jsonify({'message': 'Course deleted'})

# Rotas para Depoimentos
@app.route('/api/testimonials', methods=['GET'])
def get_testimonials():
    return jsonify(testimonials)

@app.route('/api/testimonials', methods=['POST'])
def create_testimonial():
    data = request.json
    testimonial = {
        'id': len(testimonials) + 1,
        'name': data.get('name', ''),
        'content': data.get('content', ''),
        'rating': data.get('rating', 5),
        'image_url': data.get('image_url', ''),
        'position': data.get('position', '')
    }
    testimonials.append(testimonial)
    return jsonify(testimonial), 201

@app.route('/api/testimonials/<int:testimonial_id>', methods=['PUT'])
def update_testimonial(testimonial_id):
    data = request.json
    for testimonial in testimonials:
        if testimonial['id'] == testimonial_id:
            testimonial.update(data)
            return jsonify(testimonial)
    return jsonify({'error': 'Testimonial not found'}), 404

@app.route('/api/testimonials/<int:testimonial_id>', methods=['DELETE'])
def delete_testimonial(testimonial_id):
    global testimonials
    testimonials = [testimonial for testimonial in testimonials if testimonial['id'] != testimonial_id]
    return jsonify({'message': 'Testimonial deleted'})

# Rotas para Equipe
@app.route('/api/team', methods=['GET'])
def get_team():
    return jsonify(team_members)

@app.route('/api/team', methods=['POST'])
def create_team_member():
    data = request.json
    member = {
        'id': len(team_members) + 1,
        'name': data.get('name', ''),
        'position': data.get('position', ''),
        'bio': data.get('bio', ''),
        'image_url': data.get('image_url', ''),
        'social_links': data.get('social_links', {})
    }
    team_members.append(member)
    return jsonify(member), 201

@app.route('/api/team/<int:member_id>', methods=['PUT'])
def update_team_member(member_id):
    data = request.json
    for member in team_members:
        if member['id'] == member_id:
            member.update(data)
            return jsonify(member)
    return jsonify({'error': 'Team member not found'}), 404

@app.route('/api/team/<int:member_id>', methods=['DELETE'])
def delete_team_member(member_id):
    global team_members
    team_members = [member for member in team_members if member['id'] != member_id]
    return jsonify({'message': 'Team member deleted'})

# Rotas para FAQs
@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    return jsonify(faqs)

@app.route('/api/faqs', methods=['POST'])
def create_faq():
    data = request.json
    faq = {
        'id': len(faqs) + 1,
        'question': data.get('question', ''),
        'answer': data.get('answer', ''),
        'category': data.get('category', '')
    }
    faqs.append(faq)
    return jsonify(faq), 201

@app.route('/api/faqs/<int:faq_id>', methods=['PUT'])
def update_faq(faq_id):
    data = request.json
    for faq in faqs:
        if faq['id'] == faq_id:
            faq.update(data)
            return jsonify(faq)
    return jsonify({'error': 'FAQ not found'}), 404

@app.route('/api/faqs/<int:faq_id>', methods=['DELETE'])
def delete_faq(faq_id):
    global faqs
    faqs = [faq for faq in faqs if faq['id'] != faq_id]
    return jsonify({'message': 'FAQ deleted'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

