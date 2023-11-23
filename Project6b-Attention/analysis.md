# Analysis

## Layer 3, Head 1
![[L3H1]]
- Identified and established the pattern "Each word is paying attention to the word that immediately follows it."
    - As mentioned in the document for Layer 3, Head 10: "the attention head appears to have learned a very clear pattern."

- For different sentences, the layer and head where this pattern is first identified vary (judged visually from the pattern in the images).
Example Sentences:
##### Attention_Layer1_Head4
- The dog sat on the `[MASK]`
##### Attention_Layer1_Head11
- The dog `[MASK]` on the mat
##### Attention_Layer2_Head2
- She said that she would `[MASK]` tomorrow  
- Why are you `[MASK]`
- I do not like this `[MASK]`
- The teacher explained the `[MASK]` to the students
##### Attention_Layer1_Head3
- He is looking for his `[MASK]`
    
### Conclusion
- Regardless of the complexity of the sentence, the model can identify and establish this pattern in Layer 3, Head 1.
    - Thus, it seems to be an important layer and head.
- No matter the form of the sentence, the model will certainly identify the usefulness of "understanding a word in a sequence of text often depends on knowing what word comes next."
- I believe this confirms the reliability of the model, as we do not want the model to interpret text in a random manner every time.



## Layer 1, Head 12 and Layer 2, Head 1
![[L1H12]]
![[L2H1]]
- A complete vertical line pattern at `[MASK]`
- All words focusing on `[MASK]` can almost always be visually identified here
- Depending on the structure of the sentence, this pattern may appear in Layer 1, Head 12 or Layer 2, Head 1
    - But it seems unrelated to the complexity of the sentence
        - For example, in the test sentences, "She said that she would `[MASK]` tomorrow" and "Why are you `[MASK]`" both show a more obvious pattern in Layer 2, Head 1

Example Sentences:
##### Attention_Layer1_Head12
- The dog sat on the `[MASK]`
- The dog `[MASK]` on the mat
- She said that she would `[MASK]` tomorrow
    - Pattern already recognizable
    - Attention_Layer2_Head1
        - Pattern more obvious
- Why are you `[MASK]`
    - Attention_Layer2_Head1
        - Pattern more obvious
- I do not like this `[MASK]`
- The teacher explained the `[MASK]` to the students
- He is looking for his `[MASK]`

### Conclusion
- I believe this is a layer and head where the model typically pays attention to `[MASK]` during the recognition process.
- Given our goal is for the model to predict or suggest different words, and since `[MASK]` is an important and frequently appearing tag, the model seems to regularly focus on `[MASK]` in either Layer 1, Head 12 or Layer 2, Head 1.
- In all the sentences I tested, only `[MASK]` showed this pattern.
    - I think this is reasonable, as for the model, this is a tag, and its goal is to find some reasonable words to fill in this tag.
- Clearly, the model follows a certain pattern in Layer 1, Head 12 or Layer 2, Head 1 to focus attention on `[MASK]` by each word.



## Layer 6, Head 10
![[L6H10]]
- Identified the layer and head for "the" and its following word.
- In the three test sentences containing 'the,' the chart for Layer 6, Head 10 consistently shows that 'the' always focuses on the word immediately following it.
- Even if there are two "the's" in a sentence, it's shown here that each "the" focuses on the word immediately following it.

Example Sentences:
- The dog sat on the `[MASK]`
- The dog `[MASK]` on the mat
- The teacher explained the `[MASK]` to the students

#### Conclusion
- We can almost be certain that Layer 6, Head 10 is the layer and head used by the model to process "the".










