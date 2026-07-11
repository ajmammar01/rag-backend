from io import BytesIO
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter


def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))

    pdf_texts = [
        page.extract_text().strip()
        for page in reader.pages
        if page.extract_text()
    ]

    pdf_texts = [text for text in pdf_texts if text]

    return "\n\n".join(pdf_texts)



def chunk_text(text: str) -> list[str]:
    """
    Splits extracted PDF text into embedding-friendly chunks.

    First splits by characters to preserve semantic structure,
    then splits by tokens to fit the embedding model context window.

    Args:
        text (str): Extracted PDF text.

    Returns:
        list[str]: Final token-sized chunks.
    """

    # Step 1: Character-level splitting
    character_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " ", ""],
        chunk_size=1000,
        chunk_overlap=0
    )

    character_chunks = character_splitter.split_text(text)

    # Step 2: Token-level splitting for embedding model limits
    token_splitter = SentenceTransformersTokenTextSplitter(
        chunk_overlap=0,
        tokens_per_chunk=256
    )

    token_chunks = []

    for chunk in character_chunks:
        token_chunks.extend(
            token_splitter.split_text(chunk)
        )

    return token_chunks