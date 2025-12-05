from google import genai
from google.genai import types
import httpx,pathlib,mimetypes  #httpx needed for fetching files from URLs
import pandas as pd #also install openpyxl for .xlsx support

client = genai.Client()
#----fetch pdf[<20mb] ftom filepath and respond to prompt----
upload_files = ["upload/test.pdf","upload/Payslip.pdf","upload/Topco.xlsx"]
doc_parts = []

for file_name in upload_files:
    filepath = pathlib.Path(file_name)
    
    if not filepath.exists():
        print(f"Warning: File not found at {filepath.absolute()}, skipping...")
        continue

    print(f"Reading {filepath.name}...")
    #doc_data = filepath.read_bytes()

    
    if filepath.suffix.lower() in ['.xlsx', '.xls']:
        print("  - Parsing Excel with pandas...")
        try:
            df = pd.read_excel(filepath)
            # Convert dataframe to CSV string
            csv_text = df.to_csv(index=False)
            
            # Add as a text part
            doc_parts.append(types.Part(
                text=f"--- START OF EXCEL FILE: {filepath.name} ---\n{csv_text}\n--- END OF EXCEL FILE ---"
            ))
            # IMPORTANT: Continue to next file so we don't upload the raw Excel binary below
            continue 
        except Exception as e:
            print(f"  - Error parsing Excel: {e}. ensure 'openpyxl' is installed.")
            
        
    # Automatically guess the MIME type based on the file extension
    mime_type, _ = mimetypes.guess_type(filepath)
    doc_data = filepath.read_bytes()
    # Create the Part object for this specific file
    doc_parts.append(types.Part.from_bytes(
        data=doc_data,
        mime_type=mime_type
    ))


print("Initializing chat with PDF context (Gemini 2.5 Flash)...")

chat = client.chats.create(
            model="gemini-2.5-flash",
            history=[
                types.Content(
                    role="user",
                    parts=doc_parts +[
                        types.Part(text="Here is the PDF document. Please use it as context for all following questions.")
                    ]
                ),
                types.Content(
                    role="model",
                    parts=[types.Part(text="Understood. I have analyzed the PDF and am ready to answer your questions.")]
                )
            ]
        )
print("\nChat started! Type 'exit/quit/end/bye' to quit.")
print("Tip: You can say 'Output X as JSON' to get structured data.")
while True:
        user_input = input("\nUser: ").strip()
        
        if user_input.lower() in ["end", "quit", "exit", "bye"]:
            break
            
        if not user_input:
            continue
        response = chat.send_message(
                user_input,
                config=types.GenerateContentConfig(
                    system_instruction = "You are a helpful assistant analyzing documents. Keep responses concise (approx 100 words) unless asked for details.",
                    temperature=0.2 
                )
            )
        print(f"Gemini: {response.text}")