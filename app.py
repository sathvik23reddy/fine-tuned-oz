from transformers import pipeline
import pyfiglet

def main():
    
    ascii_art = pyfiglet.figlet_format("Ozzy Chat", font="slant")
    print(ascii_art)
    
    generator = pipeline("text-generation", model='./oz-man')

    user_input = input("User> ")

    response = generator(
        user_input, 
        max_new_tokens=400, 
        num_return_sequences=1, 
        temperature=0.9
    )

    print("\nGenerated Response:")
    print(response[0]["generated_text"].removeprefix(user_input).strip())

if __name__ == "__main__":
    main()

