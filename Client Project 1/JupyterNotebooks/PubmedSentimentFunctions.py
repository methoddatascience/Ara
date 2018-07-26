
# coding: utf-8

# map part of speech for sentiment library from returned form
def map_pos(x):
    x = str(x)
    newtag = ''
    if x.startswith('NN'):
        newtag = 'n'
    elif x.startswith('JJ'):
        newtag = 'a'
    elif x.startswith('V'):
        newtag = 'v'
    elif x.startswith('R'):
        newtag = 'r'
    else:
        newtag = ''
    return newtag
    
# tag the word for pos
def abs_tagger(x):
    text = nltk.word_tokenize(x)
    return nltk.pos_tag(text)    

# get sentiment score of document
def tag_get_score(x,sentences=False,weights=None):
    import json
    
    if sentences:
        
        x = x.split('.')
        
        sent_score = []
        n_sentences = len(x)
        #print(n_sentences)
        #print(x)
        
        for i in range(n_sentences):
            sentence_score = []
            #print(x)
            tagged_tokens = abs_tagger(x[i])

            for token in tagged_tokens:
                lemma = token[0]
                newtag = map_pos(token[1])
                if newtag != '':
                    #swn_term = str(lemma + '.'+newtag+'.01')
                    swn_lemma = list(swn.senti_synsets(lemma,newtag))
                    score = 0.0
                    if (len(swn_lemma)>0):
                        for s in swn_lemma:
                            score = s.pos_score() - s.neg_score()
                        sentence_score.append(score / len(swn_lemma))
            
            sum_score = sum([word_score for word_score in sentence_score])
            sent_score.append(sum_score)
        
        #print(sent_score)
        
        if (len(sent_score) == 0) | (len(sent_score)==1):
            return float(0.0)
        else:
            if weights == None:
                return sum([word_score for word_score in sent_score])# / (len(sent_score))),
                        #(len(sent_score)/float(len(tagged_tokens))))
            else:
                weighted_scores = []
                mid = n_sentences/2.0
                if len(sent_score) > 0:
                    for j in range(len(sent_score)):
                        if j > mid:
                            weighted_scores.append((sent_score[j]*weights[1]))
                        elif j <= mid:
                            weighted_scores.append((sent_score[j]*weights[0]))
                    return sum([score for score in weighted_scores])
                    
                else:
                    return float(0.0)

    else:
    
        sent_score = []

        tagged_tokens = abs_tagger(x)

        for token in tagged_tokens:

            lemma = token[0]

            newtag = map_pos(token[1])

            if newtag != '':
                #swn_term = str(lemma + '.'+newtag+'.01')
                swn_lemma = list(swn.senti_synsets(lemma,newtag))
                score = 0.0
                if (len(swn_lemma)>0):
                    for s in swn_lemma:
                        score = s.pos_score() - s.neg_score()
                    sent_score.append(score / len(swn_lemma))

        if (len(sent_score) == 0 or len(sent_score)==1):
            return (float(0.0),0.00)
        else:
            #print(sent_score)
            return sum([word_score for word_score in sent_score])#, / (len(sent_score))),
                    #(len(sent_score)/float(len(tagged_tokens))))