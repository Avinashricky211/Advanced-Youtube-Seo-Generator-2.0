# Installation Guide

Follow these steps to set up the YouTube SEO Generator on your local machine:

1. **Clone the repository**

   ```
   git clone https://github.com/yourusername/youtube-seo-generator.git
   cd youtube-seo-generator
   ```

2. **Set up a virtual environment** (optional but recommended)

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install required packages**

   ```
   pip install -r requirements.txt
   ```

4. **Download spaCy model**

   ```
   python -m spacy download en_core_web_sm
   ```

5. **Set up YouTube Data API**

   - Go to the [Google Developers Console](https://console.developers.google.com/)
   - Create a new project or select an existing one
   - Enable the YouTube Data API v3
   - Create credentials (API key)
   - Replace the `API_KEY` variable in the script with your actual API key in line 20 of Advanced youtube seo generator 2.0.py

6. **Run the script**

   ```
   python Advanced youtube seo generator 2.0.py
   ```

## Troubleshooting

- If you encounter any issues with NLTK data, you may need to manually download it:

  ```
  python -m nltk.downloader punkt stopwords
  ```

- Make sure your API key has the necessary permissions and quotas for the YouTube Data API.

For any other issues, please check the project's issue tracker on GitHub or create a new issue if needed.