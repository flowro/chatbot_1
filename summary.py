import spacy
from spacy.tokens import Doc, Span

def set_trf_sum_score(sent):
    # Set initial score of the sentence
    sent._.trf_sum_score = 0.0

@spacy.registry.misc("trf_sum_score")
def create_trf_sum_score():
    return set_trf_sum_score

def summarize_text(text, line_limit=3):
    # Load the English language model in spaCy
    nlp = spacy.load("en_core_web_sm")

    # Register trf_sum_score extension
    Doc.set_extension("trf_sum_score", default=0.0)
    Span.set_extension("trf_sum_score", default=0.0)

    # Process the input text
    doc = nlp(text)

    # Extract sentences and their respective scores
    sentences = [sent.text for sent in doc.sents]
    scores = [sent._.trf_sum_score for sent in doc.sents]

    # Sort the sentences based on their scores
    ranked_sentences = sorted(zip(sentences, scores), key=lambda x: x[1], reverse=True)

    # Select the top N sentences as the summary
    summary = " ".join([sent for sent, _ in ranked_sentences[:line_limit]])

    return summary

# Example text
text = """
Artificial intelligence (AI) is revolutionizing many industries, including healthcare, finance, and transportation. AI systems can analyze vast amounts of data, make predictions, and automate tasks that were once performed by humans. This has the potential to increase efficiency and improve decision-making in various fields.

One of the key applications of AI is in natural language processing (NLP). NLP focuses on the interaction between computers and human language. It enables machines to understand, interpret, and generate human language, which has significant implications for text summarization.

Text summarization is the process of generating a concise and coherent summary of a text document. It involves extracting the most important information from the source text while preserving its meaning. Summarization can be done using various techniques, and one popular approach is the TextRank algorithm.

The TextRank algorithm applies the concept of PageRank, used by search engines to rank web pages, to sentences within a text document. It assigns scores to sentences based on the importance of the words they contain and the relationships between sentences. By selecting the top-ranked sentences, a summary can be created.

Let's test our text summarization program using an example text. Here's a longer text about the benefits of AI and NLP. We'll see how the program can generate a summary of the main points.
"""

# Call the summarize_text function with line_limit set to 2
print(text)
summary = summarize_text(text, line_limit=3)
print("------------------summary----------------")
print(summary)
