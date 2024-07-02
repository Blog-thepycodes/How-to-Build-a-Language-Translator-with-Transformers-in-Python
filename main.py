from transformers import MarianMTModel, MarianTokenizer
import tkinter as tk
from tkinter import messagebox, OptionMenu, StringVar, ttk
import threading
import platform




def translate(texts, src_lang="en", tgt_lang="fr", num_beams=5, early_stopping=True):
  """ This Translate texts from src_lang to tgt_lang using MarianMTModel with beam search."""
  model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
  tokenizer = MarianTokenizer.from_pretrained(model_name)
  model = MarianMTModel.from_pretrained(model_name)




  # Tokenize the text
  inputs = tokenizer(texts, return_tensors="pt", padding=True)




  # Generate translation using the model with beam search
  translated = model.generate(**inputs, num_beams=num_beams, early_stopping=early_stopping)




  # Decode the translated text
  translated_texts = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]
  return translated_texts




def on_translate():
  """Handle the translate button click."""
  source_text = text_entry.get("1.0", tk.END).strip()
  if not source_text:
      messagebox.showwarning("Input Error", "Please enter text to translate.")
      return




  src_lang_name = src_lang_var.get().strip()
  tgt_lang_name = tgt_lang_var.get().strip()




  if not src_lang_name or not tgt_lang_name:
      messagebox.showwarning("Input Error", "Please specify both source and target languages.")
      return




  src_lang = language_dict[src_lang_name]
  tgt_lang = language_dict[tgt_lang_name]




  def translate_thread():
      try:
          set_cursor("watch")
          progress_bar.start()
          translations = translate([source_text], src_lang, tgt_lang)
          result_text.set(translations[0])
      except Exception as e:
          messagebox.showerror("Translation Error", str(e))
      finally:
          progress_bar.stop()
          set_cursor("")




  # Run the translation in a separate thread
  threading.Thread(target=translate_thread).start()




def set_cursor(cursor_type):
  """Set the cursor type depending on the platform."""
  cursor = cursor_type if platform.system() != 'Linux' else 'watch'
  root.config(cursor=cursor)




def setup_gui():
  """Set up the GUI components."""
  global root
  root = tk.Tk()
  root.title("Translator - The Pycodes")




  # Blog name label
  blog_name_label = tk.Label(root, text="The Pycodes", font=("Helvetica", 16, "bold"))
  blog_name_label.pack(pady=10)




  # Source text entry
  global text_entry
  text_entry = tk.Text(root, height=10, width=50)
  text_entry.pack(pady=10)




  # Source language selection
  src_lang_label = tk.Label(root, text="Source Language:")
  src_lang_label.pack()
  global src_lang_var
  src_lang_var = StringVar(root)
  src_lang_var.set("English")
  src_lang_menu = OptionMenu(root, src_lang_var, *language_dict.keys())
  src_lang_menu.pack()




  # Target language selection
  tgt_lang_label = tk.Label(root, text="Target Language:")
  tgt_lang_label.pack()
  global tgt_lang_var
  tgt_lang_var = StringVar(root)
  tgt_lang_var.set("French")
  tgt_lang_menu = OptionMenu(root, tgt_lang_var, *language_dict.keys())
  tgt_lang_menu.pack()




  # Translate button
  translate_button = tk.Button(root, text="Translate", command=on_translate)
  translate_button.pack(pady=10)




  # Progress bar
  global progress_bar
  progress_bar = ttk.Progressbar(root, mode='indeterminate')
  progress_bar.pack(pady=10)




  # Result display
  global result_text
  result_text = tk.StringVar()
  result_label = tk.Label(root, textvariable=result_text, wraplength=400, justify="left", bg="lightgray", height=10, width=50)
  result_label.pack(pady=10)




  return root




# Available languages
language_dict = {
  "English": "en",
  "French": "fr",
  "German": "de",
  "Spanish": "es",
  "Italian": "it",
  "Dutch": "nl",
  "Portuguese": "pt",
  "Russian": "ru",
  "Chinese": "zh",
  "Japanese": "ja",
  "Korean": "ko"
}




if __name__ == "__main__":
  # Set up and run the GUI
  root = setup_gui()
  root.mainloop()
