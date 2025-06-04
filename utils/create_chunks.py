import json

def create_chunks():
    # Read the company snapshot
    with open('company_snapshot.txt', 'r') as file:
        snapshot = file.read()

    # Split the snapshot into chunks (e.g., by lines)
    chunks = snapshot.split('\n')

    # Save the chunks to chunks.txt
    with open('chunks.txt', 'w') as file:
        for chunk in chunks:
            if chunk.strip():  # Skip empty lines
                file.write(chunk + '\n')

if __name__ == '__main__':
    create_chunks() 