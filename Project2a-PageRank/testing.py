# import random

# DAMPING = 0.85
# SAMPLES = 10000

# corpus = {'4.html': {'2.html'}, '3.html': {'4.html', '2.html'}, '2.html': {'3.html', '1.html'}, '1.html': {'2.html'}}
# # corpus = {'4.html': {}, '3.html': {}, '2.html': {}, '1.html': {}}
# # corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}

# damping_factor = 0.85


# def transition_model(corpus, page, damping_factor):
#     """
#     Return a probability distribution over which page to visit next,
#     given a current page.

#     With probability `damping_factor`, choose a link at random
#     linked to by `page`. With probability `1 - damping_factor`, choose
#     a link at random chosen from all pages in the corpus.
#     """

#     total_pages = len(corpus)
#     N = 1 - damping_factor
#     model_result = {}
#     links = corpus[page]



#     # for p in corpus:
#     #     print("p:", p)
#     #     model_result[p] = 1/total_pages
#     #     print(model_result, model_result[p])

#     # print(model_result)

#     for page in corpus:
#         model_result[page] = (1 - damping_factor) / total_pages

#     # print(f"1. {model_result}")

    
#     for link in links:
#         model_result[link] += damping_factor / len(links)

#     # print(f"2. {model_result}")

#     # print(model_result)
#     return model_result



# # transition_model(corpus, '1.html', damping_factor)



# def sample_pagerank(corpus, damping_factor, n):

#     pageranks = {}
#     for page in corpus:
#         pageranks[page] = 0

#     sample = random.choice(list(corpus.keys()))

    
#     for _ in range(n):
#         pageranks[sample] += 1 
#         # print(f"A: {pageranks}")
#         model = transition_model(corpus, sample, damping_factor)
#         # print(model)
        
#         sample = random.choices(list(model.keys()), weights=list(model.values()))[0]

#         # print(sample)

#     # print(pageranks)
#     return pageranks



# # sample_pagerank(corpus, DAMPING, SAMPLES)
# # print(sample_pagerank(corpus, DAMPING, SAMPLES))


# # sample = random.choice(list(corpus.keys()))
# # model = transition_model(corpus, sample, damping_factor)
# # sample2 = random.choices(list(model.keys()), list(model.values()))

# # print(sample)

# # print(list(model.keys()))
# # print(list(model.values()))
# # print(sample2)








# # def sample_pagerank(corpus, damping_factor, n):
# #     """
# #     Return PageRank values for each page by sampling n pages
# #     according to transition model, starting with a page at random.
# #     """
# #     pageranks = {page: 0 for page in corpus}
# #     sample = random.choice(list(corpus.keys()))

# #     for _ in range(n):
# #         pageranks[sample] += 1
# #         model = transition_model(corpus, sample, damping_factor)
# #         sample = random.choices(list(model.keys()), list(model.values()))[0]

# #     # Normalize the pagerank values
# #     for page in pageranks:
# #         pageranks[page] /= n

# #     return pageranks


# # def iterate_pagerank(corpus, damping_factor):
# #     """
# #     Return PageRank values for each page by iteratively updating
# #     PageRank values until convergence.
# #     """
# #     pageranks = {page: 1/len(corpus) for page in corpus}
# #     while True:
# #         new_pageranks = {}
# #         for page in pageranks:
# #             rank = (1 - damping_factor) / len(corpus)
# #             for p in corpus:
# #                 if page in corpus[p]:
# #                     rank += damping_factor * pageranks[p] / len(corpus[p])
# #             new_pageranks[page] = rank

# #         # Check for convergence
# #         if all(abs(pageranks[p] - new_pageranks[p]) < 0.001 for p in pageranks):
# #             return new_pageranks
# #         pageranks = new_pag





# def iterate_pagerank(corpus, damping_factor):
#     pagerank = {}
#     for page in corpus:
#         pagerank[page] = 1/len(corpus)
        

#     threshold = 0.001
#     while True:
#         new_pagerank = {}
#         for page in corpus:
#             ### Divide the PageRank formula into two parts ###
#                 ### rank & sum_links ###
            
#             #### rank ####
#             ## Every page has an equal chance of being selected, so it gets a basic PageRank ##
#             rank = (1 - damping_factor) / len(corpus)
#                 # (1 - d) ×  (1 / N) the 1st part of formula
#                     # We igrone the "1" then change "*" to "/"
#                     # Because (x * 1/N) = (x / N)


#             #### sum_links ####
#             ## Each other page that links("votes") to the current page ##
#                 # Summed up these "votes" is a sum_links  
#             # d × ∑(PR(i)/NumLinks(i)) the 2nd part of formula
#                 # ∑ means sum all links, we use `+=` to do this
#             sum_links = 0 # ∑: The sum of the pages that point to the page
#             for i in corpus: 
#             # e.g. i = 3.hmtl

#                 if page in corpus[i]: # 4.html # check if there is a 4.html in 3.html
#                 # if page: 4.html in corpus[i3.html]: {'2.html', '4.html'} ➔ True

#                     # sum_likes: 0
#                     sum_links += pagerank[i] / len(corpus[i])
#                     # sum_links: 0.125 += pagerank[i: 3.html]: 0.25 / len(corpus[i3.html]): 2)
#             print(f"rank: {rank} + damping_factor: {damping_factor} * sum_links: {sum_links}")
            
            
#             ### Update the new_pagerank ###
#             new_pagerank[page] = rank + damping_factor * sum_links

            


