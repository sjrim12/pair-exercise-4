import wikipedia
import time
from concurrent.futures import ThreadPoolExecutor

import time
import re
from pathlib import Path
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError, HTTPTimeoutError, RedirectError
###################################
#Part A - 1
###################################
# ---------- Config ----------
QUERY = "generative artificial intelligence"
MAX_RESULTS = 10  # adjust if you want more/less topics
OUTPUT_DIR = Path("wiki_refs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------- Helpers ----------
def safe_filename(title: str) -> str:
    """
    Make a Windows/macOS/Linux-safe filename from a page title.
    Preserves spaces, removes illegal characters, trims length.
    """
    # Remove characters illegal on Windows: \ / : * ? " < > | and control chars
    cleaned = re.sub(r'[\\/:*?"<>|\x00-\x1F]', "", title).strip()
    # Collapse internal whitespace just a little (optional)
    cleaned = re.sub(r"\s+", " ", cleaned)
    # Limit filename length for safety
    return cleaned[:200] or "Untitled"

def write_references_to_file(title: str, references: list[str]) -> Path:
    """
    Writes references (one per line) to '<TITLE>.txt' inside OUTPUT_DIR.
    Non-string entries are coerced to str, blank lines removed.
    """
    fname = OUTPUT_DIR / f"{safe_filename(title)}.txt"
    lines = [str(ref).strip() for ref in references if str(ref).strip()]
    # Ensure each ref on its own line
    content = "\n".join(lines) + ("\n" if lines else "")
    fname.write_text(content, encoding="utf-8")
    return fname

# ---------- Main ----------
def main():
    wikipedia.set_lang("en")

    t0 = time.perf_counter()

    # 1) Search for topics
    topics = wikipedia.search(QUERY, results=MAX_RESULTS)
    print(f"Found {len(topics)} topics for query: {QUERY!r}")

    processed = 0
    skipped = 0

    # 2) Iterate topics and process each page
    for topic in topics:
        try:
            # Important per instructions: auto_suggest=False
            page = wikipedia.page(title=topic, auto_suggest=False, preload=False)
            page_title = page.title
            refs = page.references  # typically a list of URLs (strings)

            # Write references to '<TITLE>.txt'
            out_path = write_references_to_file(page_title, refs)

            print(f"✓ {page_title}  ->  {out_path.name}  ({len(refs)} refs)")
            processed += 1

        except DisambiguationError as e:
            # Topic is ambiguous when auto_suggest=False; skip to honor instruction
            print(f"– Skipped ambiguous topic: {topic!r} (options={len(e.options)})")
            skipped += 1
        except (PageError, RedirectError) as e:
            print(f"– Skipped: {topic!r} ({type(e).__name__}: {e})")
            skipped += 1
        except HTTPTimeoutError as e:
            print(f"– Network timeout on: {topic!r} ({e})")
            skipped += 1
        except Exception as e:
            print(f"– Error on: {topic!r} ({type(e).__name__}: {e})")
            skipped += 1

    # 3) Print total elapsed time
    elapsed = time.perf_counter() - t0
    print(f"\nDone. Processed: {processed}, Skipped: {skipped}, Topics total: {len(topics)}")
    print(f"Total time: {elapsed:.3f} seconds")

if __name__ == "__main__":
    main()
####################################
#Part A - 1
####################################
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
