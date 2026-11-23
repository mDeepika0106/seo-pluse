
# Technical Decisions

## 1. Python
Python was selected because it provides simple syntax and useful libraries for web crawling, data analysis, APIs, and testing.

## 2. Requests and BeautifulSoup
Requests is used to fetch webpage content, and BeautifulSoup is used to parse HTML and extract SEO elements such as titles, meta descriptions, headings, images, and links.

## 3. FastAPI
FastAPI was selected to create the backend API. It provides request validation and interactive API documentation through Swagger UI.

## 4. Streamlit
Streamlit was selected to create a simple interactive frontend without requiring separate HTML, CSS, and JavaScript development.

## 5. Python-Based Scoring
SEO scoring is calculated using Python and predefined weights. The AI model is not allowed to calculate or modify the SEO score.

## 6. Groq AI
Groq is used to generate actionable SEO recommendations based on the audit results. The AI is used for analysis and suggestions rather than metric collection.

## 7. Pytest
Pytest was selected for automated testing of important project functions.

## 8. Crawl Limits
The crawler uses a page limit and request timeout to reduce excessive requests and improve performance.

## 9. URL and Redirect Validation
URLs and redirects are validated to restrict unsafe destinations and prevent crawling outside the allowed domain.

## 10. Development Limitations
The project is an educational prototype. DNS rebinding and other advanced network security risks are not fully mitigated.
