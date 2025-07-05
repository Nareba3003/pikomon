from flask import Flask, jsonify, request, render_template
import random
import sqlite3

app = Flask(__name__)

def pegar_pokemon_aleatorio():
    numero_aleatorio = random.randint(1, 151)
    conexao = sqlite3.connect('pokedex_primeira_geracao.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM primeira_geracao_pokedex WHERE numero = ?', (numero_aleatorio,))
    pokemon = cursor.fetchone()
    conexao.close()
    return numero_aleatorio, pokemon[1]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pokemon')
def pokemon():
    numero, nome = pegar_pokemon_aleatorio()
    return jsonify({'numero': numero, 'nome': nome})

@app.route('/chutar', methods=['POST'])
def chutar():
    dados = request.get_json()
    chute = dados.get('chute')
    numero_correto = dados.get('numeroCorreto')

    if chute == numero_correto:
        return jsonify({'acertou': True, 'mensagem': 'Você acertou! Parabéns!'})
    elif chute > numero_correto:
        return jsonify({'acertou': False, 'mensagem': 'Seu chute foi maior que o número correto!'})
    else:
        return jsonify({'acertou': False, 'mensagem': 'Seu chute foi menor que o número correto!'})

if __name__ == '__main__':
    app.run(debug=True)
