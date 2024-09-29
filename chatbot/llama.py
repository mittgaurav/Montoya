# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 00:17:18 2024

@author: gaurav
"""
from transformers import LlamaForCausalLM, AutoTokenizer
import torch
import os

# Set the environment variable for memory management
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

MODEL_PATH = r"C:\Users\gaurav\Documents\GitHub\Montoya\chatbot\llama-3.1-8B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = LlamaForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16,
    revision="main",
)

# Set the model to evaluation mode
model.eval()

# Check if CUDA is available and move the model to GPU if possible
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu")
model.to(device)


def generate_response(prompt, max_length=100):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():  # Disable gradient calculation
        outputs = model.generate(
            inputs.input_ids,
            max_length=max_length,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            early_stopping=True
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response


# Example usage
if __name__ == "__main__":
    user_input = "Hello, how are you?"
    response = generate_response(user_input)
    print(response)

    
    # Clear CUDA cache
    torch.cuda.empty_cache()

    # Print memory summary
    print(torch.cuda.memory_summary())
