from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, pipeline
from datasets import load_dataset
from huggingface_hub import login
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

def main():
    api_token = "hf_what_color_is_your_token"
    login(token=api_token)
    
    # Step 1: Set up base model and dataset details
    model_name = "openai-community/gpt2"  
    dataset_name = "sathvik23reddy/oz-dataset"  
    
    # Step 2: Load the tokenizer and model
    print("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=api_token)

    if tokenizer.pad_token is None:
        print("Adding padding token to tokenizer...")
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        
    model = AutoModelForCausalLM.from_pretrained(model_name)

    model.resize_token_embeddings(len(tokenizer))

    # Step 3: Load the dataset
    print("Loading dataset...")
    dataset = load_dataset(dataset_name)

    # Step 4: Prepare the dataset by formatting fields
    print("Formatting dataset...")
    def format_for_training(examples):
        return {
            "text": f"Title: {examples['title']}\nDescription: {examples['description']}\nTranscript: {examples['transcript']}\n---\n"
        }

    formatted_dataset = dataset.map(format_for_training)

    # Step 5: Tokenize the dataset
    print("Tokenizing dataset...")
    def tokenize_function(examples):
        inputs = tokenizer(examples["text"], truncation=True, padding="max_length", max_length=512)
        inputs["labels"] = inputs["input_ids"].copy()  
        return inputs
    
    tokenized_datasets = formatted_dataset.map(tokenize_function, batched=True)

    # Step 6: Set up training arguments
    print("Setting up training arguments...")
    training_args = TrainingArguments(
        output_dir="./results",
        eval_strategy="no",
        learning_rate=2e-5,
        per_device_train_batch_size=4,
        num_train_epochs=3,
        save_steps=10_000,
        save_total_limit=2,
        logging_dir="./logs",
        logging_steps=500,
        report_to="none",  
        disable_tqdm=False, 
    )

    # Step 7: Initialize the Trainer
    print("Initializing Trainer...")    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets['train']
    )

    # Step 8: Fine-tune the model
    print("Starting training...")
    trainer.train()

    # Step 9: Save the fine-tuned model locally
    print("Saving fine-tuned model...")
    model.save_pretrained("./oz-man")
    tokenizer.save_pretrained("./oz-man")

    # Step 10: Push the model to Hugging Face Hub
    print("Pushing model to Hugging Face Hub...")
    
    model.push_to_hub("oz-man") 
    tokenizer.push_to_hub("oz-man")

    # Step 11: Test the fine-tuned model
    print("Testing fine-tuned model...")
    generator = pipeline("text-generation", model="./fine_tuned_model")
    print(generator("Greet me like a homie:"))

if __name__ == "__main__":
    main()
