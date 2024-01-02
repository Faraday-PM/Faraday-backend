from sqlalchemy import create_engine
hostname: str = "clear-steel-a3l6.turso.io"
authToken: str = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJpYXQiOiIyMDI0LTAxLTAyVDA2OjQzOjEzLjIwNDcyMDQzMloiLCJpZCI6IjAxZjIwOTQxLWE4ZjktMTFlZS1iYTEyLWE2NTRjZjMwN2E2NCJ9.lB4AtUxvsN63NBzVS8PEh3gm63Wx5rQe0Xvg8uNmEy-SPKYUI7TGyFHBKe53PZzMtYIGr9T8f8BhcFcQUlv7AA"
url: str = f"sqlite+libsql://{hostname}/?authToken={authToken}&secure=true"
print(url)
engine = create_engine(url)