**Ozzy Man CustomGPT (fine-tuned LLM)**

It is build with **openai-community/gpt2** as the base model.
It is trained against **sathvik23reddy/oz-dataset** which is a dataset containing Australian Youtuber Ozzy Man Reviews' video transcripts.

Flow:
1. A list of latest 50 videos are scraped using batch_scraper (requires Youtube channel link)
2. The list of videos is passed onto yt_scraper which scrapes individual video title, description and transcript
3. This scraped data is dumped into a csv and pushed to HuggingFace
4. A lightweight model (community gpt2) is then fine tuned with the dataset
5. User prompts the new fine tuned model
6. We've Ozzy Man speaking on the other end!

Scope for Improvement:
1. Use better base model (I was Hardware restricted)
2. Build a huger dataset
3. Play around with model's temperature, top_p, top_k, repetition_penalty, max_new_tokens

Demo:
![ozzy](https://github.com/user-attachments/assets/6c706a6d-bf32-4461-ae80-9f03d6648992)
