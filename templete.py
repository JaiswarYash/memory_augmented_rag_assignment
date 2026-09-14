import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "memory_augmented_rag_assignment"

list_of_files = [
    ".github/workflows/.gitkeep",
    "config.py",
    "embeddings.py",
    "knowledge_base.py",
    "llm_service.py",
    "long_term_memory.py",
    "rag_service.py",
    "semantic_memory.py",
    "short_term_memory.py",
    "vector_store.py",
    "self_test.py",
    "requirements.txt"
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory:{filedir} for the file {filename}")


    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath,'w') as f:
            pass
        logging.info(f"Creating empty file: {filepath}")



    else:
        logging.info(f"{filename} is already exists")