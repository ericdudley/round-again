import os
from app import app
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    # Load environment variables from .env file
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))