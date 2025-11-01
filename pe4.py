import wikipedia
import time
from concurrent.futures import ThreadPoolExecutor

#SECTION A: Sequential Download

start_time_sequential = time.perf_counter()
#1 Use the Wikipedia.search method to return a list of topics related to 'generative artificial intelligence'
results = wikipedia.search('generative artificial intelligence')
print(f"Found {len(results)} topics")

#2 Iterate over the topiocs returned in #1 above  using a for loop
for topic in results:
    try:
        #assign page contents to a variable named apge, assign page title ot variable , retrieve references for that page
        page = wikipedia.page(topic, auto_suggest=False)
        page_title = page.title
        page_references = page.references
        #write references to a .txt file where the name of hte file is the title of the topic.
        filename = f"{page_title}.txt"

        with open(filename, 'w', encoding='utf-8') as f:
            for reference in page_references:
                f.write(reference + '\n')
        
        print(f"Saved: {filename}")
        
    except Exception as e:
        print(f"Error processing {topic}: {e}")

end_time_sequential = time.perf_counter()
#print to console the amount of time it took the above code to execute, using time.perf_counter()
sequential_time = end_time_sequential - start_time_sequential
print(f"\nSequential execution time: {sequential_time:.2f} seconds")

#SECTION B: Concurrent Download

#1 Use the wikipedia.search method to return a list of topics related to 'generative artificial intelligence'
results_concurrent = wikipedia.search('generative artificial intelligence')

#2 Create a function def wiki_dl_save(topic)
def wiki_dl_and_save(topic):
    try:
        #Retrieves Page, title, and ref for the topic
        page = wikipedia.page(topic, auto_suggest=False)
        title = page.title
        references = page.references
        #Creates a .txt file where the name of the file is the title of the topoic
        filename = f"{title}.txt" 
        #write the references ot the file created in the preceding step
        with open(filename, 'w', encoding='utf-8') as f:
            for reference in references:
                f.write(reference + '\n')
                
    except Exception as e:
        print(f"Error processing {topic}: {e}")

start_time_concurrent = time.perf_counter()

print(f"Found {len(results_concurrent)} topics")

#3 Use the ThreadPoolExecutor from the concurrent.futures library to execute concurrently the function defined in step 2
with ThreadPoolExecutor() as executor:
    executor.map(wiki_dl_and_save, results_concurrent)

print("Concurrent processing complete")

end_time_concurrent = time.perf_counter()

#print to console the amount of time it took the above code to execute, using time.perf_counter()
concurrent_time = end_time_concurrent - start_time_concurrent
print(f"\nConcurrent execution time: {concurrent_time:.2f} seconds")
