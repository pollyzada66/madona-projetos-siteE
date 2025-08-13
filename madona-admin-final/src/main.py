
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

