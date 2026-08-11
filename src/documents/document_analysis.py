"""
Ascension AI - Document Analysis and Recreation
Read, analyze, and recreate uploaded documents
"""

import torch
import torch.nn as nn
from typing import Dict, List, Optional
import json
import os
from datetime import datetime

class DocumentAnalyzer:
    """Analyze uploaded documents for insights"""
    
    def __init__(self):
        self.analysis_history = {}
    
    def analyze_document(self, file_path: str, file_content: str) -> Dict:
        """Analyze a document and provide insights"""
        # Extract basic information
        analysis = {
            'file_path': file_path,
            'file_size': len(file_content),
            'word_count': len(file_content.split()),
            'sentence_count': file_content.count('.'),
            'paragraph_count': file_content.count('\n\n') + 1,
            'analyzed_at': datetime.now().isoformat()
        }
        
        # Extract insights
        analysis['insights'] = self.extract_insights(file_content)
        analysis['entities'] = self.extract_entities(file_content)
        analysis['key_points'] = self.extract_key_points(file_content)
        analysis['sentiment'] = self.analyze_sentiment(file_content)
        analysis['readability'] = self.analyze_readability(file_content)
        analysis['summary'] = self.summarize_document(file_content)
        analysis['topics'] = self.extract_topics(file_content)
        
        return analysis
    
    def extract_insights(self, content: str) -> List[str]:
        """Extract insights from document"""
        insights = []
        
        # Simple insights for demo
        if 'important' in content.lower():
            insights.append('Document contains important information')
        
        if 'urgent' in content.lower():
            insights.append('Document has urgent content')
        
        if len(content) > 1000:
            insights.append('Document is comprehensive and detailed')
        
        if len(content) < 200:
            insights.append('Document is brief and concise')
        
        return insights
    
    def extract_entities(self, content: str) -> Dict:
        """Extract entities from document"""
        entities = {
            'people': [],
            'organizations': [],
            'dates': [],
            'locations': [],
            'numbers': []
        }
        
        words = content.split()
        for word in words:
            # Simple extraction
            if word[0].isupper() and len(word) > 2:
                entities['people'].append(word)
            
            if word.replace('.', '').isdigit():
                entities['numbers'].append(word)
        
        return entities
    
    def extract_key_points(self, content: str) -> List[str]:
        """Extract key points from document"""
        sentences = content.split('.')
        
        # Extract sentences with important keywords
        key_sentences = []
        important_keywords = ['important', 'key', 'main', 'critical', 'essential', 'must']
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in important_keywords):
                key_sentences.append(sentence.strip())
        
        return key_sentences[:5]
    
    def analyze_sentiment(self, content: str) -> Dict:
        """Analyze sentiment of document"""
        positive_words = ['good', 'great', 'excellent', 'positive', 'success', 'happy']
        negative_words = ['bad', 'poor', 'negative', 'failure', 'sad', 'problem']
        
        content_lower = content.lower()
        
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        if positive_count > negative_count:
            sentiment = 'positive'
        elif negative_count > positive_count:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'positive_score': positive_count,
            'negative_score': negative_count,
            'confidence': abs(positive_count - negative_count) / max(positive_count + negative_count, 1)
        }
    
    def analyze_readability(self, content: str) -> Dict:
        """Analyze readability of document"""
        words = content.split()
        sentences = content.split('.')
        
        if not sentences:
            return {'readability': 'unknown'}
        
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # Simple readability score
        if avg_sentence_length < 15:
            readability = 'easy'
        elif avg_sentence_length < 25:
            readability = 'moderate'
        else:
            readability = 'complex'
        
        return {
            'readability': readability,
            'avg_word_length': avg_word_length,
            'avg_sentence_length': avg_sentence_length
        }
    
    def summarize_document(self, content: str) -> str:
        """Summarize the document"""
        sentences = content.split('.')
        
        # Simple extractive summary
        if len(sentences) <= 3:
            return content
        
        # Take first and last sentences
        summary = sentences[0].strip() + '. ' + sentences[-1].strip() + '.'
        
        return summary
    
    def extract_topics(self, content: str) -> List[str]:
        """Extract topics from document"""
        # Simple topic extraction
        words = content.lower().split()
        word_freq = {}
        
        for word in words:
            if len(word) > 4:  # Only words longer than 4 characters
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top 5 most frequent words
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return [word for word, count in top_words]

