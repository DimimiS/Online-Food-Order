import pandas as pd
import os


def findFiles(output="output.csv"):
    files = [
        file
        for file in os.listdir()
        if file.endswith(".csv") and file != output and file != "outputEnglish.csv"
    ]
    # print(files)
    return files


def replaceCommas(data, columns):
    for column in columns:
        attributes = []
        for attr in data[column]:
            if type(attr) == str and attr != None:
                attributes.append(attr.replace(",", ""))
            else:
                attributes.append(attr)
        data[column] = attributes
    return data


if __name__ == "__main__":
    # read burger (the one that we modified correctly)
    data = pd.read_csv("burger.csv", encoding="utf-8")
    # and get all the attributes we need for a restaurant
    columns = data.columns

    files = findFiles(output="output.csv")

    categories = []
    data = data[0:0]  # empty dataframe while keeping its structure
    for file in files:
        # data2 is the dataframe of the current file
        # data is the dataframe of all the files

        data2 = pd.read_csv(file, encoding_errors="ignore", usecols=columns)

        # add a column for the category
        data2["Category"] = file.split(".")[0]

        # if any attribute has a comma, replace it with a space
        # because we are using comma as a delimiter
        data2 = replaceCommas(data2, columns)

        # add the current dataframe to the main dataframe
        data = pd.concat([data, data2], ignore_index=True)

    # show what was saved in the dataframe
    print(data)

    # save the dataframe to a csv file
    data.to_csv("output.csv", encoding="utf-16", index=False)
