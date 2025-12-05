import os
from fastapi import FastAPI
from tavily import TavilyClient

# 1. Incolla qui la tua chiave API di Tavily
# ATTENZIONE: Mantieni le virgolette ""
tavily_api_key = "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"

# 2. Inizializza il client di Tavily con la tua chiave
# Usiamo os.environ per una maggiore sicurezza, ma per ora va bene così
os.environ["TAVILY_API_KEY"] = tavily_api_key
tavily_client = TavilyClient(api_key=tavily_api_key)


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Ciao! La mia API è pronta a cercare."}

# 3. Abbiamo aggiunto il nostro nuovo endpoint di ricerca!
@app.get("/search")
def search_web(query: str):
    """
    Esegue una ricerca web usando Tavily e restituisce una risposta concisa.
    """
    try:
        # Eseguiamo la ricerca
        response = tavily_client.search(query=query, search_depth="basic")
        
        # Estraiamo solo la risposta concisa (answer) dal risultato
        if response.get("answer"):
            return {"summary": response["answer"]}
        else:
            # Se non c'è una risposta diretta, restituiamo il contenuto della prima fonte
            return {"summary": response["results"][0]["content"]}

    except Exception as e:
        # In caso di errore, lo comunichiamo
        return {"error": f"Si è verificato un errore: {str(e)}"}
