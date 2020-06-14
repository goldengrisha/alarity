import numpy as np
from flask import Flask, jsonify, request, current_app as app
from models import Text, TextLine, db
from helpers import json_result
from encoder_helpers import Encoder
from sentence_helpers import text_to_sentence


@app.route('/ping', methods=['GET'])
def ping_pong():

    return jsonify('pong!')


@app.route('/text/<int:id>', methods=['GET'])
def get_text(id: int):

    return jsonify(json_result(
        True,
        Text.query.get(id).serialized))


@app.route('/text', methods=['GET'])
def get_all_texts():

    return jsonify(json_result(
        True,
        [text.serialized for text in Text.query.all()]))


@app.route('/text/lines/<int:id>', methods=['GET'])
def get_all_text_lines(id: int):

    return jsonify(json_result(
        True,
        [text_line.serialized for text_line in TextLine.query.filter_by(text_id=id)]))


@app.route('/text/save/<name>', methods=['POST'])
def save_text(name: str):

    texts_count = Text.query.count()
    if texts_count > 1000:
        return jsonify(json_result(
            True,
            'The amount of text is limited'))

    text = request.get_data(as_text=True)
    text = Text(None,
                name,
                [TextLine(None, sentence, None) for sentence in text_to_sentence(text)])
    db.session.add(text)
    db.session.commit()

    return jsonify(json_result(True, text.serialized))


@app.route('/text/similar/<int:id>', methods=['GET'])
def find_similar_sentences(id: int):
    encoder = Encoder()
    all_text_lines = TextLine.query.filter(TextLine.id != id).all()
    line_to_compare = TextLine.query.get(id)

    if line_to_compare is None:
        return jsonify(json_result(
            False,
            'The line for comparing couldn\'t be found!!!'))
    all_lines = np.array([text_line.line for text_line in all_text_lines])

    scores = [encoder.run_sts_benchmark(
        line_to_compare.line, line) for line in all_lines]

    scores = np.array(scores).flatten('F')
    all_scored_text_lines = [{
        'text_name': all_text_lines[index].Text.name,
        'line': all_text_lines[index].line,
        'id':  all_text_lines[index].id,
        'text_id': all_text_lines[index].text_id,
        'score': float(score)} for index, score in enumerate(scores)]
    top_lines = list(sorted(all_scored_text_lines,
                            key=lambda x: x['score'],
                            reverse=True))[:100]

    return jsonify(json_result(True, top_lines))
