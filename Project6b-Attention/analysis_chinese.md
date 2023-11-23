# Analysis

## Layer 3, Head 1
![[L3H1]]
- 辨識並確立 "Each word is paying attention to the word that immediately follows it." 這種模式
    - 在 Document 提到 Layer 3, Head 10: "attention head appears to have learned a very clear pattern"

- 不同的句子，模型首次辨識出這種 pattern 的Layer and head 都不同 (以肉眼能判斷圖片的 pattern為準)
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
    
### 結論
- 不論句子的複雜程度，模型在 Layer 3, Head 1 都能辨識並確立這種模式
    - 所以這以乎是一個重要的 Layer and Head。
- 不論是什麼形式的句子，模型都一定會辨識出 "理解文本序列中的一個單詞通常取決於知道下一個單詞是什麼" 有用的
- 我認為這樣的話，模型的可靠性就得以証實，畢竟我們不希望模型每次都以隨機的形式去理解文本



## Layer 1, Head 12 and Layer 2, Head 1
![[L1H12]]
![[L2H1]]
- 完整縱向處於 `[MASK]` 的直線 pattern
- 所有單詞都一起關注 `[MASK]` 幾乎都能在這裡以肉眼辨識出來
- 根據句子的結構不同，這個 pattern 可能會出現在 Layer 1, Head 12 或 Layer 2, Head 1
    - 但似乎與句子複雜程度無關
        - 因為在測試句子中, "She said that she would `[MASK]` tomorrow" 和 "Why are you `[MASK]`" 都是在 Layer 2, Head 1 有更明顯的 pattern

Example Sentences:
##### Attention_Layer1_Head12
- The dog sat on the `[MASK]`
- The dog `[MASK]` on the mat
- She said that she would `[MASK]` tomorrow
    - 已可辨識 pattern
    - Attention_Layer2_Head1
        - Pattern 更明顯
- Why are you `[MASK]`
    - Attention_Layer2_Head1
        - Pattern 更明顯
- I do not like this `[MASK]`
- The teacher explained the `[MASK]` to the students
- He is looking for his `[MASK]`

### 結論
- 我認為這是模型在辨識過程中，通常給予`[Mask]`關注的一個 Layer and Head
- 鑑於我們的目標是讓模型對不同字詞進行預測或建議，而 `[MASK]` 是一個重要且經常出現的標記，模型似乎在 Layer 1, Head 12 或 Layer 2, Head 1 中固定且有規律地關注 `[MASK]`
- 在我測試過的所有句子中，只有 `[MASK]` 會出現這個 pattern。
    - 我認為這很合理，因為對模型來說這是一個標記，它的目標就是找出一些合理字來填進這個標記裡
- 明顯地，model 會遵循一定的規律在 Layer 1, Head 12 或 Layer 2, Head 1 中讓每個單詞都給予 `[MASK]` 關注



## Layer 6, Head 10
![[L6H10]]
- 辨識 "the' 與其後的單詞的 Layer and Head
- 在測試包含 'the' 的三個句子中，Layer 6, Head 10 的圖表顯示 'the' 總是關注其緊隨的單詞
- 就算句子中出現兩個 "the"，也是會在這裡顯示出每個 "the" 都在關注緊跟其後的單詞

Example Sentences:
- The dog sat on the `[MASK]`
- The dog `[MASK]` on the mat
- The teacher explained the `[MASK]` to the students

#### 結論
- 我們幾乎可以確定 Layer 6, Head 10 是模型用來處理 "the" 的一個 Layer and Head












