from nltk.sentiment.vader import SentimentIntensityAnalyzer

# decently capable at sarcasm
# does not pick up on criticism stated very objectively as negative
# noticeably biased towards positive values

def sentiment_vader(sentence):
    sent_obj = SentimentIntensityAnalyzer()

    sentiment_dict = sent_obj.polarity_scores(sentence)
    negative = sentiment_dict['neg']
    neutral = sentiment_dict['neu']
    positive = sentiment_dict['pos']
    compound = sentiment_dict['compound']

    print(list(sentiment_dict.keys())[list(sentiment_dict.values()).index(max(sentiment_dict.values()))])

    # if sentiment_dict['compound'] <= 0.33:
    #     overall_sent = 'Negative'
    
    # elif sentiment_dict['compound'] >= 0.66:
    #     overall_sent = 'Positive'

    # else:
    #     overall_sent = 'Neutral'

    return sentiment_dict

    # return negative, neutral, positive, compound, overall_sent  

def vader_sent_test(sentence):
    return
 
example_sentences = [ "Great work @lufthansa take a suit carrier off me and then have me waste a full hour waiting on the incompetent services of your partner in Warsaw. #Lufthansa",
                      "Hey @lufthansa, I'd think that a company as big as yours would segment newsletter subs at least a letter. Sending a newsletter solely dedicated to family travel to people who don't have a family is kind of off-putting and utterly irrelevant.",
                      "RT @ITLNLive: .@lufthansa receives first A321neo in @Airport_FRA (@lufthansaNews)",
                      "Dear @united please follow suite with the rest of these airlines. I use you due to @lufthansa frequent flier program and would like to not pay an arm and a leg just to fly with my bike.",
                      "I really hate this. Like when I get email updates for events at the Hoxton for anywhere that isn't Amsterdam (usually London). It is a waste of time! Got excited when I opened one only to see it wasn't relevant for here 😕",
                      "@lufthansa Group Airlines offer more than 11,000 flights a week to more than 270 destinations #worldwide - http://bit.ly/2YEp8Py #Travel #connections @eurowings",
                      "OK, it is now another week that has passed and nothing. I have yet to even be reimbursed the $98.00 I paid for the selected seats and that is since April 23. At this point I am not at all impressed with @lufthansa customer service department. I need to speak to someone PLEASE.",
                      "Your parents are literally the worst people in this world, I wish I never met you, fucking peasant fuck. Your mom gave birth to you and your dad tried to push you back into her vagina",
                      "This is so bad i hate it you are terrible and i am extremely dissapointed" ]


for i in range(len(example_sentences)):
    print(sentiment_vader(example_sentences[i]))
