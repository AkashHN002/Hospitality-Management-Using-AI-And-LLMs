# AI-Driven Guest Experience Personalization System for Hospitality

This repository contains all the projects done under Infosys speringboard Internship showcasing the implimentation of LLM. Tasks includes-
- Collecting CRM dataset for sentiment analysis and Using API for impliment LLM locally.
- Implimentation of sentiment analysis ingine: to generate real-time alerts and suggestion based on detected changes in guest sentiment.
- Personalised recommondation system and Dynamic profile management system: successfully updates based on real-time behaviour analysis.
- Staff notification system integrated with Slack & Email: Automated alerts sent regarding potential service issue or personilzation opportunities.

<br>

Crteate vertual python environment "myenv" by running the following code:
A. Using conda
 ```
 conda create -p myenv python==3.12-y
 connda activate myenv
 ```
   B. Using pyhton

 ```
 python -m venv myenv
 myenv\Scripts\activate
 ```
 <br>
    
After activating python 3.12 environment, execute requirement.txt to install required libraries.

 ```
 pip install -r requirements.txt
 ```
    
<br>


Implimenting Sentiment analysis ingine.

The sentiment analysys model is deployed using streamlit, UI includes a textbox to enter the feed back and a submit button to get the sentiment and suggestions

Exicute the following command to run the model

```
streamlit run src\Sentiment_model.py
```
<br>


Implimenting Personalised Recommondation system.

To build a recommondation system , first we have to load the interaction.csv, which has all the data regarding users interaction
   Execute the following command to load interaction data
   ```
   python src/Load_recommendation_data.py
   ```

Recommondation system UI includes a text box which accepts the User ID and gives the recommooondation based on similar user by implimenting Cosine similarity.
   Execute the following command to run the recommondation system
   ```
   streamlit run src/Recommendation.py
   ```

Dynamic Profile Management

Dynamic Profile Management involves the real-time creation, modification, and management of user profiles within a system. The user interface facilitates this by allowing users to enter their User ID, request required information    which helps to efficiently manage       the database.
   Execute the following command for Dynamic profile management
   ```
   python src/Profile.py
   ```
<br>


Staff notification system integrated with Slack & Email. The notificcations based on feedback are sent to the staff via slack and the recommendations are sent to the user via the email. 

Execute the following command to send alerts to staff
```
streamlit run src/Alert.py
```
<br>


All the work done in the above Milestones are combined to one webpage. Make sure that API key is correct, Datasets are created, Versions are matching, Database has the required tables, slack bot is initialised to the required channel and requirements for sending emails are complete.

Execute the following command to run the Hospitality management webpage. 
```
streamlit run Hospitality_Management.py
```
