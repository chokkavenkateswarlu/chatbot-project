import faiss
import numpy as np
import json
from services.nlp_service import get_embedding, calculate_similarity
from config.settings import KNOWLEDGE_BASE_PATH, INTENTS_PATH, SIMILARITY_THRESHOLD

class KnowledgeBase:
    def __init__(self):
        self.faqs = []
        self.faq_embeddings = None
        self.index = None
        self.load_knowledge_base()
        self.load_intents()
        
    def load_knowledge_base(self):
        """
        Load FAQs from knowledge base file
        """
        try:
            with open(KNOWLEDGE_BASE_PATH, 'r', encoding='utf-8') as file:
                content = file.read()
                # Split by FAQ sections (assuming each FAQ starts with Q:)
                sections = content.split('Q:')
                for section in sections:
                    if section.strip():
                        lines = section.split('A:')
                        if len(lines) >= 2:
                            question = lines[0].strip()
                            answer = lines[1].strip()
                            self.faqs.append({'question': question, 'answer': answer})
        except FileNotFoundError:
            print("Knowledge base file not found. Creating empty knowledge base.")
            self.faqs = []
        
        # Create embeddings and FAISS index
        if self.faqs:
            questions = [faq['question'] for faq in self.faqs]
            self.faq_embeddings = np.array([get_embedding(q) for q in questions])
            dimension = self.faq_embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(self.faq_embeddings)
    
    def load_intents(self):
        """
        Load intents from JSON file
        """
        try:
            with open(INTENTS_PATH, 'r', encoding='utf-8') as file:
                intents_data = json.load(file)
                for intent in intents_data.get('intents', []):
                    for pattern in intent['patterns']:
                        self.faqs.append({
                            'question': pattern,
                            'answer': intent['responses'][0] if intent['responses'] else "I'm not sure how to respond to that."
                        })
        except FileNotFoundError:
            print("Intents file not found. Continuing without intents.")
    
    def search(self, query, top_k=3):
        """
        Search for similar FAQs
        """
        if not self.faqs or self.index is None:
            return None
        
        query_embedding = get_embedding(query)
        query_embedding = np.array([query_embedding])
        
        # Search in FAISS index
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.faqs):
                similarity = 1 - distances[0][i] / 2  # Convert L2 distance to similarity score
                results.append({
                    'question': self.faqs[idx]['question'],
                    'answer': self.faqs[idx]['answer'],
                    'similarity': similarity
                })
        
        return results
    
    def get_best_match(self, query):
        """
        Get the best matching FAQ for a query
        """
        results = self.search(query, top_k=1)
        if results and results[0]['similarity'] >= SIMILARITY_THRESHOLD:
            return results[0]['answer']
        return None

# Global knowledge base instance
knowledge_base = KnowledgeBase()