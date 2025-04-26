SRM Campus Chatbot 🎓🤖
A lightweight chatbot powered by Flask, OpenRouter API (Mistral model), and SQLite to provide helpful information about SRM Institute of Science and Technology — including courses, admissions, fee structure, campus life, and more!
🚀 Features
📚 Answers queries about SRM University.

🌐 Uses OpenRouter to access Mistral LLMs.

🗂️ Stores user queries and bot responses in a local SQLite database (srm_queries.db).

🌟 Easy-to-deploy Flask application.

🧩 Simple and clean code structure.

🧠 How it works
The user types a question (e.g., "What are the engineering courses offered at SRM?")

Flask backend sends the query to OpenRouter using the selected Mistral model.

OpenRouter returns a reply, which is converted from Markdown to HTML.

The bot’s reply is displayed to the user, and the conversation is saved into a local database.




🌟 SRM Campus Chatbot — making campus queries easier!
