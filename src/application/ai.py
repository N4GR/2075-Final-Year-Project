from pathlib import Path
from PySide6.QtCore import QObject, Slot, Signal

class AI(QObject):
    modelLoaded = Signal()
    translationReady = Signal(tuple)
    errorOccurred = Signal(str)
    
    def __init__(self, model_path = "data/m2m100_418M"):
        super().__init__()
        # Repository to download the model from if the client doesn't have it already.
        self.hf_repo = "facebook/m2m100_418M"
        
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        
        self.model_loaded = False
    
    @Slot()
    def load_model(self):
        print("Importing Torch and Transformers library.")
        import torch
        from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
        
        try:
            # Load a CUDA compatible device if found.
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            
            model_dir = Path(self.model_path)
            if not model_dir.exists():
                print(f"Model directory '{self.model_path}' not found. Downloading from Hugging Face...")

                # downloads and caches the model to Hugging Face's default cache dir
                self.tokenizer = M2M100Tokenizer.from_pretrained(self.hf_repo)
                self.model = M2M100ForConditionalGeneration.from_pretrained(self.hf_repo).to(self.device)
                
                # Save to desired path for future use
                model_dir.mkdir(parents = True, exist_ok = True)
                self.tokenizer.save_pretrained(model_dir)
                self.model.save_pretrained(model_dir)
            
            else:
                print(f"Model directory '{self.model_path}' found, loading model.")
                
                # Loads the model locally.
                self.tokenizer = M2M100Tokenizer.from_pretrained(self.model_path)
                self.model = M2M100ForConditionalGeneration.from_pretrained(self.model_path).to(self.device)
            
            self.model_loaded = True
            
            print(f"{self.model_path} loaded on {'cpu' if torch.cuda.is_available() is False else torch.cuda.get_device_name(0)}")
            
            self.modelLoaded.emit()
        
        except Exception as error:
            self.errorOccurred.emit(str(error))
            
            print(f"Error loading AI model {self.model_path} - {str(error)}")
    
    @Slot(str, str, str)
    def translate(self, text: str, source_lang: str, target_lang: str):
        try:
            if self.model_loaded is False:
                raise RuntimeError("Model not loaded yet.")
            
            if source_lang == target_lang:
                self.translationReady.emit(text)
                
                return
            
            self.tokenizer.src_lang = source_lang
            encoded = self.tokenizer(text, return_tensors = "pt")
            encoded = {k: v.to(self.device) for k, v in encoded.items()}
            generated_tokens = self.model.generate(**encoded, forced_bos_token_id = self.tokenizer.get_lang_id(target_lang))
            translation = self.tokenizer.decode(generated_tokens[0], skip_special_tokens = True)
            
            self.translationReady.emit((text, translation, source_lang, target_lang))
        
        except Exception as error:
            self.errorOccurred.emit(str(error))