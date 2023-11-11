import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December) [10]
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    months_index = {
        "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5,
        "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
        }
    visitor_type_index = {"New_Visitor": 0, "Other": 0, "Returning_Visitor": 1}
    weekend_index = {"FALSE": 0, "TRUE": 1}


    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # This will skip the header

        evidence = []
        labels = []


        # ###### How to use `enumerate` ######
        # string = "Hello, world!"
        # new_list = enumerate(string)
        # print(new_list)  # [(0, 'H'), (1, 'e'), (2, 'l'), (3, 'l'), (4, 'o'), (5, ','), (6, ' ')]
        for row in reader:
            row_data = []  # Set a list to store the value

            ###### Use loop and conditional to make code and data easier to maintain and adjust in the future ######
            for i, value in enumerate(row[:-1]): # Exclude the last column (labels)

                ### Columns need to special handling
                if i == 10:
                    row_data.append(months_index[value]) # value is "Jan", "Feb", etc then convert to 0, 1, ...
                elif i == 15:
                    row_data.append(visitor_type_index[value])
                elif i == 16:
                    row_data.append(weekend_index[value])
                else:
                    ### Handling float and int data type ###
                        # If more column add to data, it just need edit the [] number
                    row_data.append(float(value) if i in [1, 3, 5, 6, 7, 8, 9] else int(value))
            evidence.append(row_data)

            # If Revenue is "TRUE" assign 1, else 0
            labels.append(1 if row[-1] == "TRUE" else 0)

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Intialize KNN model
    model = KNeighborsClassifier(n_neighbors=1)

    # Put the data into model and train a model
    model.fit(evidence, labels)
    
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_positives = 0
    true_negatives = 0
    total_positives = 0
    total_negatives = 0
    
    ###### How to use zip() ######
    # list1 = [1, 2, 3]
    # list2 = ['a', 'b', 'c']
    # zipped = zip(list1, list2)
    # print(zipped) # <zip object at 0x101410380>
    # for i in zipped:
    #     print(i)
    #     (1, 'a')
    #     (2, 'b')
    #     (3, 'c')
    for actual, predicted in zip(labels, predictions): # e.g. labels=[0, 0], predictions=[0,1]
        # After zip() will be:
            # (0, 0)
            # (0, 1)
 
        ### Counting ###
        if actual == 1: # `actual` is the "answer" from csv data
            total_positives += 1
            if predicted == 1: # if actual and predicted both 1, it means prediction correct
                true_positives += 1 # Add 1 to true_positives
        else:
            total_negatives += 1 # else `actual` = 0, add 1 count into `total_negatives`
            if predicted == 0: # if actual and predicted both 0, it means prediction correct
                true_negatives += 1 # Add 1 to true_negatives
    
    
    ###### Calculate `sensitivity` ######
    if total_positives == 0: # If there are no actual positive examples in the dataset, we do not have enough information to calculate
        sensitivity = 0 # set the sensitivity to 0 in this case.
    else:
        sensitivity = true_positives / total_positives
        # Formula = "correctly predicted positives" / "total positives in data set"
    

    ###### Calculate `specificity` ######
    if total_negatives == 0: # If there are no actual negatives examples in the dataset, we do not have enough information to calculate
        specificity = 0 # set the `specificity` to 0 in this case.
    else:
        specificity = true_negatives / total_negatives
        # Formula = "correctly predicted negatives" / "total negatives in data set"


    return sensitivity, specificity



if __name__ == "__main__":
    main()
