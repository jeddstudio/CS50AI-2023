import sys
import tensorflow as tf

from PIL import Image, ImageDraw, ImageFont
from transformers import AutoTokenizer, TFBertForMaskedLM

# Pre-trained masked language model
MODEL = "bert-base-uncased"

# Number of predictions to generate
K = 3

# Constants for generating attention diagrams
FONT = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 28)
GRID_SIZE = 40
PIXELS_PER_WORD = 200


def main():
    text = input("Text: ")

    # Tokenize input
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    inputs = tokenizer(text, return_tensors="tf")
    mask_token_index = get_mask_token_index(tokenizer.mask_token_id, inputs)
    if mask_token_index is None:
        sys.exit(f"Input must include mask token {tokenizer.mask_token}.")

    # Use model to process input
    model = TFBertForMaskedLM.from_pretrained(MODEL)
    result = model(**inputs, output_attentions=True)

    # Generate predictions
    mask_token_logits = result.logits[0, mask_token_index]
    top_tokens = tf.math.top_k(mask_token_logits, K).indices.numpy()
    for token in top_tokens:
        print(text.replace(tokenizer.mask_token, tokenizer.decode([token])))

    # Visualize attentions
    visualize_attentions(inputs.tokens(), result.attentions)


def get_mask_token_index(mask_token_id, inputs):
    """
    `mask_token_id` means getting "[MASK]"'s token id, which is 103, the model given
    
    Return the index of the token with the specified `mask_token_id`, or
    `None` if not present in the `inputs`.
    """
    ### text = "I am a [MASK]" ###
    ###### `inputs` is a dictionary that contain input_ids, token_type_ids, attention_mask
    # inputs
    # {
    #   'input_ids': <tf.Tensor: shape=(1, 6), dtype=int32, numpy=array([[ 101, 1045, 2572, 1037,  103,  102]], dtype=int32)>, 
    #   'token_type_ids': <tf.Tensor: shape=(1, 6), dtype=int32, numpy=array([[0, 0, 0, 0, 0, 0]], dtype=int32)>, 
    #   'attention_mask': <tf.Tensor: shape=(1, 6), dtype=int32, numpy=array([[1, 1, 1, 1, 1, 1]], dtype=int32)>
    # }
    
    input_ids = inputs["input_ids"][0] # Get `input_ids` = tf.Tensor([ 101 1045 2572 1037  103  102], shape=(6,), dtype=int32)

    for index, token_id in enumerate(input_ids): # `enumerate` will give a index to each token_id, [(0, 101), (1, 1045), ...]
        if token_id == mask_token_id: # Check if the token id(103) is exist 
            return index # [ 101, 1045, 2572, 1037,  103,  102], find 103, so it is 4

    return None # If can't find the token, return None



def get_color_for_attention_score(attention_score):
    """
    accept an attention score (a value between 0 and 1, inclusive)
    
    Return a tuple of three integers representing a shade of gray for the
    given `attention_score`. Each value should be in the range [0, 255].
    """
    # `attention_score` is a number between 0 and 1
    attention_score_color = round(attention_score.numpy() * 255)
        # Use `.numpy()` method to convert the EagerTensor to a normal Python number
        
    color_tuple = (attention_score_color, attention_score_color, attention_score_color)

    return color_tuple



def visualize_attentions(tokens, attentions):
    """
    Produce a graphical representation of self-attention scores.

    For each attention layer, one diagram should be generated for each
    attention head in the layer. Each diagram should include the list of
    `tokens` in the sentence. The filename for each diagram should
    include both the layer number (starting count from 1) and head number
    (starting count from 1).
    """
    # tokens = ['[CLS]', 'i', 'am', 'a', '[MASK]', '[SEP]']
    # len(attentions) = 12

    for i, layer in enumerate(attentions): # `enumerate` will give a index(`i`) to each `attentions` items, then it will be `layer`
        layer_number = i + 1
        ###### How `layer` look like at the below ######
        # No `j` for loop here, because document say: `j` is the index of the beam number (always 0 in our case),
        for k, head in enumerate(layer[0]): # `enumerate` will give a index(`k`) to each `layer` items, then it will be `head`
            ###### How `head` look like at the below ######
            head_number = k + 1

            generate_diagram(
                layer_number,
                head_number,
                tokens, # ['[CLS]', 'i', 'am', 'a', '[MASK]', '[SEP]']
                head # attension head,  `attentions[i][j][k]`
            )


