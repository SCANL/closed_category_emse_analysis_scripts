import os
import csv
import argparse
import re
from spiral import ronin

#https://7esl.com/conjunctions-list/

conjunctions = {"for", "and", "nor", "but", "or", "yet", "so", "although", "after", "before", "because", "how",
                "if", "once", "since", "until", "unless", "when", "as", "that", "though", "till", "while", "where", "after",
                "although", "as", "as if", "as long as", "as much as", "as soon as", "as far as", "as though", "by the time",
                "in as much as", "in as much", "in order to", "in order that", "in case", "lest", "though", "now that", "now since", 
                "now when", "now", "even if", "even", "even though", "provided", "provided that", "else", "if then", "if when", "if only", 
                "just as", "where", "wherever", "whereas", "where if", "whether", "since", "because", "whose", "whoever", "unless",
                "while", "before", "why", "so that", "until", "how", "since", "than", "till", "whenever", "supposing", "when", 
                "or not", "what", "also", "otherwise", "for", "neither nor", "and", "not only but also", "nor", "whether or", "but", 
                "so that", "or", "such that", "yet", "as soon as", "so", "as well as", "also", "provided that", "as well as", "whoever", 
                "yet", "while", "still", "until", "too", "unless", "only", "since", "however", "as if", "no less than", "no less than", 
                "which", "otherwise", "where", "in order that", "who", "than", "after", "as", "because", "either or", "whoever", "nevertheless", 
                "though", "else", "although", "if", "if", "while", "till", "no sooner than"}


#https://en.wikipedia.org/wiki/List_of_English_determiners
#numbers like 'zero' removed.
determiners = {"a", "a few", "a little", "all", "an", "another", "any", "anybody", "anyone", "anything", "anywhere", "both", "certain", "each", 
               "either", "enough", "every", "everybody", "everyone", "everything", "everywhere", "few", "fewer", "fewest", "last", "least", "less", 
               "little", "many", "many a", "more", "most", "much", "neither", "next", "no", "no one", "nobody", "none", "nothing", "nowhere", "once", 
               "said", "several", "some", "somebody", "something", "somewhere", "sufficient", "that", "the", "these", "this", "those", "us", 
               "various", "we", "what", "whatever", "which", "whichever", "you"}


prepositions = {"aboard", "about", "above", "across", "after", "against", "along", "amid", "among", "anti", "around", "as", "at", "before", "behind",
                "below", "beneath", "beside", "besides", "between", "beyond", "but", "by", "concerning", "considering", "despite", "down", "during",
                "except", "excepting", "excluding", "following", "for", "from", "in", "inside", "into", "like", "minus", "near", "of", "off", "on",
                "onto", "opposite", "outside", "over", "past", "per", "plus", "regarding", "round", "save", "since", "than", "through", "to", "toward",
                "towards", "under", "underneath", "unlike", "until", "up", "upon", "versus", "via", "with", "within", "without", "out", "till"}

def parse_csv_files(directory_path):
    words_weve_seen = set()
    total_number_identifiers = 0
    for entry in os.listdir(directory_path):
        file_path = os.path.join(directory_path, entry)
        # Check if the entry is a regular file, if so, parse it as a CSV file
        if os.path.isfile(file_path):
            with open(file_path, 'r') as csv_file:
                reader = csv.reader(csv_file, delimiter=' ')
                num_dets = num_cjs = num_digi = num_prep = 0
                if not os.path.exists("results"):
                    os.makedirs("results")
                with open ('results/conjunctions', 'a') as cjs, open ('results/determiners', 'a') as dts,open ('results/counts', 'a') as cts, open ('results/digits', 'a') as digi, open ('results/prepositions', 'a') as prepo:
                    print("\n\nCurrently scanning: {file}\n\n".format(file=file_path), file=cts)
                    for row in reader:
                        file_split = row[5].split('/')
                        total_number_identifiers = total_number_identifiers + 1
                        word_list = ronin.split(row[1])  # Modify this line to process each row as needed
                        row.append(' '.join(word_list))
                        if any(re.search(r'\b[a-z_]*test[a-z_]*\b', x.lower()) for x in file_split) or any(re.search(r'\b[a-z_]*test[a-z_]*\b', x.lower()) for x in word_list) or (row[1].lower() in words_weve_seen):
                            continue
                        if any(str1 == str2 for str1 in word_list for str2 in set(conjunctions)):
                            num_dets = num_dets + 1
                            print(','.join(row), file=cjs)
                        if any(str1 == str2 for str1 in word_list for str2 in set(determiners)):
                            num_cjs = num_cjs + 1
                            print(','.join(row), file=dts)
                        if any(str1 == str2 for str1 in word_list for str2 in set(prepositions)):
                            num_prep = num_prep + 1
                            print(','.join(row), file=prepo)
                        if any(str1.isdigit() for str1 in word_list):
                            num_digi = num_digi + 1
                            print(','.join(row), file=digi)
                        words_weve_seen.add(row[1].lower())
                    print("\n\nFinish scanning: {file}\n\n Number of dts: {num_dets}, number of cjs: {num_cjs}, number of digi: {num_digi}, number of prep: {num_prep}"
                          .format(num_dets=num_dets, num_cjs=num_cjs, num_digi=num_digi, num_prep=num_prep, file=file_path), file=cts)
    print("Completed all files. Number of Identifiers: {num}, Number of repeats: {repeats}".format(repeats=len(words_weve_seen), num=total_number_identifiers))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse each file in the specified directory as a CSV file separated by space.")
    parser.add_argument("target_directory", help="The path to the target directory.")
    args = parser.parse_args()

    target_directory = args.target_directory

    parse_csv_files(target_directory)
