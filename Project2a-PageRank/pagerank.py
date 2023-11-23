import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

##### ❗️❗️❗️ VSCode play button Not work in this project ❗️❗️❗️#####
##### ❗️❗️❗️ Use command in terminal like `python pagerank.py corpus0` ❗️❗️❗️#####

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
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
         
    這段代碼是計算當前頁面向其它頁面分配的damping_factor部分的PageRank。
    例如，如果一個頁面有3個外部鏈接，那麼它會將其PageRank的85%（假設damping_factor為0.85）平均分配給這3個鏈接。
    """
    
    # The `corpus` is a Python dictionary
        # {'4.html': {'2.html'}, '3.html': {'4.html', '2.html'}, '2.html': {'3.html', '1.html'}, '1.html': {'2.html'}}
    # The `page` is a string representing repersent where we are
        # "3.html"
    # The `damping_factor` for calculate the model_result
        # e.g. DAMPING = 0.85

    """ ############ Two situations to handle ############ """
    # 1. the page has outgoing link
    # 2. no outgoing link 


    """ ######### Variable setup ######### """
    model_result = {}
    total_pages = len(corpus) # Total website. In corpus0, it is 4, it's mean the folder has 4 .html files
    
    links_in_page = corpus[page]
    # if now model taking data: transition_model(corpus=a_dict, page="3.html", dampling_factor)
    # Then 3.html is '3.html': {'4.html', '2.html'}
    # links = {'4.html', '2.html'} when the `page` is "3.html"


    """ ###### No outgoing link ###### """
    ### If there is no link in the page, we will assume that the user randomly clicks on any page ###
    if len(links_in_page) == 0: # links = {}
        # Click probability. If total has 4 pages => 1/4=0.25
        equal_click_prob = 1/total_pages 

        for page in corpus: # iterate all pages in corpus0
            # Assign dic's 
                # Key=`page`
                # Value=`equal_click_prob`
            model_result[page] = equal_click_prob
            # {4.html: 0.25} ➔  
                # {'4.html': 0.25, '3.html': 0.25}...

            return model_result # {'4.html': 0.25, '3.html': 0.25, '2.html': 0.25, '1.html': 0.25}
            

    """ ############ Iterative Algorithm ############ """
    ###### The page has outgoing link ######
    ### Implement the formula that the document porvided (README.md)###
    
    # corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}

    """ ###### The page has outgoing link ###### """
    ### User chose a page at random ###
    # (1-d)/N (the 1st part of formula)
        # d = dampin_factor, N = total_pages
    for page in corpus: # Do this in every page, here is "1.html"
        # "1.html" PageRank(PR)
        model_result[page] = (1 - damping_factor) / total_pages
        # (1-0.85)/3 = 0.05


    """ User click a link randomly in page "1.html" """
    # We assume PR(i)=1, becuase it is initialization
    # d × (PR(i)/NumLinks(i)) (the 2nd part of formula)
    # ∑ means sum all links, we use `+=` to do this
    # Here, each page already has a probability when it comes in, use `+=` to add up the original probability and the probability calculated here.
    for link in links_in_page: # link_in_page = "2.html", "3.html"
        model_result[link] += damping_factor / len(links_in_page)
        # `damping_factor / len(links_in_page)` actually doing:
            # d * 1/2, but
                # We igrone the "1" then change "*" to "/"
                    # Because (x * 1/2) = (x / 2)

    return model_result
    #{'1.html': 0.05, '2.html': 0.475, '3.html': 0.475}

    


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """ 
    # Initialize `pageranks{}`
    pageranks = {}
    # Add a value(0) to every key(page)
        # The value is the number of clicks
    for page in corpus:
        pageranks[page] = 0   
        # {'1.html': 0, '1.html': 0, '1.html': 0}

    # Sample will keep changging
    sample = random.choice(list(corpus.keys()))
    # `list()` will extract all keys in corpus dic to a list
        # ['1.html', '2.html', '3.html']
    # then random choice 1 page
        # e.g. "1.html"

    for _ in range(n): # If not be reused variable, convention in Python to use `_`
        pageranks[sample] += 1 
        # this page has been clicked
            # {'1.html': 1, '2.html': 0, '3.html': 0}
                # the '1.html' has been clicked
        model = transition_model(corpus, sample, damping_factor)
        # use the `transition_model` to get a result dic
            # {'1.html': 0.05, '2.html': 0.9, '3.html': 0.05}

         # Update the sample (change)
        sample = random.choices(list(model.keys()), weights=list(model.values()))[0]
        # Random choice 1 page in the `model` as sample
            # `list(model.keys())` choice a page from the dic that come from `model`
            # `weight=` is `random.chicess()`'s parameter
                # The greater the weight, the greater the chance of being chosen.
        # `sample` will looks like ["1.html"] or ["2.html"] or ["3.html"]

    # Normalize the pagerank values
    for page in pageranks: # {'4.html': 1359, '3.html': 2212, '2.html': 4257, '1.html': 2172}
        # If page is "4.html"  
        pageranks[page] /= n
        # "pageranks[page]" get the 1359
        # 1359 / 10000 (n = SAMPLES = 10000)



    return pageranks
    # {'1.html': 508, '2.html': 4728, '3.html': 4764}



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.

    PageRank，精確到 0.001。
    重複計算，直到所有 PageRank 值之間的變化都不超過 0.001。
    """
    # Setup a dic for pagerank that contain all page in corpus
    pagerank = {}
    for page in corpus:
        pagerank[page] = 1/len(corpus)
        # Assign every page a basic rank, if there are 4 pages, it will be 1/4
            # the basic rank is 0.25
        
    # If the differences <= threshold then stop iterative
    threshold = 0.001
    
    
    # Start iterative updating
    while True:
        new_pagerank = {}
        for page in corpus:
            ### Divide the PageRank formula into two parts ###
                ### basic_rank & sum_links ###
            
            """ #### basic_rank #### """
            ## Every page has an equal chance of being selected, so it gets a basic PageRank ##
            basic_rank = (1 - damping_factor) / len(corpus)
                # (1 - d) ×  (1 / N) the 1st part of formula
                    # We igrone the "1" then change "*" to "/"
                    # Because (x * 1/N) = (x / N)


            """ #### sum_links #### """
            ## Each other page that links("votes") to the current page ##
                # Summed up these "votes" is a sum_links  
            # d × ∑i(PR(i)/NumLinks(i)) the 2nd part of formula
                # ∑i means sum all links, we use `+=` to do this
            sum_links = 0 # ∑: The sum of the pages that point to the page
            for i in corpus: 
            # e.g. i = 3.hmtl

                if page in corpus[i]: # 4.html # check if there is a 4.html in 3.html
                # if page: 4.html in corpus[i3.html]: {'2.html', '4.html'} ➔ True

                    # sum_likes: 0
                    sum_links += pagerank[i] / len(corpus[i])
                    # sum_links: 0.125 += pagerank[i: 3.html]: 0.25 / len(corpus[i3.html]): 2)


            # The PageRank Formula that the Project Document provided
                # Check the formula pic in project folder
            new_pagerank[page] = basic_rank + damping_factor * sum_links
            # basic_rank = (1 - d) ×  (1 / N)
            # damping_factor = d 
            # sum_links = ∑i(PR(i)/NumLinks(i))


        """ ### Check differences convergence with threshold ### """
        differences = []
        for page in pagerank:
            diff = abs(new_pagerank[page] - pagerank[page])
            # `abs()` for turn the -x to x
            differences.append(diff)

        ### Update the pagerank ###
        pagerank = new_pagerank

         # If all the differences are less than the threshold value
        below_threshold = True  # By default, all differences are below the threshold.

        for diff in differences:
            if diff >= threshold:
                below_threshold = False
                break

        # If difference below the threshold, return pagerank and end this functon
        if below_threshold:
            return pagerank


if __name__ == "__main__":
    main()
