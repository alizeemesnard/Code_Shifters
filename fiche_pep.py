import tiktoken
from openai import OpenAI
from PyPDF2 import PdfReader


from openai import OpenAI

def get_pep_co2(pep_path):
  client = OpenAI()

  assistant = client.beta.assistants.create(
  name="""Chercheur en science de l'environnement, expert en CO2 équivalent des produits du quotidien""",
  instructions="""Voici une fiche environnementale PEP. Les fiches PEP comportent et décrivent des informations sur l'impact 
                  environnemental d'un produit. Imagine que tu es un chercheur, très à l'aise avec les sujets d'impact environnemental 
                  et d'émissions de gaz à effet de serre. Analyse le contenu de la fiche ci-jointe et identifie la quantité de gaz à
                    effet de serre associée au produit présenté, en CO2eq émis. Combien trouves-tu?
                    Garde en tête que E+ correspond à une puissance de 10 et que tu dois retourner seulement un nombre flottant, pas de texte du tout !""",
  model="gpt-4o",
  tools=[{"type": "file_search"}],
  )

  # Upload the user provided file to OpenAI
  
  message_file = client.files.create(
  file=open(pep_path, "rb"), purpose="assistants"
  )

  reader = PdfReader(pep_path)

  # Extraire le texte de toutes les pages
  text = ""
  for page in reader.pages:
      text += page.extract_text()
  enc = tiktoken.get_encoding("cl100k_base")

  if len(enc.encode(text)) > 4300:
     print("Warning, PEP file too long !")
     return(0)

  # Create a thread and attach the file to the message
 
  thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": """Voici une fiche environnementale PEP. Les fiches PEP comportent et décrivent des informations sur l'impact 
                  environnemental d'un produit. Imagine que tu es un chercheur, très à l'aise avec les sujets d'impact environnemental 
                  et d'émissions de gaz à effet de serre. Analyse le contenu de la fiche ci-jointe et identifie la quantité de gaz à
                    effet de serre associée au produit présenté, en CO2eq émis. Combien trouves-tu?
                    Garde en tête que E+ correspond à une puissance de 10 et que tu dois seulement retourner un nombre flottant, pas de texte""",
      # Attach the new file to the message.
      "attachments": [
        { "file_id": message_file.id, "tools": [{"type": "file_search"}] }
      ],
    }
  ]
  )
  # print(thread.tool_resources.file_search)

  run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id
  )

  messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

  message_content = messages[0].content[0].text
  return(message_content.value) 


# print(get_pep_co2('C:\Alibarbare\\fiches_pep\PEP_Vegeta ENVPEP1412005_V2 650 up to 3150MVA.pdf'))
