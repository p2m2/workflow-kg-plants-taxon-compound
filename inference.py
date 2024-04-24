import torch

def inference(text):
    device = torch.device("cuda")

    # Decoding arguments
    EVAL_GENERATION_ARGS = {
        "max_length": 1024,
        "do_sample": False,
        "forced_eos_token_id": tokenizer.eos_token_id,
        "num_beams": 3,
        "early_stopping": "never",
        "length_penalty": 1.5,
        "temperature": 0
        }

    # Prepare the input
    input_text = text + tokenizer.eos_token + tokenizer.bos_token

    # Tokenize
    input_tokens = tokenizer(input_text, return_tensors='pt')
    input_tokens.to(device)

  # Generate
  with torch.no_grad():
    beam_output = model.generate(**input_tokens, **EVAL_GENERATION_ARGS)
  output = tokenizer.decode(beam_output[0][len(input_tokens["input_ids"][0]):], skip_special_tokens=True)

  # Parse and print
  rels = output.strip().split("; ")
  for rel in rels:
    print("- " + rel)
  torch.cuda.empty_cache()
  gc.collect()