def generate_diagram(layer_number, head_number, tokens, attention_weights):
    """
    Generate a diagram representing the self-attention scores for a single
    attention head. The diagram shows one row and column for each of the
    `tokens`, and cells are shaded based on `attention_weights`, with lighter
    cells corresponding to higher attention scores.

    The diagram is saved with a filename that includes both the `layer_number`
    and `head_number`.
    """
    # Create new image
    image_size = GRID_SIZE * len(tokens) + PIXELS_PER_WORD
    img = Image.new("RGBA", (image_size, image_size), "black")
    draw = ImageDraw.Draw(img)

    # Draw each token onto the image
    for i, token in enumerate(tokens):
        # Draw token columns
        token_image = Image.new("RGBA", (image_size, image_size), (0, 0, 0, 0))
        token_draw = ImageDraw.Draw(token_image)
        token_draw.text(
            (image_size - PIXELS_PER_WORD, PIXELS_PER_WORD + i * GRID_SIZE),
            token,
            fill="white",
            font=FONT
        )
        token_image = token_image.rotate(90)
        img.paste(token_image, mask=token_image)

        # Draw token rows
        _, _, width, _ = draw.textbbox((0, 0), token, font=FONT)
        draw.text(
            (PIXELS_PER_WORD - width, PIXELS_PER_WORD + i * GRID_SIZE),
            token,
            fill="white",
            font=FONT
        )

    # Draw each word
    for i in range(len(tokens)):
        y = PIXELS_PER_WORD + i * GRID_SIZE
        for j in range(len(tokens)):
            x = PIXELS_PER_WORD + j * GRID_SIZE
            color = get_color_for_attention_score(attention_weights[i][j])
            draw.rectangle((x, y, x + GRID_SIZE, y + GRID_SIZE), fill=color)

    # Save image
    img.save(f"Attention_Layer{layer_number}_Head{head_number}.png")


if __name__ == "__main__":
    main()






####################  How `head` look like at the below ####################
# tf.Tensor(
# [[0.01237046 0.0934256  0.08169395 0.12281024 0.2692147  0.4204851 ]
#  [0.01283372 0.02126785 0.01923147 0.01858194 0.00490376 0.92318124]
#  [0.03517947 0.05988495 0.05430293 0.04942672 0.01550243 0.7857034 ]
#  [0.0175418  0.03574592 0.02370158 0.13210581 0.02318027 0.76772463]
#  [0.00744741 0.01290579 0.01125522 0.12516473 0.00471473 0.83851206]
#  [0.0031575  0.00561968 0.00411203 0.00676647 0.004384   0.9759603 ]], shape=(6, 6), dtype=float32)
# ####################





#################### How `layer` look like at the below ####################
# tf.Tensor(
# [[[[0.34687352 0.04233294 0.05527904 0.03886557 0.12055959 0.3960894 ]
#    [0.02979699 0.02286384 0.02723755 0.02474351 0.05256964 0.8427885 ]
#    [0.02821026 0.01667533 0.02018396 0.02522021 0.05250066 0.85720956]
#    [0.02435393 0.01836583 0.01818775 0.01774842 0.01939908 0.901945  ]
#    [0.03536181 0.01151882 0.02116669 0.02036151 0.04158567 0.8700054 ]
#    [0.01089906 0.00794178 0.00703958 0.00950539 0.00587353 0.95874065]]

#   [[0.19280098 0.0809918  0.06551743 0.08189613 0.13392965 0.44486403]
#    [0.01945849 0.01369948 0.01746703 0.02328239 0.02432958 0.901763  ]
#    [0.01192074 0.01160703 0.00684879 0.00952527 0.01754363 0.94255453]
#    [0.04463115 0.06762791 0.03757316 0.0334372  0.07773472 0.73899585]
#    [0.03236038 0.02543367 0.04317477 0.0212725  0.04138163 0.8363771 ]
#    [0.00498398 0.00706213 0.00719164 0.0123251  0.01875681 0.94968045]]

#   [[0.41684213 0.1341772  0.0943699  0.09707221 0.17524831 0.08229032]
#    [0.05962666 0.13122523 0.07840201 0.06213865 0.12307067 0.5455367 ]
#    [0.04553659 0.11761434 0.09708366 0.19985348 0.1353273  0.40458462]
#    [0.06684157 0.04139737 0.04746815 0.09435996 0.08122344 0.6687095 ]
#    [0.04812749 0.0668987  0.042991   0.030131   0.05755878 0.754293  ]
#    [0.01044417 0.0102696  0.01021805 0.01549248 0.0205255  0.93305016]]

#   [[0.12128255 0.339862   0.18385062 0.09261605 0.09053242 0.17185642]
#    [0.02960555 0.02335693 0.02161264 0.01258098 0.01461881 0.8982251 ]
#    [0.01540414 0.01310916 0.0104727  0.00813305 0.0049938  0.9478872 ]
#    [0.06670182 0.01986295 0.01130977 0.01284646 0.01473814 0.8745409 ]
#    [0.01001274 0.00210247 0.00159134 0.00329386 0.00388897 0.97911066]
#    [0.0066715  0.00363773 0.00271793 0.00397696 0.00407793 0.9789179 ]]

