from huggingface_hub import login
from huggingface_hub import whoami
from huggingface_hub import HfApi
from datasets import Dataset
import pandas as pd

api_token = "hf_what_color_is_your_token"
login(token=api_token)

print(f"Logged in to Hugging Face! {whoami()}")

df = pd.read_csv("output.csv")

dataset = Dataset.from_pandas(df)

repo_name = "sathvik23reddy/oz-dataset"

dataset.push_to_hub(repo_name)