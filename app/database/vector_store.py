# from sqlalchemy.orm import Session
# from app.database.models import DocumentModel, ChunkModel
# from app.database.relational_db import get_db

# def store_document(db: Session, title: str, content: str, embedding: list, chunks: list):
#     # Store the document
#     db_document = DocumentModel(content=content, embedding=embedding)
#     db.add(db_document)
#     db.commit()
#     db.refresh(db_document)
    
#     # Store the chunks
#     for chunk_content, chunk_embedding in chunks:
#         db_chunk = ChunkModel(document_id=db_document.id, content=chunk_content, embedding=chunk_embedding)
#         db.add(db_chunk)
    
#     db.commit()
#     return db_document

# def search_documents(db: Session, query_vector: list):
#     results = db.query(DocumentModel).order_by(DocumentModel.embedding.l2_distance(query_vector)).limit(5).all()
#     return [result.title for result in results]