class DocumentRecreator:
    """Recreate documents based on analysis"""
    
    def __init__(self):
        self.recreation_history = {}
    
    def recreate_document(self, analysis: Dict, style: str = 'original') -> Dict:
        """Recreate a document based on analysis"""
        original_content = analysis.get('content', '')
        
        if style == 'original':
            recreated = self.recreate_original_style(analysis)
        elif style == 'simplified':
            recreated = self.recreate_simplified(analysis)
        elif style == 'expanded':
            recreated = self.recreate_expanded(analysis)
        else:
            recreated = self.recreate_original_style(analysis)
        
        return {
            'original_length': len(original_content),
            'recreated_length': len(recreated),
            'style': style,
            'recreated_content': recreated,
            'recreated_at': datetime.now().isoformat()
        }
    
    def recreate_original_style(self, analysis: Dict) -> str:
        """Recreate document in original style"""
        # In production, use the model to regenerate
        summary = analysis.get('summary', '')
        key_points = analysis.get('key_points', [])
        
        recreated = summary + '\n\nKey Points:\n'
        for point in key_points:
            recreated += f'- {point}\n'
        
        return recreated
    
    def recreate_simplified(self, analysis: Dict) -> str:
        """Recreate document in simplified style"""
        summary = analysis.get('summary', '')
        
        # Simplify summary
        words = summary.split()
        simplified = ' '.join(words[:len(words)//2])
        
        return simplified + '.'
    
    def recreate_expanded(self, analysis: Dict) -> str:
        """Recreate document in expanded style"""
        summary = analysis.get('summary', '')
        key_points = analysis.get('key_points', [])
        topics = analysis.get('topics', [])
        
        expanded = summary + '\n\n'
        expanded += 'Detailed Analysis:\n'
        
        for topic in topics:
            expanded += f'{topic}: This topic is discussed in the document.\n'
        
        expanded += '\nKey Points:\n'
        for point in key_points:
            expanded += f'- {point}\n'
        
        return expanded

class DocumentComparison:
    """Compare documents for similarities and differences"""
    
    def __init__(self):
        self.comparison_history = {}
    
    def compare_documents(self, doc1: Dict, doc2: Dict) -> Dict:
        """Compare two documents"""
        comparison = {
            'similarity_score': self.calculate_similarity(doc1, doc2),
            'differences': self.find_differences(doc1, doc2),
            'common_topics': self.find_common_topics(doc1, doc2),
            'compared_at': datetime.now().isoformat()
        }
        
        return comparison
    
    def calculate_similarity(self, doc1: Dict, doc2: Dict) -> float:
        """Calculate similarity between documents"""
        topics1 = set(doc1.get('topics', []))
        topics2 = set(doc2.get('topics', []))
        
        if not topics1 or not topics2:
            return 0.0
        
        intersection = len(topics1 & topics2)
        union = len(topics1 | topics2)
        
        return intersection / union if union > 0 else 0.0
    
    def find_differences(self, doc1: Dict, doc2: Dict) -> List[str]:
        """Find differences between documents"""
        differences = []
        
        sentiment1 = doc1.get('sentiment', {}).get('sentiment', 'neutral')
        sentiment2 = doc2.get('sentiment', {}).get('sentiment', 'neutral')
        
        if sentiment1 != sentiment2:
            differences.append(f'Sentiment differs: {sentiment1} vs {sentiment2}')
        
        readability1 = doc1.get('readability', {}).get('readability', 'unknown')
        readability2 = doc2.get('readability', {}).get('readability', 'unknown')
        
        if readability1 != readability2:
            differences.append(f'Readability differs: {readability1} vs {readability2}')
        
        return differences
    
    def find_common_topics(self, doc1: Dict, doc2: Dict) -> List[str]:
        """Find common topics between documents"""
        topics1 = set(doc1.get('topics', []))
        topics2 = set(doc2.get('topics', []))
        
        return list(topics1 & topics2)

# For production, we'll implement:
# - Advanced NLP models for analysis
# - Deep learning for sentiment analysis
# - Topic modeling (LDA, BERTopic)
# - Document generation using GPT-style models
# - Style transfer for recreation
# - Advanced similarity metrics (cosine similarity, Jaccard)
# - Diff comparison algorithms
# - Format preservation
# - Metadata extraction
# - OCR for scanned documents

if __name__ == '__main__':
    print("Document analysis and recreation system ready")
