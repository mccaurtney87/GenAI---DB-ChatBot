import tkinter as tk
import tkinter.ttk as ttk
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
#from langchain.agents import AgentExecutor
#import psycopg2
import openai
from langchain.chat_models import ChatOpenAI

llm = OpenAI(model_name="gpt-3.5-turbo",openai_api_key="****",temperature=0)


# Define your PostgreSQL database connection details
db_credentials = {
    "host": "localhost",
    "database": "***",
    "user": "***",
    "password": "***",
}

# Create a SQLAlchemy-compatible connection using psycopg2
connection_string = f"postgresql+psycopg2://{db_credentials['user']}:{db_credentials['password']}@{db_credentials['host']}/{db_credentials['database']}"
#engine = create_engine(connection_string)

# Pass the engine to the SQLDatabase
db = SQLDatabase.from_uri(connection_string)

# Create the toolkit
toolkit = SQLDatabaseToolkit(db=db,llm=llm)

# Create the agent executor as you did before
agent_executor = create_sql_agent(
    handle_parsing_errors=True,
    llm=llm,
    toolkit=toolkit,
    verbose=True
)

# Create the UI window
root = tk.Tk()
root.title("Chat with your Tabular Data")

# Create the text entry widget
entry = ttk.Entry(root, font=("Arial", 14))
entry.pack(padx=20, pady=20, fill=tk.X)

# Create the button callback
def on_click():
    # Get the query text from the entry widget
    query = entry.get()

    # Run the query using the agent executor
    result = agent_executor.run(query)

    # Display the result in the text widget
    text.delete("1.0", tk.END)
    text.insert(tk.END, result)

# Create the button widget
button = ttk.Button(root, text="Chat", command=on_click)
button.pack(padx=20, pady=20)

# Create the text widget to display the result
text = tk.Text(root, height=10, width=60, font=("Arial", 14))
text.pack(padx=20, pady=20)

# Start the UI event loop
root.mainloop()