#   [[0.01940287 0.03604952 0.1284923  0.32042065 0.47075513 0.02487959]
#    [0.04144786 0.03249265 0.06101525 0.1584818  0.07742457 0.6291379 ]
#    [0.05893876 0.02504501 0.06788714 0.2387175  0.06194655 0.547465  ]
#    [0.10195666 0.05014061 0.11107173 0.2896702  0.06819754 0.37896326]
#    [0.5411717  0.01110943 0.0469359  0.14248097 0.21063228 0.04766963]
#    [0.00807295 0.00435419 0.00575289 0.01283983 0.00556834 0.96341175]]

#   [[0.07245984 0.08967677 0.11408892 0.32992816 0.1564881  0.2373582 ]
#    [0.01537071 0.06426252 0.04758146 0.15199734 0.09906454 0.6217234 ]
#    [0.01454664 0.05101245 0.08720912 0.15593489 0.08439741 0.60689944]
#    [0.03134338 0.04180603 0.03376304 0.38674426 0.0802735  0.42606977]
#    [0.01029174 0.01438287 0.01841665 0.1337228  0.07167045 0.75151545]
#    [0.00648823 0.00723607 0.00678018 0.0244835  0.00456064 0.9504514 ]]

#   [[0.20073979 0.03552518 0.06027422 0.20648645 0.39226627 0.10470806]
#    [0.06835698 0.02916134 0.01868143 0.08001067 0.02316525 0.78062433]
#    [0.0582551  0.0292982  0.04313417 0.06630413 0.04740249 0.75560594]
#    [0.07142169 0.04370872 0.04807097 0.10075387 0.09322404 0.6428207 ]
#    [0.15788321 0.0686309  0.07780106 0.10770759 0.0407136  0.5472637 ]
#    [0.01706294 0.01535958 0.0104934  0.01516984 0.01508245 0.9268318 ]]

#   [[0.24741276 0.08043555 0.06110797 0.12057894 0.20798327 0.28248146]
#    [0.01963033 0.01194585 0.0130127  0.08311756 0.01611687 0.85617673]
#    [0.01624535 0.01071245 0.01299302 0.07270518 0.01456669 0.87277734]
#    [0.03981989 0.01787128 0.0178214  0.25292662 0.03790906 0.63365173]
#    [0.04475446 0.02856929 0.03980565 0.26339763 0.03007578 0.59339714]
#    [0.00239966 0.00159641 0.00236453 0.00594839 0.00171636 0.9859746 ]]

#   [[0.38827583 0.0704089  0.08151007 0.1445785  0.27176955 0.04345712]
#    [0.08502356 0.1957086  0.1167701  0.12158998 0.04652693 0.43438092]
#    [0.03391171 0.10618664 0.5883146  0.06083287 0.03258085 0.17817338]
#    [0.03698301 0.0360493  0.04646106 0.44437116 0.03806093 0.39807454]
#    [0.02450416 0.01450756 0.0162872  0.09821139 0.12290732 0.7235823 ]
#    [0.00247247 0.00350599 0.00496725 0.01971895 0.00170531 0.96763   ]]

#   [[0.3970214  0.14606585 0.14692768 0.16558847 0.08296105 0.06143556]
#    [0.14979507 0.13190968 0.10609161 0.06557339 0.21101949 0.33561072]
#    [0.11180272 0.09532279 0.1364689  0.06583477 0.10618379 0.48438704]
#    [0.0629893  0.04418528 0.04364034 0.0947134  0.1401994  0.6142723 ]
#    [0.0319114  0.05545734 0.01617319 0.02459869 0.12635323 0.7455061 ]
#    [0.02356754 0.01488467 0.01357921 0.01389387 0.04518403 0.8888907 ]]

#   [[0.01237046 0.0934256  0.08169395 0.12281024 0.2692147  0.4204851 ]
#    [0.01283372 0.02126785 0.01923147 0.01858194 0.00490376 0.92318124]
#    [0.03517947 0.05988495 0.05430293 0.04942672 0.01550243 0.7857034 ]
#    [0.0175418  0.03574592 0.02370158 0.13210581 0.02318027 0.76772463]
#    [0.00744741 0.01290579 0.01125522 0.12516473 0.00471473 0.83851206]
#    [0.0031575  0.00561968 0.00411203 0.00676647 0.004384   0.9759603 ]]

#   [[0.00496631 0.02078294 0.01428395 0.08010499 0.0815016  0.7983602 ]
#    [0.00614037 0.01041782 0.01045649 0.03592163 0.01686138 0.9202024 ]
#    [0.00965811 0.0215684  0.01987125 0.02892488 0.01831484 0.90166247]
#    [0.04106911 0.03134402 0.02710971 0.1761441  0.04082673 0.68350637]
#    [0.05886307 0.01709531 0.02372343 0.19543694 0.04631519 0.65856606]
#    [0.00255576 0.00388115 0.00383885 0.01347578 0.00321828 0.9730302 ]]]], shape=(1, 12, 6, 6), dtype=float32)
####################