#             differences = []
#             for page in pagerank:
                
#                 if page in new_pagerank:
#                 # if page: 4.html in new_pagerank: {'4.html': 0.0375}

#                     differences.append(new_pagerank[page] - pagerank[page])
#                     # differences.append(0.0375 - 0.25)
#                 else:
#                     differences.append(0)


#         # 檢查收斂
#         if all(diff < threshold for diff in differences):  # 如果所有差異都小於閾值
#             return new_pagerank
            
#         pagerank = new_pagerank
            
#         return pagerank
        

# iterate_pagerank(corpus, DAMPING)


#                     # print("Start")
#                     # print(f"if page: {page} in new_pagerank: {new_pagerank}")

#                     # print(f"differences.append({new_pagerank[page]} - {pagerank[page]})")

# # (1-d)/N (the 1st part of formula)
#     #     # d = dampin_factor, N = total_pages
#     # for page in corpus: # Do this in every page, here is "1.html"
#     #     # "1.html" PageRank(PR)
#     #     model_result[page] = (1 - damping_factor) / total_pages
#     #     # (1-0.85)/3 = 0.05



#                 # print("START")
#                 # print(f"i: {i}")
#                 # print(f"corpus: {corpus}")

#                 #     print(f"if page: {page} in corpus[i{i}]: {corpus[i]}")
#                 #     print(f"sum_likes: {sum_links}")

#                 #     print(f"sum_links: {sum_links} += pagerank[i: {i}]: {pagerank[i]} / len(corpus[i{i}]): {len(corpus[i])})")





import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

##### ❗️❗️❗️ VSCode play button Not work in this project ❗️❗️❗️#####

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
        # Here is take 2 parameters in terminal
        # in terminal: python pagerank.py corpus0
            # the "pagerank.py"=0, "corpus0"=1

    # "sys.argv[1]" is the name of a folder that contian some webpage(.html)
    # The crawl() is doing that
        # Extract the link in html and make a Python dict
    corpus = crawl(sys.argv[1])
    # it will return a dict
        # {'4.html': {'2.html'}, '3.html': {'4.html', '2.html'}, '2.html': {'3.html', '1.html'}, '1.html': {'2.html'}}

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):

    model_result = {}
    total_pages = len(corpus) 
    links_in_page = corpus[page]

    if len(links_in_page) == 0: # links = {}
        # Click probability. If total has 4 pages => 1/4=0.25
        equal_click_prob = round(1/total_pages, 3)

        for page in corpus: # iterate all pages in corpus0
            model_result[page] = equal_click_prob
        return model_result # {'4.html': 0.25, '3.html': 0.25, '2.html': 0.25, '1.html': 0.25}

    for page in corpus: # Do this in every page, here is "1.html"
        # "1.html" PageRank(PR)
        model_result[page] = round((1 - damping_factor) / total_pages, 3)

    for link in links_in_page: # link_in_page = "2.html", "3.html"
        model_result[link] = round(model_result[link] + damping_factor / len(links_in_page), 3)

    return model_result


import random

def sample_pagerank(corpus, damping_factor, n):

    pageranks = {}

    for page in corpus:
        pageranks[page] = 0

    sample = random.choice(list(corpus.keys()))

    for _ in range(n):  # If not be reused variable, convention in Python to use `_`
        pageranks[sample] += 1

        model = transition_model(corpus, sample, damping_factor)

        # Update the sample (change)
        sample = random.choices(list(model.keys()), weights=list(model.values()))[0]

    for page in pageranks:
        pageranks[page] = round(pageranks[page] / n, 3)

    return pageranks


def iterate_pagerank(corpus, damping_factor):

    pagerank = {}
    for page in corpus:
        pagerank[page] = 1/len(corpus)

    threshold = 0.001

    while True:
        new_pagerank = {}
        for page in corpus:

            basic_rank = (1 - damping_factor) / len(corpus)

            sum_links = 0  # ∑: The sum of the pages that point to the page
            for i in corpus:

                if page in corpus[i]:  # 4.html # check if there is a 4.html in 3.html
                    sum_links += pagerank[i] / len(corpus[i])

            new_pagerank[page] = basic_rank + damping_factor * sum_links

        differences = []
        for page in pagerank:
            diff = abs(new_pagerank[page] - pagerank[page])
            differences.append(diff)

        pagerank = new_pagerank

        below_threshold = True  # By default, all differences are below the threshold.

        for diff in differences:
            if diff >= threshold:
                below_threshold = False
                break

        if below_threshold:
            # Round the final pagerank values to 3 decimal places before returning
            for page in pagerank:
                pagerank[page] = round(pagerank[page], 3)
            return pagerank




if __name__ == "__main__":
    main()





""" 
$ python pagerank.py corpus0
PageRank Results from Sampling (n = 10000)
  1.html: 0.2223
  2.html: 0.4303
  3.html: 0.2145
  4.html: 0.1329
PageRank Results from Iteration
  1.html: 0.2202
  2.html: 0.4289
  3.html: 0.2202
  4.html: 0.1307
"""


