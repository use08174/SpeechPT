
from fastapi import UploadFile
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
from models.text.hanspell import spell_checker
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import re

templates = Jinja2Templates(directory="frontend/templates")

def split_text_into_paragraphs(text):
    paragraphs = re.split(r'\b\d+\.\s', text)[1:]
    result_paragraphs = [p.strip() for p in paragraphs if p.strip()]

    return result_paragraphs    

def summarize_text(extracted_text):
    print("Start summarization")
    paragraphs = split_text_into_paragraphs(extracted_text)

    print("Loading tokenizer and model")
    # Load the model
    tokenizer = PreTrainedTokenizerFast.from_pretrained("ainize/kobart-news")
    model = BartForConditionalGeneration.from_pretrained("ainize/kobart-news")

    # Summarize each paragraph
    summary_paragraphs = []
    for i, paragraph in enumerate(paragraphs, start=1):
        print(f"Processing paragraph {i}")
        input_ids = tokenizer.encode(paragraph, return_tensors="pt")
        summary_text_ids = model.generate(
            input_ids=input_ids,
            bos_token_id=model.config.bos_token_id,
            eos_token_id=model.config.eos_token_id,
            length_penalty=2.0,
            max_length=142,
            min_length=56,
            num_beams=10,
        )

        try:
            # summary_text = tokenizer.decode(summary_text_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
            decoded_tokens = tokenizer.decode(summary_text_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
            summary_text = "".join(decoded_tokens.split())
        except UnicodeDecodeError as e:
            print("A UnicodeDecodeError occurred:", e)
            continue
        except Exception as e:
            print("An unexpected error occurred:", e)
            continue
        # summary_paragraphs.append(summary_text)
        # print(summary_text)
        # return summary_paragraphs
        checked_txt = ""
        for j in range(0, len(summary_text), 1000):
             part_of_txt = summary_text[j:j+1000]
             try:
                 spelled_sent = spell_checker.check(part_of_txt)
                 checked_txt += spelled_sent.checked
             except KeyError as e:
                print(f"A KeyError occurred at paragraph {i}, index {j}: {e}")
                break 
             except Exception as e:
                print(f"An unexpected error occurred at paragraph {i}, index {j}: {e}")
        summary_paragraphs.append(f"<br>Paragraph {i}<br>")
        summary_paragraphs.append(checked_txt)

    return summary_paragraphs


