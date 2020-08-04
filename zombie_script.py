import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv('phone'))
print(os.getenv('pass'))