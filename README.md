# Infosys Springboard Internship 5.0

This repository contains all the projects done under Infosys speringboard Internship showcasing the implimentation of LLM. It includes Creating Dataset, using API for impliment LLM locally , model management, and creating documentation.

## Internship Structure

### Milestone 1

Task done during Milestone 1:
1. Successful settup of the project environment environment:
  Crteating vertual python environment "myenv" by running the following code:
  A. Using conda
  ```
  conda create -p myenv python==3.12-y
  ```
  B. Using pyhton
  ```
    python -m venv myenv
```
2  . Creating mock CRM data for Sentiment Analysis
  The dataset "Sentiment.csv" is created using two sources and randomly chosing values to create remaining columns

  Sources used:
  - `For Feedbacks:`  https://huggingface.co/datasets/argilla/tripadvisor-hotel-reviews?row=62&library=datasets .
  - `For names and emails:`  https://www.datablist.com/learn/csv/download-sample-csv-files?form=MG0AV3 .

Exicute the dataset.py to create dataset for sentiment analysis:
```
python src/dataset.py
```

### Milestone 2

Implimenting Sentiment analysis ingine
The sentiment analysys model is deployed using streamlit, UI includes a textbox to enter the feed back and a submit button to get the sentiment and suggestions
Exicute the following command to run the model

```
streamlit run src\Sentiment_model.py
```