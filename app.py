# === Imports ===
import os
import json
import faiss
import glob
import numpy as np
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer
import logging
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import time
import uuid

# === Configuration ===
logging.basicConfig(level=logging.INFO)
logging.getLogger("werkzeug").setLevel(logging.ERROR)
logging.getLogger("Llama").setLevel(logging.ERROR)

# === Initialisation de l'application Flask ===
app = Flask(__name__, static_folder='static', template_folder='templates')

# === Chemins et constantes ===
INDEX_FILE = "index.faiss"
VECTORS_FILE = "doc_vectors.npy"
DOCS_FILE = "docs.json"
MODEL_FILE = "llamaQ4.gguf"
UPLOAD_FOLDER = "files"
ALLOWED_EXTENSIONS = {'txt', 'md'}
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), UPLOAD_FOLDER)

# === Modèles et données globales ===
embedder = None
index = None
docs = []
llm = None
conversations = {}

# === Fonctions Utilitaires ===
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def split_markdown(text, max_chars=500):
    paragraphs = text.split("\n\n")
    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) < max_chars:
            current += para + "\n\n"
        else:
            chunks.append(current.strip())
            current = para + "\n\n"
    if current:
        chunks.append(current.strip())
    return chunks

def rebuild_index():
    """Scanne le dossier 'files', reconstruit l'index FAISS et le sauvegarde."""
    global index, docs
    logging.info("🧠 Reconstruction de l'index...")
    
    temp_docs = []
    print(os.getcwd())
    doc_files = glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*.md'))
    doc_files += glob.glob(os.path.join(app.config['UPLOAD_FOLDER'], '*.txt'))

    if not doc_files:
        logging.warning("Aucun document trouvé pour l'indexation.")
        index = None
        docs = []
        return False

    for path in doc_files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                markdown_text = f.read()
                chunks = split_markdown(markdown_text, max_chars=500)
                temp_docs.extend(chunks)
        except Exception as e:
            logging.error(f"Erreur de lecture du fichier {path}: {e}")
            continue

    if not temp_docs:
        logging.error("Aucun contenu textuel extrait. L'index ne sera pas mis à jour.")
        return False

    logging.info(f"   -> Encodage de {len(temp_docs)} chunks de document...")
    doc_vectors = embedder.encode(temp_docs)
    
    logging.info("   -> Création du nouvel index FAISS...")
    new_index = faiss.IndexFlatL2(doc_vectors.shape[1])
    new_index.add(doc_vectors)

    # Remplacement atomique des données
    docs = temp_docs
    index = new_index

    logging.info(f"   -> Sauvegarde de l'index dans {INDEX_FILE}...")
    faiss.write_index(index, INDEX_FILE)
    np.save(VECTORS_FILE, doc_vectors)
    with open(DOCS_FILE, "w", encoding="utf-8") as f:
        json.dump(docs, f)
        
    logging.info("✅ Index reconstruit et sauvegardé avec succès.")
    return True

# === Initialisation de l'application ===
def init_app():
    global embedder, llm, index, docs
    logging.info("🚀 Initialisation de l'application...")
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    logging.info("⚡️ Chargement du modèle d'embedding...")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    if os.path.exists(INDEX_FILE):
        logging.info(f"📦 Chargement de l'index FAISS...")
        index = faiss.read_index(INDEX_FILE)
        with open(DOCS_FILE, "r", encoding="utf-8") as f:
            docs = json.load(f)
    else:
        rebuild_index()

    logging.info(f"🦙 Chargement du LLM...")
    llm = Llama(model_path=MODEL_FILE, n_ctx=4096, verbose=False)
    logging.info("✅ Application prête !")

# === API pour les Conversations ===

@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    sorted_convs = sorted(conversations.values(), key=lambda x: x['created_at'], reverse=True)
    return jsonify([{'id': c['id'], 'title': c['title']} for c in sorted_convs])

@app.route('/api/conversations', methods=['POST'])
def create_conversation():
    conv_id = str(uuid.uuid4())
    new_conv = {
        "id": conv_id,
        "title": "Nouvelle Discussion",
        "messages": [],
        "created_at": time.time()
    }
    conversations[conv_id] = new_conv
    return jsonify({'id': conv_id, 'title': new_conv['title']})

@app.route('/api/conversations/<conv_id>', methods=['GET'])
def get_conversation(conv_id):
    return jsonify(conversations.get(conv_id, {}))

@app.route('/api/conversations/<conv_id>', methods=['DELETE'])
def delete_conversation(conv_id):
    if conv_id in conversations:
        del conversations[conv_id]
        return jsonify({"message": "Conversation supprimée"}), 200
    return jsonify({"error": "Conversation non trouvée"}), 404

# === API pour le Chat ===

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    conv_id = data.get('conversation_id')

    if not all([question, conv_id, llm, index]):
        return jsonify({"error": "Requête invalide ou système non prêt"}), 400

    conversation = conversations.get(conv_id)
    if not conversation:
        return jsonify({"error": "Conversation non trouvée"}), 404

    conversation["messages"].append({"role": "user", "content": question})

    q_vec = embedder.encode([question])
    _, I = index.search(q_vec, k=3)
    retrieved_context = "\n".join([docs[i] for i in I[0]])

    system_prompt = f"Tu es un assistant spécialisé dans les documents juridiques belges. Utilise le contexte suivant pour répondre. Si le contexte ne suffit pas, dis-le.\n\n--- Contexte ---\n{retrieved_context}"
    
    messages_for_llm = [
        {"role": "system", "content": system_prompt},
    ] + conversation["messages"][-10:] # Garde l'historique récent

    response = llm.create_chat_completion(messages=messages_for_llm, temperature=0.4)
    answer = response["choices"][0]["message"]["content"]

    conversation["messages"].append({"role": "assistant", "content": answer})
    
    new_title = None
    if len(conversation['messages']) == 2: # system + user
        title = question[:40] + '...' if len(question) > 40 else question
        conversation['title'] = title
        new_title = title

    return jsonify({'answer': answer, 'new_title': new_title})

@app.route('/api/upload', methods=['POST'])
def upload_files_route():
    files = request.files.getlist('files')
    if not files or all(f.filename == '' for f in files):
        return jsonify({"error": "Aucun fichier sélectionné"}), 400

    saved_files_count = 0
    errors = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            try:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                saved_files_count += 1
            except Exception as e:
                errors.append(f"Erreur lors de la sauvegarde de {filename}: {e}")
        elif file and file.filename != '':
            errors.append(f"Type de fichier non autorisé: {file.filename}")

    if saved_files_count == 0:
        return jsonify({"error": "Aucun fichier valide n'a été téléversé.", "details": errors}), 400

    logging.info(f"{saved_files_count} fichier(s) téléversé(s). Démarrage de la reconstruction de l'index.")
    start_time = time.time()
    success = rebuild_index()
    end_time = time.time()

    if success:
        message = f"{saved_files_count} fichier(s) ajouté(s) et index mis à jour en {end_time - start_time:.2f} secondes."
        return jsonify({"message": message, "errors": errors if errors else None})
    else:
        message = f"{saved_files_count} fichier(s) sauvegardé(s), mais la mise à jour de l'index a échoué."
        return jsonify({"error": message, "details": errors}), 500

# === Route Principale ===
@app.route('/')
def home():
    return render_template('index.html')

# === Démarrage ===

if __name__ == '__main__':
    init_app()
    app.run(host='0.0.0.0', port=5001, debug=False)
